# Workflow Notes

`generate-character-sheet` and `generate-expression-sheet` expect API-format ComfyUI workflow JSON.

## Supported placeholders
- `{{character_prompt}}`
- `{{seed}}`
- `{{run_id}}`
- `{{reference_image}}`
- `{{reference_image_name}}`
- `{{reference_image_subfolder}}`
- `{{reference_image_type}}`
- `{{expression_name}}`
- `{{base_image}}`
- `{{base_image_name}}`
- `{{base_image_subfolder}}`
- `{{base_image_type}}`

## Workflow format
- Supported: prompt JSON that can be sent directly to `POST /prompt`
- Not supported: UI export JSON with top-level `nodes` and `links`

## Bundled workflows
- `neta-yume-lumina-base.api.json`
  - Source: derived from PNG metadata of a locally successful generation on 2026-03-04
  - Purpose: base image generation for `generate-character-sheet` / `generate-character-from-brief`
  - Required checkpoint: `NetaYumev35_pretrained_all_in_one.safetensors`
  - Required placeholders: `{{character_prompt}}`, `{{seed}}`, `{{run_id}}`
- `neta-yume-lumina-base-transparent.api.json`
  - Source: derived from the bundled base workflow and extended on 2026-03-14 for transparent PNG output
  - Purpose: base image generation with best-effort transparent background for `generate-character-sheet` / `generate-character-from-brief`
  - Required checkpoint: `NetaYumev35_pretrained_all_in_one.safetensors`
  - Required placeholders: `{{character_prompt}}`, `{{seed}}`, `{{run_id}}`
  - Implementation note: local-only standard-node workflow using white-background keying via `ImageColorToMask` and `JoinImageWithAlpha`
- `neta-yume-lumina-expressions.api.json`
  - Source: derived from a locally successful real ComfyUI expression run on 2026-03-14
  - Purpose: image-to-image expression generation for `generate-expression-sheet`
  - Required checkpoint: `NetaYumev35_pretrained_all_in_one.safetensors`
  - Required base image: uploaded PNG resolved through `{{base_image_name}}`
  - Required placeholders: `{{character_prompt}}`, `{{expression_name}}`, `{{seed}}`, `{{run_id}}`, `{{base_image_name}}`
- `neta-yume-lumina-expressions-transparent.api.json`
  - Source: derived from the bundled expression workflow and extended on 2026-03-14 for transparent PNG output
  - Purpose: image-to-image expression generation with best-effort transparent background for `generate-expression-sheet`
  - Required checkpoint: `NetaYumev35_pretrained_all_in_one.safetensors`
  - Required base image: uploaded PNG resolved through `{{base_image_name}}`
  - Required placeholders: `{{character_prompt}}`, `{{expression_name}}`, `{{seed}}`, `{{run_id}}`, `{{base_image_name}}`
  - Implementation note: local-only standard-node workflow using white-background keying via `ImageColorToMask` and `JoinImageWithAlpha`

## Transparent workflow constraints
- The transparent workflows are local-only and do not use cloud API nodes such as Bria or Recraft.
- Transparency is best-effort white-background keying, not high-precision segmentation.
- For clean alpha edges, prompts should keep the background plain pure white and avoid props or floor shadows.

## Suggested flow
1. Export an API-format workflow from ComfyUI.
2. Replace prompt and seed literals with placeholders.
3. Use `{{reference_image}}` or `{{reference_image_name}}` in image input nodes when a reference upload is required.
4. Use `{{base_image}}` or `{{base_image_name}}` when expression generation needs a base character image.
5. Run `generate-character-sheet` with `--workflow` and `--character-prompt`, or `generate-expression-sheet` with `--workflow`, `--base-image`, and `--character-prompt`.
