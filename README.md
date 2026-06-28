# kyarakuri

`kyarakuri` is a repo-local workspace for building the Forma asset creation skills.

The current focus is `Forma Character`: character creation with local ComfyUI and Blender. The repo also includes background and background-removal helper skills.

## What This Repo Provides

- `forma-character`: create character base images, expression images, Blender workspaces, and motion previews.
- `forma-background`: create background plates with `imagegen`, then make fixed-composition time/weather variants.
- `background-transparent`: remove backgrounds from existing raster images and save transparent PNG cutouts.

## Current Status

- Phase: `P0`
- Main skill pack: [`.codex/skills/forma-character/SKILL.md`](./.codex/skills/forma-character/SKILL.md)
- Background skill: [`.codex/skills/forma-background/SKILL.md`](./.codex/skills/forma-background/SKILL.md)
- Background transparent skill: [`.codex/skills/background-transparent/SKILL.md`](./.codex/skills/background-transparent/SKILL.md)
- Default config: [`config/forma-character.json`](./config/forma-character.json)
- Project docs entry: [`docs/OVERVIEW.md`](./docs/OVERVIEW.md)

## Required Local Apps

- ComfyUI running locally, usually at `http://127.0.0.1:8000`.
- Blender installed locally for Blender-based workspace and motion preview commands.
- Codex with repo-local skills enabled.

Background generation is the exception: `forma-background` uses `imagegen`, not ComfyUI, because composition quality and fixed-layout editing are more important than local checkpoint reproducibility for backgrounds.

## Skills And Intended Use

### Forma Character

Use `forma-character` when creating character images and Blender assets.

Available public command names:

- `forma-character-prepare-environment`
- `forma-character-generate-base-image`
- `forma-character-generate-expressions`
- `forma-character-build-vrm`
- `forma-character-apply-motion-preview`

The scripts behind those commands are under `.codex/skills/forma-character/scripts/`.

### Forma Background

Use `forma-background` when creating environment/background images.

The intended flow is:

1. Ask for or infer a background brief.
2. Generate the base background with `imagegen`.
3. Save the approved base under `outputs/<project-name>/backgrounds/<location-name>/base.png`.
4. Generate weather/time variants as image edits from that approved base.
5. Preserve the same camera position, perspective, crop, layout, and object positions.

Do not use ComfyUI for background generation in this repo. If a background needs rain, snow, night, morning, or fog, edit the approved base image and change only light/weather/surface conditions.

### Background Transparent

Use `background-transparent` when an existing image needs a transparent PNG.

For character images, the best path is ComfyUI-RMBG if installed. For simple white/checker backgrounds, the Pillow fallback script can be used.

## Quick Start

### 1. Check The Environment

```powershell
python .codex/skills/forma-character/scripts/prepare_environment.py
```

This checks the configured ComfyUI URL, Blender path, workflow directory, and output directory.

The default config is:

```text
config/forma-character.json
```

### 2. Prepare A Character Brief

For repeatable character generation, prepare a brief JSON. Minimal example:

```json
{
  "character_name": "toko",
  "core_concept": "adult Japanese woman caretaker and manager of a renovated school creator residence",
  "visual_traits": "short brown hair, warm amber eyes, calm expression",
  "outfit": "white blouse, brown vest, long skirt, simple pendant",
  "personality": "kind, practical, quietly reliable",
  "pose": "standing full-body, relaxed posture"
}
```

Save it anywhere under `outputs/`, for example:

```text
outputs/toko/brief.json
```

### 3. Generate A Character Base Image

Transparent-background workflow:

```powershell
python .codex/skills/forma-character/scripts/generate_base_image.py `
  --workflow .codex/skills/forma-character/workflows/neta-yume-lumina-base-transparent.api.json `
  --brief-file outputs/toko/brief.json
```

Non-transparent workflow:

```powershell
python .codex/skills/forma-character/scripts/generate_base_image.py `
  --workflow .codex/skills/forma-character/workflows/neta-yume-lumina-base.api.json `
  --brief-file outputs/toko/brief.json
```

The base-image prompt always targets:

- standing full-body character image
- no background scene
- no explanatory text or labels

Outputs are saved under:

```text
outputs/<project-name>/images/base/<run-id>/
outputs/<project-name>/logs/
```

### 4. Generate Expressions

Use the saved base image as input:

```powershell
python .codex/skills/forma-character/scripts/generate_expressions.py `
  --workflow .codex/skills/forma-character/workflows/neta-yume-lumina-expressions.api.json `
  --base-image outputs/<project-name>/images/base/<run-id>/images/<image>.png `
  --character-prompt "<same character prompt>" `
  --expressions neutral,smile,thinking,concerned
```

Transparent-expression workflow:

```powershell
python .codex/skills/forma-character/scripts/generate_expressions.py `
  --workflow .codex/skills/forma-character/workflows/neta-yume-lumina-expressions-transparent.api.json `
  --base-image outputs/<project-name>/images/base/<run-id>/images/<image>.png `
  --character-prompt "<same character prompt>" `
  --expressions neutral,smile
```

Outputs are saved under:

```text
outputs/<project-name>/images/expressions/<run-id>/<expression>/
outputs/<project-name>/logs/
```

### 5. Create Backgrounds

Use `forma-background` through Codex natural-language requests, for example:

