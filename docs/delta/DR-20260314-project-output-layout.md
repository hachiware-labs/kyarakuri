# delta-request

## Delta ID
- DR-20260314-project-output-layout

## Delta Type
- FEATURE

## 目的
- `outputs/` 配下を project 単位の構成へ寄せ、base image と expression image を同じ project folder の下に集約する。
- project 名は最初の base image 生成時に自動決定し、expression 側は base image path から同じ project folder を引き継ぐ。

## 変更対象（In Scope）
- `generate-character-sheet` / `generate-character-from-brief` の保存先を `output_dir/<project-name>/images/base/<run-id>/...` へ変更する。
- `generate-expression-sheet` の保存先を `output_dir/<project-name>/images/expressions/<run-id>/<expression>/...` へ変更する。
- metadata の保存先を `output_dir/<project-name>/logs/` に寄せる。
- project 名の自動決定 / 引継ぎロジックを追加する。
- canonical docs と skill references に新しい出力構成を同期する。
- delta 記録を `docs/delta/DR-20260314-project-output-layout.md` に残す。

## 非対象（Out of Scope）
- `build-vrm-base` と `apply-motion-preview` の保存先変更。
- 既存の `outputs/character` / `outputs/expressions` / `outputs/logs` の移行処理。
- project 名を CLI 引数で手動指定する I/F 追加。
- ComfyUI workflow や生成品質の変更。

## Candidate Files/Artifacts
- docs/delta/DR-20260314-project-output-layout.md
- docs/OVERVIEW.md
- docs/plan.md
- docs/concept.md
- docs/spec.md
- docs/architecture.md
- .codex/skills/comfy-blender-vrm/SKILL.md
- .codex/skills/comfy-blender-vrm/references/pipeline.md
- .codex/skills/kyarakuri-comfy-blender-vrm/references/pipeline.md
- .codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md
- .codex/skills/comfy-blender-vrm/scripts/comfy_helpers.py
- .codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py
- .codex/skills/comfy-blender-vrm/scripts/generate_character_from_brief.py
- .codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py

## 差分仕様
- DS-01:
  - Given: base image を生成したい。
  - When: `generate-character-from-brief` または `generate-character-sheet` を実行する。
  - Then: project 名を自動決定し、成果物は `output_dir/<project-name>/images/base/<run-id>/` と `output_dir/<project-name>/logs/` に保存される。
- DS-02:
  - Given: base image から表情差分を生成したい。
  - When: `generate-expression-sheet` を実行する。
  - Then: base image path から project 名を引き継ぎ、成果物は `output_dir/<project-name>/images/expressions/<run-id>/<expression>/` と `output_dir/<project-name>/logs/` に保存される。
- DS-03:
  - Given: project folder 名を決めたい。
  - When: base image 生成を開始する。
  - Then: brief の `core_concept` を優先し、それがない経路では prompt 先頭句から project 名を自動決定する。

## 受入条件（Acceptance Criteria）
- AC-01: base image 成果物が `output_dir/<project-name>/images/base/<run-id>/images/` に保存される。
- AC-02: base image metadata が `output_dir/<project-name>/logs/<run-id>.json` に保存される。
- AC-03: expression 成果物が `output_dir/<project-name>/images/expressions/<run-id>/<expression>/images/` に保存される。
- AC-04: expression metadata が `output_dir/<project-name>/logs/<run-id>.json` に保存され、base image から引き継いだ `project_name` を持つ。
- AC-05: docs / references が新しい project output layout を示している。
- AC-06: 実 ComfyUI で `kyarakuri-generate-base-image` と `kyarakuri-generate-expressions` を再実行し、新しい保存先で成功する。
- AC-07: `delta-project-validator` の `links-only` が PASS する。

## Verify Profile
- static check: Required
- targeted unit: Not Required
- targeted integration / E2E: Required
- delta-project-validator: links-only

## Canonical Sync Mode
- mode: post-archive sync
- reason: code と docs の両方を変更するため、verify PASS 後に正本を最小同期する。

## 制約
- project 名は自動決定のみとし、今回は新しい CLI 引数を追加しない。
- 既存 outputs はそのまま残し、今後の新規 run だけ新構成に出力する。
- Blender 系コマンドの保存先は今回変更しない。

## Review Gate
- required: No
- reason: base / expressions の保存先変更に閉じた差分であり、レイヤー追加や設計刷新は伴わない。

## 未確定事項
- Q-01: Blender 系も project output layout に寄せるかは follow-up delta で判断する。

## Step 2: delta-apply
- changed files:
  - .codex/skills/comfy-blender-vrm/scripts/comfy_helpers.py
  - .codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py
  - .codex/skills/comfy-blender-vrm/scripts/generate_character_from_brief.py
  - .codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py
  - .codex/skills/comfy-blender-vrm/SKILL.md
  - .codex/skills/comfy-blender-vrm/references/pipeline.md
  - .codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md
  - .codex/skills/kyarakuri-comfy-blender-vrm/references/pipeline.md
  - docs/concept.md
  - docs/spec.md
  - docs/architecture.md
  - docs/OVERVIEW.md
  - docs/plan.md
  - docs/delta/DR-20260314-project-output-layout.md
