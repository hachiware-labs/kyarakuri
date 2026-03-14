from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class BuildVrmError(Exception):
    def __init__(self, detail: str, next_action: str) -> None:
        super().__init__(detail)
        self.detail = detail
        self.next_action = next_action


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Blender in background mode to prepare a base VRM workspace from an existing blend file."
    )
    parser.add_argument("--blend-file", type=Path, required=True, help="Path to the source .blend file.")
    parser.add_argument(
        "--texture-image",
        type=Path,
        default=None,
        help="Optional texture image applied to the first mesh material before saving.",
    )
    parser.add_argument(
        "--output-name",
        default="build-vrm-base",
        help="Run name prefix used for the output directory name.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to the config JSON file. Defaults to config/forma-character.json under the repository root.",
    )
    return parser.parse_args()


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "AGENTS.md").exists() and (candidate / "docs").is_dir():
            return candidate
    raise BuildVrmError(
        detail="Repository root could not be found from the script location.",
        next_action="Run the command inside the project workspace.",
    )


def default_config_path(repo_root: Path) -> Path:
    return repo_root / "config" / "forma-character.json"


def resolve_repo_path(path_value: Path | str, repo_root: Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return (repo_root / path).resolve()


def load_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        raise BuildVrmError(
            detail=f"Config file was not found: {config_path}",
            next_action="Run prepare-environment first or create the config JSON file.",
        )

    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise BuildVrmError(
            detail=f"Config JSON is invalid at line {exc.lineno}, column {exc.colno}: {exc.msg}",
            next_action="Fix the config JSON syntax and rerun the command.",
        ) from exc
    except OSError as exc:
        raise BuildVrmError(
            detail=f"Config file could not be read: {exc}",
            next_action="Check the config file path and permissions.",
        ) from exc

    if not isinstance(payload, dict):
        raise BuildVrmError(
            detail="Config JSON must be an object.",
            next_action="Rewrite the config file as a JSON object.",
        )

    blender_path = payload.get("blender_path")
    output_dir = payload.get("output_dir")
    if not isinstance(blender_path, str) or not blender_path.strip():
        raise BuildVrmError(
            detail="Config is missing a valid 'blender_path' string.",
            next_action="Add 'blender_path' to the config JSON.",
        )
    if not isinstance(output_dir, str) or not output_dir.strip():
        raise BuildVrmError(
            detail="Config is missing a valid 'output_dir' string.",
            next_action="Add 'output_dir' to the config JSON.",
        )

    return payload


def sanitize_slug(value: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in "._-" else "-" for char in value).strip("-")
    return cleaned or "build-vrm-base"


def prepare_output_paths(output_root: Path, output_name: str, timestamp: str) -> tuple[str, Path, Path]:
    run_id = f"{timestamp}-{sanitize_slug(output_name)}"
    run_dir = output_root / "blender" / run_id
    logs_dir = output_root / "logs"
    try:
        run_dir.mkdir(parents=True, exist_ok=False)
        logs_dir.mkdir(parents=True, exist_ok=True)
    except FileExistsError as exc:
        raise BuildVrmError(
            detail=f"Output run directory already exists: {run_dir}",
            next_action="Retry with a different --output-name or rerun at a different time.",
        ) from exc
    except OSError as exc:
        raise BuildVrmError(
            detail=f"Output directory could not be created: {exc}",
            next_action="Check the configured output directory permissions.",
        ) from exc
    return run_id, run_dir, logs_dir


def ensure_existing_file(path: Path, *, label: str, missing_hint: str) -> None:
    if not path.exists():
        raise BuildVrmError(
            detail=f"{label} was not found: {path}",
            next_action=missing_hint,
        )
    if path.is_dir():
        raise BuildVrmError(
            detail=f"{label} points to a directory, not a file: {path}",
            next_action=missing_hint,
        )


def save_json(path: Path, payload: dict[str, Any]) -> None:
    try:
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    except OSError as exc:
        raise BuildVrmError(
            detail=f"JSON output could not be written: {exc}",
            next_action="Check the destination directory permissions and free space.",
        ) from exc


def summarize_output(stdout: str, stderr: str) -> str:
    combined = "\n".join(part for part in (stdout.strip(), stderr.strip()) if part)
    if not combined:
        return "<no output>"
    lines = combined.splitlines()
    tail = lines[-10:]
    return "\n".join(tail)


def run_blender(
    blender_path: Path,
    blend_file: Path,
    blender_script: Path,
    output_blend: Path,
    review_render: Path,
    result_json: Path,
    texture_image: Path | None,
) -> subprocess.CompletedProcess[str]:
    command = [
        str(blender_path),
        "--background",
        str(blend_file),
        "--python",
        str(blender_script),
        "--",
        "--output-blend",
        str(output_blend),
        "--review-render",
        str(review_render),
        "--result-json",
        str(result_json),
    ]
    if texture_image is not None:
        command.extend(["--texture-image", str(texture_image)])

    try:
        return subprocess.run(command, capture_output=True, text=True, check=False)
    except OSError as exc:
        raise BuildVrmError(
            detail=f"Blender could not be started: {exc}",
            next_action="Check 'blender_path' in the config and confirm Blender can be executed from this machine.",
        ) from exc


def main() -> int:
    args = parse_args()
    try:
        repo_root = find_repo_root(Path(__file__).resolve())
        config_path = args.config.resolve() if args.config else default_config_path(repo_root)
        config = load_config(config_path)

        blender_path = resolve_repo_path(str(config["blender_path"]), repo_root)
        output_root = resolve_repo_path(str(config["output_dir"]), repo_root)
        blend_file = resolve_repo_path(args.blend_file, repo_root)
        texture_image = resolve_repo_path(args.texture_image, repo_root) if args.texture_image else None
        blender_script = repo_root / ".codex" / "skills" / "forma-character" / "blender" / "build_vrm_base.py"

        ensure_existing_file(
            blender_path,
            label="Blender executable",
            missing_hint="Update 'blender_path' in the config to the installed blender executable.",
        )
        ensure_existing_file(
            blend_file,
            label="Blend file",
            missing_hint="Pass --blend-file with an existing .blend file.",
        )
        if texture_image is not None:
            ensure_existing_file(
                texture_image,
                label="Texture image",
                missing_hint="Pass --texture-image with an existing image file or omit the flag.",
            )
        ensure_existing_file(
            blender_script,
            label="Blender build script",
            missing_hint="Restore .codex/skills/forma-character/blender/build_vrm_base.py and rerun the command.",
        )

        timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
        run_id, run_dir, logs_dir = prepare_output_paths(output_root, args.output_name, timestamp)

        output_blend = run_dir / "result.blend"
        review_render = run_dir / "review.png"
        result_json = run_dir / "blender-result.json"
        metadata_path = logs_dir / f"{run_id}.json"

        completed = run_blender(
            blender_path=blender_path,
            blend_file=blend_file,
            blender_script=blender_script,
            output_blend=output_blend,
            review_render=review_render,
            result_json=result_json,
            texture_image=texture_image,
        )

        if completed.returncode != 0:
            raise BuildVrmError(
                detail=(
                    "Blender background execution failed "
                    f"(exit {completed.returncode}).\n{summarize_output(completed.stdout, completed.stderr)}"
                ),
                next_action="Inspect the Blender output above and verify the source blend file can be opened manually.",
            )

        ensure_existing_file(
            output_blend,
            label="Updated blend output",
            missing_hint="Check the Blender script output and confirm the output directory is writable.",
        )
        ensure_existing_file(
            review_render,
            label="Review render output",
            missing_hint="Check the Blender scene camera / light setup and rerun the command.",
        )
        ensure_existing_file(
            result_json,
            label="Blender result JSON",
            missing_hint="Check the Blender script output and rerun the command.",
        )

        try:
            blender_result = json.loads(result_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise BuildVrmError(
                detail=f"Blender result JSON is invalid at line {exc.lineno}, column {exc.colno}: {exc.msg}",
                next_action="Check the Blender script output and rerun the command.",
            ) from exc
        except OSError as exc:
            raise BuildVrmError(
                detail=f"Blender result JSON could not be read: {exc}",
                next_action="Check the output directory permissions and rerun the command.",
            ) from exc

        save_json(
            metadata_path,
            {
                "command": "forma-character-build-vrm",
                "run_id": run_id,
                "timestamp_utc": datetime.now(UTC).isoformat(),
                "config_path": str(config_path),
                "blend_file": str(blend_file),
                "texture_image": str(texture_image) if texture_image else None,
                "blender_path": str(blender_path),
                "blender_script": str(blender_script),
                "output_dir": str(run_dir),
                "output_blend": str(output_blend),
                "review_render": str(review_render),
                "blender_result": blender_result,
                "blender_stdout": completed.stdout,
                "blender_stderr": completed.stderr,
                "blender_returncode": completed.returncode,
            },
        )

        print("forma-character-build-vrm")
        print(f"Run id: {run_id}")
        print(f"Output dir: {run_dir}")
        print(f"Updated blend: {output_blend}")
        print(f"Review render: {review_render}")
        print(f"Metadata: {metadata_path}")
        return 0

    except BuildVrmError as exc:
        print("forma-character-build-vrm failed")
        print(f"detail: {exc.detail}")
        print(f"next: {exc.next_action}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
