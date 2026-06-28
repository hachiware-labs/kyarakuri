# delta-request

## Delta ID
- DR-20260628-readme-usage-and-model-setup

## Delta Type
- DOCS

## 目的
- `README.md` / `README_ja.md` に、Forma Character / Forma Background / Background Transparent の使い方を整理して記載する。
- 全体説明の後、末尾に ComfyUI 側へ追加で必要な custom model / custom node の詳細手順を記載する。

## 変更対象（In Scope）
- `README.md` を更新する。
- `README_ja.md` を更新する。
- `docs/OVERVIEW.md` と `docs/plan.md` に current state を最小反映する。
- delta 記録を `docs/delta/DR-20260628-readme-usage-and-model-setup.md` に残す。

## 非対象（Out of Scope）
- script / skill 実装の変更。
- ComfyUI や Blender の自動インストール。
- custom model の download URL 正本化。
- 生成画像の作成。

## 受入条件（Acceptance Criteria）
- AC-01: README 英語版に、キャラクター、背景、背景透明化の基本利用手順がある。
- AC-02: README 日本語版に、同等の基本利用手順がある。
- AC-03: README 末尾に、ComfyUI 追加 model / custom node の詳細手順がある。
- AC-04: 背景作成は `imagegen` 主経路で、ComfyUI を使わないことが明記されている。
- AC-05: character workflow の必須 checkpoint `NetaYumev35_pretrained_all_in_one.safetensors` が明記されている。

## Verify Profile
- static check: Required
- docs consistency: Required

## Review Gate
- required: No
- reason: README の利用手順拡充に閉じ、実装・仕様挙動を変更しない。

---

# delta-apply

## 実装
- `README.md` に Forma Character / Forma Background / Background Transparent の用途、quick start、出力レイアウトを追加した。
- `README_ja.md` に同等の日本語手順を追加した。
- 両 README の末尾に、ComfyUI 側で必要な `NetaYumev35_pretrained_all_in_one.safetensors` の配置手順を追加した。
- 両 README の末尾に、透明化向け optional setup として `ComfyUI-RMBG` / `BiRefNet-portrait` / `RMBG-2.0` の手順を追加した。
- 背景作成は `imagegen` 主経路であり、ComfyUI 追加背景 checkpoint は不要であることを明記した。

---

# delta-verify

## 結果
- PASS: AC-01 README 英語版に、キャラクター、背景、背景透明化の基本利用手順がある。
- PASS: AC-02 README 日本語版に、同等の基本利用手順がある。
- PASS: AC-03 README 末尾に、ComfyUI 追加 model / custom node の詳細手順がある。
- PASS: AC-04 背景作成は `imagegen` 主経路で、ComfyUI を使わないことが明記されている。
- PASS: AC-05 character workflow の必須 checkpoint `NetaYumev35_pretrained_all_in_one.safetensors` が明記されている。

## 実行した検証
- `rg -n "NetaYumev35|ComfyUI-RMBG|BiRefNet-portrait|RMBG-2.0|Do not use ComfyUI|背景生成は意図的に ComfyUI を使いません|imagegen|forma-background|forma-character" README.md README_ja.md`
- `git diff --check`

---

# delta-archive

## Archive Status
- PASS

## Summary
- README 日英に、repo 全体の使い方と、末尾の ComfyUI 追加 model / custom node setup 手順を追加した。
