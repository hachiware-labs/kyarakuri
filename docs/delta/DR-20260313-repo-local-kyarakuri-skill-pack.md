# delta-request

## Delta ID
- DR-20260313-repo-local-kyarakuri-skill-pack

## Delta Type
- FEATURE

## 目的
- 合意した `kyarakuri-*` 名で repo 内スキルパックを追加し、既存の実装済み機能を user-facing な入口として試せるようにする。
- 配布用 skill へ移す前段として、repo-local skill から `prepare-environment`、`generate-base-image`、`generate-expressions` が呼べる状態を作る。

## 変更対象（In Scope）
- `.codex/skills/kyarakuri-comfy-blender-vrm/` を repo-local skill pack として追加する。
- `kyarakuri-prepare-environment`、`kyarakuri-generate-base-image`、`kyarakuri-generate-expressions` に対応する wrapper script を追加する。
- wrapper script が既存の `comfy-blender-vrm` 実装を再利用し、必要なら新 config を既定値として注入できるようにする。
- `config/kyarakuri-comfy-blender-vrm.json` と新 skill 用 `workflows/` ディレクトリを追加する。
- 新 skill pack の `SKILL.md` と reference を追加し、`kyarakuri-build-vrm` と `kyarakuri-apply-motion-preview` は planned として明示する。

## 非対象（Out of Scope）
- 既存の `.codex/skills/comfy-blender-vrm/` 実装を削除・移動・全面 rename すること。
- 既存の archive 済み delta 記録のパスを書き換えること。
- `kyarakuri-build-vrm` と `kyarakuri-apply-motion-preview` の本実装。
- user skill / 提供可能 skill への移動。

## Candidate Files/Artifacts
- docs/delta/DR-20260313-repo-local-kyarakuri-skill-pack.md
- docs/OVERVIEW.md
- docs/plan.md
- .codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md
- .codex/skills/kyarakuri-comfy-blender-vrm/references/pipeline.md
- .codex/skills/kyarakuri-comfy-blender-vrm/references/character_brief.md
- .codex/skills/kyarakuri-comfy-blender-vrm/workflows/README.md
- .codex/skills/kyarakuri-comfy-blender-vrm/scripts/_wrapper_common.py
- .codex/skills/kyarakuri-comfy-blender-vrm/scripts/prepare_environment.py
- .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py
- .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expressions.py
- config/kyarakuri-comfy-blender-vrm.json

## 差分仕様
- DS-01:
  - Given: ユーザーが repo 内 skill 一覧から `kyarakuri-comfy-blender-vrm` を見る。
  - When: `SKILL.md` を読む。
  - Then: `kyarakuri-prepare-environment`、`kyarakuri-generate-base-image`、`kyarakuri-generate-expressions` の実行方法と、planned の `kyarakuri-build-vrm`、`kyarakuri-apply-motion-preview` が区別して分かる。
- DS-02:
  - Given: ユーザーが wrapper script を実行する。
  - When: `prepare_environment.py`、`generate_base_image.py`、`generate_expressions.py` が起動する。
  - Then: 既存の `comfy-blender-vrm` 実装へ委譲し、同等の処理を実行できる。
- DS-03:
  - Given: ユーザーが新 skill pack を既定 config で使う。
  - When: wrapper script が `--config` 未指定で起動する。
  - Then: `config/kyarakuri-comfy-blender-vrm.json` を既定として利用できる。

## 受入条件（Acceptance Criteria）
- AC-01: `.codex/skills/kyarakuri-comfy-blender-vrm/` が repo-local skill pack として追加され、public name 一覧に `kyarakuri-prepare-environment`、`kyarakuri-generate-base-image`、`kyarakuri-generate-expressions`、`kyarakuri-build-vrm`、`kyarakuri-apply-motion-preview` が定義されている。
- AC-02: `kyarakuri-prepare-environment`、`kyarakuri-generate-base-image`、`kyarakuri-generate-expressions` に対応する wrapper script が追加され、既存実装へ委譲できる。
- AC-03: `config/kyarakuri-comfy-blender-vrm.json` と新 skill pack の `workflows/` が存在し、repo-local skill として使う既定 path が文書化されている。
- AC-04: `kyarakuri-build-vrm` と `kyarakuri-apply-motion-preview` は planned / not implemented として明示され、実装済みと誤認しない。
- AC-05: wrapper script の static check、targeted integration、links-only validator が PASS する。

## Verify Profile
- static check: Required
- targeted unit: Not Required
- targeted integration / E2E: Required
- delta-project-validator: links-only

## Canonical Sync Mode
- mode: post-archive sync
- reason: repo-local skill pack の追加を verify PASS で確定した後、正本 docs に最小差分で同期する。

## 制約
- 既存実装の主要ロジックは再利用し、重複実装しない。
- wrapper は repo 内 skill として完結させ、global / user skill への移動は行わない。
- 既存 skill pack の archive 済み履歴を壊さないため、既存フォルダの削除や rename は行わない。

## Review Gate
- required: No
- reason: 新規 repo-local wrapper skill pack の追加であり、既存ロジックの再利用が中心で大規模設計変更ではない。

