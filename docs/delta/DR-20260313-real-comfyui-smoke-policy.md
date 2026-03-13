# delta-request

## Delta ID
- DR-20260313-real-comfyui-smoke-policy

## Delta Type
- DOCS-SYNC

## 目的
- 実 ComfyUI を使う検証方針を明文化する。
- 日常 verify は mock / fake を主力とし、実 ComfyUI は主要機能が使えることを確認する smoke verify に使う方針を固定する。

## 変更対象（In Scope）
- `docs/OVERVIEW.md` に verify 方針を追加する。
- `docs/architecture.md` に verify strategy を追加する。
- `docs/plan.md` に次の seed として実 ComfyUI smoke verify の検討項目を残す。
- delta 記録を `docs/delta/DR-20260313-real-comfyui-smoke-policy.md` に残す。

## 非対象（Out of Scope）
- 実 ComfyUI smoke test の具体的な実装。
- CI 導入や test runner 追加。
- 既存 feature code の変更。
- Blender 実機 smoke test の詳細定義。

## Candidate Files/Artifacts
- docs/delta/DR-20260313-real-comfyui-smoke-policy.md
- docs/OVERVIEW.md
- docs/architecture.md
- docs/plan.md

## 差分仕様
- DS-01:
  - Given: このプロジェクトの verify 方針を定めたい。
  - When: 正本 docs を参照する。
  - Then: mock / fake を主力 verify とし、実 ComfyUI は主要機能が使えることを確認する smoke verify に使う方針が読める。
- DS-02:
  - Given: 次の作業 seed を決めたい。
  - When: `docs/plan.md` を参照する。
  - Then: 実 ComfyUI smoke verify delta を次候補として確認できる。

## 受入条件（Acceptance Criteria）
- AC-01: `docs/OVERVIEW.md` に verify 方針として「mock / fake を主力、実 ComfyUI は主要機能の smoke verify」が明記されている。
- AC-02: `docs/architecture.md` に verify strategy が追記されている。
- AC-03: `docs/plan.md` に実 ComfyUI smoke verify を次候補として残している。
- AC-04: `delta-project-validator` の `links-only` が PASS する。

## Verify Profile
- static check: Not Required
- targeted unit: Not Required
- targeted integration / E2E: Not Required
- delta-project-validator: links-only

## Canonical Sync Mode
- mode: direct canonical update
- reason: docs-only の差分であり、同一 delta 内で正本更新を完結できる。

## 制約
- 実 ComfyUI の位置づけは smoke verify に限定し、毎回の主力 verify に昇格させない。
- 主要機能は現時点で `generate-base-image` と `generate-expressions` を想定するが、この delta では候補明記に留める。

## Review Gate
- required: No
- reason: 運用方針の明文化に留まり、設計刷新や実装変更を含まない。

## 未確定事項
- Q-01: 実 ComfyUI smoke verify の固定 workflow / fixed prompt は follow-up delta で定義する。

## Step 2: delta-apply
- changed files:
  - docs/OVERVIEW.md
  - docs/architecture.md
  - docs/plan.md
  - docs/delta/DR-20260313-real-comfyui-smoke-policy.md
- applied AC:
  - AC-01:
    - 変更: `docs/OVERVIEW.md` に verify 方針を追加した。
    - 根拠: mock / fake を主力、実 ComfyUI は smoke verify という運用が読める。
  - AC-02:
    - 変更: `docs/architecture.md` に `Verify Strategy` を追加した。
    - 根拠: verify の主力経路と smoke verify の位置づけをレイヤー文書へ反映した。
  - AC-03:
    - 変更: `docs/plan.md` の future に実 ComfyUI smoke verify delta seed を追加した。
    - 根拠: 次候補として `DR-20260313-real-comfyui-smoke-verify` を残した。
  - AC-04:
    - 変更: validator 実行可能な形で plan / delta 参照を更新した。
    - 根拠: plan current / archive 参照を追加して delta 記録を閉じる状態にした。
- non-goal kept:
  - Out of Scope への変更なし: Yes
- canonical sync:
  - mode: direct canonical update
  - action: `docs/OVERVIEW.md`、`docs/architecture.md`、`docs/plan.md` を直接更新した
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
  - targeted integration / E2E: Not Required
  - delta validator: links-only
- executed verify:
  - delta validator: `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- review delta outcome:
  - pass: Yes
  - follow-up delta seeds:
    - `DR-20260313-real-comfyui-smoke-verify`
- AC result table:
  - AC-01: PASS
    - 根拠: `docs/OVERVIEW.md` に verify 方針が記載された。
  - AC-02: PASS
    - 根拠: `docs/architecture.md` に `Verify Strategy` が記載された。
  - AC-03: PASS
    - 根拠: `docs/plan.md` future に実 ComfyUI smoke verify delta seed を追加した。
  - AC-04: PASS
    - 根拠: `validate_delta_links.js` が `OK` で終了した。
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
    - architecture: `docs/architecture.md`
    - plan: `docs/plan.md`
- closed scope:
  - 目的: 実 ComfyUI を smoke verify に使う方針を正本 docs に反映する
  - 変更対象: verify 方針の docs 記述、follow-up delta seed
  - 非対象: smoke test 実装、CI、既存 feature code
- unresolved items:
  - Q-01: 実 ComfyUI smoke verify の固定 workflow / fixed prompt は follow-up delta で定義する
- follow-up delta seeds:
  - `DR-20260313-real-comfyui-smoke-verify`
