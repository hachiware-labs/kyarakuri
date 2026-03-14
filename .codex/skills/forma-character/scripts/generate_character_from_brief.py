from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from comfy_helpers import GenerationError, save_json
from generate_character_sheet import CharacterSheetRequest, print_success, run_character_sheet_generation


LIST_FIELDS = {"style_keywords", "visual_traits", "negative_constraints"}
STRING_FIELDS = {"character_name", "core_concept", "outfit", "pose", "expression", "background", "extra_notes"}
ALLOWED_BRIEF_KEYS = LIST_FIELDS | STRING_FIELDS
BASE_IMAGE_PROMPT_PARTS = (
    "full body standing character concept illustration",
    "single character only",
    "front-facing standing composition",
    "both feet visible",
    "clean silhouette",
    "plain pure white background for cutout",
    "no background scene",
    "no text, no caption, no watermark, no logo",
    "suitable as a base character sheet",
)
BASE_IMAGE_NEGATIVE_CONSTRAINTS = (
    "background objects",
    "detailed scenery",
    "props",
    "floor shadow",
    "cast shadow",
    "caption text",
    "letters on image",
    "speech bubbles",
    "logo",
    "watermark",
    "signage",
    "multiple characters",
    "cropped feet",
    "sitting pose",
    "crouching pose",
    "lying pose",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect a character brief and generate a base image through the existing character sheet workflow."
    )
    parser.add_argument("--workflow", type=Path, required=True, help="Path to the API-format workflow JSON.")
    parser.add_argument(
        "--brief-file",
        type=Path,
        default=None,
        help="Optional character brief JSON file. When omitted, the command prompts for the brief interactively.",
    )
    parser.add_argument("--seed", type=int, default=None, help="Optional seed. A random seed is generated when omitted.")
    parser.add_argument(
        "--output-name",
        default="character-from-brief",
        help="Run name prefix used for the output directory name.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to the config JSON file. Defaults to config/forma-character.json under the repository root.",
    )
    parser.add_argument("--timeout-seconds", type=int, default=180, help="Maximum wait time for the ComfyUI job.")
    parser.add_argument("--poll-interval", type=float, default=2.0, help="Polling interval in seconds.")
    return parser.parse_args()


def split_csv_like(raw_value: str) -> list[str]:
    values: list[str] = []
    for part in raw_value.split(","):
        value = part.strip()
        if value and value not in values:
            values.append(value)
    return values


def merge_unique(parts: list[str], extras: list[str]) -> list[str]:
    merged = list(parts)
    for extra in extras:
        if extra not in merged:
            merged.append(extra)
    return merged


def normalize_string(value: Any, key: str, required: bool = False) -> str | None:
    if value is None:
        if required:
            raise GenerationError(
                detail=f"Character brief is missing required field '{key}'.",
                next_action="Add the missing field to the brief JSON or provide it during interactive input.",
            )
        return None

    if not isinstance(value, str):
        raise GenerationError(
            detail=f"Character brief field '{key}' must be a string.",
            next_action=f"Rewrite '{key}' as a JSON string.",
        )

    normalized = value.strip()
    if not normalized:
        if required:
            raise GenerationError(
                detail=f"Character brief field '{key}' must not be empty.",
                next_action=f"Provide a non-empty value for '{key}'.",
            )
        return None
    return normalized


def normalize_list(value: Any, key: str) -> list[str]:
    if value is None:
        return []

    if isinstance(value, str):
        return split_csv_like(value)

    if not isinstance(value, list):
        raise GenerationError(
            detail=f"Character brief field '{key}' must be an array of strings.",
            next_action=f"Rewrite '{key}' as a JSON array of strings.",
        )

    normalized: list[str] = []
    for item in value:
        if not isinstance(item, str):
            raise GenerationError(
                detail=f"Character brief field '{key}' contains a non-string item.",
                next_action=f"Rewrite '{key}' so every item is a string.",
            )
        stripped = item.strip()
        if stripped and stripped not in normalized:
            normalized.append(stripped)
    return normalized


