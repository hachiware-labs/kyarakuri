# delta-request

## Delta ID
- DR-20260628-forma-background-executable-generation

## Delta Type
- ADD

## 目的
- `forma-background` skill で、kyarakuri / local ComfyUI を使って背景 base と weather variant を実生成できるようにする。
- ユーザー要望の「バックネットから見た野球場」と、その雨天 variation を repo 経由で生成する。

## 変更対象（In Scope）
- `.codex/skills/forma-background/scripts/generate_background.py` を追加する。
- `forma-background/SKILL.md` に実行例を追記する。
- 実 ComfyUI で baseball backstop base と rain variant を生成し、`outputs/<project>/backgrounds/<location>/` に保存する。
- `docs/OVERVIEW.md` と `docs/plan.md` に current state を最小反映する。
- delta 記録を `docs/delta/DR-20260628-forma-background-executable-generation.md` に残す。

## 非対象（Out of Scope）
- imagegen の使用。
- ComfyUI workflow UI JSON の作成。
- ControlNet / depth / canny による完全な構図固定。
- 生成済み画像の手動レタッチ。

## 受入条件（Acceptance Criteria）
- AC-01: `generate_background.py` が base と weather variant を ComfyUI API 経由で生成できる。
- AC-02: base と rain variant が `outputs/baseball-stadium/backgrounds/backnet-view/` 配下に保存される。
- AC-03: SKILL.md に script 実行例がある。
- AC-04: `py_compile` と skill validation が PASS する。

## Verify Profile
- static check: Required
- real ComfyUI smoke: Required
- skill validation: Required

## Review Gate
- required: No
- reason: repo-local skill の script 追加と実生成に閉じ、既存 public command の破壊を伴わない。

---

# delta-apply

## 実装
- `.codex/skills/forma-background/scripts/generate_background.py` を追加し、local ComfyUI API 経由で base text-to-image と base image からの img2img variant を実行できるようにした。
- `.codex/skills/forma-background/SKILL.md` に bundled script の base / variant 実行例を追加した。
- `outputs/baseball-stadium/backgrounds/backnet-view/base.png` を生成した。
- `outputs/baseball-stadium/backgrounds/backnet-view/variants/rain.png` を生成した。
- prompt JSON と run log を同じ project output tree に保存した。

## 実行内容
- base: `NetaYumev35_pretrained_all_in_one.safetensors` / seed `42028001` / 1024x768
- rain variant: base image img2img / seed `42028002` / denoise `0.28`

---

# delta-verify

## 結果
- PASS: AC-01 `generate_background.py` で base と weather variant を ComfyUI API 経由で生成できた。
- PASS: AC-02 base と rain variant が `outputs/baseball-stadium/backgrounds/backnet-view/` 配下に保存された。
- PASS: AC-03 `SKILL.md` に script 実行例を追加した。
- PASS: AC-04 `py_compile` と skill validation が PASS した。

## 実行した検証
- `uv run python -m py_compile .codex\skills\forma-background\scripts\generate_background.py`
- `$env:PYTHONUTF8='1'; uv run --with pyyaml python C:\Users\naruhide\.codex\skills\.system\skill-creator\scripts\quick_validate.py .codex\skills\forma-background`
- `git diff --check`
- `outputs\baseball-stadium\backgrounds\backnet-view\base.png` と `variants\rain.png` の存在確認

## 確認した出力
- `outputs/baseball-stadium/backgrounds/backnet-view/base.png`
- `outputs/baseball-stadium/backgrounds/backnet-view/base.prompt.json`
- `outputs/baseball-stadium/backgrounds/backnet-view/variants/rain.png`
- `outputs/baseball-stadium/backgrounds/backnet-view/variants/rain.prompt.json`
- `outputs/baseball-stadium/backgrounds/backnet-view/logs/`

## 既知の限界
- 現時点では ControlNet / depth / canny による厳密な構図固定は入れていないため、variant で細部の形状は多少変化する。
- baseball field のマウンドやダイヤモンド表現は生成モデル依存で、必要なら次 delta で構図固定 workflow を追加する。

---

# delta-archive

## Archive Status
- PASS

## Summary
- `forma-background` は kyarakuri repo-local skill として、local ComfyUI を使った背景 base 生成と、base image からの雨天 variant 生成を実行できる状態になった。
- `imagegen` は本 delta の生成経路に含めていない。
