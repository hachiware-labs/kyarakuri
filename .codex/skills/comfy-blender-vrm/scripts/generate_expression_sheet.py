from __future__ import annotations

import argparse
import secrets
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path
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
    render_template,
    resolve_repo_path,
    save_json,
    upload_reference_image,
    wait_for_history,
)


DEFAULT_EXPRESSIONS = ("neutral", "smile", "angry", "sad", "surprised", "blink")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate multiple facial expression images from an API-format ComfyUI workflow."
    )
    parser.add_argument("--workflow", type=Path, required=True, help="Path to the API-format workflow JSON.")
    parser.add_argument("--base-image", type=Path, required=True, help="Base character image uploaded to ComfyUI.")
    parser.add_argument(
        "--character-prompt",
        required=True,
        help="Prompt text inserted into the workflow via {{character_prompt}}.",
    )
    parser.add_argument(
        "--expressions",
        default=",".join(DEFAULT_EXPRESSIONS),
        help="Comma-separated expression list. Defaults to neutral,smile,angry,sad,surprised,blink.",
    )
    parser.add_argument("--seed", type=int, default=None, help="Optional base seed. Derived per-expression seeds use +index.")
    parser.add_argument(
        "--output-name",
        default="expression-sheet",
        help="Run name prefix used for the output directory name.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to the config JSON file. Defaults to config/comfy-blender-vrm.json under the repository root.",
    )
    parser.add_argument("--timeout-seconds", type=int, default=180, help="Maximum wait time for each ComfyUI job.")
    parser.add_argument("--poll-interval", type=float, default=2.0, help="Polling interval in seconds.")
    return parser.parse_args()


def parse_expression_list(raw_value: str) -> list[str]:
    expressions: list[str] = []
    for part in raw_value.split(","):
        value = part.strip()
        if not value:
            continue
        if value not in expressions:
            expressions.append(value)

    if not expressions:
        raise GenerationError(
            detail="Expression list is empty after parsing --expressions.",
            next_action="Pass at least one expression name, for example --expressions neutral,smile.",
        )
    return expressions


def sanitize_slug(value: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in "._-" else "-" for char in value).strip("-")
    return cleaned or "expression"


def prepare_expression_output_paths(output_root: Path, output_name: str, timestamp: str) -> tuple[str, Path, Path]:
    run_id = f"{timestamp}-{sanitize_slug(output_name)}"
    run_dir = output_root / "expressions" / run_id
    logs_dir = output_root / "logs"
    try:
        run_dir.mkdir(parents=True, exist_ok=False)
        logs_dir.mkdir(parents=True, exist_ok=True)
    except FileExistsError as exc:
        raise GenerationError(
            detail=f"Output run directory already exists: {run_dir}",
            next_action="Retry with a different --output-name or rerun at a different time.",
        ) from exc
    except OSError as exc:
        raise GenerationError(
            detail=f"Output directory could not be created: {exc}",
            next_action="Check the configured output directory permissions.",
        ) from exc
    return run_id, run_dir, logs_dir


def build_base_image_placeholders(uploaded_base_image: dict[str, object]) -> dict[str, object]:
    uploaded_name = uploaded_base_image.get("name") or uploaded_base_image.get("filename")
    if not isinstance(uploaded_name, str) or not uploaded_name:
        raise GenerationError(
            detail="ComfyUI upload response did not include an uploaded base image name.",
            next_action="Check the ComfyUI upload API response format.",
        )

    return {
        "base_image": uploaded_name,
        "base_image_name": uploaded_name,
        "base_image_subfolder": str(uploaded_base_image.get("subfolder", "")),
        "base_image_type": str(uploaded_base_image.get("type", "input")),
    }


