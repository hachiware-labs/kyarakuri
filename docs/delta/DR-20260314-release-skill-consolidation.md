# delta-request

## Delta ID
- DR-20260314-release-skill-consolidation

## Delta Type
- FEATURE

## 目的
- `kyarakuri-comfy-blender-vrm` を repo 内の canonical implementation skill pack に昇格し、release 前提の単一実装系に寄せる。
- 旧 `comfy-blender-vrm` は互換 CLI entry だけを残し、実装本体の委譲先を `kyarakuri-comfy-blender-vrm` に反転する。

## 変更対象（In Scope）
- `kyarakuri-comfy-blender-vrm` 配下に ComfyUI / Blender 実装本体を持たせる。
- repo-local public wrappers が同 skill pack 内の実装を呼ぶように変更する。
- 旧 `comfy-blender-vrm` の CLI entry scripts を compatibility wrapper に置き換える。
- skill docs / pipeline refs / canonical docs に canonical skill pack の変更を同期する。
- 実 ComfyUI と fake Blender を使って `kyarakuri-*` と legacy CLI entry の基本動作を確認する。
- delta 記録を `docs/delta/DR-20260314-release-skill-consolidation.md` に残す。

## 非対象（Out of Scope）
- ユーザー向け command 名の変更。
- workflow JSON や config key 仕様の変更。
- 旧 `comfy-blender-vrm` skill pack 自体の削除。
- 提供用 skill への移動。
- Blender / motion の output layout 変更。

