# comfy-blender-vrm

Local skill pack for character creation workflows driven by ComfyUI and Blender.

## Current scope
- `doctor`: implemented
- `generate-character-sheet`: implemented
- `generate-character-from-brief`: implemented
- `generate-expression-sheet`: implemented
- `build-vrm-base`: planned
- `apply-motion-preview`: planned

## Purpose
- Validate the local ComfyUI endpoint.
- Validate the Blender executable path.
- Validate required workflow and output directories.
- Keep outputs and configuration under the current repository.

## Usage
```powershell
python .codex/skills/comfy-blender-vrm/scripts/doctor.py
python .codex/skills/comfy-blender-vrm/scripts/doctor.py --config config/comfy-blender-vrm.json
python .codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py --workflow path\\to\\character.api.json --character-prompt "front-facing anime character"
python .codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py --workflow path\\to\\character.api.json --character-prompt "front-facing anime character" --reference-image path\\to\\ref.png --seed 12345
python .codex/skills/comfy-blender-vrm/scripts/generate_character_from_brief.py --workflow path\\to\\character.api.json
python .codex/skills/comfy-blender-vrm/scripts/generate_character_from_brief.py --workflow path\\to\\character.api.json --brief-file path\\to\\brief.json --seed 12345
python .codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py --workflow path\\to\\expressions.api.json --base-image path\\to\\character.png --character-prompt "same anime character" 
python .codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py --workflow path\\to\\expressions.api.json --base-image path\\to\\character.png --character-prompt "same anime character" --expressions neutral,smile,angry --seed 12345
```

## Defaults
- Default config path: `config/comfy-blender-vrm.json`
- Relative paths inside the config are resolved from the repository root.

## References
- Pipeline notes: `./references/pipeline.md`
- Character brief schema: `./references/character_brief.md`
- Workflow notes: `./workflows/README.md`
- Latest delta: `docs/delta/DR-20260313-generate-character-from-brief.md`
