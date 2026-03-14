# delta-request

## Delta ID
- DR-20260314-rename-to-forma-character

## Delta Type
- DESIGN

## 目的
- repo-local canonical skill pack の外向き名称を `Forma Character` 系へ統一し、release 名として使える形にする。
- skill pack ID、既定 config 名、public command 名を `forma-character` 系へ揃える。

## 変更対象（In Scope）
- canonical skill pack directory を `.codex/skills/forma-character/` へ rename する。
- canonical config を `config/forma-character.json` へ rename する。
- public command 名を `forma-character-prepare-environment`、`forma-character-generate-base-image`、`forma-character-generate-expressions`、`forma-character-build-vrm`、`forma-character-apply-motion-preview` に更新する。
- canonical pack 配下の docs / workflow notes / helper messages / default paths を `forma-character` 系へ更新する。
- current docs と root README を `Forma Character` / `forma-character` 前提へ同期する。
- renamed canonical pack で real ComfyUI と fake Blender verify を行う。
- delta 記録を `docs/delta/DR-20260314-rename-to-forma-character.md` に残す。

## 非対象（Out of Scope）
- archived delta docs の歴史記録書き換え。
- `docs/comfy-blender-vrm_requirements.md` の歴史的ファイル名表記変更。
- internal implementation command 名 `doctor` / `generate-character-from-brief` / `generate-expression-sheet` / `build-vrm-base` / `apply-motion-preview` の rename。
- output layout 変更。
- distributable skill への移行。

## Candidate Files/Artifacts
- docs/delta/DR-20260314-rename-to-forma-character.md
- docs/OVERVIEW.md
- docs/plan.md
- docs/concept.md
- docs/spec.md
- docs/architecture.md
- README.md
- README_ja.md
- config/kyarakuri-comfy-blender-vrm.json
- config/forma-character.json
- .codex/skills/kyarakuri-comfy-blender-vrm/
- .codex/skills/forma-character/

## 差分仕様
- DS-01:
  - Given: repo 内 skill 一覧と root README を確認する。
  - When: canonical skill pack 名と command 一覧を読む。
  - Then: `Forma Character` / `forma-character` 系の名称だけが current docs に現れる。
- DS-02:
  - Given: default config を使って public wrapper を実行する。
  - When: `prepare_environment.py`、`generate_base_image.py`、`generate_expressions.py`、`build_vrm.py`、`apply_motion_preview.py` を new pack path から実行する。
  - Then: `.codex/skills/forma-character/` と `config/forma-character.json` を既定として動作する。
- DS-03:
  - Given: internal implementation command を使う。
  - When: same-pack `doctor`、`generate_character_from_brief`、`generate_expression_sheet`、`build_vrm_base`、`apply_motion_preview` を実行する。
  - Then: old `kyarakuri` naming に依存せず、new pack path / config path で動作する。

## 受入条件（Acceptance Criteria）
- AC-01: canonical skill pack path が `.codex/skills/forma-character/` になっている。
- AC-02: canonical default config が `config/forma-character.json` になっている。
- AC-03: current docs / root README / canonical skill docs の public command 名が `forma-character-*` に更新されている。
- AC-04: `forma-character-prepare-environment` が既定 config で成功する。
- AC-05: `forma-character-generate-base-image` が real ComfyUI で成功する。
- AC-06: `forma-character-generate-expressions` が real ComfyUI で成功する。
- AC-07: `forma-character-build-vrm` と `forma-character-apply-motion-preview` が fake Blender で成功する。
- AC-08: `delta-project-validator` の `full` が PASS する。

## Verify Profile
- static check: Required
- targeted unit: Not Required
- targeted integration / E2E: Required
- delta-project-validator: full

## Canonical Sync Mode
- mode: post-archive sync
- reason: rename と current docs 更新を verify PASS 後に archive で確定する。

## 制約
- `AppData` / `Documents/ComfyUI` 配下は編集しない。
- archive 済み delta docs は historical record として書き換えない。
- public wrapper script の filename は現状の generic name を維持してよい。

## Review Gate
- required: Yes
- reason: pack directory rename と public naming update を伴うため、layer integrity と docs sync を明示確認する必要がある。

## Review Focus（REVIEW または review gate required の場合）
- checklist: `docs/delta/REVIEW_CHECKLIST.md`
- target area: renamed canonical pack の path integrity、default config resolution、docs sync

## 未確定事項
- Q-01: 将来 `Forma Assets` など別 skill set をどう並べるかは別 delta に切り分ける。

## Step 2: delta-apply
- changed files:
  - `.codex/skills/kyarakuri-comfy-blender-vrm/` -> `.codex/skills/forma-character/`
  - `config/kyarakuri-comfy-blender-vrm.json` -> `config/forma-character.json`
  - `README.md`
  - `README_ja.md`
  - `docs/concept.md`
  - `docs/spec.md`
  - `docs/architecture.md`
  - `docs/OVERVIEW.md`
  - `docs/plan.md`
  - `docs/delta/DR-20260314-rename-to-forma-character.md`
