#!/usr/bin/env python3
"""Run ComfyUI-RMBG through the ComfyUI HTTP API and save an alpha PNG."""

from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from pathlib import Path
from urllib import parse, request
from urllib.error import HTTPError, URLError

try:
    from PIL import Image
except ImportError:  # pragma: no cover - preview is optional but useful
    Image = None


RMBG_MODELS = {"RMBG-2.0", "INSPYRENET", "BEN", "BEN2"}


def parse_color(value: str) -> tuple[int, int, int]:
    raw = value.strip()
    if raw.startswith("#"):
        raw = raw[1:]
    if len(raw) != 6:
        raise argparse.ArgumentTypeError("color must be #RRGGBB")
    try:
        return int(raw[0:2], 16), int(raw[2:4], 16), int(raw[4:6], 16)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("color must be #RRGGBB") from exc


def default_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}-transparent.png")


def alpha_counts(path: Path) -> dict[str, int] | None:
    if Image is None:
        return None
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A")
    data = alpha.get_flattened_data() if hasattr(alpha, "get_flattened_data") else alpha.getdata()
    counts = {"transparent": 0, "partial": 0, "opaque": 0}
    for value in data:
        if value == 0:
            counts["transparent"] += 1
        elif value == 255:
            counts["opaque"] += 1
        else:
            counts["partial"] += 1
    return counts


def make_preview(image_path: Path, preview_path: Path, color: tuple[int, int, int]) -> None:
    if Image is None:
        raise SystemExit("Pillow is required for --preview. Run with: uv run --with pillow python comfyui_rmbg.py ...")
    image = Image.open(image_path).convert("RGBA")
    background = Image.new("RGBA", image.size, (*color, 255))
    Image.alpha_composite(background, image).save(preview_path)


def http_json(url: str, *, timeout: int) -> dict:
    try:
        with request.urlopen(url, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"failed to GET {url}: {exc}") from exc


def post_json(url: str, payload: dict, *, timeout: int) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        detail = ""
        if isinstance(exc, HTTPError):
            detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"failed to POST {url}: {exc} {detail}".strip()) from exc


def get_bytes(url: str, *, timeout: int) -> bytes:
    try:
        with request.urlopen(url, timeout=timeout) as response:
            return response.read()
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"failed to GET {url}: {exc}") from exc


def choose_engine(model: str, engine: str) -> str:
    if engine != "auto":
        return engine
    if model.startswith("BiRefNet"):
        return "birefnet"
    return "rmbg"


def build_prompt(args: argparse.Namespace, *, filename_prefix: str) -> dict:
    engine = choose_engine(args.model, args.engine)
    nodes: dict[str, dict] = {
        "1": {
            "class_type": "AILab_LoadImage",
            "inputs": {
                "image_path_or_URL": str(args.input),
                "image": "",
                "upscale_method": "lanczos",
                "megapixels": 0.0,
                "scale_by": 1.0,
                "resize_mode": "longest_side",
                "size": 0,
            },
        },
        "3": {
            "class_type": "SaveImage",
            "inputs": {
                "images": ["2", 0],
                "filename_prefix": filename_prefix,
            },
        },
    }

    if engine == "birefnet":
        nodes["2"] = {
            "class_type": "BiRefNetRMBG",
            "inputs": {
                "image": ["1", 0],
                "model": args.model,
                "mask_blur": args.mask_blur,
                "mask_offset": args.mask_offset,
                "invert_output": False,
                "refine_foreground": args.refine_foreground,
                "background": "Alpha",
                "background_color": "#222222",
            },
        }
    else:
        nodes["2"] = {
            "class_type": "RMBG",
            "inputs": {
                "image": ["1", 0],
                "model": args.model,
                "sensitivity": args.sensitivity,
                "process_res": args.process_res,
                "mask_blur": args.mask_blur,
                "mask_offset": args.mask_offset,
                "invert_output": False,
                "refine_foreground": args.refine_foreground,
                "background": "Alpha",
                "background_color": "#222222",
            },
        }
    return nodes


def require_nodes(comfy_url: str, class_names: set[str], *, timeout: int) -> None:
    info = http_json(f"{comfy_url.rstrip('/')}/object_info", timeout=timeout)
    missing = sorted(name for name in class_names if name not in info)
    if missing:
        raise RuntimeError(f"ComfyUI is missing required node(s): {', '.join(missing)}")


