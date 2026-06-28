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
   - For people, character art, white clothing, pale subjects, hair detail, or non-trivial backgrounds, prefer local ComfyUI-RMBG: `uv run --with pillow python <skill-dir>/scripts/comfyui_rmbg.py <input> --model BiRefNet-portrait --out <output> --preview <preview.png>`.
   - For white or checkerboard-like backgrounds when ComfyUI is not available, use the bundled deterministic script: `uv run --with pillow python <skill-dir>/scripts/remove_background.py <input> --mode auto --out <output> --preview <preview.png>`.
   - For a plain white or nearly white background, a keying workflow is acceptable if it preserves subject edges cleanly.
   - For complex backgrounds, prefer semantic background removal over simple white/checker keying.
4. Save non-destructively. Do not overwrite the source image unless the user explicitly asks for replacement.
5. Use a clear output filename such as `<original-stem>-transparent.png` or `<original-stem>-cutout.png`.
6. For project-bound outputs, save inside the current workspace and report the final path.

## ComfyUI-RMBG Path

Use `scripts/comfyui_rmbg.py` when local ComfyUI is running and `ComfyUI-RMBG` is installed. This is the preferred path for character images because it uses semantic background removal instead of global white keying.

Requirements:

- ComfyUI is reachable, usually at `http://127.0.0.1:8000`.
- `ComfyUI-RMBG` is installed under the active ComfyUI `custom_nodes` directory.
- `object_info` includes `AILab_LoadImage`, `RMBG`, and/or `BiRefNetRMBG`.

Examples:

```powershell
uv run --with pillow python .codex/skills/background-transparent/scripts/comfyui_rmbg.py image.png --model BiRefNet-portrait --out image-transparent.png --preview image-preview.png
uv run --with pillow python .codex/skills/background-transparent/scripts/comfyui_rmbg.py image.png --model RMBG-2.0 --out image-transparent.png --preview image-preview.png
uv run --with pillow python .codex/skills/background-transparent/scripts/comfyui_rmbg.py image.png --comfy-url http://127.0.0.1:8000 --model RMBG-2.0 --process-res 1024 --out image-transparent.png
```

Options to prefer:

- `--model BiRefNet-portrait`: first choice for character portraits and white clothing; it tends to preserve facial details better.
- `--model RMBG-2.0`: try for general objects or when BiRefNet leaves too much foreground fringe.
- `--mask-offset 1` or `--mask-offset 2`: slightly expands the kept subject mask when edges are over-cut.
- `--mask-blur 1` to `--mask-blur 3`: softens harsh alpha edges.
- `--no-refine-foreground`: try if foreground colors become unexpectedly altered by RMBG foreground refinement.

If this path fails because ComfyUI is down, nodes are missing, or a model cannot run on the local GPU/CPU stack, use the Pillow fallback below.

## Pillow Fallback Script

Use `scripts/remove_background.py` for deterministic local processing when the background is white, near-white, or a baked checkerboard. The script removes border-connected background-like pixels, writes a PNG, optionally writes a colored preview, and prints JSON alpha statistics.

Examples:

```powershell
uv run --with pillow python .codex/skills/background-transparent/scripts/remove_background.py image.png --mode auto --out image-transparent.png --preview image-preview.png
uv run --with pillow python .codex/skills/background-transparent/scripts/remove_background.py image.png --mode white --replace
uv run --with pillow python .codex/skills/background-transparent/scripts/remove_background.py image.png --mode checker --out image-transparent.png --preview image-preview.png --preview-color "#377ddc"
uv run --with pillow python .codex/skills/background-transparent/scripts/remove_background.py image.png --mode auto --seed-source corners --out image-transparent.png --preview image-preview.png
uv run --with pillow python .codex/skills/background-transparent/scripts/remove_background.py image.png --mode auto --seed-source corners --flood-source corners --out image-transparent.png --preview image-preview.png
uv run --with pillow python .codex/skills/background-transparent/scripts/remove_background.py image.png --mode auto --protect-enclosed-radius 96 --out image-transparent.png --preview image-preview.png
uv run --with pillow python .codex/skills/background-transparent/scripts/remove_background.py image.png --mode auto --refine-passes 2 --out image-transparent.png --preview image-preview.png
```

Options to prefer:

- `--mode auto`: first choice for typical white/checker backgrounds.
- `--mode auto`: safest default when the subject contains white clothing or pale highlights, because it follows border-connected pixels that are close to the corner background colors.
- `--seed-source corners`: default for `auto`; prefer it for cropped portraits because sleeves or white clothes can touch the image border.
- `--flood-source corners`: default flood-fill start; keeps cropped clothing on the left/right/bottom border from becoming a background seed.
- `--seed-source border`: use only when all image borders are background and corners are not representative.
- `--flood-source border`: use only when every image edge is definitely background.
- `--protect-enclosed-radius 96`: default protection for light clothing and highlights enclosed by stronger foreground strokes.
- `--refine-passes 2`: use when a first safe pass leaves background remnants. Later passes expand only from already selected background, rather than deleting near-white pixels globally.
- `--mode white`: use when the background is plain white or nearly white and the subject does not contain border-connected white clothing.
- `--mode checker`: use when the source has a baked checkerboard background.
- `--preview <path>`: generate a colored preview before deciding whether to overwrite a project asset.
- `--replace`: overwrite only when the user explicitly asked for replacement.

When the subject has a white blouse, pale sleeves, bright hair highlights, or other light details, prefer `--mode auto --seed-source corners --flood-source corners` first and inspect the preview. If the preview keeps the subject but leaves background fringe, rerun with `--refine-passes 2`. Avoid `--mode white` and `--flood-source border` for cropped portraits where white clothing touches the image edge.

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
