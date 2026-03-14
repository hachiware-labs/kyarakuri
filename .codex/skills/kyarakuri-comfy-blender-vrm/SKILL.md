# kyarakuri-comfy-blender-vrm

Repo-local canonical implementation skill pack for the public `kyarakuri-*` commands before moving them into a distributable skill.

## Current scope
- `kyarakuri-prepare-environment`: implemented via wrapper
- `kyarakuri-generate-base-image`: implemented via wrapper
- `kyarakuri-generate-expressions`: implemented via wrapper
- `kyarakuri-build-vrm`: implemented via wrapper
- `kyarakuri-apply-motion-preview`: implemented

## Command mapping
- `kyarakuri-prepare-environment` -> same-pack `doctor`
- `kyarakuri-generate-base-image` -> same-pack `generate_character_from_brief`
- `kyarakuri-generate-expressions` -> same-pack `generate_expression_sheet`
- `kyarakuri-build-vrm` -> same-pack `build_vrm_base`
- `kyarakuri-apply-motion-preview` -> same-pack `apply_motion_preview`

## Usage
```powershell
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/prepare_environment.py
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/prepare_environment.py --config config/kyarakuri-comfy-blender-vrm.json
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py --workflow path\\to\\character.api.json
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py --workflow path\\to\\character.api.json --brief-file path\\to\\brief.json --seed 12345
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py --workflow .codex\\skills\\kyarakuri-comfy-blender-vrm\\workflows\\neta-yume-lumina-base.api.json
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py --workflow .codex\\skills\\kyarakuri-comfy-blender-vrm\\workflows\\neta-yume-lumina-base-transparent.api.json
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expressions.py --workflow path\\to\\expressions.api.json --base-image path\\to\\character.png --character-prompt "same anime character"
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expressions.py --workflow path\\to\\expressions.api.json --base-image path\\to\\character.png --character-prompt "same anime character" --expressions neutral,smile,angry --seed 12345
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expressions.py --workflow .codex\\skills\\kyarakuri-comfy-blender-vrm\\workflows\\neta-yume-lumina-expressions.api.json --base-image path\\to\\character.png --character-prompt "same anime character" --expressions neutral,smile
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expressions.py --workflow .codex\\skills\\kyarakuri-comfy-blender-vrm\\workflows\\neta-yume-lumina-expressions-transparent.api.json --base-image path\\to\\character.png --character-prompt "same anime character" --expressions neutral,smile
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/build_vrm.py --blend-file path\\to\\base.blend
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/build_vrm.py --blend-file path\\to\\base.blend --texture-image path\\to\\texture.png --output-name review-pass
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/apply_motion_preview.py --blend-file path\\to\\base.blend --motion-file path\\to\\idle.bvh
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/apply_motion_preview.py --blend-file path\\to\\base.blend --motion-file path\\to\\idle.bvh --output-name idle-preview
```

## Defaults
- Default config path: `config/kyarakuri-comfy-blender-vrm.json`
- Relative paths inside the config are resolved from the repository root.
- Public entry scripts resolve to `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/`.
- Legacy `comfy-blender-vrm` commands are compatibility wrappers around this pack.

## References
- Pipeline notes: `./references/pipeline.md`
- Character brief schema: `./references/character_brief.md`
- Workflow notes: `./workflows/README.md`
- Bundled base workflow: `./workflows/neta-yume-lumina-base.api.json`
- Bundled transparent base workflow: `./workflows/neta-yume-lumina-base-transparent.api.json`
- Bundled expression workflow: `./workflows/neta-yume-lumina-expressions.api.json`
- Bundled transparent expression workflow: `./workflows/neta-yume-lumina-expressions-transparent.api.json`
- Latest delta: `docs/delta/DR-20260314-release-skill-consolidation.md`