- applied AC:
  - AC-01:
    - 変更: canonical skill pack path を `.codex/skills/forma-character/` に rename した。
    - 根拠: tracked skill files を `git mv` で移動し、same-pack path 参照も更新した。
  - AC-02:
    - 変更: canonical default config を `config/forma-character.json` に rename した。
    - 根拠: config file を rename し、default config lookup と help text を更新した。
  - AC-03:
    - 変更: current docs / root README / canonical skill docs の public command 名を `forma-character-*` に更新した。
    - 根拠: `SKILL.md`、`pipeline.md`、`workflows/README.md`、`character_brief.md`、`README*`、`concept/spec/architecture` を同期した。
  - AC-04:
    - 変更: canonical environment check が `forma-character` の表示と path を使うようにした。
    - 根拠: `doctor.py` の default config path、description、printed command name を更新した。
  - AC-05:
    - 変更: base-image flow が `forma-character` の path / config / public name で動くようにした。
    - 根拠: `_wrapper_common.py`、`generate_character_from_brief.py`、`generate_character_sheet.py` を更新した。
  - AC-06:
    - 変更: expressions flow が `forma-character` の path / config / public name で動くようにした。
    - 根拠: `generate_expression_sheet.py` と public docs を更新した。
  - AC-07:
    - 変更: Blender build / motion flow が `forma-character` の path / config / public name で動くようにした。
    - 根拠: `build_vrm_base.py`、`apply_motion_preview.py`、`build_vrm.py` を更新した。
  - AC-08:
    - 変更: validator full を通せるよう current docs と delta record を揃えた。
    - 根拠: links/code-size validate の前提になる current docs を同期した。
- non-goal kept:
  - Out of Scope への変更なし: Yes
- canonical sync:
  - mode: post-archive sync
  - action: verify PASS 後に current docs の archived state を反映する
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
    - `python -m py_compile` for `.codex/skills/forma-character/scripts/*.py`
  - targeted integration / E2E:
    - canonical environment check:
      - `python .codex/skills/forma-character/scripts/prepare_environment.py`
      - result: `9/9 checks passed`
    - real ComfyUI base image:
      - `python .codex/skills/forma-character/scripts/generate_base_image.py --workflow .codex/skills/forma-character/workflows/neta-yume-lumina-base.api.json --brief-file outputs/tmp/real-comfyui-brief.json --output-name forma-character-base --timeout-seconds 600`
      - metadata: `outputs/future-inspired-japanese-idol-mechanic/logs/20260314-065114-forma-character-base.json`
    - real ComfyUI expressions:
      - `python .codex/skills/forma-character/scripts/generate_expressions.py --workflow .codex/skills/forma-character/workflows/neta-yume-lumina-expressions.api.json --base-image outputs/future-inspired-japanese-idol-mechanic/images/base/20260314-065114-forma-character-base/images/001_9_20260314-065114-forma-character-base_00001_.png --character-prompt "<prompt>" --expressions neutral,smile --output-name forma-character-expressions --timeout-seconds 600`
      - metadata: `outputs/future-inspired-japanese-idol-mechanic/logs/20260314-065247-forma-character-expressions.json`
    - fake Blender build:
      - `python .codex/skills/forma-character/scripts/build_vrm.py --blend-file outputs/tmp/consolidation/fake-input.blend --texture-image outputs/tmp/consolidation/fake-texture.png --config outputs/tmp/forma-rename/build-config.json --output-name forma-character-build`
      - metadata: `outputs/tmp/forma-rename/build-output/logs/20260314-065449-forma-character-build.json`
    - fake Blender motion:
      - `python .codex/skills/forma-character/scripts/apply_motion_preview.py --blend-file outputs/tmp/consolidation/fake-input.blend --motion-file outputs/tmp/consolidation/fake-motion.bvh --config outputs/tmp/forma-rename/motion-config.json --output-name forma-character-motion`
      - metadata: `outputs/tmp/forma-rename/motion-output/logs/20260314-065455-forma-character-motion.json`
    - path existence check:
      - `Test-Path .codex/skills/kyarakuri-comfy-blender-vrm` -> `False`
      - `Test-Path config/kyarakuri-comfy-blender-vrm.json` -> `False`
      - `Test-Path .codex/skills/forma-character` -> `True`
      - `Test-Path config/forma-character.json` -> `True`
    - post-run health check:
      - `http://127.0.0.1:8000/system_stats` returned `200`
  - delta validator:
    - `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
    - `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/check_code_size.js --dir C:/Users/naruhide/workspace/kyarakuri`
- AC result table:
  - AC-01: PASS
    - 根拠: `.codex/skills/forma-character/` は存在し、old pack path は存在しない。
  - AC-02: PASS
    - 根拠: `config/forma-character.json` は存在し、old config path は存在しない。
  - AC-03: PASS
    - 根拠: current docs / root README / canonical skill docs の public command 名が `forma-character-*` に更新された。
  - AC-04: PASS
    - 根拠: `forma-character-prepare-environment` が `9/9 checks passed` で終了した。
  - AC-05: PASS
    - 根拠: bundled base workflow で `20260314-065114-forma-character-base` と metadata を保存した。
  - AC-06: PASS
    - 根拠: bundled expression workflow で `20260314-065247-forma-character-expressions` と metadata を保存した。
  - AC-07: PASS
    - 根拠: `forma-character-build-vrm` と `forma-character-apply-motion-preview` が fake Blender で output と metadata を保存した。
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
  - 目的: canonical skill pack の外向き名称を `Forma Character` / `forma-character` 系へ統一する
  - 変更対象: pack dir rename、config rename、public command 名更新、canonical docs / root docs 同期、renamed pack verify
  - 非対象: archived delta docs の書き換え、historical requirements の旧 path 更新、internal implementation command rename、output layout 変更、distributable skill への移行
- unresolved items:
  - Q-01: 将来 `Forma Assets` など別 skill set をどう並べるかは別 delta に切り分ける
- follow-up delta seeds:
  - `review delta`
  - `distributable-skill migration`
