# delta-request

## Delta ID
- DR-20260314-remove-legacy-compat-layer

## Delta Type
- OPS

## 目的
- release 前の整理として legacy compatibility layer を repo から物理削除し、canonical skill pack だけで使える状態にする。
- current docs を canonical single-pack 前提に揃え、旧 pack 依存が残らないことを確認する。

## 変更対象（In Scope）
- `.codex/skills/comfy-blender-vrm/` を削除する。
- `config/comfy-blender-vrm.json` を削除する。
- root README、canonical skill docs、canonical docs から legacy compatibility layer の現行運用説明を削除する。
- canonical `kyarakuri-*` commands が旧 pack 非依存で動くことを verify する。
- delta 記録を `docs/delta/DR-20260314-remove-legacy-compat-layer.md` に残す。

## 非対象（Out of Scope）
- archived delta docs の歴史記録書き換え。
- `docs/comfy-blender-vrm_requirements.md` の歴史的ファイル名表記変更。
- `kyarakuri-*` command 名、CLI 引数、config key の変更。
- distributable skill への移行。
- output layout の変更。

## Candidate Files/Artifacts
- docs/delta/DR-20260314-remove-legacy-compat-layer.md
- docs/OVERVIEW.md
- docs/plan.md
- docs/concept.md
- docs/spec.md
- docs/architecture.md
- README.md
- README_ja.md
- .codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md
- .codex/skills/kyarakuri-comfy-blender-vrm/references/pipeline.md
- .codex/skills/comfy-blender-vrm/
- config/comfy-blender-vrm.json

## 差分仕様
- DS-01:
  - Given: repo 内 skill 一覧を確認する。
  - When: canonical implementation の位置づけを読む。
  - Then: `.codex/skills/kyarakuri-comfy-blender-vrm/` だけが現行 skill pack として示される。
- DS-02:
  - Given: 旧 compatibility layer が不要になっている。
  - When: repo の skill / config 配置を確認する。
  - Then: `.codex/skills/comfy-blender-vrm/` と `config/comfy-blender-vrm.json` は存在しない。
- DS-03:
  - Given: ユーザーが canonical command を使う。
  - When: `kyarakuri-prepare-environment`、`kyarakuri-generate-base-image`、`kyarakuri-generate-expressions`、`kyarakuri-build-vrm`、`kyarakuri-apply-motion-preview` を実行する。
  - Then: 旧 pack なしで成功し、主要成果物または metadata を保存する。

## 受入条件（Acceptance Criteria）
- AC-01: `.codex/skills/comfy-blender-vrm/` が repo から削除されている。
- AC-02: `config/comfy-blender-vrm.json` が repo から削除されている。
- AC-03: README / canonical skill docs / canonical docs が single canonical pack 前提に更新されている。
- AC-04: `kyarakuri-prepare-environment` が canonical config で成功する。
- AC-05: `kyarakuri-generate-base-image` が real ComfyUI で成功する。
- AC-06: `kyarakuri-generate-expressions` が real ComfyUI で成功する。
- AC-07: `kyarakuri-build-vrm` と `kyarakuri-apply-motion-preview` が fake Blender で成功する。
- AC-08: `delta-project-validator` の `full` が PASS する。

## Verify Profile
- static check: Required
- targeted unit: Not Required
- targeted integration / E2E: Required
- delta-project-validator: full

## Canonical Sync Mode
- mode: post-archive sync
- reason: 削除対象の物理変更と current docs 更新を verify PASS 後の archive で確定する。

## 制約
- `AppData` / `Documents/ComfyUI` 配下は編集しない。
- history record としての archived delta docs は書き換えない。
- canonical skill pack の public command 名と引数は変えない。

## Review Gate
- required: Yes
- reason: runtime deletion と current docs の同期を伴う release 前整理であり、layer integrity と docs sync を明示確認する必要がある。

## Review Focus（REVIEW または review gate required の場合）
- checklist: `docs/delta/REVIEW_CHECKLIST.md`
- target area: canonical single-pack 化後の layer integrity、docs sync、verify coverage

## 未確定事項
- Q-01: archived docs 内の旧 pack path を将来どう扱うかは別 delta に切り分ける。

## Step 2: delta-apply
- changed files:
  - `.codex/skills/comfy-blender-vrm/` を削除
  - `config/comfy-blender-vrm.json` を削除
  - `.codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/references/pipeline.md`
  - `README.md`
  - `README_ja.md`
  - `docs/concept.md`
  - `docs/spec.md`
  - `docs/architecture.md`
  - `docs/OVERVIEW.md`
  - `docs/plan.md`
  - `docs/delta/DR-20260314-remove-legacy-compat-layer.md`
- applied AC:
  - AC-01:
    - 変更: legacy compatibility skill pack 一式を repo から削除した。
    - 根拠: `.codex/skills/comfy-blender-vrm/` 以下の tracked files を削除し、残っていた `__pycache__` を含むディレクトリも消した。
  - AC-02:
    - 変更: old default config を削除した。
    - 根拠: `config/comfy-blender-vrm.json` を削除し、canonical config のみを残した。
  - AC-03:
    - 変更: root README、canonical skill docs、canonical docs を single-pack 前提に更新した。
    - 根拠: README / SKILL / concept / spec / architecture から legacy layer の現行運用説明を除去した。
  - AC-04:
    - 変更: canonical config で `kyarakuri-prepare-environment` が成功する前提に整理した。
    - 根拠: verify で canonical command を直接実行する。
  - AC-05:
    - 変更: real ComfyUI で canonical base-image flow を再実行できる状態にした。
    - 根拠: verify で bundled base workflow を使って生成する。
  - AC-06:
    - 変更: real ComfyUI で canonical expressions flow を再実行できる状態にした。
    - 根拠: verify で bundled expression workflow を使って生成する。
  - AC-07:
    - 変更: fake Blender で canonical build / motion flow を再実行できる状態にした。
    - 根拠: verify で canonical public command から fake Blender config を使って生成する。
  - AC-08:
    - 変更: validator full を通せるよう current docs と delta record を揃えた。
    - 根拠: verify で links/code-size の両方を実行する。
