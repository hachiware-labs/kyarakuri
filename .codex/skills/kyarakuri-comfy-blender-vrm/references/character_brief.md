# Character Brief

`kyarakuri-generate-base-image` accepts a minimal brief from interactive CLI prompts or a JSON file.

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
- `expression`: string
- `background`: string
- `negative_constraints`: array of strings
- `extra_notes`: string

## JSON example
```json
{
  "character_name": "Airi",
  "core_concept": "young mechanic idol with a retro sci-fi vibe",
  "style_keywords": ["anime", "bright palette", "clean lineart"],
  "visual_traits": ["orange bob cut", "amber eyes", "small headset"],
  "outfit": "utility jacket over a stage costume",
  "pose": "front-facing relaxed standing pose",
  "expression": "gentle smile",
  "background": "simple light studio background",
  "negative_constraints": ["extra arms", "cropped feet", "heavy shadows"],
  "extra_notes": "design should read clearly as a base image for later VRM work"
}
```

## Saved artifacts
- `outputs/<project-name>/brief.json`
- `outputs/<project-name>/images/base/<run-id>/brief.json`
- `prompt-preview.txt`
