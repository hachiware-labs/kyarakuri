# Character Brief

`generate-character-from-brief` accepts a minimal brief from interactive CLI prompts or a JSON file.

## Required field
- `core_concept`: short sentence describing the character idea

## Optional fields
- `style_keywords`: array of strings, for example `["anime", "cel shaded", "clean lineart"]`
- `visual_traits`: array of strings, for example `["silver hair", "teal eyes", "short twin tails"]`
- `outfit`: string
- `pose`: string
- `expression`: string
- `background`: string
- `negative_constraints`: array of strings, used as an `Avoid:` suffix in the synthesized prompt
- `extra_notes`: string

## JSON example
```json
{
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

## Prompt synthesis rules
- `core_concept` is always required.
- The command adds a base framing suffix for a clean full-body character sheet image.
- Optional fields are appended only when present.
- `negative_constraints` become an `Avoid:` clause at the end of the prompt.

## Saved artifacts
- `brief.json`
- `prompt-preview.txt`
