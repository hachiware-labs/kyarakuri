# delta-request

## Delta ID
- DR-20260314-transparent-background-workflows

## Delta Type
- FEATURE

## 目的
- `generate-base-image` と `generate-expressions` で使える、透過 PNG 出力向けの bundled workflow を repo 内に追加する。
- 実装は local-only 前提とし、ComfyUI 標準ノードだけで alpha 付き PNG を保存できる状態を作る。

## 変更対象（In Scope）
- internal / repo-local の workflow dir に transparent background 向け bundled workflow を追加する。
- transparent workflow が local-only で動くよう、cloud API node ではなく ComfyUI 標準ノードだけを使う。
- skill docs / workflow docs / canonical docs に transparent workflow の使い方と制約を同期する。
- 実 ComfyUI で base / expressions の transparent workflow を実行し、alpha 付き PNG が保存されることを確認する。
- delta 記録を `docs/delta/DR-20260314-transparent-background-workflows.md` に残す。

## 非対象（Out of Scope）
- ComfyUI 本体や `AppData` / `Documents/ComfyUI` 配下ファイルの編集。
- `generate_base_image.py` / `generate_expressions.py` の CLI I/F 変更。
- Bria / Recraft などの cloud API node を使う workflow 追加。
- Blender review / preview render の透過対応。
- 高精度セグメンテーション導入や custom node インストール。

## Candidate Files/Artifacts
- docs/delta/DR-20260314-transparent-background-workflows.md
- docs/OVERVIEW.md
- docs/plan.md
- docs/concept.md
- docs/spec.md
- docs/architecture.md
- .codex/skills/comfy-blender-vrm/SKILL.md
- .codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md
- .codex/skills/comfy-blender-vrm/workflows/README.md
- .codex/skills/kyarakuri-comfy-blender-vrm/workflows/README.md
- .codex/skills/comfy-blender-vrm/workflows/neta-yume-lumina-base-transparent.api.json
- .codex/skills/comfy-blender-vrm/workflows/neta-yume-lumina-expressions-transparent.api.json
- .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-base-transparent.api.json
- .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-expressions-transparent.api.json

## 差分仕様
- DS-01:
  - Given: base image を transparent PNG で保存したい。
  - When: transparent background 用 bundled base workflow を `generate-base-image` に渡して実行する。
  - Then: workflow は ComfyUI 標準ノードだけで alpha 付き `IMAGE` を作り、`SaveImage` で PNG 保存する。
- DS-02:
  - Given: expression image を transparent PNG で保存したい。
  - When: transparent background 用 bundled expression workflow を `generate-expressions` に渡して実行する。
  - Then: workflow は ComfyUI 標準ノードだけで alpha 付き `IMAGE` を作り、`SaveImage` で PNG 保存する。
- DS-03:
  - Given: transparent workflow の前提条件を知りたい。
  - When: docs を確認する。
  - Then: local-only / standard nodes only / white background keying の best-effort 制約が明記されている。

## 受入条件（Acceptance Criteria）
- AC-01: `neta-yume-lumina-base-transparent.api.json` が internal / repo-local の両 workflow dir に追加されている。
- AC-02: `neta-yume-lumina-expressions-transparent.api.json` が internal / repo-local の両 workflow dir に追加されている。
- AC-03: transparent workflow は cloud API node を使わず、ComfyUI 標準ノードだけで alpha 付き `IMAGE` を `SaveImage` に渡す。
- AC-04: docs / workflow README / skill docs が transparent workflow の導線と制約を示している。
- AC-05: 実 ComfyUI で `kyarakuri-generate-base-image` を transparent workflow で実行し、保存 PNG が alpha channel を持ち、少なくとも一部 pixel が透明になる。
- AC-06: 実 ComfyUI で `kyarakuri-generate-expressions` を transparent workflow で実行し、保存 PNG が alpha channel を持ち、少なくとも一部 pixel が透明になる。
- AC-07: `delta-project-validator` の `links-only` が PASS する。

## Verify Profile
- static check: Not Required
- targeted unit: Not Required
- targeted integration / E2E: Required
- delta-project-validator: links-only

## Canonical Sync Mode
- mode: post-archive sync
- reason: workflow 追加と docs 同期を verify PASS 後に正本へ最小反映する。

## 制約
- transparent 化は local-only / standard nodes only の範囲に閉じる。
- mask は white background keying の best-effort とし、今回は custom node を追加しない。
- 既存 opaque workflow は残し、transparent workflow は別名で追加する。

## Review Gate
- required: No
- reason: workflow 追加と docs 同期に閉じた差分であり、レイヤー追加や I/F 変更は伴わない。

## 未確定事項
- Q-01: white background keying だけで edge quality が十分かは real ComfyUI verify の結果で判断する。

## Step 2: delta-apply
- changed files:
  - `.codex/skills/comfy-blender-vrm/workflows/neta-yume-lumina-base-transparent.api.json`
  - `.codex/skills/comfy-blender-vrm/workflows/neta-yume-lumina-expressions-transparent.api.json`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-base-transparent.api.json`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-expressions-transparent.api.json`
  - `.codex/skills/comfy-blender-vrm/workflows/README.md`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/workflows/README.md`
  - `.codex/skills/comfy-blender-vrm/SKILL.md`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md`
  - `docs/concept.md`
  - `docs/spec.md`
  - `docs/architecture.md`
  - `docs/OVERVIEW.md`
  - `docs/plan.md`
  - `docs/delta/DR-20260314-transparent-background-workflows.md`
