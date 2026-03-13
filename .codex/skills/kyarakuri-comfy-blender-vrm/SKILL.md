# kyarakuri-comfy-blender-vrm

Repo-local skill pack for testing the public `kyarakuri-*` command names before moving them into a distributable skill.

## Current scope
- `kyarakuri-prepare-environment`: implemented via wrapper
- `kyarakuri-generate-base-image`: implemented via wrapper
- `kyarakuri-generate-expressions`: implemented via wrapper
- `kyarakuri-build-vrm`: planned
- `kyarakuri-apply-motion-preview`: planned

## Command mapping
- `kyarakuri-prepare-environment` -> existing `doctor`
- `kyarakuri-generate-base-image` -> existing `generate-character-from-brief`
- `kyarakuri-generate-expressions` -> existing `generate-expression-sheet`

## Usage
```powershell
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/prepare_environment.py
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/prepare_environment.py --config config/kyarakuri-comfy-blender-vrm.json
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py --workflow path\\to\\character.api.json
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py --workflow path\\to\\character.api.json --brief-file path\\to\\brief.json --seed 12345
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expressions.py --workflow path\\to\\expressions.api.json --base-image path\\to\\character.png --character-prompt "same anime character"
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expressions.py --workflow path\\to\\expressions.api.json --base-image path\\to\\character.png --character-prompt "same anime character" --expressions neutral,smile,angry --seed 12345
```

## Defaults
- Default config path: `config/kyarakuri-comfy-blender-vrm.json`
- Relative paths inside the config are resolved from the repository root.
- The wrapper scripts delegate to `.codex/skills/comfy-blender-vrm/scripts/`.

## References
- Pipeline notes: `./references/pipeline.md`
- Character brief schema: `./references/character_brief.md`
- Workflow notes: `./workflows/README.md`
- Latest delta: `docs/delta/DR-20260313-repo-local-kyarakuri-skill-pack.md`