def save_expression_images(
    comfyui_url: str,
    expression_images_dir: Path,
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
        destination = expression_images_dir / target_name
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


def generate_expression(
    comfyui_url: str,
    workflow_payload: dict[str, object],
    expression_dir: Path,
    expression_name: str,
    placeholders: dict[str, object],
    timeout_seconds: int,
    poll_interval: float,
) -> dict[str, object]:
    expression_dir.mkdir(parents=True, exist_ok=True)
    images_dir = expression_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    submitted_workflow = render_template(workflow_payload, placeholders)
    unresolved = collect_unresolved_tokens(submitted_workflow)
    if unresolved:
        raise GenerationError(
            detail=f"Unresolved workflow placeholders remain for expression '{expression_name}': {', '.join(unresolved)}",
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
            detail=f"ComfyUI prompt response did not include a prompt_id for expression '{expression_name}'.",
            next_action="Check the ComfyUI server logs for the rejected prompt request.",
        )

    history_entry = wait_for_history(comfyui_url, prompt_id, timeout_seconds, poll_interval)
    image_records = collect_images(history_entry)
    if not image_records:
        raise GenerationError(
            detail=f"ComfyUI completed expression '{expression_name}' but returned no image outputs.",
            next_action="Ensure the workflow ends with image-producing output nodes such as SaveImage.",
        )

    downloaded_images = save_expression_images(comfyui_url, images_dir, image_records)
    save_json(expression_dir / "submitted-workflow.json", submitted_workflow)
    save_json(expression_dir / "history.json", history_entry)

    return {
        "expression": expression_name,
        "prompt_id": prompt_id,
        "client_id": client_id,
        "output_dir": str(expression_dir),
        "images": [image.__dict__ for image in downloaded_images],
    }


def main() -> int:
    args = parse_args()
    try:
        repo_root = find_repo_root(Path(__file__).resolve())
        config_path = args.config.resolve() if args.config else default_config_path(repo_root)
        config = load_config(config_path)

        comfyui_url = str(config["comfyui_url"]).rstrip("/")
        output_root = resolve_repo_path(str(config["output_dir"]), repo_root)
        workflow_path = resolve_repo_path(args.workflow, repo_root)
        base_image_path = resolve_repo_path(args.base_image, repo_root)
        workflow_payload = load_workflow_payload(workflow_path)
        expressions = parse_expression_list(args.expressions)

        base_seed = args.seed if args.seed is not None else secrets.randbelow(2**53)
        uploaded_base_image = upload_reference_image(comfyui_url, base_image_path)
        base_image_placeholders = build_base_image_placeholders(uploaded_base_image)

        timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
        run_id, run_dir, logs_dir = prepare_expression_output_paths(output_root, args.output_name, timestamp)

        expression_results: list[dict[str, object]] = []
        for index, expression_name in enumerate(expressions):
            expression_seed = base_seed + index
            expression_dir = run_dir / sanitize_slug(expression_name)
            placeholders: dict[str, object] = {
                "character_prompt": args.character_prompt,
                "expression_name": expression_name,
                "seed": expression_seed,
                "run_id": run_id,
                **base_image_placeholders,
            }
            result = generate_expression(
                comfyui_url=comfyui_url,
                workflow_payload=workflow_payload,
                expression_dir=expression_dir,
                expression_name=expression_name,
                placeholders=placeholders,
                timeout_seconds=args.timeout_seconds,
                poll_interval=args.poll_interval,
            )
            result["seed"] = expression_seed
            expression_results.append(result)

        metadata_path = logs_dir / f"{run_id}.json"
        save_json(
            metadata_path,
            {
                "command": "generate-expression-sheet",
                "run_id": run_id,
                "timestamp_utc": datetime.now(UTC).isoformat(),
                "config_path": str(config_path),
                "workflow_path": str(workflow_path),
                "base_image": str(base_image_path),
                "uploaded_base_image": uploaded_base_image,
                "character_prompt": args.character_prompt,
                "base_seed": base_seed,
                "expressions": expressions,
                "expression_runs": expression_results,
                "expressions_output_dir": str(run_dir),
            },
        )

        print("generate-expression-sheet")
        print(f"Run id: {run_id}")
        print(f"Expressions output: {run_dir}")
        print(f"Metadata: {metadata_path}")
        print("Generated expressions:")
        for result in expression_results:
            print(f"- {result['expression']}: {result['output_dir']}")
        return 0

    except GenerationError as exc:
        print("generate-expression-sheet failed")
        print(f"detail: {exc.detail}")
        print(f"next: {exc.next_action}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
