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

## Suggested flow
1. Export an API-format workflow from ComfyUI.
2. Replace prompt and seed literals with placeholders.
3. Use `{{reference_image}}` or `{{reference_image_name}}` in image input nodes when a reference upload is required.
4. Use `{{base_image}}` or `{{base_image_name}}` when expression generation needs a base character image.
5. Run `generate-character-sheet` with `--workflow` and `--character-prompt`, or `generate-expression-sheet` with `--workflow`, `--base-image`, and `--character-prompt`.
