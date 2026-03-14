# Pipeline Notes

## Repo-local trial flow
- `kyarakuri-prepare-environment`
- `kyarakuri-generate-base-image`
- `kyarakuri-generate-expressions`
- `kyarakuri-build-vrm`
- `kyarakuri-apply-motion-preview`

## Canonical contract
- This skill pack is the repo-local canonical implementation for `kyarakuri-*`.
- Public entry scripts stay inside `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/`.
- `kyarakuri-prepare-environment` resolves to `doctor`.
- `kyarakuri-generate-base-image` resolves to `generate_character_from_brief`.
- `kyarakuri-generate-expressions` resolves to `generate_expression_sheet`.
- `kyarakuri-build-vrm` resolves to `build_vrm_base`.
- `kyarakuri-apply-motion-preview` resolves to `apply_motion_preview`.
- When `--config` is omitted, public entry scripts inject `config/kyarakuri-comfy-blender-vrm.json`.
- Legacy `comfy-blender-vrm` entry scripts forward into this pack.

## Current output behavior
- Generated base / expression outputs follow the project layout under `outputs/<project-name>/`.
- `kyarakuri-generate-base-image` saves generated images plus `brief.json` and `prompt-preview.txt` under `outputs/<project-name>/images/base/<run-id>/`.
- `kyarakuri-generate-expressions` saves expression images under `outputs/<project-name>/images/expressions/<run-id>/<expression>/`.
- `kyarakuri-build-vrm` saves the updated `.blend` and one review render under `outputs/blender/<run-id>/`.
- `kyarakuri-apply-motion-preview` saves the updated `.blend` and one preview render under `outputs/motion/<run-id>/`.
