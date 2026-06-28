#!/usr/bin/env python3
"""Offline checks for the ComfyUI-RMBG workflow builder."""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from PIL import Image

import comfyui_rmbg


def make_input(path: Path) -> None:
    Image.new("RGBA", (16, 16), (255, 255, 255, 255)).save(path)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        image_path = Path(tmp) / "input.png"
        make_input(image_path)

        rmbg_args = argparse.Namespace(
            input=image_path,
            engine="auto",
            model="RMBG-2.0",
            process_res=1024,
            sensitivity=1.0,
            mask_blur=0,
            mask_offset=0,
            refine_foreground=True,
        )
        rmbg_prompt = comfyui_rmbg.build_prompt(rmbg_args, filename_prefix="test/rmbg")
        if rmbg_prompt["2"]["class_type"] != "RMBG":
            raise AssertionError("RMBG-2.0 should use RMBG node")
        if rmbg_prompt["2"]["inputs"]["background"] != "Alpha":
            raise AssertionError("RMBG workflow must request alpha output")

        biref_args = argparse.Namespace(
            input=image_path,
            engine="auto",
            model="BiRefNet-portrait",
            process_res=1024,
            sensitivity=1.0,
            mask_blur=0,
            mask_offset=0,
            refine_foreground=True,
        )
        biref_prompt = comfyui_rmbg.build_prompt(biref_args, filename_prefix="test/biref")
        if biref_prompt["2"]["class_type"] != "BiRefNetRMBG":
            raise AssertionError("BiRefNet-* should use BiRefNetRMBG node")
        if "sensitivity" in biref_prompt["2"]["inputs"]:
            raise AssertionError("BiRefNetRMBG workflow should not pass RMBG-only sensitivity")

    print("verify-comfyui-rmbg-ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
