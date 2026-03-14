# Pipeline Notes

## Repo-local trial flow
- `forma-character-prepare-environment`
- `forma-character-generate-base-image`
- `forma-character-generate-expressions`
- `forma-character-build-vrm`
- `forma-character-apply-motion-preview`

## Canonical contract
- This skill pack is the repo-local canonical implementation for `forma-character-*`.
- Public entry scripts stay inside `.codex/skills/forma-character/scripts/`.
- `forma-character-prepare-environment` resolves to `doctor`.
- `forma-character-generate-base-image` resolves to `generate_character_from_brief`.
- `forma-character-generate-expressions` resolves to `generate_expression_sheet`.
- `forma-character-build-vrm` resolves to `build_vrm_base`.
- `forma-character-apply-motion-preview` resolves to `apply_motion_preview`.
- When `--config` is omitted, public entry scripts inject `config/forma-character.json`.

## Current output behavior
- Generated base / expression outputs follow the project layout under `outputs/<project-name>/`.
- `forma-character-generate-base-image` saves generated images plus `brief.json` and `prompt-preview.txt` under `outputs/<project-name>/images/base/<run-id>/`.
- `forma-character-generate-expressions` saves expression images under `outputs/<project-name>/images/expressions/<run-id>/<expression>/`.
- `forma-character-build-vrm` saves the updated `.blend` and one review render under `outputs/blender/<run-id>/`.
- `forma-character-apply-motion-preview` saves the updated `.blend` and one preview render under `outputs/motion/<run-id>/`.
