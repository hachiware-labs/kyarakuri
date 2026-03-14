# kyarakuri

Repo-local character creation workflow built around local ComfyUI and Blender.

This repository currently uses `Forma Character` (`forma-character`) as the canonical repo-local skill pack for:

- environment checks
- base image generation from a character brief
- expression image generation from a base image
- Blender-based VRM workspace preparation
- Blender-based motion preview

## Status

- Phase: `P0`
- Canonical skill pack: [`./.codex/skills/forma-character/SKILL.md`](./.codex/skills/forma-character/SKILL.md)
- Default repo-local config: [`./config/forma-character.json`](./config/forma-character.json)
- Canonical project docs entry: [`./docs/OVERVIEW.md`](./docs/OVERVIEW.md)

## Available Commands

- `forma-character-prepare-environment`
- `forma-character-generate-base-image`
- `forma-character-generate-expressions`
- `forma-character-build-vrm`
- `forma-character-apply-motion-preview`

## Quick Start

1. Check the local environment.

```powershell
python .codex/skills/forma-character/scripts/prepare_environment.py
```

2. Generate a base image from a brief.

```powershell
python .codex/skills/forma-character/scripts/generate_base_image.py `
  --workflow .codex/skills/forma-character/workflows/neta-yume-lumina-base-transparent.api.json `
  --brief-file outputs/tmp/real-comfyui-brief.json
```

`forma-character-generate-base-image` always synthesizes a standing full-body base-image prompt with no background scene and no text overlays.

3. Generate expressions from the saved base image.

```powershell
python .codex/skills/forma-character/scripts/generate_expressions.py `
  --workflow .codex/skills/forma-character/workflows/neta-yume-lumina-expressions.api.json `
  --base-image outputs/<project-name>/images/base/<run-id>/images/<image>.png `
  --character-prompt "<same prompt>" `
  --expressions neutral,smile
```

## Bundled Workflows

The canonical skill pack includes repo-local bundled workflows:

- `neta-yume-lumina-base.api.json`
- `neta-yume-lumina-base-transparent.api.json`
- `neta-yume-lumina-expressions.api.json`
- `neta-yume-lumina-expressions-transparent.api.json`

See [`./.codex/skills/forma-character/workflows/README.md`](./.codex/skills/forma-character/workflows/README.md) for workflow assumptions and placeholders.

## Output Layout

Base image and expression outputs are grouped by project name under [`./outputs`](./outputs):

- `outputs/<project-name>/images/base/<run-id>/`
- `outputs/<project-name>/images/expressions/<run-id>/<expression>/`
- `outputs/<project-name>/logs/`

Blender and motion outputs currently remain command-specific:

- `outputs/blender/<run-id>/`
- `outputs/motion/<run-id>/`

## Documentation

- Project entry: [`./docs/OVERVIEW.md`](./docs/OVERVIEW.md)
- Concept: [`./docs/concept.md`](./docs/concept.md)
- Spec: [`./docs/spec.md`](./docs/spec.md)
- Architecture: [`./docs/architecture.md`](./docs/architecture.md)
- Plan: [`./docs/plan.md`](./docs/plan.md)

## Notes

- This repository assumes local ComfyUI and Blender are already installed.
- The current focus is repo-local validation before moving the skill pack into a distributable form.
- Real ComfyUI is used as a smoke verify target for major generation flows.