def validate_brief(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise GenerationError(
            detail="Character brief JSON must be an object.",
            next_action="Rewrite the brief file as a JSON object with the documented keys.",
        )

    unknown_keys = sorted(set(payload) - ALLOWED_BRIEF_KEYS)
    if unknown_keys:
        raise GenerationError(
            detail=f"Character brief contains unsupported fields: {', '.join(unknown_keys)}",
            next_action="Remove the unsupported fields or update the brief to use the documented keys only.",
        )

    brief: dict[str, Any] = {
        "core_concept": normalize_string(payload.get("core_concept"), "core_concept", required=True),
    }

    for key in sorted(STRING_FIELDS - {"core_concept"}):
        value = normalize_string(payload.get(key), key)
        if value:
            brief[key] = value

    for key in sorted(LIST_FIELDS):
        values = normalize_list(payload.get(key), key)
        if values:
            brief[key] = values

    return brief


def read_brief_file(brief_path: Path) -> dict[str, Any]:
    if not brief_path.exists():
        raise GenerationError(
            detail=f"Brief file was not found: {brief_path}",
            next_action="Pass --brief-file with an existing JSON file or omit it to use interactive input.",
        )

    try:
        payload = json.loads(brief_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise GenerationError(
            detail=f"Brief JSON is invalid at line {exc.lineno}, column {exc.colno}: {exc.msg}",
            next_action="Fix the brief JSON syntax and rerun the command.",
        ) from exc
    except OSError as exc:
        raise GenerationError(
            detail=f"Brief file could not be read: {exc}",
            next_action="Check the brief file path and permissions.",
        ) from exc

    return validate_brief(payload)


def prompt_required_text(message: str) -> str:
    while True:
        try:
            value = input(message).strip()
        except EOFError as exc:
            raise GenerationError(
                detail="Interactive brief input ended before the required field was entered.",
                next_action="Provide the missing answer or use --brief-file for non-interactive execution.",
            ) from exc

        if value:
            return value
        print("This field is required.")


def prompt_optional_text(message: str) -> str | None:
    try:
        value = input(message).strip()
    except EOFError as exc:
        raise GenerationError(
            detail="Interactive brief input ended unexpectedly.",
            next_action="Provide all prompted answers or use --brief-file for non-interactive execution.",
        ) from exc
    return value or None


def prompt_optional_list(message: str) -> list[str]:
    value = prompt_optional_text(message)
    if not value:
        return []
    return split_csv_like(value)


def collect_interactive_brief() -> dict[str, Any]:
    print("forma-character-generate-base-image")
    print("Enter a short character brief for a standing base image. Press Enter to skip optional fields.")

    brief: dict[str, Any] = {
        "character_name": prompt_required_text("Character name (required): "),
        "core_concept": prompt_required_text("Core concept (required): "),
    }

    style_keywords = prompt_optional_list("Style keywords, comma separated (optional): ")
    if style_keywords:
        brief["style_keywords"] = style_keywords

    visual_traits = prompt_optional_list("Visual traits, comma separated (optional): ")
    if visual_traits:
        brief["visual_traits"] = visual_traits

    for key, message in (
        ("outfit", "Outfit or accessories (optional): "),
        ("pose", "Standing pose detail (optional): "),
        ("expression", "Facial expression (optional): "),
        ("extra_notes", "Extra notes (optional): "),
    ):
        value = prompt_optional_text(message)
        if value:
            brief[key] = value

    negative_constraints = prompt_optional_list("Avoid elements, comma separated (optional): ")
    if negative_constraints:
        brief["negative_constraints"] = negative_constraints

    return validate_brief(brief)


def synthesize_character_prompt(brief: dict[str, Any]) -> str:
    prompt_parts: list[str] = [brief["core_concept"], *BASE_IMAGE_PROMPT_PARTS]

    style_keywords = brief.get("style_keywords", [])
    if style_keywords:
        prompt_parts.append(", ".join(style_keywords))

    visual_traits = brief.get("visual_traits", [])
    if visual_traits:
        prompt_parts.append(", ".join(visual_traits))

    if "outfit" in brief:
        prompt_parts.append(f"wearing {brief['outfit']}")
    if "pose" in brief:
        prompt_parts.append(f"standing pose detail: {brief['pose']}")
    if "expression" in brief:
        prompt_parts.append(f"expression: {brief['expression']}")
    if "extra_notes" in brief:
        prompt_parts.append(brief["extra_notes"])

    prompt = ", ".join(prompt_parts)
    negative_constraints = merge_unique(list(BASE_IMAGE_NEGATIVE_CONSTRAINTS), brief.get("negative_constraints", []))
    if negative_constraints:
        prompt = f"{prompt}. Avoid: {', '.join(negative_constraints)}."
    return prompt


def build_prompt_preview(brief: dict[str, Any], character_prompt: str) -> str:
    lines = [
        "Character brief",
        json.dumps(brief, indent=2, ensure_ascii=False),
        "",
        "Synthesized character_prompt",
        character_prompt,
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    try:
        brief_source = "interactive"
        if args.brief_file is not None:
            brief = read_brief_file(args.brief_file)
            brief_source = str(args.brief_file)
        else:
            brief = collect_interactive_brief()

        character_prompt = synthesize_character_prompt(brief)
        prompt_preview = build_prompt_preview(brief, character_prompt)
        project_name_hint = brief.get("character_name") or brief["core_concept"]
        result = run_character_sheet_generation(
            CharacterSheetRequest(
                workflow_path=args.workflow,
                character_prompt=character_prompt,
                seed=args.seed,
                output_name=args.output_name,
                config_path=args.config,
                timeout_seconds=args.timeout_seconds,
                poll_interval=args.poll_interval,
                command_name="forma-character-generate-base-image",
                project_name_hint=project_name_hint,
                extra_output_json={"brief.json": brief},
                extra_output_text={"prompt-preview.txt": prompt_preview},
                extra_metadata={
                    "brief": brief,
                    "brief_source": brief_source,
                    "project_name_hint": project_name_hint,
                    "prompt_preview_path": str(Path("prompt-preview.txt")),
                    "brief_path": str(Path("brief.json")),
                },
            )
        )
        project_brief_path = result.project_dir / "brief.json"
        save_json(project_brief_path, brief)

        print_success("forma-character-generate-base-image", result)
        print(f"Project brief: {project_brief_path}")
        print(f"Brief: {result.character_dir / 'brief.json'}")
        print(f"Prompt preview: {result.character_dir / 'prompt-preview.txt'}")
        return 0
    except GenerationError as exc:
        print("forma-character-generate-base-image failed")
        print(f"detail: {exc.detail}")
        print(f"next: {exc.next_action}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
