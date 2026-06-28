---
name: background-transparent
description: Make raster image backgrounds transparent and save clean PNG cutouts. Use when the user asks to remove a background, make the background transparent, create a cutout, alpha PNG, transparent PNG, 背景透明化, 背景を透明にする, or 背景を消す for an existing image.
---

# Background Transparent

## Workflow

Use this skill for existing raster images that need a transparent background.

1. Identify the edit target image. If the user provided a local path, inspect it first so the image content is visible before editing.
2. Treat the requested edit as background extraction: remove only the background and preserve the main subject, pose, expression, clothing, colors, line art, transparency-worthy edges, and image resolution as much as possible.
3. Use an image editing path suitable for the input:
   - For white or checkerboard-like backgrounds, prefer the bundled deterministic script: `uv run --with pillow python <skill-dir>/scripts/remove_background.py <input> --mode auto --out <output> --preview <preview.png>`.
   - For a plain white or nearly white background, a keying workflow is acceptable if it preserves subject edges cleanly.
   - For complex backgrounds, prefer semantic background removal over simple white/checker keying.
4. Save non-destructively. Do not overwrite the source image unless the user explicitly asks for replacement.
5. Use a clear output filename such as `<original-stem>-transparent.png` or `<original-stem>-cutout.png`.
6. For project-bound outputs, save inside the current workspace and report the final path.

## Bundled Script

Use `scripts/remove_background.py` for deterministic local processing when the background is white, near-white, or a baked checkerboard. The script removes border-connected background-like pixels, writes a PNG, optionally writes a colored preview, and prints JSON alpha statistics.

Examples:

```powershell
uv run --with pillow python .codex/skills/background-transparent/scripts/remove_background.py image.png --mode auto --out image-transparent.png --preview image-preview.png
uv run --with pillow python .codex/skills/background-transparent/scripts/remove_background.py image.png --mode white --replace
uv run --with pillow python .codex/skills/background-transparent/scripts/remove_background.py image.png --mode checker --out image-transparent.png --preview image-preview.png --preview-color "#377ddc"
```

Options to prefer:

- `--mode auto`: first choice for typical white/checker backgrounds.
- `--mode white`: use when the background is plain white or nearly white.
- `--mode checker`: use when the source has a baked checkerboard background.
- `--preview <path>`: generate a colored preview before deciding whether to overwrite a project asset.
- `--replace`: overwrite only when the user explicitly asked for replacement.

## Prompt Pattern

Use a concise edit prompt like:

```text
Use case: background-extraction
Primary request: Remove the background and return a transparent PNG cutout.
Input images: Image 1 is the edit target.
Constraints: Change only the background; preserve the subject identity, pose, expression, clothing, colors, line art, edges, and resolution as much as possible. No new background, no text, no watermark.
Avoid: cropping the subject, changing the character design, adding shadows, adding outlines unless they already exist.
```

## Quality Check

Before finishing, check:

- The output is PNG with an alpha / transparent background when the tool exposes that information or visual inspection can confirm it.
- The subject is not cropped or redesigned.
- Hair, clothing edges, and small accessories remain readable.
- The saved file path is reported to the user.
