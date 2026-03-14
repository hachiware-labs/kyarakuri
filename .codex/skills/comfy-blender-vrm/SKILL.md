# comfy-blender-vrm

Legacy compatibility skill pack for the pre-release `comfy-blender-vrm` command names.

## Current scope
- `doctor`: compatibility wrapper
- `generate-character-sheet`: compatibility wrapper
- `generate-character-from-brief`: compatibility wrapper
- `generate-expression-sheet`: compatibility wrapper
- `build-vrm-base`: compatibility wrapper
- `apply-motion-preview`: compatibility wrapper

## Purpose
- Preserve the legacy CLI names and default config path.
- Forward execution into the canonical `kyarakuri-comfy-blender-vrm` implementation.
- Keep existing local workflows and examples callable during the release transition.

## Usage
```powershell
python .codex/skills/comfy-blender-vrm/scripts/doctor.py
python .codex/skills/comfy-blender-vrm/scripts/doctor.py --config config/comfy-blender-vrm.json
python .codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py --workflow path\\to\\character.api.json --character-prompt "front-facing anime character"
python .codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py --workflow path\\to\\character.api.json --character-prompt "front-facing anime character" --reference-image path\\to\\ref.png --seed 12345
python .codex/skills/comfy-blender-vrm/scripts/generate_character_from_brief.py --workflow path\\to\\character.api.json
python .codex/skills/comfy-blender-vrm/scripts/generate_character_from_brief.py --workflow path\\to\\character.api.json --brief-file path\\to\\brief.json --seed 12345
python .codex/skills/comfy-blender-vrm/scripts/generate_character_from_brief.py --workflow .codex\\skills\\comfy-blender-vrm\\workflows\\neta-yume-lumina-base.api.json
python .codex/skills/comfy-blender-vrm/scripts/generate_character_from_brief.py --workflow .codex\\skills\\comfy-blender-vrm\\workflows\\neta-yume-lumina-base-transparent.api.json
python .codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py --workflow path\\to\\expressions.api.json --base-image path\\to\\character.png --character-prompt "same anime character"
python .codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py --workflow path\\to\\expressions.api.json --base-image path\\to\\character.png --character-prompt "same anime character" --expressions neutral,smile,angry --seed 12345
python .codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py --workflow .codex\\skills\\comfy-blender-vrm\\workflows\\neta-yume-lumina-expressions.api.json --base-image path\\to\\character.png --character-prompt "same anime character" --expressions neutral,smile
python .codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py --workflow .codex\\skills\\comfy-blender-vrm\\workflows\\neta-yume-lumina-expressions-transparent.api.json --base-image path\\to\\character.png --character-prompt "same anime character" --expressions neutral,smile
python .codex/skills/comfy-blender-vrm/scripts/build_vrm_base.py --blend-file path\\to\\base.blend
python .codex/skills/comfy-blender-vrm/scripts/build_vrm_base.py --blend-file path\\to\\base.blend --texture-image path\\to\\texture.png --output-name review-pass
python .codex/skills/comfy-blender-vrm/scripts/apply_motion_preview.py --blend-file path\\to\\base.blend --motion-file path\\to\\idle.bvh
python .codex/skills/comfy-blender-vrm/scripts/apply_motion_preview.py --blend-file path\\to\\base.blend --motion-file path\\to\\idle.bvh --output-name idle-preview
```

## Defaults
- Default config path: `config/comfy-blender-vrm.json`
- Relative paths inside the config are resolved from the repository root.
- Canonical implementation pack: `.codex/skills/kyarakuri-comfy-blender-vrm/`

## References
- Pipeline notes: `./references/pipeline.md`
- Character brief schema: `./references/character_brief.md`
- Workflow notes: `./workflows/README.md`
- Bundled base workflow: `./workflows/neta-yume-lumina-base.api.json`
- Bundled transparent base workflow: `./workflows/neta-yume-lumina-base-transparent.api.json`
- Bundled expression workflow: `./workflows/neta-yume-lumina-expressions.api.json`
- Bundled transparent expression workflow: `./workflows/neta-yume-lumina-expressions-transparent.api.json`
- Latest delta: `docs/delta/DR-20260314-release-skill-consolidation.md`
