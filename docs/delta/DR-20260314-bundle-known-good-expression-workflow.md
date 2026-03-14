# delta-request

## Delta ID
- DR-20260314-bundle-known-good-expression-workflow

## Delta Type
- FEATURE

## 目的
- 実 ComfyUI で成功した image-to-image ベースの expression workflow を、repo 内の bundled workflow asset として取り込む。
- `generate-expression-sheet` / `kyarakuri-generate-expressions` から参照しやすい fixed workflow を用意し、expression 系 smoke verify の土台を揃える。

## 変更対象（In Scope）
- 実 ComfyUI で成功した API-format expression workflow JSON を internal skill の workflow dir に追加する。
- 同じ workflow JSON を repo-local wrapper skill の workflow dir に追加する。
- workflow README / SKILL docs に bundled workflow 名、前提 checkpoint、base image 前提、用途を追記する。
- `docs/OVERVIEW.md` と `docs/plan.md` に active delta と follow-up seed を反映する。
- delta 記録を `docs/delta/DR-20260314-bundle-known-good-expression-workflow.md` に残す。

## 非対象（Out of Scope）
- ComfyUI backend crash の根本修正。
- expression workflow の品質改善ループ。
- base-image workflow の変更。
- config や command I/F の変更。

## Candidate Files/Artifacts
- docs/delta/DR-20260314-bundle-known-good-expression-workflow.md
- docs/OVERVIEW.md
- docs/plan.md
- docs/concept.md
- docs/spec.md
- docs/architecture.md
- .codex/skills/comfy-blender-vrm/SKILL.md
- .codex/skills/comfy-blender-vrm/workflows/README.md
- .codex/skills/comfy-blender-vrm/workflows/neta-yume-lumina-expressions.api.json
- .codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md
- .codex/skills/kyarakuri-comfy-blender-vrm/workflows/README.md
- .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-expressions.api.json

## 差分仕様
- DS-01:
  - Given: repo 内 skill から expression workflow を選びたい。
  - When: workflow dir と skill docs を参照する。
  - Then: `NetaYumev35_pretrained_all_in_one.safetensors` と uploaded base image を前提にした bundled API-format workflow を見つけられる。
- DS-02:
  - Given: bundled workflow を `generate-expression-sheet` または `kyarakuri-generate-expressions` に渡したい。
  - When: workflow JSON を読み、placeholder を解決する。
  - Then: `character_prompt`、`expression_name`、`seed`、`run_id`、`base_image_name` が解決でき、未解決 placeholder は残らない。
- DS-03:
  - Given: 実 ComfyUI で expression 経路を確認したい。
  - When: bundled workflow を使って 2 表情を生成する。
  - Then: expression ごとの画像、submitted workflow、history、metadata が `output_dir` 配下へ保存される。

## 受入条件（Acceptance Criteria）
- AC-01: `.codex/skills/comfy-blender-vrm/workflows/neta-yume-lumina-expressions.api.json` が追加され、API-format prompt JSON として読み込める。
- AC-02: `.codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-expressions.api.json` が追加され、repo-local skill docs から参照できる。
- AC-03: internal / repo-local の workflow README と SKILL docs に bundled workflow 名、checkpoint 名、base image 前提、用途が記載される。
- AC-04: bundled workflow に対して `character_prompt`、`expression_name`、`seed`、`run_id`、`base_image_name` を解決したとき、未解決 placeholder が残らない。
- AC-05: 実 ComfyUI で `kyarakuri-generate-expressions` を bundled workflow と 2 表情で実行し、expression ごとの成果物と metadata を保存できる。
- AC-06: `delta-project-validator` の `links-only` が PASS する。

## Verify Profile
- static check: Required
- targeted unit: Not Required
- targeted integration / E2E: Required
- delta-project-validator: links-only

## Canonical Sync Mode
- mode: post-archive sync
- reason: workflow asset 追加と docs 同期を同一 delta で閉じ、verify PASS 後に正本へ最小差分で反映する。

## 制約
- workflow JSON は API-format prompt とし、UI export JSON は追加しない。
- placeholder は既存 skill がサポートする `{{character_prompt}}`、`{{expression_name}}`、`{{seed}}`、`{{run_id}}`、`{{base_image_name}}` に限定する。
- 実 ComfyUI verify は 2 表情の最小ケースに留める。

## Review Gate
- required: No
- reason: workflow asset と docs 導線の追加に閉じた差分であり、既存 code path や I/F を変更しない。

## 未確定事項
- Q-01: 実 ComfyUI smoke verify の formalization は follow-up delta `DR-20260313-real-comfyui-smoke-verify` で扱う。

## Step 2: delta-apply
- changed files:
  - .codex/skills/comfy-blender-vrm/SKILL.md
  - .codex/skills/comfy-blender-vrm/workflows/README.md
  - .codex/skills/comfy-blender-vrm/workflows/neta-yume-lumina-expressions.api.json
  - .codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md
  - .codex/skills/kyarakuri-comfy-blender-vrm/workflows/README.md
  - .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-expressions.api.json
  - docs/concept.md
  - docs/spec.md
  - docs/architecture.md
  - docs/OVERVIEW.md
  - docs/plan.md
  - docs/delta/DR-20260314-bundle-known-good-expression-workflow.md