def wait_for_history(comfy_url: str, prompt_id: str, *, timeout: int, poll_interval: float) -> dict:
    deadline = time.time() + timeout
    history_url = f"{comfy_url.rstrip('/')}/history/{prompt_id}"
    while time.time() < deadline:
        history = http_json(history_url, timeout=10)
        if prompt_id in history:
            item = history[prompt_id]
            status = item.get("status", {})
            if status.get("completed") is True:
                return item
            raise RuntimeError(f"ComfyUI prompt did not complete: {json.dumps(status, ensure_ascii=False)}")
        time.sleep(poll_interval)
    raise RuntimeError(f"timed out waiting for ComfyUI prompt: {prompt_id}")


def download_saved_image(comfy_url: str, history_item: dict, output_path: Path, *, timeout: int) -> dict:
    outputs = history_item.get("outputs", {})
    images = outputs.get("3", {}).get("images", [])
    if not images:
        raise RuntimeError("ComfyUI history did not contain SaveImage output for node 3")
    image = images[0]
    query = parse.urlencode(
        {
            "filename": image["filename"],
            "subfolder": image.get("subfolder", ""),
            "type": image.get("type", "output"),
        }
    )
    data = get_bytes(f"{comfy_url.rstrip('/')}/view?{query}", timeout=timeout)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(data)
    return image


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Remove image background with ComfyUI-RMBG.")
    parser.add_argument("input", type=Path, help="Input image path.")
    parser.add_argument("--out", type=Path, help="Output PNG path. Defaults to <input-stem>-transparent.png.")
    parser.add_argument("--preview", type=Path, help="Optional preview PNG path composited on a solid color.")
    parser.add_argument("--preview-color", type=parse_color, default=(55, 125, 220), help="Preview color as #RRGGBB.")
    parser.add_argument("--comfy-url", default="http://127.0.0.1:8000", help="ComfyUI base URL.")
    parser.add_argument("--engine", choices=("auto", "rmbg", "birefnet"), default="auto", help="ComfyUI-RMBG node family.")
    parser.add_argument("--model", default="BiRefNet-portrait", help="RMBG model name, for example BiRefNet-portrait or RMBG-2.0.")
    parser.add_argument("--process-res", type=int, default=1024, help="RMBG processing resolution.")
    parser.add_argument("--sensitivity", type=float, default=1.0, help="RMBG mask sensitivity.")
    parser.add_argument("--mask-blur", type=int, default=0, help="Mask blur amount.")
    parser.add_argument("--mask-offset", type=int, default=0, help="Mask boundary offset.")
    parser.add_argument("--refine-foreground", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--timeout", type=int, default=600, help="Total wait timeout in seconds.")
    parser.add_argument("--poll-interval", type=float, default=2.0, help="Prompt polling interval in seconds.")
    args = parser.parse_args(argv)
    if not args.input.exists():
        parser.error(f"input does not exist: {args.input}")
    engine = choose_engine(args.model, args.engine)
    if engine == "rmbg" and args.model not in RMBG_MODELS:
        parser.error(f"RMBG engine model must be one of: {', '.join(sorted(RMBG_MODELS))}")
    if engine == "birefnet" and not args.model.startswith("BiRefNet"):
        parser.error("BiRefNet engine model must start with 'BiRefNet'")
    return args


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    output_path = args.out or default_output_path(args.input)
    engine = choose_engine(args.model, args.engine)
    class_name = "BiRefNetRMBG" if engine == "birefnet" else "RMBG"
    require_nodes(args.comfy_url, {"AILab_LoadImage", class_name, "SaveImage"}, timeout=20)

    prefix = f"background-transparent/{args.input.stem}-{uuid.uuid4().hex[:8]}"
    prompt = build_prompt(args, filename_prefix=prefix)
    response = post_json(
        f"{args.comfy_url.rstrip('/')}/prompt",
        {"client_id": f"background-transparent-{uuid.uuid4()}", "prompt": prompt},
        timeout=20,
    )
    prompt_id = response["prompt_id"]
    history_item = wait_for_history(
        args.comfy_url,
        prompt_id,
        timeout=args.timeout,
        poll_interval=args.poll_interval,
    )
    saved_image = download_saved_image(args.comfy_url, history_item, output_path, timeout=60)
    if args.preview:
        args.preview.parent.mkdir(parents=True, exist_ok=True)
        make_preview(output_path, args.preview, args.preview_color)

    result = {
        "input": str(args.input),
        "output": str(output_path),
        "preview": str(args.preview) if args.preview else None,
        "comfy_url": args.comfy_url,
        "engine": engine,
        "model": args.model,
        "prompt_id": prompt_id,
        "saved_image": saved_image,
        "alpha_after": alpha_counts(output_path),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
