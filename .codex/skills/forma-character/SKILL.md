# Forma Character

Repo-local canonical implementation skill pack for the public `forma-character-*` commands before moving them into a distributable skill.

## Current scope
- `forma-character-prepare-environment`: implemented
- `forma-character-generate-base-image`: implemented
- `forma-character-generate-expressions`: implemented
- `forma-character-build-vrm`: implemented
- `forma-character-apply-motion-preview`: implemented

## Command mapping
- `forma-character-prepare-environment` -> same-pack `doctor`
- `forma-character-generate-base-image` -> same-pack `generate_character_from_brief`
- `forma-character-generate-expressions` -> same-pack `generate_expression_sheet`
- `forma-character-build-vrm` -> same-pack `build_vrm_base`
- `forma-character-apply-motion-preview` -> same-pack `apply_motion_preview`

## Usage
```powershell
python .codex/skills/forma-character/scripts/prepare_environment.py
python .codex/skills/forma-character/scripts/prepare_environment.py --config config/forma-character.json
python .codex/skills/forma-character/scripts/generate_base_image.py --workflow path\\to\\character.api.json
python .codex/skills/forma-character/scripts/generate_base_image.py --workflow path\\to\\character.api.json --brief-file path\\to\\brief.json --seed 12345
python .codex/skills/forma-character/scripts/generate_base_image.py --workflow .codex\\skills\\forma-character\\workflows\\neta-yume-lumina-base-transparent.api.json
python .codex/skills/forma-character/scripts/generate_base_image.py --workflow .codex\\skills\\forma-character\\workflows\\neta-yume-lumina-base.api.json
python .codex/skills/forma-character/scripts/generate_expressions.py --workflow path\\to\\expressions.api.json --base-image path\\to\\character.png --character-prompt "same anime character"
python .codex/skills/forma-character/scripts/generate_expressions.py --workflow path\\to\\expressions.api.json --base-image path\\to\\character.png --character-prompt "same anime character" --expressions neutral,smile,angry --seed 12345
python .codex/skills/forma-character/scripts/generate_expressions.py --workflow .codex\\skills\\forma-character\\workflows\\neta-yume-lumina-expressions.api.json --base-image path\\to\\character.png --character-prompt "same anime character" --expressions neutral,smile
python .codex/skills/forma-character/scripts/generate_expressions.py --workflow .codex\\skills\\forma-character\\workflows\\neta-yume-lumina-expressions-transparent.api.json --base-image path\\to\\character.png --character-prompt "same anime character" --expressions neutral,smile
python .codex/skills/forma-character/scripts/build_vrm.py --blend-file path\\to\\base.blend
python .codex/skills/forma-character/scripts/build_vrm.py --blend-file path\\to\\base.blend --texture-image path\\to\\texture.png --output-name review-pass
python .codex/skills/forma-character/scripts/apply_motion_preview.py --blend-file path\\to\\base.blend --motion-file path\\to\\idle.bvh
python .codex/skills/forma-character/scripts/apply_motion_preview.py --blend-file path\\to\\base.blend --motion-file path\\to\\idle.bvh --output-name idle-preview
```

## Defaults
- Default config path: `config/forma-character.json`
- Relative paths inside the config are resolved from the repository root.
- Public entry scripts resolve to `.codex/skills/forma-character/scripts/`.
- `forma-character-generate-base-image` synthesizes a standing full-body base-image prompt with no background scene and no text overlays.
- Use `neta-yume-lumina-base-transparent.api.json` when you want a cutout-friendly base image PNG.

## References
- Pipeline notes: `./references/pipeline.md`
- Character brief schema: `./references/character_brief.md`
- Workflow notes: `./workflows/README.md`
- Bundled base workflow: `./workflows/neta-yume-lumina-base.api.json`
- Bundled transparent base workflow: `./workflows/neta-yume-lumina-base-transparent.api.json`
- Bundled expression workflow: `./workflows/neta-yume-lumina-expressions.api.json`
- Bundled transparent expression workflow: `./workflows/neta-yume-lumina-expressions-transparent.api.json`
- Latest delta: `docs/delta/DR-20260314-base-image-standing-defaults.md`
