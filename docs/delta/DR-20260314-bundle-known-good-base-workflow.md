# delta-request

## Delta ID
- DR-20260314-bundle-known-good-base-workflow

## Delta Type
- FEATURE

## 目的
- 過去に実生成成功した PNG に埋め込まれていた API-format workflow を、repo 内の bundled workflow asset として取り込む。
- `generate-character-from-brief` / `kyarakuri-generate-base-image` から参照しやすい fixed workflow を用意し、実 ComfyUI smoke verify の土台を揃える。

## 変更対象（In Scope）
- 成功 PNG の metadata 由来の API-format workflow JSON を internal skill の workflow dir に追加する。
- 同じ workflow JSON を repo-local wrapper skill の workflow dir に追加する。
- workflow README / SKILL docs に bundled workflow 名、前提 checkpoint、用途を追記する。
- `docs/OVERVIEW.md` と `docs/plan.md` に active delta と follow-up seed を反映する。
- delta 記録を `docs/delta/DR-20260314-bundle-known-good-base-workflow.md` に残す。

## 非対象（Out of Scope）
- ComfyUI backend crash の修正。
- 実 ComfyUI の smoke verify 完了。
- `generate-expression-sheet` 用 workflow の追加。
- config や command I/F の変更。

## Candidate Files/Artifacts
- docs/delta/DR-20260314-bundle-known-good-base-workflow.md
- docs/concept.md
- docs/spec.md
- docs/architecture.md
- docs/OVERVIEW.md
- docs/plan.md
- .codex/skills/comfy-blender-vrm/SKILL.md
- .codex/skills/comfy-blender-vrm/workflows/README.md
- .codex/skills/comfy-blender-vrm/workflows/neta-yume-lumina-base.api.json
- .codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md
- .codex/skills/kyarakuri-comfy-blender-vrm/workflows/README.md
- .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-base.api.json

## 差分仕様
- DS-01:
  - Given: repo 内 skill から base image workflow を選びたい。
  - When: workflow dir と skill docs を参照する。
  - Then: `NetaYumev35_pretrained_all_in_one.safetensors` 前提の bundled API-format workflow を見つけられる。
- DS-02:
  - Given: bundled workflow を `generate-character-from-brief` または `kyarakuri-generate-base-image` に渡したい。
  - When: workflow JSON を読み、placeholder を解決する。
  - Then: `character_prompt`、`seed`、`run_id` が解決でき、未解決 placeholder は残らない。
- DS-03:
  - Given: 実 ComfyUI smoke verify の次 seed を明確にしたい。
  - When: 正本 docs を確認する。
  - Then: bundled workflow を使った smoke verify が follow-up として読める。

## 受入条件（Acceptance Criteria）
- AC-01: `.codex/skills/comfy-blender-vrm/workflows/neta-yume-lumina-base.api.json` が追加され、API-format prompt JSON として読み込める。
- AC-02: `.codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-base.api.json` が追加され、repo-local skill docs から参照できる。
- AC-03: internal / repo-local の workflow README と SKILL docs に bundled workflow 名、checkpoint 名、用途が記載される。
- AC-04: bundled workflow に対して `character_prompt`、`seed`、`run_id` を解決したとき、未解決 placeholder が残らない。
- AC-05: `delta-project-validator` の `links-only` が PASS する。

## Verify Profile
- static check: Required
- targeted unit: Not Required
- targeted integration / E2E: Not Required
- delta-project-validator: links-only

## Canonical Sync Mode
- mode: post-archive sync
- reason: workflow asset 追加と docs 同期を同一 delta で閉じ、verify PASS 後に正本へ最小差分で反映する。

## 制約
- workflow JSON は PNG metadata に含まれていた API-format prompt をベースにし、UI export JSON は追加しない。
- placeholder は既存 skill がサポートする `{{character_prompt}}`、`{{seed}}`、`{{run_id}}` に限定する。
- 実行時クラッシュの有無はこの delta の受入条件に含めない。

