# delta-request

## Delta ID
- DR-20260313-align-comfyui-url-8000

## Delta Type
- FIX

## 目的
- ローカルの ComfyUI 実待受ポート `127.0.0.1:8000` に合わせて、既定 config の `comfyui_url` を修正する。
- `doctor` と `kyarakuri-prepare-environment` が現行ローカル環境で PASS する状態に合わせる。

## 変更対象（In Scope）
- `config/comfy-blender-vrm.json` の `comfyui_url` を `http://127.0.0.1:8000` に更新する。
- `config/kyarakuri-comfy-blender-vrm.json` の `comfyui_url` を `http://127.0.0.1:8000` に更新する。
- Active Delta の現在地として `docs/OVERVIEW.md` と `docs/plan.md` を更新する。
- verify / archive 記録を `docs/delta/DR-20260313-align-comfyui-url-8000.md` に残す。

## 非対象（Out of Scope）
- ComfyUI GUI アプリのポート設定変更。
- Blender path や workflow path の変更。
- skill 名や command 名の変更。
- concept / spec / architecture の機能仕様変更。

## Candidate Files/Artifacts
- docs/delta/DR-20260313-align-comfyui-url-8000.md
- docs/OVERVIEW.md
- docs/plan.md
- config/comfy-blender-vrm.json
- config/kyarakuri-comfy-blender-vrm.json

## 差分仕様
- DS-01:
  - Given: 現在のローカル ComfyUI が `127.0.0.1:8000` で応答している。
  - When: 既定 config を使って `doctor` または `kyarakuri-prepare-environment` を実行する。
  - Then: `comfyui_url` は `http://127.0.0.1:8000` を使う。
- DS-02:
  - Given: config 更新後に `doctor` / `kyarakuri-prepare-environment` を実行する。
  - When: ComfyUI / Blender / workflow / output の確認を行う。
  - Then: 現行ローカル環境では 9/9 checks PASS で終了する。

## 受入条件（Acceptance Criteria）
- AC-01: `config/comfy-blender-vrm.json` の `comfyui_url` が `http://127.0.0.1:8000` になっている。
- AC-02: `config/kyarakuri-comfy-blender-vrm.json` の `comfyui_url` が `http://127.0.0.1:8000` になっている。
- AC-03: `python .codex/skills/comfy-blender-vrm/scripts/doctor.py` が既定 config で PASS する。
- AC-04: `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/prepare_environment.py` が既定 config で PASS する。
- AC-05: Active Delta と archive 状態が `docs/OVERVIEW.md` / `docs/plan.md` に反映される。

## Verify Profile
- static check: Not Required
- targeted unit: Not Required
- targeted integration / E2E: Required
- delta-project-validator: links-only

## Canonical Sync Mode
- mode: direct canonical update
- reason: 変更対象が config と運用 docs に限定されており、同一 delta 内で状態反映まで完結できる。

## 制約
- ComfyUI の実待受ポートは 2026-03-13 時点で `127.0.0.1:8000` を使う。
- 既定 config のみを変更し、CLI 引数や code path は変更しない。

## Review Gate
- required: No
- reason: 設定値の整合修正であり、機能拡張や設計変更を含まない。

## 未確定事項
- なし

## Step 2: delta-apply
- changed files:
  - config/comfy-blender-vrm.json
  - config/kyarakuri-comfy-blender-vrm.json
  - docs/OVERVIEW.md
  - docs/plan.md
  - docs/delta/DR-20260313-align-comfyui-url-8000.md
- applied AC:
  - AC-01:
    - 変更: `config/comfy-blender-vrm.json` の `comfyui_url` を `http://127.0.0.1:8000` に更新した。
    - 根拠: internal 既定 config が実待受ポートと一致する。
  - AC-02:
    - 変更: `config/kyarakuri-comfy-blender-vrm.json` の `comfyui_url` を `http://127.0.0.1:8000` に更新した。
    - 根拠: repo-local 既定 config が実待受ポートと一致する。
  - AC-03:
    - 変更: internal `doctor` が既定 config で `8000` を参照する状態にした。
    - 根拠: code path は変えず config 値だけを修正した。
  - AC-04:
    - 変更: repo-local `kyarakuri-prepare-environment` が既定 config で `8000` を参照する状態にした。
    - 根拠: wrapper 既定 config の URL を修正した。
  - AC-05:
    - 変更: Active Delta 状態を `docs/OVERVIEW.md` / `docs/plan.md` に反映した。
    - 根拠: request 起票時点で current 状態を更新した。
- non-goal kept:
  - Out of Scope への変更なし: Yes
- canonical sync:
  - mode: direct canonical update
  - action: `docs/OVERVIEW.md` と `docs/plan.md` を delta 状態に合わせて更新した
  - status: DONE
- code split check:
  - file over 500 lines: No
  - file over 800 lines: No
  - file over 1000 lines: No
  - long function issue: N/A
  - module responsibility issue: N/A
- status: APPLIED

## Step 3: delta-verify
- verify profile:
  - static check: Not Required
  - targeted unit: Not Required
  - targeted integration / E2E: Required
  - delta validator: links-only
- executed verify:
  - targeted integration / E2E:
    - success case: `python .codex/skills/comfy-blender-vrm/scripts/doctor.py`
    - success case: `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/prepare_environment.py`
  - delta validator: `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- review delta outcome:
  - pass: Yes
  - follow-up delta seeds:
    - `review delta`
- AC result table:
  - AC-01: PASS
    - 根拠: `config/comfy-blender-vrm.json` の `comfyui_url` が `http://127.0.0.1:8000` になっている。
  - AC-02: PASS
    - 根拠: `config/kyarakuri-comfy-blender-vrm.json` の `comfyui_url` が `http://127.0.0.1:8000` になっている。
  - AC-03: PASS
    - 根拠: internal `doctor` が 9/9 checks passed で終了した。
  - AC-04: PASS
    - 根拠: repo-local `kyarakuri-prepare-environment` が 9/9 checks passed で終了した。
  - AC-05: PASS
    - 根拠: `docs/OVERVIEW.md` / `docs/plan.md` に active delta 起票状態を反映し、validator も OK だった。
- scope deviation:
  - Out of Scope 変更あり: No
- review findings:
  - layer integrity: NOT CHECKED
  - docs sync: PASS
  - data size: NOT CHECKED
  - code split health: NOT CHECKED
  - file-size threshold: NOT CHECKED
- canonical sync:
  - mode: direct canonical update
  - status: DONE
  - result: PASS
- references:
  - internal / repo-local の両経路で `http://127.0.0.1:8000/system_stats (HTTP 200)` を確認した。
  - `validate_delta_links.js` returned `OK: errors=0, warnings=0`.
- overall: PASS

## Step 4: delta-archive
- verify result: PASS
- review gate: NOT REQUIRED
- archive status: archived
- canonical sync:
  - mode: direct canonical update
  - status: DONE
  - synced docs:
    - overview: `docs/OVERVIEW.md`
    - plan: `docs/plan.md`
- closed scope:
  - 目的: 既定 config の `comfyui_url` をローカル実待受 `127.0.0.1:8000` に揃える
  - 変更対象: internal / repo-local config、運用 docs
  - 非対象: GUI 側ポート設定変更、skill 名変更、機能仕様変更
- unresolved items:
  - なし
- follow-up delta seeds:
  - `review delta`
