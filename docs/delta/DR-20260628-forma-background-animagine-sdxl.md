# delta-request

## Delta ID
- DR-20260628-forma-background-animagine-sdxl

## Delta Type
- CHANGE

## 目的
- `forma-background` で、custom node なしにダウンロード配置できる背景向け候補モデル `Animagine XL 4.0 Opt` を試せるようにする。
- 既存の NetaYume/AuraFlow workflow とは別に、ComfyUI 標準ノードだけの SDXL checkpoint workflow を追加する。

## 変更対象（In Scope）
- `.codex/skills/forma-background/scripts/generate_background.py` に `--model-name` と SDXL workflow preset を追加する。
- `Animagine XL 4.0 Opt` をローカル ComfyUI の checkpoints に配置する。
- `forma-background/SKILL.md` に Animagine XL 4.0 Opt の導入・実行例を追記する。
- 実 ComfyUI で baseball backstop background を Animagine XL 4.0 Opt で smoke 生成する。
- `docs/OVERVIEW.md` と `docs/plan.md` に current state を最小反映する。
- delta 記録を `docs/delta/DR-20260628-forma-background-animagine-sdxl.md` に残す。

## 非対象（Out of Scope）
- custom node の追加。
- 背景専用 LoRA / ControlNet / depth / canny の導入。
- Anima など checkpoint 以外の複数ファイル構成モデルの導入。
- ComfyUI 本体の再インストール。
- 生成済み画像の手動レタッチ。

## 受入条件（Acceptance Criteria）
- AC-01: `generate_background.py` で SDXL checkpoint workflow を選べる。
- AC-02: `--model-name animagine-xl-4.0-opt.safetensors` を指定できる。
- AC-03: `Animagine XL 4.0 Opt` が ComfyUI checkpoints で検出できる。
- AC-04: 実 ComfyUI で Animagine XL 4.0 Opt の背景 smoke 生成が成功する。
- AC-05: `py_compile` と skill validation が PASS する。

## Verify Profile
- static check: Required
- real ComfyUI smoke: Required
- skill validation: Required

## Review Gate
- required: No
- reason: optional model/workflow preset の追加であり、既存 NetaYume 既定動作を維持する。

---

# delta-apply

## 実装
- `.codex/skills/forma-background/scripts/generate_background.py` に `--workflow-preset` と `--model-name` を追加した。
- 既定の `neta-yume-aura` workflow に加え、ComfyUI 標準ノードだけの `sdxl-checkpoint` workflow を追加した。
- `animagine-xl-4.0-opt.safetensors` を `C:\Users\naruhide\Documents\ComfyUI\models\checkpoints\` に配置した。
- `.codex/skills/forma-background/SKILL.md` に Animagine XL 4.0 Opt の download / 実行例を追加した。

## 実生成
- `outputs/baseball-stadium/backgrounds/backnet-view/base-animagine-candidate-1.png`: seed `42028401`
- `outputs/baseball-stadium/backgrounds/backnet-view/base-animagine-candidate-2.png`: seed `42028402`

---

# delta-verify

## 結果
- PASS: AC-01 `generate_background.py` で SDXL checkpoint workflow を選べる。
- PASS: AC-02 `--model-name animagine-xl-4.0-opt.safetensors` を指定できる。
- PASS: AC-03 `Animagine XL 4.0 Opt` が ComfyUI checkpoints で検出できる。
- PASS: AC-04 実 ComfyUI で Animagine XL 4.0 Opt の背景 smoke 生成が成功した。
- PASS: AC-05 `py_compile` と skill validation が PASS した。

## 実行した検証
- `uv run python -m py_compile .codex\skills\forma-background\scripts\generate_background.py`
- `$env:PYTHONUTF8='1'; uv run --with pyyaml python C:\Users\naruhide\.codex\skills\.system\skill-creator\scripts\quick_validate.py .codex\skills\forma-background`
- ComfyUI `/object_info` で `animagine-xl-4.0-opt.safetensors` の検出を確認
- 実 ComfyUI で `sdxl-checkpoint` workflow の画像生成を確認

## 判断
- Animagine XL 4.0 Opt は導入・実行できたが、今回の用途である「センスのよい背景 base」を安定して作る主経路としては採用しない。
- 背景 base は `imagegen` を主経路にし、`forma-background` は brief / output 管理と、同一構図の time/weather variant 手順を担う方針へ切り替える。

---

# delta-archive

## Archive Status
- PASS

## Summary
- SDXL checkpoint workflow と Animagine XL 4.0 Opt の local smoke は完了した。
- 次 delta では、ComfyUI model 探索ではなく `imagegen` 主体の固定構図背景作成スキルへ整理する。
