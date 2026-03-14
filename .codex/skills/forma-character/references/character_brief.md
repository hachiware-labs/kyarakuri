# Character Brief

`forma-character-generate-base-image` accepts a minimal brief from interactive CLI prompts or a JSON file.

## Required field
- `core_concept`: short sentence describing the character idea

## Additional field
- `character_name`: short project-facing character name
- interactive input では最初に必須で聞く
- brief JSON では optional で、ある場合は project 名導出に優先して使う

## Optional fields
- `style_keywords`: array of strings
- `visual_traits`: array of strings
- `outfit`: string
- `pose`: string
- standing pose の detail 用
- `expression`: string
- `background`: string
- backward compatibility 用に受け付けるが、`forma-character-generate-base-image` の prompt 合成では使わない
- `negative_constraints`: array of strings
- `extra_notes`: string

## Base image defaults
- `forma-character-generate-base-image` は standing full-body の base image prompt を常に合成する
- base image prompt は backgroundless / plain white cutout-ready / no text overlay を既定に含む
- `background` field は保存されるが、base image prompt には反映しない

## JSON example
```json
{
  "character_name": "Airi",
  "core_concept": "young mechanic idol with a retro sci-fi vibe",
  "style_keywords": ["anime", "bright palette", "clean lineart"],
  "visual_traits": ["orange bob cut", "amber eyes", "small headset"],
  "outfit": "utility jacket over a stage costume",
  "pose": "relaxed standing pose with both hands lightly in front",
  "expression": "gentle smile",
  "negative_constraints": ["extra arms", "cropped feet", "heavy shadows"],
  "extra_notes": "design should read clearly as a base image for later VRM work"
}
```

## Saved artifacts
- `outputs/<project-name>/brief.json`
- `outputs/<project-name>/images/base/<run-id>/brief.json`
- `prompt-preview.txt`