```text
Create a Forma background of an empty children's park. It has swings and a slide. Make one sunny base image, then make a rainy variant with exactly the same composition.
```

Expected output layout:

```text
outputs/<project-name>/backgrounds/<location-name>/brief.json
outputs/<project-name>/backgrounds/<location-name>/base.png
outputs/<project-name>/backgrounds/<location-name>/base.prompt.json
outputs/<project-name>/backgrounds/<location-name>/variants/<variant-name>.png
outputs/<project-name>/backgrounds/<location-name>/variants/<variant-name>.prompt.json
outputs/<project-name>/backgrounds/<location-name>/logs/
```

For variants, composition preservation is the top priority. The edit should keep the same camera position, crop, perspective, object positions, scale, and layout. Only weather, time, light, sky, wetness, snow, fog, or surface conditions should change.

### 6. Remove Backgrounds From Existing Images

ComfyUI-RMBG path for character images:

```powershell
uv run --with pillow python .codex/skills/background-transparent/scripts/comfyui_rmbg.py `
  image.png `
  --model BiRefNet-portrait `
  --out image-transparent.png `
  --preview image-preview.png
```

Pillow fallback for white/checker backgrounds:

```powershell
uv run --with pillow python .codex/skills/background-transparent/scripts/remove_background.py `
  image.png `
  --mode auto `
  --out image-transparent.png `
  --preview image-preview.png
```

## Bundled Workflows

The `forma-character` skill includes API-format ComfyUI workflows:

- `neta-yume-lumina-base.api.json`
- `neta-yume-lumina-base-transparent.api.json`
- `neta-yume-lumina-expressions.api.json`
- `neta-yume-lumina-expressions-transparent.api.json`

Workflow assumptions and placeholders are documented in [`.codex/skills/forma-character/workflows/README.md`](./.codex/skills/forma-character/workflows/README.md).

## Output Layout Summary

Character outputs:

```text
outputs/<project-name>/brief.json
outputs/<project-name>/images/base/<run-id>/
outputs/<project-name>/images/expressions/<run-id>/<expression>/
outputs/<project-name>/logs/
```

Background outputs:

```text
outputs/<project-name>/backgrounds/<location-name>/base.png
outputs/<project-name>/backgrounds/<location-name>/variants/<variant-name>.png
outputs/<project-name>/backgrounds/<location-name>/logs/
```

Blender and motion outputs:

```text
outputs/blender/<run-id>/
outputs/motion/<run-id>/
```

## Documentation

- Project entry: [`docs/OVERVIEW.md`](./docs/OVERVIEW.md)
- Concept: [`docs/concept.md`](./docs/concept.md)
- Spec: [`docs/spec.md`](./docs/spec.md)
- Architecture: [`docs/architecture.md`](./docs/architecture.md)
- Plan: [`docs/plan.md`](./docs/plan.md)

## Detailed ComfyUI Model And Custom Node Setup

This repository does not install ComfyUI, Blender, checkpoints, or ComfyUI custom nodes automatically. Prepare them in your local ComfyUI installation first.

### Required For Forma Character

The bundled character workflows require this checkpoint:

```text
NetaYumev35_pretrained_all_in_one.safetensors
```

Place it in the active ComfyUI checkpoints directory. For the current Windows desktop setup, the expected path is:

```text
C:\Users\<you>\Documents\ComfyUI\models\checkpoints\NetaYumev35_pretrained_all_in_one.safetensors
```

If your ComfyUI uses a different model directory, place the file in that installation's `models/checkpoints/` directory or register the directory through ComfyUI's extra model paths config.

After copying the checkpoint:

1. Restart ComfyUI, or refresh the model list if your UI supports it.
2. Confirm that `CheckpointLoaderSimple` can select `NetaYumev35_pretrained_all_in_one.safetensors`.
3. Run:

```powershell
python .codex/skills/forma-character/scripts/prepare_environment.py
```

If generation fails with a checkpoint-not-found error, the workflow is loading correctly but ComfyUI cannot see the model. Re-check the filename and checkpoint directory.

### Optional But Recommended For Transparent Character Cutouts

For higher-quality background removal, install `ComfyUI-RMBG` in the active ComfyUI `custom_nodes` directory.

Expected location:

```text
C:\Users\<you>\Documents\ComfyUI\custom_nodes\ComfyUI-RMBG
```

After installing the custom node, install its Python requirements in the same Python environment used by ComfyUI, then restart ComfyUI.

Example using the ComfyUI virtual environment:

```powershell
C:\Users\<you>\Documents\ComfyUI\.venv\Scripts\python.exe -m pip install -r C:\Users\<you>\Documents\ComfyUI\custom_nodes\ComfyUI-RMBG\requirements.txt
```

Verify that ComfyUI exposes RMBG nodes:

```powershell
$json = Invoke-RestMethod http://127.0.0.1:8000/object_info
$json | ConvertTo-Json -Depth 4 | Select-String "RMBG"
```

Recommended model choice for character art:

```text
BiRefNet-portrait
```

Fallback model to try for general objects:

```text
RMBG-2.0
```

### Not Required For Backgrounds

Background generation intentionally does not use ComfyUI. Do not install extra background checkpoints just for `forma-background`. Use `imagegen` for the base background and `imagegen` edits for fixed-composition weather/time variants.
