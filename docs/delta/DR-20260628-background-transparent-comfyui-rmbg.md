# delta-request

## Delta ID
- DR-20260628-background-transparent-comfyui-rmbg

## Delta Type
- IMPROVE

## 目的
- `background-transparent` skill に ComfyUI-RMBG 経路を追加し、人物画像や白い服を含む画像では Pillow keying より高品質な背景除去を優先できるようにする。

## 変更対象（In Scope）
- `.codex/skills/background-transparent/scripts/comfyui_rmbg.py` を追加し、ComfyUI API 経由で `AILab_LoadImage -> RMBG/BiRefNetRMBG -> SaveImage` を実行して任意の `--out` へ PNG を保存できるようにする。
- `.codex/skills/background-transparent/scripts/verify_comfyui_rmbg.py` を追加し、workflow payload の構築と model/engine 選択をネットワークなしで検証する。
- `.codex/skills/background-transparent/SKILL.md` に ComfyUI-RMBG 優先、Pillow fallback の運用を追記する。
- 実 ComfyUI の `RMBG` node が使えることを smoke verify する。
- `docs/OVERVIEW.md` と `docs/plan.md` に current state を最小反映する。
- delta 記録を `docs/delta/DR-20260628-background-transparent-comfyui-rmbg.md` に残す。

## 非対象（Out of Scope）
- ComfyUI-RMBG custom node の repo 管理。
- hidamari の React コード変更。
- 元画像や既存 transparent 出力の上書き。
- SAM / GroundingDINO / YOLO など追加の segmentation workflow 化。
- ComfyUI が未起動の状態での semantic background removal 保証。

## Candidate Files/Artifacts
- `.codex/skills/background-transparent/SKILL.md`
- `.codex/skills/background-transparent/scripts/comfyui_rmbg.py`
- `.codex/skills/background-transparent/scripts/verify_comfyui_rmbg.py`
- `docs/OVERVIEW.md`
- `docs/plan.md`
- `docs/delta/DR-20260628-background-transparent-comfyui-rmbg.md`

## 差分仕様
- DS-01:
  - Given: ComfyUI が起動し、`RMBG` node が `object_info` に登録されている。
  - When: `comfyui_rmbg.py <input> --model RMBG-2.0 --out <output>` を実行する。
  - Then: ComfyUI API 経由で RGBA PNG が `--out` に保存される。
- DS-02:
  - Given: `--model BiRefNet-portrait` が指定される。
  - When: workflow payload を作る。
  - Then: `BiRefNetRMBG` node を使う。
- DS-03:
  - Given: ComfyUI-RMBG が使えない。
  - When: 背景透明化を行う。
  - Then: `SKILL.md` は Pillow script fallback を案内する。

## 受入条件（Acceptance Criteria）
- AC-01: `comfyui_rmbg.py` は stdlib + optional Pillow で ComfyUI workflow を queue し、`/view` 経由で出力 PNG を任意パスに保存できる。
- AC-02: `RMBG-2.0` と `BiRefNet-*` の engine 選択を検証でき、人物向け既定は `BiRefNet-portrait` とする。
- AC-03: `SKILL.md` に ComfyUI-RMBG 優先 / Pillow fallback の使い分けが明記される。
- AC-04: 実 ComfyUI で `RMBG-2.0` smoke が PASS する。
- AC-05: `py_compile`、script verify、skill validation が PASS する。

## Verify Profile
- static check: Required
- targeted unit/smoke: Required
- real ComfyUI smoke: Required
- skill validation: `skill-creator/scripts/quick_validate.py`

## Canonical Sync Mode
- mode: post-archive sync
- reason: script と skill docs を verify PASS 後に閉じる。

## 制約
- 元画像は上書きしない。
- ComfyUI-RMBG の install / requirements は skill 外の環境前提として扱う。
- Pillow fallback 経路は残す。

## Review Gate
- required: No
- reason: repo-local skill の追加 script と docs 更新に閉じ、既存 public command の破壊を伴わない。

---

## Step 2: delta apply
- `comfyui_rmbg.py` を追加し、ComfyUI API の `object_info` / `prompt` / `history` / `view` を使って、ComfyUI-RMBG の出力 PNG を任意の `--out` に保存できるようにした。
- `comfyui_rmbg.py` は `BiRefNet-*` model では `BiRefNetRMBG`、`RMBG-2.0` / `INSPYRENET` / `BEN` / `BEN2` では `RMBG` を使う。
- 人物・キャラクター向けの既定 model を `BiRefNet-portrait` にした。
- `verify_comfyui_rmbg.py` を追加し、workflow payload と engine 選択を offline で検証できるようにした。
- `SKILL.md` に ComfyUI-RMBG 優先 / Pillow fallback の使い分けと推奨 model を追記した。
- hidamari 管理人さん画像 4 枚を `transparent-rmbg` に `BiRefNet-portrait` で非破壊出力した。

## Step 3: delta verify
- PASS: `uv run --with pillow python -m py_compile .codex\skills\background-transparent\scripts\comfyui_rmbg.py .codex\skills\background-transparent\scripts\verify_comfyui_rmbg.py .codex\skills\background-transparent\scripts\remove_background.py .codex\skills\background-transparent\scripts\verify_remove_background.py`
- PASS: `uv run --with pillow python .codex\skills\background-transparent\scripts\verify_comfyui_rmbg.py`
- PASS: `uv run --with pillow python .codex\skills\background-transparent\scripts\verify_remove_background.py`
- PASS: `$env:PYTHONUTF8='1'; uv run --with pyyaml python C:\Users\naruhide\.codex\skills\.system\skill-creator\scripts\quick_validate.py .codex\skills\background-transparent`
- PASS: 実 ComfyUI `RMBG-2.0` smoke で API 実行と RGBA PNG 保存を確認した。
- PASS: 実 ComfyUI `BiRefNet-portrait` で hidamari 管理人さん画像 4 枚の `transparent-rmbg` 出力を確認した。
- NOTE: `RMBG-2.0` は neutral 画像で瞳の一部が抜けたため、人物向け既定は `BiRefNet-portrait` とした。

## Step 4: delta archive
- status: PASS
- archived_at: 2026-06-28
- sync:
  - `docs/OVERVIEW.md` の Active Delta をなしに戻し、直近完了を本 delta に更新した。
  - `docs/plan.md` の current checkbox と archive summary を更新した。