- applied AC:
  - AC-01:
    - 変更: internal / repo-local の両 workflow dir に transparent base workflow を追加した。
    - 根拠: `neta-yume-lumina-base-transparent.api.json` を 2 か所に追加した。
  - AC-02:
    - 変更: internal / repo-local の両 workflow dir に transparent expression workflow を追加した。
    - 根拠: `neta-yume-lumina-expressions-transparent.api.json` を 2 か所に追加した。
  - AC-03:
    - 変更: transparent workflow は `ImageColorToMask`、`InvertMask`、`GrowMask`、`FeatherMask`、`JoinImageWithAlpha`、`SaveImage` だけで alpha 付き PNG を作る構成にした。
    - 根拠: workflow JSON に cloud API node は含めず、ComfyUI 標準ノードだけを追加した。
  - AC-04:
    - 変更: workflow README、skill docs、canonical docs に transparent workflow の導線と制約を追加した。
    - 根拠: `README.md`、`SKILL.md`、`concept/spec/architecture` に transparent workflow と best-effort 制約を追記した。
  - AC-05:
    - 変更: real ComfyUI verify 用の transparent base workflow を repo-local から実行した。
    - 根拠: `kyarakuri-generate-base-image` が `20260314-011818-character-from-brief` として成功した。
  - AC-06:
    - 変更: real ComfyUI verify 用の transparent expression workflow を repo-local から実行した。
    - 根拠: `kyarakuri-generate-expressions` が `20260314-011949-expression-sheet` として成功した。
  - AC-07:
    - 変更: docs link 整合が通る形に delta / overview / plan を同期した。
    - 根拠: `validate_delta_links.js` が `OK` を返した。
- non-goal kept:
  - Out of Scope への変更なし: Yes
- canonical sync:
  - mode: post-archive sync
  - action: verify PASS 後に正本 docs と skill docs を同期した
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
  - static check: Not Required
  - targeted unit: Not Required
  - targeted integration / E2E: Required
  - delta validator: links-only
- executed verify:
  - targeted integration / E2E:
    - base image:
      - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py --workflow .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-base-transparent.api.json --brief-file outputs/tmp/transparent-brief.json --timeout-seconds 600`
      - output dir: `outputs/future-inspired-japanese-idol-mechanic-transparent-test/images/base/20260314-011818-character-from-brief/`
      - image: `outputs/future-inspired-japanese-idol-mechanic-transparent-test/images/base/20260314-011818-character-from-brief/images/001_9_20260314-011818-character-from-brief_00001_.png`
      - alpha check: `mode=RGBA`, `alpha_extrema=(0,255)`, `transparent_pixels=296264`
    - expressions:
      - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expressions.py --workflow .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-expressions-transparent.api.json --base-image outputs/future-inspired-japanese-idol-mechanic-transparent-test/images/base/20260314-011818-character-from-brief/images/001_9_20260314-011818-character-from-brief_00001_.png --character-prompt "<saved prompt>" --expressions neutral,smile --timeout-seconds 600`
      - output dir: `outputs/future-inspired-japanese-idol-mechanic-transparent-test/images/expressions/20260314-011949-expression-sheet/`
      - `neutral` alpha check: `mode=RGBA`, `alpha_extrema=(0,255)`, `transparent_pixels=490614`
      - `smile` alpha check: `mode=RGBA`, `alpha_extrema=(0,255)`, `transparent_pixels=396864`
    - post-run health check: `http://127.0.0.1:8000/system_stats` returned `200`
  - workflow copy integrity:
    - base transparent workflow SHA-256:
      - internal / repo-local ともに `395faa5d80b0e52d84e0809ab770af8aa500ed102370cec2c697e8fce1e16bb3`
    - expression transparent workflow SHA-256:
      - internal / repo-local ともに `8ddf619258918d43ed66fe295f45baf617f9c9cb5046dd061e6991192ef3f20b`
  - delta validator:
    - `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- AC result table:
  - AC-01: PASS
    - 根拠: transparent base workflow が internal / repo-local の両 dir に追加された。
  - AC-02: PASS
    - 根拠: transparent expression workflow が internal / repo-local の両 dir に追加された。
  - AC-03: PASS
    - 根拠: workflow JSON は cloud API node を含まず、ComfyUI 標準ノードで alpha 付き `IMAGE` を `SaveImage` に渡す。
  - AC-04: PASS
    - 根拠: workflow README、skill docs、canonical docs が transparent workflow の導線と制約を示す。
  - AC-05: PASS
    - 根拠: base image verify で `RGBA` PNG が保存され、一部 pixel が透明だった。
  - AC-06: PASS
    - 根拠: expression verify で `neutral` / `smile` ともに `RGBA` PNG が保存され、一部 pixel が透明だった。
  - AC-07: PASS
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
  - 目的: base / expressions 向け transparent background bundled workflow を repo 内へ追加する
  - 変更対象: transparent workflow JSON、skill docs、workflow docs、canonical docs
  - 非対象: ComfyUI 本体編集、CLI I/F 変更、cloud API node、Blender render 透過化、custom node 導入
- unresolved items:
  - Q-01: white background keying の edge quality をさらに上げるかは follow-up delta で判断する
- follow-up delta seeds:
  - `DR-20260313-real-comfyui-smoke-verify`
  - `transparent-background-quality-improvement`