- non-goal kept:
  - Out of Scope への変更なし: Yes
- canonical sync:
  - mode: post-archive sync
  - action: verify PASS 後に current docs の archive 状態を反映する
  - status: DONE
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
  - delta validator: full
- executed verify:
  - static check:
    - `python -m py_compile` for `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/*.py`
  - targeted integration / E2E:
    - canonical environment check:
      - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/prepare_environment.py`
      - result: `9/9 checks passed`
    - real ComfyUI base image:
      - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py --workflow .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-base.api.json --brief-file outputs/tmp/real-comfyui-brief.json --output-name remove-legacy-base --timeout-seconds 600`
      - project output: `outputs/future-inspired-japanese-idol-mechanic/images/base/20260314-062915-remove-legacy-base/`
      - metadata: `outputs/future-inspired-japanese-idol-mechanic/logs/20260314-062915-remove-legacy-base.json`
    - real ComfyUI expressions:
      - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expressions.py --workflow .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-expressions.api.json --base-image outputs/future-inspired-japanese-idol-mechanic/images/base/20260314-062915-remove-legacy-base/images/001_9_20260314-062915-remove-legacy-base_00001_.png --character-prompt "<prompt>" --expressions neutral,smile --output-name remove-legacy-expressions --timeout-seconds 600`
      - project output: `outputs/future-inspired-japanese-idol-mechanic/images/expressions/20260314-063041-remove-legacy-expressions/`
      - metadata: `outputs/future-inspired-japanese-idol-mechanic/logs/20260314-063041-remove-legacy-expressions.json`
    - fake Blender build:
      - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/build_vrm.py --blend-file outputs/tmp/consolidation/fake-input.blend --texture-image outputs/tmp/consolidation/fake-texture.png --config outputs/tmp/consolidation/kyarakuri-build-config.json --output-name remove-legacy-build`
      - metadata: `outputs/tmp/consolidation/kyarakuri-build-output/logs/20260314-063228-remove-legacy-build.json`
    - fake Blender motion:
      - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/apply_motion_preview.py --blend-file outputs/tmp/consolidation/fake-input.blend --motion-file outputs/tmp/consolidation/fake-motion.bvh --config outputs/tmp/consolidation/kyarakuri-motion-config.json --output-name remove-legacy-motion`
      - metadata: `outputs/tmp/consolidation/kyarakuri-motion-output/logs/20260314-063235-remove-legacy-motion.json`
    - post-run health check:
      - `http://127.0.0.1:8000/system_stats` returned `200`
    - deletion check:
      - `Test-Path .codex/skills/comfy-blender-vrm` -> `False`
      - `Test-Path config/comfy-blender-vrm.json` -> `False`
  - delta validator:
    - `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
    - `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/check_code_size.js --dir C:/Users/naruhide/workspace/kyarakuri`
- AC result table:
  - AC-01: PASS
    - 根拠: `.codex/skills/comfy-blender-vrm/` は `Test-Path` で `False` になった。
  - AC-02: PASS
    - 根拠: `config/comfy-blender-vrm.json` は `Test-Path` で `False` になった。
  - AC-03: PASS
    - 根拠: README / SKILL / concept / spec / architecture で canonical single-pack の説明に更新された。
  - AC-04: PASS
    - 根拠: `kyarakuri-prepare-environment` が canonical config で `9/9 checks passed` を返した。
  - AC-05: PASS
    - 根拠: bundled base workflow で `20260314-062915-remove-legacy-base` と metadata を保存した。
  - AC-06: PASS
    - 根拠: bundled expression workflow で `20260314-063041-remove-legacy-expressions` と metadata を保存した。
  - AC-07: PASS
    - 根拠: `kyarakuri-build-vrm` と `kyarakuri-apply-motion-preview` が fake Blender で output と metadata を保存した。
  - AC-08: PASS
    - 根拠: `validate_delta_links.js` が `OK: errors=0, warnings=0`、`check_code_size.js` が `review=0, split=0, exception=0` を返した。
- scope deviation:
  - Out of Scope 変更あり: No
- canonical sync:
  - mode: post-archive sync
  - status: DONE
  - result: PASS
- review findings:
  - layer integrity: PASS
  - docs sync: PASS
  - data size: PASS
  - code split health: PASS
  - file-size threshold: PASS
- overall: PASS

## Step 4: delta-archive
- verify result: PASS
- review gate: PASSED
- archive status: archived
- canonical sync:
  - mode: post-archive sync
  - status: DONE
  - synced docs:
    - overview: `docs/OVERVIEW.md`
    - plan: `docs/plan.md`
    - concept: `docs/concept.md`
    - spec: `docs/spec.md`
    - architecture: `docs/architecture.md`
    - root docs: `README.md`, `README_ja.md`
- closed scope:
  - 目的: legacy compatibility layer を物理削除し、canonical skill pack だけで使える repo 状態にする
  - 変更対象: old skill pack 削除、old config 削除、current docs / root README / canonical skill docs 更新、canonical command verify
  - 非対象: archived delta docs の書き換え、historical requirements の旧 path 更新、command 名 / config key 変更、distributable skill への移行、output layout 変更
- unresolved items:
  - Q-01: archived docs 内の旧 pack path をどう扱うかは別 delta に切り分ける
- follow-up delta seeds:
  - `review delta`
  - `distributable-skill migration`