- applied AC:
  - AC-01:
    - 変更: base image の出力先を `outputs/<project-name>/images/base/<run-id>/images/` に変更した。
    - 根拠: `generate_character_sheet.py` が `prepare_project_output_paths(..., "base", ...)` を使う。
  - AC-02:
    - 変更: base image metadata の出力先を `outputs/<project-name>/logs/` に変更した。
    - 根拠: `generate_character_sheet.py` が project ごとの `logs_dir` を使う。
  - AC-03:
    - 変更: expression 出力先を `outputs/<project-name>/images/expressions/<run-id>/<expression>/images/` に変更した。
    - 根拠: `generate_expression_sheet.py` が `prepare_project_output_paths(..., "expressions", ...)` を使う。
  - AC-04:
    - 変更: expression 側に base image path からの project 名引継ぎロジックを追加した。
    - 根拠: `infer_project_name_from_output_path()` で project folder を引き継ぎ、metadata に `project_name` を残す。
  - AC-05:
    - 変更: canonical docs と pipeline refs を新しい output layout に更新した。
    - 根拠: spec / architecture / overview / plan / pipeline が `outputs/<project-name>/...` を示す。
  - AC-06:
    - 変更: real ComfyUI verify 用に base / expressions の両コマンドが project output を表示するようにした。
    - 根拠: success 出力に `Project` と `Project output` を追加した。
  - AC-07:
    - 変更: delta validator が通る形で docs と delta record の参照を整えた。
    - 根拠: plan archive / current と delta record を同期した。
- non-goal kept:
  - Out of Scope への変更なし: Yes
- canonical sync:
  - mode: post-archive sync
  - action: 正本 docs の同期は verify PASS 後に実施
  - status: NOT STARTED
- code split check:
  - file over 500 lines: No
  - file over 800 lines: No
  - file over 1000 lines: No
  - long function issue: No
  - module responsibility issue: No
- status: APPLIED

## Step 3: delta-verify
- verify profile:
  - static check: Required
  - targeted unit: Not Required
  - targeted integration / E2E: Required
  - delta validator: links-only
- executed verify:
  - static check:
    - `python -m py_compile .codex/skills/comfy-blender-vrm/scripts/comfy_helpers.py .codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py .codex/skills/comfy-blender-vrm/scripts/generate_character_from_brief.py .codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py`
  - targeted integration / E2E:
    - base image:
      - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py --workflow .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-base.api.json --brief-file outputs/tmp/real-comfyui-brief.json --timeout-seconds 600`
      - output dir: `outputs/future-inspired-japanese-idol-mechanic/images/base/20260314-003720-character-from-brief/`
      - metadata: `outputs/future-inspired-japanese-idol-mechanic/logs/20260314-003720-character-from-brief.json`
    - expressions:
      - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expressions.py --workflow .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-expressions.api.json --base-image outputs/future-inspired-japanese-idol-mechanic/images/base/20260314-003720-character-from-brief/images/001_9_20260314-003720-character-from-brief_00001_.png --character-prompt "<saved prompt>" --expressions neutral,smile --timeout-seconds 600`
      - output dir: `outputs/future-inspired-japanese-idol-mechanic/images/expressions/20260314-003834-expression-sheet/`
      - metadata: `outputs/future-inspired-japanese-idol-mechanic/logs/20260314-003834-expression-sheet.json`
    - post-run health check: `http://127.0.0.1:8000/system_stats` returned `200`
  - delta validator: `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- review delta outcome:
  - pass: Yes
  - follow-up delta seeds:
    - `DR-20260313-real-comfyui-smoke-verify`
    - Blender 系を project output layout に寄せる follow-up delta
- AC result table:
  - AC-01: PASS
    - 根拠: base image は `outputs/future-inspired-japanese-idol-mechanic/images/base/20260314-003720-character-from-brief/images/` に保存された。
  - AC-02: PASS
    - 根拠: base metadata は `outputs/future-inspired-japanese-idol-mechanic/logs/20260314-003720-character-from-brief.json` に保存された。
  - AC-03: PASS
    - 根拠: expression は `outputs/future-inspired-japanese-idol-mechanic/images/expressions/20260314-003834-expression-sheet/<expression>/images/` に保存された。
  - AC-04: PASS
    - 根拠: expression metadata は同 project の `logs/` に保存され、`project_name` は `future-inspired-japanese-idol-mechanic` だった。
  - AC-05: PASS
    - 根拠: docs / pipeline refs が新しい project output layout を示すように更新された。
  - AC-06: PASS
    - 根拠: real ComfyUI で base / expressions の両方が成功し、新しい保存先に成果物を出力した。
  - AC-07: PASS
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
  - base metadata: `outputs/future-inspired-japanese-idol-mechanic/logs/20260314-003720-character-from-brief.json`
  - expression metadata: `outputs/future-inspired-japanese-idol-mechanic/logs/20260314-003834-expression-sheet.json`
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
  - 目的: base / expressions の保存先を project 単位へまとめる
  - 変更対象: base / expressions の output path、project 名導出 / 引継ぎ、関連 docs
  - 非対象: Blender / motion の保存先変更、既存 outputs の移行、CLI project name 引数、workflow / 品質変更
- unresolved items:
  - Q-01: Blender 系を project output layout に寄せるかは follow-up delta で判断する
- follow-up delta seeds:
  - `DR-20260313-real-comfyui-smoke-verify`
  - Blender 系を project output layout に寄せる follow-up delta
