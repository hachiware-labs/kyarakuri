from __future__ import annotations

import argparse
import secrets
import sys
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib import parse

from comfy_helpers import (
    DownloadedImage,
    GenerationError,
    collect_images,
    collect_unresolved_tokens,
    default_config_path,
    download_file,
    find_repo_root,
    load_config,
    load_workflow_payload,
    post_json,
    prepare_output_paths,
    render_template,
    resolve_repo_path,
    save_json,
    upload_reference_image,
    wait_for_history,
)


@dataclass
class CharacterSheetRequest:
    workflow_path: Path
    character_prompt: str
    seed: int | None = None
    reference_image_path: Path | None = None
    output_name: str = "character-sheet"
    config_path: Path | None = None
    timeout_seconds: int = 180
    poll_interval: float = 2.0
    command_name: str = "generate-character-sheet"
    extra_output_json: dict[str, dict[str, Any]] = field(default_factory=dict)
    extra_output_text: dict[str, str] = field(default_factory=dict)
    extra_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CharacterSheetResult:
    run_id: str
    seed: int
    prompt_id: str
    character_dir: Path
    metadata_path: Path
    images: list[DownloadedImage]
    uploaded_reference: dict[str, object] | None
    config_path: Path
    workflow_path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a character sheet image from an API-format ComfyUI workflow."
    )
    parser.add_argument("--workflow", type=Path, required=True, help="Path to the API-format workflow JSON.")
    parser.add_argument(
        "--character-prompt",
        required=True,
        help="Prompt text inserted into the workflow via {{character_prompt}}.",
    )
    parser.add_argument("--seed", type=int, default=None, help="Optional seed. A random seed is generated when omitted.")
    parser.add_argument(
        "--reference-image",
        type=Path,
        default=None,
        help="Optional reference image uploaded to ComfyUI for {{reference_image}} placeholders.",
    )
    parser.add_argument(
        "--output-name",
        default="character-sheet",
        help="Run name prefix used for the output directory name.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to the config JSON file. Defaults to config/comfy-blender-vrm.json under the repository root.",
    )
    parser.add_argument("--timeout-seconds", type=int, default=180, help="Maximum wait time for the ComfyUI job.")
    parser.add_argument("--poll-interval", type=float, default=2.0, help="Polling interval in seconds.")
    return parser.parse_args()


def build_placeholders(
    character_prompt: str,
    seed: int,
    run_id: str,
    uploaded_reference: dict[str, object] | None,
) -> dict[str, object]:
    placeholders: dict[str, object] = {
        "character_prompt": character_prompt,
        "seed": seed,
        "run_id": run_id,
    }

    if uploaded_reference is None:
        return placeholders

    uploaded_name = uploaded_reference.get("name") or uploaded_reference.get("filename")
    if not isinstance(uploaded_name, str) or not uploaded_name:
        raise GenerationError(
            detail="ComfyUI upload response did not include an uploaded image name.",
            next_action="Check the ComfyUI upload API response format.",
        )

    placeholders["reference_image"] = uploaded_name
    placeholders["reference_image_name"] = uploaded_name
    placeholders["reference_image_subfolder"] = str(uploaded_reference.get("subfolder", ""))
    placeholders["reference_image_type"] = str(uploaded_reference.get("type", "input"))
    return placeholders


def save_downloaded_images(
    comfyui_url: str,
    character_dir: Path,
    image_records: list[dict[str, str]],
) -> list[DownloadedImage]:
    downloaded_images: list[DownloadedImage] = []
    for index, image in enumerate(image_records, start=1):
        query = parse.urlencode(
            {
                "filename": image["filename"],
                "subfolder": image["subfolder"],
                "type": image["type"],
            }
        )
        target_name = f"{index:03d}_{image['node_id']}_{Path(image['filename']).name}"
        destination = character_dir / "images" / target_name
        download_file(f"{comfyui_url}/view?{query}", destination)
        downloaded_images.append(
            DownloadedImage(
                node_id=image["node_id"],
                filename=image["filename"],
                subfolder=image["subfolder"],
                image_type=image["type"],
                saved_path=str(destination),
            )
        )
    return downloaded_images


def save_text_artifact(path: Path, content: str) -> None:
    try:
        path.write_text(content, encoding="utf-8")
    except OSError as exc:
        raise GenerationError(
            detail=f"Text output could not be written: {exc}",
            next_action="Check the destination directory permissions and free space.",
        ) from exc


