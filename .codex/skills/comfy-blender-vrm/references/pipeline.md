# Pipeline Notes

## Phase 1
- `doctor`
- `generate-character-sheet`
- `generate-character-from-brief`
- `generate-expression-sheet`

## Phase 2
- `build-vrm-base`
- `export-review-renders`

## Phase 3
- `apply-motion-preview`

## Current command contract
- `doctor` reads `config/comfy-blender-vrm.json` by default.
- `doctor` checks `comfyui_url`, `blender_path`, `workflow_dir`, and `output_dir`.
- `doctor` creates `output_dir` when it is missing and creation is possible.
- `doctor` fails with actionable guidance when any required item is missing or unreachable.
- `generate-character-sheet` reads an API-format workflow JSON and submits it to ComfyUI.
- `generate-character-sheet` supports placeholders for `character_prompt`, `seed`, `run_id`, and reference image values.
- `generate-character-sheet` stores images under `outputs/character/<run-id>/` and metadata under `outputs/logs/`.
- `generate-character-from-brief` collects a minimal character brief from interactive CLI input or a brief JSON file.
- `generate-character-from-brief` synthesizes `character_prompt` and reuses the same generation path as `generate-character-sheet`.
- `generate-character-from-brief` stores `brief.json` and `prompt-preview.txt` inside the generated character output directory.
- `generate-expression-sheet` uploads one base image and reuses it across multiple expression prompts.
- `generate-expression-sheet` derives per-expression seeds from a base seed and stores outputs under `outputs/expressions/<run-id>/<expression>/`.
- `generate-expression-sheet` stores run metadata under `outputs/logs/`.
- `build-vrm-base` opens an existing `.blend` in Blender background mode and optionally applies one texture image to the first mesh material.
- `build-vrm-base` stores the updated `.blend`, one review render, and run metadata under `outputs/blender/<run-id>/` and `outputs/logs/`.
- `apply-motion-preview` opens an existing `.blend`, imports one BVH motion, assigns it to the first armature, and renders one preview frame.
- `apply-motion-preview` stores the updated `.blend`, one preview render, and run metadata under `outputs/motion/<run-id>/` and `outputs/logs/`.