## Review Gate
- required: No
- reason: workflow asset と docs 導線の追加に閉じた差分であり、既存 code path や I/F を変更しない。

## 未確定事項
- Q-01: 実 ComfyUI smoke verify は follow-up delta `DR-20260313-real-comfyui-smoke-verify` で扱う。

## Step 2: delta-apply
- changed files:
  - .codex/skills/comfy-blender-vrm/SKILL.md
  - .codex/skills/comfy-blender-vrm/workflows/README.md
  - .codex/skills/comfy-blender-vrm/workflows/neta-yume-lumina-base.api.json
  - .codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md
  - .codex/skills/kyarakuri-comfy-blender-vrm/workflows/README.md
  - .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-base.api.json
  - docs/concept.md
  - docs/spec.md
  - docs/architecture.md
  - docs/OVERVIEW.md
  - docs/plan.md
  - docs/delta/DR-20260314-bundle-known-good-base-workflow.md
- applied AC:
  - AC-01:
    - 変更: internal skill の workflow dir に `neta-yume-lumina-base.api.json` を追加した。
    - 根拠: PNG metadata の API-format prompt をベースにし、`{{character_prompt}}`、`{{seed}}`、`{{run_id}}` を差し込める。
  - AC-02:
    - 変更: repo-local skill の workflow dir に同名 workflow を追加した。
    - 根拠: `config/kyarakuri-comfy-blender-vrm.json` が指す workflow dir から直接参照できる。
  - AC-03:
    - 変更: internal / repo-local の README と `SKILL.md` に bundled workflow の用途、checkpoint、参照例を追記した。
    - 根拠: `generate-character-from-brief` / `kyarakuri-generate-base-image` の実行例から bundled workflow を辿れる。
  - AC-04:
    - 変更: workflow JSON を既存 placeholder 契約だけで構成した。
    - 根拠: positive prompt、seed、filename prefix 以外に未対応 placeholder を追加していない。
  - AC-05:
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
  - targeted integration / E2E: Not Required
  - delta validator: links-only
- executed verify:
  - static check:
    - `load_workflow_payload()` で internal / repo-local の bundled workflow を読込
    - `render_template()` に `character_prompt`、`seed`、`run_id` を渡して placeholder 展開
    - `collect_unresolved_tokens()` で未解決 placeholder がないことを確認
    - internal / repo-local の workflow copy が一致することを確認
  - delta validator: `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- review delta outcome:
  - pass: Yes
  - follow-up delta seeds:
    - `DR-20260313-real-comfyui-smoke-verify`
- AC result table:
  - AC-01: PASS
    - 根拠: `load_workflow_payload()` で `.codex/skills/comfy-blender-vrm/workflows/neta-yume-lumina-base.api.json` を正常に読めた。
  - AC-02: PASS
    - 根拠: repo-local copy も正常に読め、internal copy と一致した。
  - AC-03: PASS
    - 根拠: internal / repo-local の `README.md` と `SKILL.md` に bundled workflow 名、checkpoint、用途、実行例を追加した。
  - AC-04: PASS
    - 根拠: `render_template()` 後の `collect_unresolved_tokens()` が空配列で、`seed`、`filename_prefix`、prompt 差し込みも確認できた。
  - AC-05: PASS
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
  - static check では `seed=123456789`、`run_id=verify-run-id`、`character_prompt=front-facing anime mechanic, clean silhouette` を展開した。
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
  - 目的: 成功 PNG metadata 由来の bundled base-image workflow を repo に追加する
  - 変更対象: internal / repo-local workflow asset、workflow docs、skill docs、current status docs
  - 非対象: backend crash 修正、実 ComfyUI smoke verify、expression workflow、config / command I/F 変更
- unresolved items:
  - Q-01: 実 ComfyUI smoke verify は follow-up delta `DR-20260313-real-comfyui-smoke-verify` で扱う
- follow-up delta seeds:
  - `DR-20260313-real-comfyui-smoke-verify`