def run_character_sheet_generation(request: CharacterSheetRequest) -> CharacterSheetResult:
    repo_root = find_repo_root(Path(__file__).resolve())
    config_path = request.config_path.resolve() if request.config_path else default_config_path(repo_root)
    config = load_config(config_path)

    comfyui_url = str(config["comfyui_url"]).rstrip("/")
    output_root = resolve_repo_path(str(config["output_dir"]), repo_root)
    workflow_path = resolve_repo_path(request.workflow_path, repo_root)
    reference_image_path = (
        resolve_repo_path(request.reference_image_path, repo_root) if request.reference_image_path else None
    )
    workflow_payload = load_workflow_payload(workflow_path)

    seed = request.seed if request.seed is not None else secrets.randbelow(2**53)
    uploaded_reference = upload_reference_image(comfyui_url, reference_image_path) if reference_image_path else None

    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    run_id, character_dir, logs_dir = prepare_output_paths(output_root, request.output_name, timestamp)
    placeholders = build_placeholders(request.character_prompt, seed, run_id, uploaded_reference)

    submitted_workflow = render_template(workflow_payload, placeholders)
    unresolved = collect_unresolved_tokens(submitted_workflow)
    if unresolved:
        raise GenerationError(
            detail=f"Unresolved workflow placeholders remain: {', '.join(unresolved)}",
            next_action="Add the missing command inputs or remove the unsupported placeholders from the workflow JSON.",
        )

    client_id = str(uuid.uuid4())
    prompt_response = post_json(
        f"{comfyui_url}/prompt",
        {
            "prompt": submitted_workflow,
            "client_id": client_id,
        },
    )
    prompt_id = prompt_response.get("prompt_id")
    if not isinstance(prompt_id, str) or not prompt_id:
        raise GenerationError(
            detail="ComfyUI prompt response did not include a prompt_id.",
            next_action="Check the ComfyUI server logs for the rejected prompt request.",
        )

    history_entry = wait_for_history(comfyui_url, prompt_id, request.timeout_seconds, request.poll_interval)
    image_records = collect_images(history_entry)
    if not image_records:
        raise GenerationError(
            detail="ComfyUI completed the prompt but returned no image outputs.",
            next_action="Ensure the workflow ends with image-producing output nodes such as SaveImage.",
        )

    downloaded_images = save_downloaded_images(comfyui_url, character_dir, image_records)
    submitted_workflow_path = character_dir / "submitted-workflow.json"
    history_path = character_dir / "history.json"
    metadata_path = logs_dir / f"{run_id}.json"

    save_json(submitted_workflow_path, submitted_workflow)
    save_json(history_path, history_entry)
    for relative_path, payload in request.extra_output_json.items():
        save_json(character_dir / relative_path, payload)
    for relative_path, content in request.extra_output_text.items():
        save_text_artifact(character_dir / relative_path, content)

    metadata_payload: dict[str, Any] = {
        "command": request.command_name,
        "run_id": run_id,
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "config_path": str(config_path),
        "workflow_path": str(workflow_path),
        "character_prompt": request.character_prompt,
        "seed": seed,
        "reference_image": str(reference_image_path) if reference_image_path else None,
        "uploaded_reference": uploaded_reference,
        "client_id": client_id,
        "prompt_id": prompt_id,
        "character_output_dir": str(character_dir),
        "images": [image.__dict__ for image in downloaded_images],
    }
    metadata_payload.update(request.extra_metadata)
    save_json(metadata_path, metadata_payload)

    return CharacterSheetResult(
        run_id=run_id,
        seed=seed,
        prompt_id=prompt_id,
        character_dir=character_dir,
        metadata_path=metadata_path,
        images=downloaded_images,
        uploaded_reference=uploaded_reference,
        config_path=config_path,
        workflow_path=workflow_path,
    )


def print_success(command_name: str, result: CharacterSheetResult) -> None:
    print(command_name)
    print(f"Run id: {result.run_id}")
    print(f"Prompt id: {result.prompt_id}")
    print(f"Character output: {result.character_dir}")
    print(f"Metadata: {result.metadata_path}")
    print("Saved images:")
    for image in result.images:
        print(f"- {image.saved_path}")


def main() -> int:
    args = parse_args()
    try:
        result = run_character_sheet_generation(
            CharacterSheetRequest(
                workflow_path=args.workflow,
                character_prompt=args.character_prompt,
                seed=args.seed,
                reference_image_path=args.reference_image,
                output_name=args.output_name,
                config_path=args.config,
                timeout_seconds=args.timeout_seconds,
                poll_interval=args.poll_interval,
            )
        )
        print_success("generate-character-sheet", result)
        return 0
    except GenerationError as exc:
        print("generate-character-sheet failed")
        print(f"detail: {exc.detail}")
        print(f"next: {exc.next_action}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
