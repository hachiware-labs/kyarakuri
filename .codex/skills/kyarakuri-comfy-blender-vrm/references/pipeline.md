# Pipeline Notes

## Repo-local trial flow
- `kyarakuri-prepare-environment`
- `kyarakuri-generate-base-image`
- `kyarakuri-generate-expressions`
- `kyarakuri-build-vrm`
- `kyarakuri-apply-motion-preview`

## Wrapper contract
- This skill pack is repo-local and delegates to the existing `.codex/skills/comfy-blender-vrm/` implementation.
- `kyarakuri-prepare-environment` forwards to `doctor`.
- `kyarakuri-generate-base-image` forwards to `generate-character-from-brief`.
- `kyarakuri-generate-expressions` forwards to `generate-expression-sheet`.
- `kyarakuri-build-vrm` forwards to `build-vrm-base`.
- `kyarakuri-apply-motion-preview` forwards to `apply-motion-preview`.
- When `--config` is omitted, wrappers inject `config/kyarakuri-comfy-blender-vrm.json`.

## Current output behavior
- Generated outputs still follow the existing implementation layout under `outputs/`.
- `kyarakuri-generate-base-image` saves generated images plus `brief.json` and `prompt-preview.txt`.
- `kyarakuri-generate-expressions` saves expression images under `outputs/expressions/<run-id>/<expression>/`.
- `kyarakuri-build-vrm` saves the updated `.blend` and one review render under `outputs/blender/<run-id>/`.
- `kyarakuri-apply-motion-preview` saves the updated `.blend` and one preview render under `outputs/motion/<run-id>/`.