## Candidate Files/Artifacts
- docs/delta/DR-20260314-release-skill-consolidation.md
- docs/OVERVIEW.md
- docs/plan.md
- docs/concept.md
- docs/architecture.md
- .codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md
- .codex/skills/kyarakuri-comfy-blender-vrm/references/pipeline.md
- .codex/skills/kyarakuri-comfy-blender-vrm/scripts/_wrapper_common.py
- .codex/skills/kyarakuri-comfy-blender-vrm/scripts/*.py
- .codex/skills/kyarakuri-comfy-blender-vrm/blender/*.py
- .codex/skills/comfy-blender-vrm/SKILL.md
- .codex/skills/comfy-blender-vrm/references/pipeline.md
- .codex/skills/comfy-blender-vrm/scripts/_compat_common.py
- .codex/skills/comfy-blender-vrm/scripts/doctor.py
- .codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py
- .codex/skills/comfy-blender-vrm/scripts/generate_character_from_brief.py
- .codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py
- .codex/skills/comfy-blender-vrm/scripts/build_vrm_base.py
- .codex/skills/comfy-blender-vrm/scripts/apply_motion_preview.py

## 差分仕様
- DS-01:
  - Given: repo-local public skill pack を使う。
  - When: `kyarakuri-prepare-environment`、`kyarakuri-generate-base-image`、`kyarakuri-generate-expressions`、`kyarakuri-build-vrm`、`kyarakuri-apply-motion-preview` を実行する。
  - Then: `kyarakuri-comfy-blender-vrm` 配下の実装だけで完結し、別 skill pack への委譲は行わない。
- DS-02:
  - Given: 旧 internal CLI entry を使う。
  - When: `doctor`、`generate-character-sheet`、`generate-character-from-brief`、`generate-expression-sheet`、`build-vrm-base`、`apply-motion-preview` を実行する。
  - Then: compatibility wrapper として canonical `kyarakuri-comfy-blender-vrm` 実装を呼べる。
- DS-03:
  - Given: docs を確認する。
  - When: skill pack の位置づけを読む。
  - Then: `kyarakuri-comfy-blender-vrm` が canonical implementation、`comfy-blender-vrm` が legacy compatibility layer と分かる。

## 受入条件（Acceptance Criteria）
- AC-01: `kyarakuri-comfy-blender-vrm` 配下に ComfyUI / Blender の実装本体が存在する。
- AC-02: repo-local public wrappers は `.codex/skills/comfy-blender-vrm/` ではなく同 skill pack 内の実装を呼ぶ。
- AC-03: 旧 `comfy-blender-vrm` の CLI entry は compatibility wrapper 化され、canonical 実装を呼ぶ。
- AC-04: skill docs / pipeline refs / canonical docs が canonical skill pack と legacy compatibility layer の役割を示す。
- AC-05: `kyarakuri-prepare-environment` と `kyarakuri-generate-base-image` が実 ComfyUI で成功する。
- AC-06: `kyarakuri-build-vrm` と `kyarakuri-apply-motion-preview` が fake Blender で成功する。
- AC-07: 旧 `doctor` と `build-vrm-base` の compatibility wrapper が動作する。
- AC-08: `delta-project-validator` の `links-only` が PASS する。

## Verify Profile
- static check: Required
- targeted unit: Not Required
- targeted integration / E2E: Required
- delta-project-validator: links-only

## Canonical Sync Mode
- mode: post-archive sync
- reason: 実装位置と docs の正本を verify PASS 後に最小同期する。

## 制約
- `AppData` / `Documents/ComfyUI` 配下は編集しない。
- 既存 command 名と CLI 引数は変えない。
- 互換 layer は最小 wrapper に留め、追加機能を入れない。

## Review Gate
- required: No
- reason: skill pack の依存方向整理に閉じた差分であり、ユーザー向け I/F は変更しない。

## 未確定事項
- Q-01: 旧 `comfy-blender-vrm` の helper / blender script の物理削除は別 delta に切り分ける。

## Step 2: delta-apply
- changed files:
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/_wrapper_common.py`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/comfy_helpers.py`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/doctor.py`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_character_sheet.py`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_character_from_brief.py`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expression_sheet.py`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/build_vrm_base.py`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/apply_motion_preview.py`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/blender/build_vrm_base.py`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/blender/apply_motion_preview.py`
  - `.codex/skills/comfy-blender-vrm/scripts/_compat_common.py`
  - `.codex/skills/comfy-blender-vrm/scripts/doctor.py`
  - `.codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py`
  - `.codex/skills/comfy-blender-vrm/scripts/generate_character_from_brief.py`
  - `.codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py`
  - `.codex/skills/comfy-blender-vrm/scripts/build_vrm_base.py`
  - `.codex/skills/comfy-blender-vrm/scripts/apply_motion_preview.py`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/references/pipeline.md`
  - `.codex/skills/comfy-blender-vrm/SKILL.md`
  - `.codex/skills/comfy-blender-vrm/references/pipeline.md`
  - `docs/concept.md`
  - `docs/spec.md`
  - `docs/architecture.md`
  - `docs/OVERVIEW.md`
  - `docs/plan.md`
  - `docs/delta/DR-20260314-release-skill-consolidation.md`
- applied AC:
  - AC-01:
    - 変更: `kyarakuri-comfy-blender-vrm` 配下へ ComfyUI / Blender 実装本体を持たせた。
    - 根拠: `doctor`、`generate_*`、`build_vrm_base`、`apply_motion_preview` と Blender scripts を same-pack に配置した。
  - AC-02:
    - 変更: repo-local public entry が old pack ではなく same-pack 実装を呼ぶようにした。
    - 根拠: `_wrapper_common.py` の implementation path を `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/` に反転した。
  - AC-03:
    - 変更: 旧 `comfy-blender-vrm` の CLI entry scripts を compatibility wrapper に置き換えた。
    - 根拠: `_compat_common.py` を追加し、旧 entry から canonical module `main()` を呼ぶ形にした。
  - AC-04:
    - 変更: skill docs / pipeline refs / canonical docs を canonical implementation と legacy compatibility layer の説明に更新した。
    - 根拠: `SKILL.md`、`pipeline.md`、`concept/spec/architecture` を同期した。
  - AC-05:
    - 変更: real ComfyUI で `kyarakuri-prepare-environment` と `kyarakuri-generate-base-image` を成功させた。
    - 根拠: `prepare_environment.py` が 9/9 PASS、`generate_base_image.py` が `20260314-014720-consolidation-base` を保存した。
  - AC-06:
    - 変更: fake Blender で `kyarakuri-build-vrm` と `kyarakuri-apply-motion-preview` を成功させた。
    - 根拠: fake blender config で `20260314-014914-consolidation-build` と `20260314-014914-consolidation-motion` を保存した。
  - AC-07:
    - 変更: 旧 `doctor` と `build-vrm-base` の compatibility wrapper を成功させた。
    - 根拠: `doctor.py` が old config で 9/9 PASS、`build_vrm_base.py` が `20260314-014915-legacy-consolidation-build` を保存した。
  - AC-08:
    - 変更: links-only validator が通る形に docs を同期した。
    - 根拠: `validate_delta_links.js` が `OK` を返した。
- non-goal kept:
  - Out of Scope への変更なし: Yes
- canonical sync:
  - mode: post-archive sync
  - action: verify PASS 後に skill docs / canonical docs を同期する
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
  - delta validator: links-only
- executed verify:
  - static check:
    - `py_compile` on canonical / public entry / compatibility wrapper scripts
  - targeted integration / E2E:
    - real ComfyUI:
      - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/prepare_environment.py`
      - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py --workflow .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-base.api.json --brief-file outputs/tmp/real-comfyui-brief.json --output-name consolidation-base --timeout-seconds 600`
      - output dir: `outputs/future-inspired-japanese-idol-mechanic/images/base/20260314-014720-consolidation-base/`
      - metadata: `outputs/future-inspired-japanese-idol-mechanic/logs/20260314-014720-consolidation-base.json`
      - post-run health check: `http://127.0.0.1:8000/system_stats` returned `200`
    - fake Blender:
      - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/build_vrm.py --blend-file outputs/tmp/consolidation/fake-input.blend --texture-image outputs/tmp/consolidation/fake-texture.png --config outputs/tmp/consolidation/kyarakuri-build-config.json --output-name consolidation-build`
      - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/apply_motion_preview.py --blend-file outputs/tmp/consolidation/fake-input.blend --motion-file outputs/tmp/consolidation/fake-motion.bvh --config outputs/tmp/consolidation/kyarakuri-motion-config.json --output-name consolidation-motion`
      - canonical blender script evidence:
        - `outputs/tmp/consolidation/kyarakuri-build-output/logs/20260314-014914-consolidation-build.json`
        - `outputs/tmp/consolidation/kyarakuri-motion-output/logs/20260314-014914-consolidation-motion.json`
    - legacy compatibility:
      - `python .codex/skills/comfy-blender-vrm/scripts/doctor.py`
      - `python .codex/skills/comfy-blender-vrm/scripts/build_vrm_base.py --blend-file outputs/tmp/consolidation/fake-input.blend --texture-image outputs/tmp/consolidation/fake-texture.png --config outputs/tmp/consolidation/legacy-build-config.json --output-name legacy-consolidation-build`
      - canonical blender script evidence:
        - `outputs/tmp/consolidation/legacy-build-output/logs/20260314-014915-legacy-consolidation-build.json`
  - delta validator:
    - `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- AC result table:
  - AC-01: PASS
    - 根拠: canonical implementation scripts / blender scripts が `kyarakuri-comfy-blender-vrm` 配下に存在する。
  - AC-02: PASS
    - 根拠: `_wrapper_common.py` が same-pack script dir を返し、real ComfyUI verify が `config/kyarakuri-comfy-blender-vrm.json` で成功した。
  - AC-03: PASS
    - 根拠: 旧 entry scripts は `_compat_common.py` を使う最小 wrapper に置き換わった。
  - AC-04: PASS
    - 根拠: skill docs / pipeline refs / `concept/spec/architecture` が canonical / legacy の役割を示す。
  - AC-05: PASS
    - 根拠: `kyarakuri-prepare-environment` が 9/9 PASS、`kyarakuri-generate-base-image` が real ComfyUI で画像と metadata を保存した。
  - AC-06: PASS
    - 根拠: `kyarakuri-build-vrm` と `kyarakuri-apply-motion-preview` が fake Blender で output と metadata を保存した。
  - AC-07: PASS
    - 根拠: legacy `doctor` が old config で 9/9 PASS、legacy `build-vrm-base` metadata の `blender_script` が canonical pack path を指した。
  - AC-08: PASS
    - 根拠: `validate_delta_links.js` が `OK: errors=0, warnings=0` で終了した。
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
  - 目的: `kyarakuri-comfy-blender-vrm` を canonical implementation skill pack に昇格し、旧 pack を compatibility layer に落とす
  - 変更対象: same-pack 実装化、legacy CLI wrapper 化、skill docs、canonical docs、targeted verify
  - 非対象: command rename、workflow / config key 変更、old pack 削除、提供用 skill への移動、Blender / motion output layout 変更
- unresolved items:
  - Q-01: 旧 `comfy-blender-vrm` の helper / blender script の物理削除は follow-up delta で扱う
- follow-up delta seeds:
  - `review delta`
  - `distributable-skill migration`
