# Pipeline Notes

## Legacy compatibility flow
- `doctor`
- `generate-character-sheet`
- `generate-character-from-brief`
- `generate-expression-sheet`
- `build-vrm-base`
- `apply-motion-preview`

## Compatibility contract
- This pack keeps the legacy CLI names and `config/comfy-blender-vrm.json`.
- Entry scripts in `.codex/skills/comfy-blender-vrm/scripts/` forward to `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/`.
- `doctor` forwards to canonical `doctor`.
- `generate-character-sheet` forwards to canonical `generate_character_sheet`.
- `generate-character-from-brief` forwards to canonical `generate_character_from_brief`.
- `generate-expression-sheet` forwards to canonical `generate_expression_sheet`.
- `build-vrm-base` forwards to canonical `build_vrm_base`.
- `apply-motion-preview` forwards to canonical `apply_motion_preview`.
