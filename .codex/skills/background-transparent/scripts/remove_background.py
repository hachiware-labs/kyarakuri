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


def corner_points(width: int, height: int, *, size: int) -> Iterable[tuple[int, int]]:
    ranges = (
        (range(0, size), range(0, size)),
        (range(width - size, width), range(0, size)),
        (range(0, size), range(height - size, height)),
        (range(width - size, width), range(height - size, height)),
    )
    for xs, ys in ranges:
        for x in xs:
            for y in ys:
                yield x, y


def flood_start_points(width: int, height: int, *, source: str) -> Iterable[tuple[int, int]]:
    if source == "corners":
        seed_size = max(4, min(width, height) // 32)
        yield from corner_points(width, height, size=seed_size)
        return
    yield from border_points(width, height)


def quantized_seed_colors(image: Image.Image, *, source: str, limit: int = 24) -> list[tuple[int, int, int]]:
    width, height = image.size
    pixels = image.load()
    buckets: dict[tuple[int, int, int], int] = {}
    if source == "corners":
        seed_size = max(4, min(width, height) // 16)
        points = corner_points(width, height, size=seed_size)
    else:
        points = border_points(width, height)
    for x, y in points:
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


def strong_foreground(pixel: Pixel, *, dark_max: int, saturation_min: int) -> bool:
    r, g, b, a = pixel
    if a == 0:
        return False
    high = max(r, g, b)
    low = min(r, g, b)
    return high <= dark_max or (high - low) >= saturation_min


def seed_has_bright_white(seeds: list[tuple[int, int, int]], *, min_value: int, delta: int) -> bool:
    return any(bright_neutral(seed, min_value=min_value, delta=delta) for seed in seeds)


def light_edge_background(rgb: tuple[int, int, int], *, min_value: int, delta: int) -> bool:
    high = max(rgb)
    low = min(rgb)
    return low >= min_value and (high - low) <= delta


def build_predicate(args: argparse.Namespace, seeds: list[tuple[int, int, int]]):
    auto_has_white_border = seed_has_bright_white(seeds, min_value=args.white_min, delta=args.neutral_delta)

    def is_background(pixel: Pixel) -> bool:
        r, g, b, a = pixel
        if a == 0:
            return False
        rgb = (r, g, b)
        if args.mode == "white":
            return bright_neutral(rgb, min_value=args.white_min, delta=args.neutral_delta)
        if args.mode == "checker":
            return bright_neutral(rgb, min_value=args.checker_min, delta=args.checker_delta)
        if not near_color(rgb, seeds, args.seed_threshold):
            return False
        if auto_has_white_border and bright_neutral(rgb, min_value=args.white_min, delta=args.neutral_delta):
            return True
        return light_edge_background(rgb, min_value=args.auto_min, delta=args.auto_delta)

    return is_background


def collect_background(image: Image.Image, predicate, *, source: str) -> set[tuple[int, int]]:
    width, height = image.size
    pixels = image.load()
    queue: deque[tuple[int, int]] = deque()
    selected: set[tuple[int, int]] = set()
    for point in flood_start_points(width, height, source=source):
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


def expand_background(
    image: Image.Image,
    selected: set[tuple[int, int]],
    predicate,
    protected: bytearray,
) -> set[tuple[int, int]]:
    width, height = image.size
    pixels = image.load()
    expanded = set(selected)
    queue: deque[tuple[int, int]] = deque(
        (x, y)
        for x, y in selected
        if not protected[y * width + x]
    )

    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if nx < 0 or nx >= width or ny < 0 or ny >= height or (nx, ny) in expanded:
                continue
            if protected[ny * width + nx]:
                expanded.add((nx, ny))
                continue
            if predicate(pixels[nx, ny]):
                expanded.add((nx, ny))
                queue.append((nx, ny))

    return expanded


def mark_range(mask: bytearray, width: int, start: int, end: int, fixed: int, *, axis: str) -> None:
    if start > end:
        return
    if axis == "x":
        offset = fixed * width
        for x in range(start, end + 1):
            mask[offset + x] = 1
    else:
        for y in range(start, end + 1):
            mask[y * width + fixed] = 1


def mark_enclosed_between_strong_points(
    mask: bytearray,
    strong_positions: list[int],
    *,
    limit: int,
    radius: int,
    fixed: int,
    axis: str,
    width: int,
) -> None:
    if len(strong_positions) < 2:
        return
    previous = strong_positions[0]
    for current in strong_positions[1:]:
        if current - previous <= radius * 2:
            start = max(previous + 1, current - radius)
            end = min(current - 1, previous + radius, limit - 1)
            mark_range(mask, width, start, end, fixed, axis=axis)
        previous = current


def collect_enclosed_protection(image: Image.Image, args: argparse.Namespace) -> bytearray:
    width, height = image.size
    pixels = image.load()
    protected = bytearray(width * height)
    radius = args.protect_enclosed_radius
    if radius <= 0:
        return protected

    for y in range(height):
        strong_positions = [
            x
            for x in range(width)
            if strong_foreground(
                pixels[x, y],
                dark_max=args.protect_dark_max,
                saturation_min=args.protect_saturation_min,
            )
        ]
        mark_enclosed_between_strong_points(
            protected,
            strong_positions,
            limit=width,
            radius=radius,
            fixed=y,
            axis="x",
            width=width,
        )

    for x in range(width):
        strong_positions = [
            y
            for y in range(height)
            if strong_foreground(
                pixels[x, y],
                dark_max=args.protect_dark_max,
                saturation_min=args.protect_saturation_min,
            )
        ]
        mark_enclosed_between_strong_points(
            protected,
            strong_positions,
            limit=height,
            radius=radius,
            fixed=x,
            axis="y",
            width=width,
        )

    return protected


def refinement_args(args: argparse.Namespace) -> argparse.Namespace:
    refined = argparse.Namespace(**vars(args))
    refined.seed_threshold = args.refine_seed_threshold
    refined.auto_min = args.refine_auto_min
    refined.auto_delta = args.refine_auto_delta
    return refined


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
    parser.add_argument("--auto-min", type=int, default=176, help="Minimum channel value for auto edge-color background detection.")
    parser.add_argument("--auto-delta", type=int, default=76, help="Maximum channel spread for auto edge-color background detection.")
    parser.add_argument("--seed-threshold", type=int, default=40, help="Maximum channel distance to dominant border colors in auto mode.")
    parser.add_argument(
        "--seed-source",
        choices=("corners", "border"),
        default="corners",
        help="Pixel source for auto background color seeds. Use corners to protect cropped light clothing.",
    )
    parser.add_argument(
        "--flood-source",
        choices=("corners", "border"),
        default="corners",
        help="Flood-fill start points. Use corners for cropped portraits where clothing touches image borders.",
    )
    parser.add_argument(
        "--protect-enclosed-radius",
        type=int,
        default=96,
        help="Keep background-like pixels enclosed by strong foreground strokes within this radius. Use 0 to disable.",
    )
    parser.add_argument("--protect-dark-max", type=int, default=214, help="Maximum channel value for strong dark foreground detection.")
    parser.add_argument("--protect-saturation-min", type=int, default=52, help="Minimum channel spread for strong foreground detection.")
    parser.add_argument(
        "--refine-passes",
        type=int,
        default=1,
        help="Total connected background passes. Values above 1 expand only from already selected background.",
    )
    parser.add_argument("--refine-seed-threshold", type=int, default=56, help="Seed distance used after the first pass.")
    parser.add_argument("--refine-auto-min", type=int, default=156, help="Minimum channel value used after the first pass.")
    parser.add_argument("--refine-auto-delta", type=int, default=96, help="Maximum channel spread used after the first pass.")
    args = parser.parse_args(argv)
    if args.replace and args.out:
        parser.error("--replace cannot be combined with --out")
    if not args.input.exists():
        parser.error(f"input does not exist: {args.input}")
    if args.refine_passes < 1:
        parser.error("--refine-passes must be >= 1")
    return args


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    input_path = args.input
    output_path = input_path if args.replace else args.out or default_output_path(input_path)
    image = Image.open(input_path).convert("RGBA")
    before = alpha_counts(image)
    seeds = quantized_seed_colors(image, source=args.seed_source)
    predicate = build_predicate(args, seeds)
    selected = collect_background(image, predicate, source=args.flood_source)
    protected = collect_enclosed_protection(image, args)
    pass_counts = [len(selected)]
    if args.refine_passes > 1:
        refine_predicate = build_predicate(refinement_args(args), seeds)
        for _ in range(args.refine_passes - 1):
            selected = expand_background(image, selected, refine_predicate, protected)
            pass_counts.append(len(selected))

    output = image.copy()
    pixels = output.load()
    width = image.width
    removed_pixels = 0
    protected_pixels = 0
    for x, y in selected:
        if protected[y * width + x]:
            protected_pixels += 1
            continue
        r, g, b, _ = pixels[x, y]
        pixels[x, y] = (r, g, b, 0)
        removed_pixels += 1

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
        "seed_source": args.seed_source,
        "flood_source": args.flood_source,
        "size": list(output.size),
        "removed_pixels": removed_pixels,
        "protected_pixels": protected_pixels,
        "candidate_pixels": len(selected),
        "pass_candidate_pixels": pass_counts,
        "alpha_before": before,
        "alpha_after": alpha_counts(output),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
