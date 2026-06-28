---
name: forma-background
description: Create Forma background images with imagegen and fixed-composition time, weather, and lighting variants. Use when Codex needs to generate a background scene, ask for a background brief, make a base background, or create morning/noon/evening/night/rain/snow/fog/storm variations while preserving the exact camera position, perspective, layout, object positions, and scene identity.
---

# Forma Background

## Workflow

Use this skill for environment/background assets, especially when the user wants the same place at different times or in different weather.

1. Collect or infer a background brief.
2. Create the base background with `imagegen`, not local ComfyUI.
3. Save the approved base background before making variants.
4. Create time/weather variants as image edits from the approved base image, not from text-only regeneration.
5. Preserve the exact camera position, perspective, horizon, layout, object positions, scale, and cropping across variants.
6. Change only time, weather, precipitation, ground wetness/snow cover, light color, shadow intensity, sky/window color, and ambient mood.
7. Save outputs under `outputs/<project-name>/backgrounds/`.

Do not add characters, captions, UI labels, logos, watermarks, speech bubbles, or explanatory text unless the user explicitly asks.

## Background Brief

Ask for the missing fields only when they matter:

- `project_name`: folder name under `outputs/`.
- `location_name`: scene name, such as `tokokan-entrance` or `creator-dorm-common-room`.
- `scene_concept`: what the place is and what it is used for.
- `camera`: angle and framing, such as `fixed wide interior shot from doorway`.
- `style`: illustration style, level of realism, color mood.
- `important_layout`: objects that must stay fixed.
- `time_variants`: list such as `morning`, `noon`, `golden-hour`, `night`.
- `weather_variants`: list such as `clear`, `rain`, `heavy-rain`, `snow`, `fog`, `storm`, `rainy-night`.
- `negative_constraints`: things to avoid.

Save the brief as:

```text
outputs/<project-name>/backgrounds/<location-name>/brief.json
```

## Base Background

Use `imagegen` as the base-background generator. Do not use ComfyUI for background base generation because local checkpoints drift too much from the requested art direction and composition quality.

Generate or request one or more base candidates before variants. The base prompt should describe stable geometry and art direction:

```text
background environment only, no characters,
fixed establishing shot, stable camera angle,
<scene_concept>,
<important_layout>,
<style and art direction>,
strong foreground / midground / background depth,
intentional lighting and color design,
no text, no caption, no logo, no watermark, no readable signage
```

Save:

```text
outputs/<project-name>/backgrounds/<location-name>/base.png
outputs/<project-name>/backgrounds/<location-name>/base.prompt.json
```

Base prompt example:

```text
Create a polished anime / visual-novel background plate.
Scene: baseball stadium viewed from directly behind home plate through the backstop net.
Composition: foreground backstop net frames the image, home plate and batter box lines in the foreground, centered pitcher mound, symmetrical infield diamond, foul lines leading into the distance, layered empty stadium seats, outfield fence.
Camera: fixed wide establishing shot, eye-level from behind home plate.
Lighting: clear daylight with appealing background-art color design.
Constraints: background only, no people, no players, no text, no captions, no logos, no watermarks.
```

When multiple base candidates are useful, keep the same brief and compare candidates. Do not start variants until a base is selected.

## Fixed-Composition Variants

Use `imagegen` image editing with the approved `base.png` as the input image. Do not create variants from text only.

The edit instruction must explicitly preserve structure:

```text
Edit the provided background image.
Preserve the exact camera position, perspective, composition, cropping, horizon, object positions, object scale, architectural layout, and scene identity.
Do not move, add, remove, or redesign major objects.
Change only <time/weather/light/surface condition>.
Keep it as a background plate with no characters, no captions, no readable text, no logos, and no watermarks.
```

Variant prompt pattern:

```text
Use the provided base background image as the source.
Keep the same place, same camera position, same perspective, same composition, same layout, same horizon, same objects in the same positions, same scale, and same crop.
Variant: <variant-name>.
Change only:
time of day: <morning | noon | evening | night | custom>
lighting: <time-specific light>
weather: <clear | rain | snow | fog | storm | custom weather>
surface condition: <dry | wet reflective surfaces | thin snow cover | accumulated snow>
Do not add characters, people, captions, readable signs, logos, or watermarks.
```

Allowed changes:

- Time of day and light direction/color.
- Weather, rain/snow/fog/storm effects.
- Wetness, puddles, snow cover on horizontal surfaces.
- Ambient mood and contrast.
- Sky/window color and shadow strength.

Forbidden changes:

- Camera angle, lens feel, zoom, crop, aspect ratio, horizon, or perspective changes.
- Moved, added, removed, resized, or redesigned buildings, furniture, trees, field lines, paths, windows, doors, props, or other major objects.
- Characters, people, vehicles, creatures, captions, readable signs, logos, watermarks, or UI.
- Weather effects that hide the scene identity or make the layout unreadable.

Save variants as:

```text
outputs/<project-name>/backgrounds/<location-name>/variants/<variant-name>.png
outputs/<project-name>/backgrounds/<location-name>/variants/<variant-name>.prompt.json
outputs/<project-name>/backgrounds/<location-name>/logs/<run-id>.json
```

## Variant Presets

Use these as prompt tokens when the user asks generally for time or weather changes:

- `dawn`: pale blue ambient light, soft low contrast, faint warm horizon.
- `morning`: clean sunlight, cool shadows, fresh atmosphere.
- `noon`: bright neutral daylight, short shadows, high clarity.
- `golden-hour`: warm orange sunlight, long shadows, glowing highlights.
- `dusk`: dim violet-blue ambient light, warm interior/window lights.
- `night`: dark blue ambience, artificial lamps, visible light pools.
- `rain`: overcast sky, visible rainfall, wet reflective ground, softened contrast.
- `heavy-rain`: dense rain streaks, stronger reflections, darker sky, reduced distant clarity.
- `after-rain`: no active rainfall, wet surfaces, puddles, clear reflections, fresh air.
- `snow`: falling snow, cool muted light, thin snow on horizontal surfaces, layout still readable.
- `heavy-snow`: denser snowfall and accumulated snow, but major shapes and paths remain visible.
- `fog`: low contrast, misty air, softened distant objects, foreground layout still clear.
- `storm`: dark clouds, dramatic light, wind-swept rain, high contrast, no layout changes.
- `rainy-night`: wet reflective surfaces, muted colors, lamp reflections.
- `snowy-night`: blue-black ambient light, warm window or street lights, snow catching highlights.

## Quality Check

Before finishing, compare base and variants:

- Camera position and horizon match.
- Major objects stay in the same positions.
- Cropping and scale match.
- No characters or explanatory text were added.
- Time/light/weather changed enough to be useful.
- Weather effects do not hide the scene identity or move/add structural objects.
- Output paths and any known drift are reported.
