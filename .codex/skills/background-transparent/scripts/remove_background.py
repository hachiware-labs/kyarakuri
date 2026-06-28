#!/usr/bin/env python3
"""Remove simple white/checker-like backgrounds from raster images."""

from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - user environment guard
    raise SystemExit("Pillow is required. Run with: uv run --with pillow python remove_background.py ...") from exc


Pixel = tuple[int, int, int, int]


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


def alpha_counts(image: Image.Image) -> dict[str, int]:
    alpha = image.getchannel("A")
    counts = {"transparent": 0, "partial": 0, "opaque": 0}
    data = alpha.get_flattened_data() if hasattr(alpha, "get_flattened_data") else alpha.getdata()
    for value in data:
        if value == 0:
            counts["transparent"] += 1
        elif value == 255:
            counts["opaque"] += 1
        else:
            counts["partial"] += 1
    return counts


def border_points(width: int, height: int) -> Iterable[tuple[int, int]]:
    for x in range(width):
        yield x, 0
        yield x, height - 1
    for y in range(1, height - 1):
        yield 0, y
        yield width - 1, y


def quantized_edge_colors(image: Image.Image, *, limit: int = 24) -> list[tuple[int, int, int]]:
    width, height = image.size
    pixels = image.load()
    buckets: dict[tuple[int, int, int], int] = {}
    for x, y in border_points(width, height):
        r, g, b, a = pixels[x, y]
        if a == 0:
            continue
        key = (round(r / 16) * 16, round(g / 16) * 16, round(b / 16) * 16)
        buckets[key] = buckets.get(key, 0) + 1
    return [color for color, _ in sorted(buckets.items(), key=lambda item: item[1], reverse=True)[:limit]]


def near_color(rgb: tuple[int, int, int], seeds: list[tuple[int, int, int]], threshold: int) -> bool:
    r, g, b = rgb
    for sr, sg, sb in seeds:
        if max(abs(r - sr), abs(g - sg), abs(b - sb)) <= threshold:
            return True
    return False


def bright_neutral(rgb: tuple[int, int, int], *, min_value: int, delta: int) -> bool:
    high = max(rgb)
    low = min(rgb)
    return low >= min_value and (high - low) <= delta


def build_predicate(args: argparse.Namespace, seeds: list[tuple[int, int, int]]):
    def is_background(pixel: Pixel) -> bool:
        r, g, b, a = pixel
        if a == 0:
            return False
        rgb = (r, g, b)
        if args.mode == "white":
            return bright_neutral(rgb, min_value=args.white_min, delta=args.neutral_delta)
        if args.mode == "checker":
            return bright_neutral(rgb, min_value=args.checker_min, delta=args.checker_delta)
        return bright_neutral(rgb, min_value=args.white_min, delta=args.neutral_delta) or (
            bright_neutral(rgb, min_value=args.checker_min, delta=args.checker_delta)
            and near_color(rgb, seeds, args.seed_threshold)
        )

    return is_background


def collect_background(image: Image.Image, predicate) -> set[tuple[int, int]]:
    width, height = image.size
    pixels = image.load()
    queue: deque[tuple[int, int]] = deque()
    selected: set[tuple[int, int]] = set()
    for point in border_points(width, height):
        if point not in selected and predicate(pixels[point[0], point[1]]):
            selected.add(point)
            queue.append(point)
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if nx < 0 or nx >= width or ny < 0 or ny >= height or (nx, ny) in selected:
                continue
            if predicate(pixels[nx, ny]):
                selected.add((nx, ny))
                queue.append((nx, ny))
    return selected


def make_preview(image: Image.Image, path: Path, color: tuple[int, int, int]) -> None:
    background = Image.new("RGBA", image.size, (*color, 255))
    Image.alpha_composite(background, image).save(path)


def default_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}-transparent.png")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Remove simple white/checker-like backgrounds from an image.")
    parser.add_argument("input", type=Path, help="Input raster image path.")
    parser.add_argument("--out", type=Path, help="Output PNG path. Defaults to <input-stem>-transparent.png.")
    parser.add_argument("--replace", action="store_true", help="Overwrite the input file. Cannot be combined with --out.")
    parser.add_argument("--mode", choices=("auto", "white", "checker"), default="auto", help="Background detector mode.")
    parser.add_argument("--preview", type=Path, help="Optional preview PNG path composited on a solid color.")
    parser.add_argument("--preview-color", type=parse_color, default=(55, 125, 220), help="Preview color as #RRGGBB.")
    parser.add_argument("--white-min", type=int, default=232, help="Minimum channel value for white background detection.")
    parser.add_argument("--neutral-delta", type=int, default=28, help="Maximum channel spread for white neutral detection.")
    parser.add_argument("--checker-min", type=int, default=196, help="Minimum channel value for checker-like neutral detection.")
    parser.add_argument("--checker-delta", type=int, default=48, help="Maximum channel spread for checker-like neutral detection.")
    parser.add_argument("--seed-threshold", type=int, default=40, help="Maximum channel distance to dominant border colors in auto mode.")
    args = parser.parse_args(argv)
    if args.replace and args.out:
        parser.error("--replace cannot be combined with --out")
    if not args.input.exists():
        parser.error(f"input does not exist: {args.input}")
    return args


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    input_path = args.input
    output_path = input_path if args.replace else args.out or default_output_path(input_path)
    image = Image.open(input_path).convert("RGBA")
    before = alpha_counts(image)
    seeds = quantized_edge_colors(image)
    predicate = build_predicate(args, seeds)
    selected = collect_background(image, predicate)

    output = image.copy()
    pixels = output.load()
    for x, y in selected:
        r, g, b, _ = pixels[x, y]
        pixels[x, y] = (r, g, b, 0)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.save(output_path)
    if args.preview:
        args.preview.parent.mkdir(parents=True, exist_ok=True)
        make_preview(output, args.preview, args.preview_color)

    result = {
        "input": str(input_path),
        "output": str(output_path),
        "preview": str(args.preview) if args.preview else None,
        "mode": args.mode,
        "size": list(output.size),
        "removed_pixels": len(selected),
        "alpha_before": before,
        "alpha_after": alpha_counts(output),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