- applied AC:
  - AC-01:
    - 変更: internal skill の workflow dir に `neta-yume-lumina-expressions.api.json` を追加した。
    - 根拠: 実 ComfyUI で成功した image-to-image expression prompt を bundled asset として固定した。
  - AC-02:
    - 変更: repo-local skill の workflow dir に同名 workflow を追加した。
    - 根拠: `config/kyarakuri-comfy-blender-vrm.json` が指す workflow dir から直接参照できる。
  - AC-03:
    - 変更: internal / repo-local の README と `SKILL.md` に bundled workflow の用途、checkpoint、base image 前提、実行例を追記した。
    - 根拠: `generate-expression-sheet` / `kyarakuri-generate-expressions` の実行例から bundled workflow を辿れる。
  - AC-04:
    - 変更: workflow JSON を既存 placeholder 契約だけで構成した。
    - 根拠: `character_prompt`、`expression_name`、`seed`、`run_id`、`base_image_name` 以外の未対応 placeholder を追加していない。
  - AC-05:
    - 変更: 実 ComfyUI で使った bundled workflow と同名 asset を repo に保存した。
    - 根拠: repo-local workflow path を直接 `generate_expressions.py` に渡せる状態にした。
  - AC-06:
    - 変更: delta validator で参照整合を取れる形に docs と delta record を更新した。
    - 根拠: `docs/OVERVIEW.md` と `docs/plan.md` に active delta / archive 反映の導線を加えた。
- non-goal kept:
  - Out of Scope への変更なし: Yes
- canonical sync:
  - mode: post-archive sync
  - action: 正本 docs の追加同期は verify PASS 後に実施
  - status: NOT STARTED
- code split check:
  - file over 500 lines: No
  - file over 800 lines: No
  - file over 1000 lines: No
  - long function issue: N/A
  - module responsibility issue: N/A
- status: APPLIED

## Step 3: delta-verify
- verify profile:
  - static check: Required
  - targeted unit: Not Required
  - targeted integration / E2E: Required
  - delta validator: links-only
- executed verify:
  - static check:
    - `load_workflow_payload()` で internal / repo-local の bundled workflow を読込
    - `render_template()` に `character_prompt`、`expression_name`、`seed`、`run_id`、`base_image_name` を渡して placeholder 展開
    - `collect_unresolved_tokens()` で未解決 placeholder がないことを確認
    - internal / repo-local の workflow copy が一致することを確認
  - targeted integration / E2E:
    - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expressions.py --workflow .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-expressions.api.json --base-image outputs/character/20260314-001459-character-from-brief/images/001_9_20260314-001459-character-from-brief_00001_.png --character-prompt "<saved prompt>" --expressions neutral,smile --timeout-seconds 600`
    - metadata: `outputs/logs/20260314-002359-expression-sheet.json`
    - output dir: `outputs/expressions/20260314-002359-expression-sheet/`
    - post-run health check: `http://127.0.0.1:8000/system_stats` returned `200`
  - delta validator: `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- review delta outcome:
  - pass: Yes
  - follow-up delta seeds:
    - `DR-20260313-real-comfyui-smoke-verify`
- AC result table:
  - AC-01: PASS
    - 根拠: `load_workflow_payload()` で `.codex/skills/comfy-blender-vrm/workflows/neta-yume-lumina-expressions.api.json` を正常に読めた。
  - AC-02: PASS
    - 根拠: repo-local copy も正常に読め、internal copy と一致した。
  - AC-03: PASS
    - 根拠: internal / repo-local の `README.md` と `SKILL.md` に bundled workflow 名、checkpoint、base image 前提、用途、実行例を追加した。
  - AC-04: PASS
    - 根拠: `render_template()` 後の `collect_unresolved_tokens()` が空配列で、`base_image_name`、`seed`、`expression_name`、`filename_prefix` 差し込みも確認できた。
  - AC-05: PASS
    - 根拠: bundled workflow を使った `kyarakuri-generate-expressions` が `neutral` と `smile` の 2 表情を保存し、metadata `outputs/logs/20260314-002359-expression-sheet.json` を出力した。
  - AC-06: PASS
    - 根拠: `validate_delta_links.js` が `OK` で終了した。
- scope deviation:
  - Out of Scope 変更あり: No
- review findings:
  - layer integrity: PASS
  - docs sync: PASS
  - data size: PASS
  - code split health: PASS
  - file-size threshold: PASS
- canonical sync:
  - mode: post-archive sync
  - status: DONE
  - result: PASS
- references:
  - static check では `expression_name=smile`、`seed=987654321`、`run_id=verify-expression-run`、`base_image_name=base.png` を展開した。
  - real ComfyUI verify では `outputs/expressions/20260314-002359-expression-sheet/neutral/` と `.../smile/` に画像、submitted workflow、history を保存した。
  - `validate_delta_links.js` returned `OK: errors=0, warnings=0`.
- overall: PASS

## Step 4: delta-archive
- verify result: PASS
- review gate: NOT REQUIRED
- archive status: archived
- canonical sync:
  - mode: post-archive sync
  - status: DONE
  - synced docs:
    - concept: `docs/concept.md`
    - spec: `docs/spec.md`
    - architecture: `docs/architecture.md`
    - overview: `docs/OVERVIEW.md`
    - plan: `docs/plan.md`
- closed scope:
  - 目的: 成功した expression workflow を bundled asset として repo に追加する
  - 変更対象: internal / repo-local workflow asset、workflow docs、skill docs、current status docs
  - 非対象: backend crash 修正、品質改善ループ、base-image workflow 変更、config / command I/F 変更
- unresolved items:
  - Q-01: 実 ComfyUI smoke verify の formalization は follow-up delta `DR-20260313-real-comfyui-smoke-verify` で扱う
- follow-up delta seeds:
  - `DR-20260313-real-comfyui-smoke-verify`
