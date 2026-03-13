# Workflow Notes

`kyarakuri-generate-base-image` and `kyarakuri-generate-expressions` expect API-format ComfyUI workflow JSON.

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
