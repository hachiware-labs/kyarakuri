#!/usr/bin/env python3
"""Smoke checks for deterministic background removal."""

from __future__ import annotations

import tempfile
from pathlib import Path

from PIL import Image

import remove_background


def run_case(input_path: Path, output_path: Path, mode: str, extra_args: list[str] | None = None) -> Image.Image:
    argv = [str(input_path), "--mode", mode, "--out", str(output_path)]
    if extra_args:
        argv.extend(extra_args)
    code = remove_background.main(argv)
    if code != 0:
        raise AssertionError(f"remove_background returned {code}")
    return Image.open(output_path).convert("RGBA")


def make_white_subject_on_warm_background(path: Path) -> None:
    image = Image.new("RGBA", (96, 96), (232, 219, 190, 255))
    pixels = image.load()
    for y in range(12, 96):
        for x in range(34, 62):
            pixels[x, y] = (246, 244, 236, 255)
    for y in range(12, 96):
        pixels[33, y] = (96, 70, 48, 255)
        pixels[62, y] = (96, 70, 48, 255)
    for x in range(34, 62):
        pixels[x, 12] = (96, 70, 48, 255)
    image.save(path)


def make_enclosed_white_clothing(path: Path) -> None:
    image = Image.new("RGBA", (128, 128), (232, 219, 190, 255))
    pixels = image.load()
    for y in range(24, 128):
        for x in range(44, 84):
            pixels[x, y] = (246, 244, 236, 255)
    for y in range(24, 128):
        pixels[43, y] = (100, 64, 36, 255)
        pixels[84, y] = (100, 64, 36, 255)
    for x in range(44, 84):
        pixels[x, 24] = (100, 64, 36, 255)
    image.save(path)


def make_plain_white_background(path: Path) -> None:
    image = Image.new("RGBA", (96, 96), (248, 248, 248, 255))
    pixels = image.load()
    for y in range(24, 72):
        for x in range(32, 64):
            pixels[x, y] = (120, 90, 58, 255)
    image.save(path)


def count_transparent(image: Image.Image, box: tuple[int, int, int, int]) -> int:
    alpha = image.getchannel("A").crop(box)
    data = alpha.get_flattened_data() if hasattr(alpha, "get_flattened_data") else alpha.getdata()
    return sum(1 for value in data if value == 0)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        warm_input = tmp_path / "warm-bg-white-subject.png"
        warm_output = tmp_path / "warm-bg-white-subject-out.png"
        make_white_subject_on_warm_background(warm_input)
        warm = run_case(warm_input, warm_output, "auto")
        subject_transparent = count_transparent(warm, (34, 12, 62, 96))
        background_transparent = count_transparent(warm, (0, 0, 20, 20))
        if subject_transparent != 0:
            raise AssertionError(f"white subject became transparent: {subject_transparent} pixels")
        if background_transparent < 300:
            raise AssertionError("warm background was not removed")

        white_input = tmp_path / "plain-white-bg.png"
        white_output = tmp_path / "plain-white-bg-out.png"
        make_plain_white_background(white_input)
        white = run_case(white_input, white_output, "auto")
        center_transparent = count_transparent(white, (32, 24, 64, 72))
        edge_transparent = count_transparent(white, (0, 0, 20, 20))
        if center_transparent != 0:
            raise AssertionError(f"center subject became transparent: {center_transparent} pixels")
        if edge_transparent < 300:
            raise AssertionError("plain white background was not removed")

        clothing_input = tmp_path / "enclosed-white-clothing.png"
        clothing_output = tmp_path / "enclosed-white-clothing-out.png"
        make_enclosed_white_clothing(clothing_input)
        clothing = run_case(clothing_input, clothing_output, "auto", ["--refine-passes", "2"])
        clothing_transparent = count_transparent(clothing, (44, 24, 84, 128))
        clothing_edge_transparent = count_transparent(clothing, (0, 0, 24, 24))
        if clothing_transparent != 0:
            raise AssertionError(f"white clothing became transparent: {clothing_transparent} pixels")
        if clothing_edge_transparent < 500:
            raise AssertionError("background around enclosed clothing was not removed")

    print("verify-remove-background-ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
