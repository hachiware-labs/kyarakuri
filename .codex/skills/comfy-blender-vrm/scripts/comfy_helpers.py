from __future__ import annotations

import json
import re
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request


TOKEN_PATTERN = re.compile(r"\{\{([a-zA-Z0-9_]+)\}\}")


class GenerationError(Exception):
    def __init__(self, detail: str, next_action: str) -> None:
        super().__init__(detail)
        self.detail = detail
        self.next_action = next_action


@dataclass
class DownloadedImage:
    node_id: str
    filename: str
    subfolder: str
    image_type: str
    saved_path: str


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "AGENTS.md").exists() and (candidate / "docs").is_dir():
            return candidate
    raise GenerationError(
        detail="Repository root could not be found from the script location.",
        next_action="Run the script inside the project workspace.",
    )


def default_config_path(repo_root: Path) -> Path:
    return repo_root / "config" / "comfy-blender-vrm.json"


def resolve_repo_path(path_value: Path | str, repo_root: Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return (repo_root / path).resolve()


def load_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        raise GenerationError(
            detail=f"Config file was not found: {config_path}",
            next_action="Run doctor first or create config/comfy-blender-vrm.json.",
        )

    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise GenerationError(
            detail=f"Config JSON is invalid at line {exc.lineno}, column {exc.colno}: {exc.msg}",
            next_action="Fix the config JSON syntax and rerun the command.",
        ) from exc
    except OSError as exc:
        raise GenerationError(
            detail=f"Config file could not be read: {exc}",
            next_action="Check the config file path and permissions.",
        ) from exc

    if not isinstance(payload, dict):
        raise GenerationError(
            detail="Config JSON must be an object.",
            next_action="Rewrite the config file as a JSON object.",
        )

    comfyui_url = payload.get("comfyui_url")
    output_dir = payload.get("output_dir")
    if not isinstance(comfyui_url, str) or not comfyui_url.strip():
        raise GenerationError(
            detail="Config is missing a valid 'comfyui_url' string.",
            next_action="Add 'comfyui_url' to config/comfy-blender-vrm.json.",
        )
    if not isinstance(output_dir, str) or not output_dir.strip():
        raise GenerationError(
            detail="Config is missing a valid 'output_dir' string.",
            next_action="Add 'output_dir' to config/comfy-blender-vrm.json.",
        )
    return payload


def load_workflow_payload(workflow_path: Path) -> dict[str, Any]:
    if not workflow_path.exists():
        raise GenerationError(
            detail=f"Workflow file was not found: {workflow_path}",
            next_action="Pass --workflow with an existing API-format workflow JSON file.",
        )

    try:
        payload = json.loads(workflow_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise GenerationError(
            detail=f"Workflow JSON is invalid at line {exc.lineno}, column {exc.colno}: {exc.msg}",
            next_action="Fix the workflow JSON syntax or re-export the API workflow.",
        ) from exc
    except OSError as exc:
        raise GenerationError(
            detail=f"Workflow file could not be read: {exc}",
            next_action="Check the workflow path and file permissions.",
        ) from exc

    if not isinstance(payload, dict):
        raise GenerationError(
            detail="Workflow JSON must be an object.",
            next_action="Export an API-format workflow JSON from ComfyUI.",
        )

    if "prompt" in payload and isinstance(payload["prompt"], dict):
        payload = payload["prompt"]
    if "nodes" in payload and "links" in payload:
        raise GenerationError(
            detail="Workflow JSON looks like a UI export, not an API-format prompt.",
            next_action="Export the workflow in API format or provide a prompt JSON file.",
        )
    if not payload or not all(isinstance(key, str) and isinstance(value, dict) for key, value in payload.items()):
        raise GenerationError(
            detail="Workflow JSON must be a prompt object keyed by node id strings.",
            next_action="Provide an API-format workflow JSON that can be sent to POST /prompt.",
        )
    return payload


def upload_reference_image(base_url: str, image_path: Path) -> dict[str, Any]:
    if not image_path.exists():
        raise GenerationError(
            detail=f"Reference image was not found: {image_path}",
            next_action="Pass --reference-image with an existing image file or omit the flag.",
        )

    boundary = uuid.uuid4().hex
    try:
        image_bytes = image_path.read_bytes()
    except OSError as exc:
        raise GenerationError(
            detail=f"Reference image could not be read: {exc}",
            next_action="Check the reference image path and file permissions.",
        ) from exc

    parts: list[bytes] = []
    for name, value in (("type", "input"), ("overwrite", "true")):
        parts.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"),
                f"{value}\r\n".encode("utf-8"),
            ]
        )
    parts.extend(
        [
            f"--{boundary}\r\n".encode("utf-8"),
            f'Content-Disposition: form-data; name="image"; filename="{image_path.name}"\r\n'.encode("utf-8"),
            b"Content-Type: application/octet-stream\r\n\r\n",
            image_bytes,
            b"\r\n",
            f"--{boundary}--\r\n".encode("utf-8"),
        ]
    )

    req = request.Request(
        f"{base_url.rstrip('/')}/upload/image",
        data=b"".join(parts),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        raise GenerationError(
            detail=f"ComfyUI upload failed with HTTP {exc.code}.",
            next_action="Check that the ComfyUI server is running and accepts image uploads.",
        ) from exc
    except error.URLError as exc:
        raise GenerationError(
            detail=f"ComfyUI upload failed: {exc.reason}",
            next_action="Check that ComfyUI is running at the configured URL.",
        ) from exc

    if not isinstance(payload, dict):
        raise GenerationError(
            detail="ComfyUI upload response was not a JSON object.",
            next_action="Check the ComfyUI server version and upload API compatibility.",
        )
    return payload


def render_template(value: Any, placeholders: dict[str, Any]) -> Any:
    if isinstance(value, str):
        exact_match = TOKEN_PATTERN.fullmatch(value)
        if exact_match:
            token_name = exact_match.group(1)
            if token_name in placeholders:
                return placeholders[token_name]
            return value

        rendered = value
        for token_name, replacement in placeholders.items():
            rendered = rendered.replace(f"{{{{{token_name}}}}}", str(replacement))
        return rendered
    if isinstance(value, dict):
        return {key: render_template(child, placeholders) for key, child in value.items()}
    if isinstance(value, list):
        return [render_template(child, placeholders) for child in value]
    return value


def collect_unresolved_tokens(value: Any) -> list[str]:
    tokens: list[str] = []
    if isinstance(value, str):
        tokens.extend(match.group(0) for match in TOKEN_PATTERN.finditer(value))
    elif isinstance(value, dict):
        for child in value.values():
            tokens.extend(collect_unresolved_tokens(child))
    elif isinstance(value, list):
        for child in value:
            tokens.extend(collect_unresolved_tokens(child))
    return sorted(set(tokens))


def post_json(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    req = request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=30) as response:
            data = response.read().decode("utf-8")
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise GenerationError(
            detail=f"ComfyUI request failed with HTTP {exc.code}: {body}",
            next_action="Check the workflow content and confirm the ComfyUI API is reachable.",
        ) from exc
    except error.URLError as exc:
        raise GenerationError(
            detail=f"ComfyUI request failed: {exc.reason}",
            next_action="Check that ComfyUI is running at the configured URL.",
        ) from exc

    try:
        decoded = json.loads(data)
    except json.JSONDecodeError as exc:
        raise GenerationError(
            detail=f"ComfyUI returned invalid JSON: {exc.msg}",
            next_action="Check the ComfyUI server logs for the failed request.",
        ) from exc

    if not isinstance(decoded, dict):
        raise GenerationError(
            detail="ComfyUI response must be a JSON object.",
            next_action="Check the ComfyUI server version and endpoint compatibility.",
        )
    return decoded


def get_json(url: str) -> dict[str, Any]:
    req = request.Request(url, method="GET")
    try:
        with request.urlopen(req, timeout=30) as response:
            data = response.read().decode("utf-8")
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise GenerationError(
            detail=f"ComfyUI history request failed with HTTP {exc.code}: {body}",
            next_action="Check the prompt id and ComfyUI server logs.",
        ) from exc
    except error.URLError as exc:
        raise GenerationError(
            detail=f"ComfyUI history request failed: {exc.reason}",
            next_action="Check that ComfyUI is still reachable during polling.",
        ) from exc

    try:
        decoded = json.loads(data)
    except json.JSONDecodeError as exc:
        raise GenerationError(
            detail=f"ComfyUI returned invalid JSON: {exc.msg}",
            next_action="Check the ComfyUI server logs for the history response.",
        ) from exc

    if not isinstance(decoded, dict):
        raise GenerationError(
            detail="ComfyUI history response must be a JSON object.",
            next_action="Check the ComfyUI server version and endpoint compatibility.",
        )
    return decoded


def wait_for_history(base_url: str, prompt_id: str, timeout_seconds: int, poll_interval: float) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        payload = get_json(f"{base_url.rstrip('/')}/history/{prompt_id}")
        entry = payload.get(prompt_id)
        if isinstance(entry, dict):
            status = entry.get("status")
            if isinstance(status, dict) and status.get("status_str") == "error":
                raise GenerationError(
                    detail=f"ComfyUI reported an error for prompt {prompt_id}: {status}",
                    next_action="Inspect the workflow and ComfyUI server logs for the failed nodes.",
                )
            if isinstance(entry.get("outputs"), dict):
                return entry
        elif isinstance(payload.get("outputs"), dict):
            return payload
        time.sleep(poll_interval)

    raise GenerationError(
        detail=f"ComfyUI job did not finish within {timeout_seconds} seconds.",
        next_action="Increase --timeout-seconds or inspect the ComfyUI queue for stalled jobs.",
    )


def collect_images(history_entry: dict[str, Any]) -> list[dict[str, str]]:
    outputs = history_entry.get("outputs")
    if not isinstance(outputs, dict):
        return []

    records: list[dict[str, str]] = []
    for node_id, node_payload in outputs.items():
        if not isinstance(node_payload, dict):
            continue
        images = node_payload.get("images")
        if not isinstance(images, list):
            continue
        for image in images:
            if not isinstance(image, dict):
                continue
            filename = image.get("filename")
            if not isinstance(filename, str):
                continue
            records.append(
                {
                    "node_id": str(node_id),
                    "filename": filename,
                    "subfolder": str(image.get("subfolder", "")),
                    "type": str(image.get("type", "output")),
                }
            )
    return records


def download_file(url: str, destination: Path) -> None:
    req = request.Request(url, method="GET")
    try:
        with request.urlopen(req, timeout=30) as response:
            destination.write_bytes(response.read())
    except error.HTTPError as exc:
        raise GenerationError(
            detail=f"Image download failed with HTTP {exc.code} for {destination.name}.",
            next_action="Check that the ComfyUI output file still exists on disk.",
        ) from exc
    except error.URLError as exc:
        raise GenerationError(
            detail=f"Image download failed: {exc.reason}",
            next_action="Check that ComfyUI is reachable while downloading outputs.",
        ) from exc
    except OSError as exc:
        raise GenerationError(
            detail=f"Downloaded image could not be written: {exc}",
            next_action="Check the output directory permissions and free space.",
        ) from exc


def sanitize_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")
    return slug or "character-sheet"


def prepare_output_paths(output_root: Path, output_name: str, timestamp: str) -> tuple[str, Path, Path]:
    run_id = f"{timestamp}-{sanitize_slug(output_name)}"
    character_dir = output_root / "character" / run_id
    images_dir = character_dir / "images"
    logs_dir = output_root / "logs"
    try:
        images_dir.mkdir(parents=True, exist_ok=False)
        logs_dir.mkdir(parents=True, exist_ok=True)
    except FileExistsError as exc:
        raise GenerationError(
            detail=f"Output run directory already exists: {images_dir.parent}",
            next_action="Retry with a different --output-name or rerun at a different time.",
        ) from exc
    except OSError as exc:
        raise GenerationError(
            detail=f"Output directory could not be created: {exc}",
            next_action="Check the configured output directory permissions.",
        ) from exc
    return run_id, character_dir, logs_dir


def save_json(path: Path, payload: dict[str, Any]) -> None:
    try:
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    except OSError as exc:
        raise GenerationError(
            detail=f"JSON output could not be written: {exc}",
            next_action="Check the destination directory permissions and free space.",
        ) from exc
