# delta-request

## Delta ID
- DR-20260628-forma-background-art-direction-method

## Delta Type
- CHANGE

## 目的
- `forma-background` で、背景画像に定評のある「背景美術向け art direction prompt + 複数 seed candidate 生成 + approved base から variant 化」の手法を使えるようにする。
- 既存のバックネット野球場背景を、より背景素材らしい構図・光・奥行き・色設計で再生成する。

## 変更対象（In Scope）
- `.codex/skills/forma-background/scripts/generate_background.py` に quality preset と output name 指定を追加する。
- `.codex/skills/forma-background/SKILL.md` に背景美術向けの推奨手法を追記する。
- 実 ComfyUI で baseball backstop の quality candidate と rain variant を生成する。
- `docs/OVERVIEW.md` と `docs/plan.md` に current state を最小反映する。
- delta 記録を `docs/delta/DR-20260628-forma-background-art-direction-method.md` に残す。

## 非対象（Out of Scope）
- imagegen の使用。
- ComfyUI 本体や custom node の追加インストール。
- 背景専用 checkpoint / LoRA の導入。
- ControlNet / depth / canny による厳密な構図固定 workflow の追加。
- 生成済み画像の手動レタッチ。

## 受入条件（Acceptance Criteria）
- AC-01: `generate_background.py` で背景美術向け quality preset を指定できる。
- AC-02: base / variant の保存名を指定でき、候補画像を上書きせず残せる。
- AC-03: `SKILL.md` に定評ある背景生成手法として、art direction prompt、seed candidate、approved base から variant 化を記載する。
- AC-04: 実 ComfyUI で quality candidate と rain variant を生成する。
- AC-05: `py_compile` と skill validation が PASS する。

## Verify Profile
- static check: Required
- real ComfyUI smoke: Required
- skill validation: Required

## Review Gate
- required: No
- reason: repo-local skill の生成品質改善に閉じ、既存 command 互換を壊さない optional 引数追加である。

---

# delta-apply

## 実装
- `.codex/skills/forma-background/scripts/generate_background.py` に `--quality-preset` を追加した。
- `cinematic-anime-bg` と `visual-novel-bg` の背景美術向け prompt preset を追加した。
- `.codex/skills/forma-background/scripts/generate_background.py` に `--output-name` を追加し、base / variant の候補画像を上書きせず保存できるようにした。
- `.codex/skills/forma-background/SKILL.md` に、背景美術向けの art direction prompt、複数 seed candidate、approved base からの低 denoise variant 化を記載した。

## 実生成
- `base-cinematic-candidate-1.png`: seed `42028201`
- `base-cinematic-candidate-2.png`: seed `42028202`
- `base-cinematic-candidate-3.png`: seed `42028203`
- `rain-cinematic-candidate-2.png`: base `base-cinematic-candidate-2.png` / seed `42028212` / denoise `0.24`

---

# delta-verify

## 結果
- PASS: AC-01 `generate_background.py` で背景美術向け quality preset を指定できる。
- PASS: AC-02 base / variant の保存名を指定でき、候補画像を上書きせず残せる。
- PASS: AC-03 `SKILL.md` に定評ある背景生成手法として、art direction prompt、seed candidate、approved base から variant 化を記載した。
- PASS: AC-04 実 ComfyUI で quality candidate と rain variant を生成した。
- PASS: AC-05 `py_compile` と skill validation が PASS した。

## 実行した検証
- `uv run python -m py_compile .codex\skills\forma-background\scripts\generate_background.py`
- `$env:PYTHONUTF8='1'; uv run --with pyyaml python C:\Users\naruhide\.codex\skills\.system\skill-creator\scripts\quick_validate.py .codex\skills\forma-background`
- `git diff --check`
- 生成画像 4 ファイルの存在確認

## 確認した出力
- `outputs/baseball-stadium/backgrounds/backnet-view/base-cinematic-candidate-1.png`
- `outputs/baseball-stadium/backgrounds/backnet-view/base-cinematic-candidate-2.png`
- `outputs/baseball-stadium/backgrounds/backnet-view/base-cinematic-candidate-3.png`
- `outputs/baseball-stadium/backgrounds/backnet-view/variants/rain-cinematic-candidate-2.png`

## 既知の限界
- 背景専用 checkpoint / LoRA は導入していないため、現行モデルの背景表現力を超える改善はできない。
- ControlNet / depth / canny は未導入のため、variant の細部は完全固定ではない。
- 候補2は構図と奥行きがよいが、実野球場としての厳密なフィールド形状はまだモデル依存である。

---

# delta-archive

## Archive Status
- PASS

## Summary
- `forma-background` は、背景美術向け prompt preset と複数 seed candidate 生成を使って、より背景素材らしい base image を作れるようになった。
- approved base から低 denoise img2img で雨天 variant を作る手順を実生成で確認した。