## 未確定事項
- Q-01: Resolved. wrapper の標準出力は既存 implementation の表示を維持し、public 名は repo-local skill docs 側で表現する形にした。
- Q-02: Resolved. 新 skill pack の reference は最小内容を複製し、repo-local skill として self-contained にした。

## Step 2: delta-apply
- changed files:
  - .codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md
  - .codex/skills/kyarakuri-comfy-blender-vrm/references/pipeline.md
  - .codex/skills/kyarakuri-comfy-blender-vrm/references/character_brief.md
  - .codex/skills/kyarakuri-comfy-blender-vrm/workflows/README.md
  - .codex/skills/kyarakuri-comfy-blender-vrm/scripts/_wrapper_common.py
  - .codex/skills/kyarakuri-comfy-blender-vrm/scripts/prepare_environment.py
  - .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py
  - .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expressions.py
  - config/kyarakuri-comfy-blender-vrm.json
  - docs/delta/DR-20260313-repo-local-kyarakuri-skill-pack.md
- applied AC:
  - AC-01:
    - 変更: repo-local skill pack `.codex/skills/kyarakuri-comfy-blender-vrm/` を追加し、public name 一覧を `SKILL.md` に定義した。
    - 根拠: `kyarakuri-prepare-environment`、`kyarakuri-generate-base-image`、`kyarakuri-generate-expressions` を implemented、`kyarakuri-build-vrm` と `kyarakuri-apply-motion-preview` を planned として記載した。
  - AC-02:
    - 変更: 3 本の wrapper script と共通 helper を追加し、既存の `doctor`、`generate_character_from_brief`、`generate_expression_sheet` へ委譲するようにした。
    - 根拠: wrapper が implementation script dir を `sys.path` に追加し、legacy `main()` をそのまま呼ぶ。
  - AC-03:
    - 変更: `config/kyarakuri-comfy-blender-vrm.json` と新 skill pack の `workflows/README.md` を追加した。
    - 根拠: wrapper が `--config` 未指定時に新 config を注入し、新 skill pack 側の workflow dir を既定 path として使える。
  - AC-04:
    - 変更: `SKILL.md` と `references/pipeline.md` で `kyarakuri-build-vrm` と `kyarakuri-apply-motion-preview` を planned と明示した。
    - 根拠: repo-local skill pack 上で未実装コマンドを implemented と表記していない。
  - AC-05:
    - 変更: wrapper scripts を対象に static check と targeted integration を実行できる状態にした。
    - 根拠: apply 後に verify 用の wrapper 経路が揃っている。
- non-goal kept:
  - Out of Scope への変更なし: Yes
- canonical sync:
  - mode: post-archive sync
  - action: 正本 docs の追加同期は未実施
  - status: NOT STARTED
- code split check:
  - file over 500 lines: No
  - file over 800 lines: No
  - file over 1000 lines: No
  - `_wrapper_common.py`: 30 lines
  - `prepare_environment.py`: 5 lines
  - `generate_base_image.py`: 5 lines
  - `generate_expressions.py`: 5 lines
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
  - static check: `python -m py_compile .codex/skills/kyarakuri-comfy-blender-vrm/scripts/_wrapper_common.py .codex/skills/kyarakuri-comfy-blender-vrm/scripts/prepare_environment.py .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expressions.py`
  - targeted integration / E2E:
    - success case: `prepare_environment.py` を wrapper default config 注入で実行し、9/9 checks pass
    - success case: `generate_base_image.py` を wrapper default config 注入で実行し、画像、`brief.json`、`prompt-preview.txt` を保存
    - success case: `generate_expressions.py` を wrapper default config 注入で実行し、`neutral` expression の画像を保存
  - delta validator: `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- review delta outcome:
  - pass: Yes
  - follow-up delta seeds:
    - `build-vrm-base` request
    - `rename / migrate distributable skill` request
- AC result table:
  - AC-01: PASS
    - 根拠: repo-local skill pack の `SKILL.md` に public name 一覧と implemented / planned の区別を記載した。
  - AC-02: PASS
    - 根拠: wrapper 3 本がそれぞれ既存 implementation `main()` を呼び、success case を完了した。
  - AC-03: PASS
    - 根拠: new config file と workflow dir が存在し、wrapper default config 注入で 3 コマンドが動作した。
  - AC-04: PASS
    - 根拠: `kyarakuri-build-vrm` と `kyarakuri-apply-motion-preview` は docs 上で planned のみとし、実行例を出していない。
  - AC-05: PASS
    - 根拠: static check、wrapper integration、links-only validator がすべて PASS した。
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
  - status: NOT STARTED
  - result: PASS
- references:
  - wrapper integration では repo config を一時的に差し替えて、mock ComfyUI で prepare / base / expressions の 3 経路を確認した。
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
  - 目的: repo 内で `kyarakuri-*` public name を試せる wrapper skill pack を追加する
  - 変更対象: repo-local skill pack、wrapper scripts、新 config、新 references
  - 非対象: 既存 skill pack の rename / 削除、planned command の本実装、provided skill への移動
- unresolved items:
  - なし
- follow-up delta seeds:
  - `build-vrm-base` request
  - `rename / migrate distributable skill` request
