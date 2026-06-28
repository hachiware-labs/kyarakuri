# delta-request

## Delta ID
- DR-20260628-forma-background-no-comfyui

## Delta Type
- CHANGE

## 目的
- 背景画像作成では ComfyUI を使わず、`imagegen` による base 生成と fixed-composition edit variants を正規方針として確定する。
- `forma-background` skill から背景用 ComfyUI fallback script / 手順を外し、運用上の迷いをなくす。

## 変更対象（In Scope）
- `.codex/skills/forma-background/SKILL.md` から ComfyUI fallback 記述を削除し、`imagegen` only 方針を明記する。
- `.codex/skills/forma-background/scripts/generate_background.py` を削除する。
- `docs/OVERVIEW.md` と `docs/plan.md` に current state を最小反映する。
- delta 記録を `docs/delta/DR-20260628-forma-background-no-comfyui.md` に残す。

## 非対象（Out of Scope）
- 既存の実験ログ delta の削除。
- ローカル ComfyUI に配置済みモデルファイルの削除。
- `background-transparent` など他 skill の ComfyUI 利用方針変更。
- 新規背景画像の生成。

## 受入条件（Acceptance Criteria）
- AC-01: `forma-background/SKILL.md` が背景作成で ComfyUI を使わない方針を明示する。
- AC-02: `forma-background` の repo-local skill から背景生成用 ComfyUI script が削除される。
- AC-03: `SKILL.md` は base を `imagegen` generate、variants を `imagegen` edit として説明する。
- AC-04: skill validation が PASS する。

## Verify Profile
- static check: Required
- skill validation: Required
- real image generation: Not Required

## Review Gate
- required: No
- reason: 背景 skill の運用方針確定と不要 script 削除に閉じ、他 skill の public command を変更しない。

---

# delta-apply

## 実装
- `.codex/skills/forma-background/SKILL.md` から ComfyUI fallback 手順を削除し、base は `imagegen`、variant は `imagegen` edit として説明する形に統一した。
- `.codex/skills/forma-background/scripts/generate_background.py` を削除した。
- 生成済み `__pycache__` を削除した。
- `docs/OVERVIEW.md` と `docs/plan.md` に、背景作成では ComfyUI を使わない方針を反映した。

---

# delta-verify

## 結果
- PASS: AC-01 `forma-background/SKILL.md` が背景作成で ComfyUI を使わない方針を明示する。
- PASS: AC-02 `forma-background` の repo-local skill から背景生成用 ComfyUI script が削除された。
- PASS: AC-03 `SKILL.md` は base を `imagegen` generate、variants を `imagegen` edit として説明する。
- PASS: AC-04 skill validation が PASS した。

## 実行した検証
- `$env:PYTHONUTF8='1'; uv run --with pyyaml python C:\Users\naruhide\.codex\skills\.system\skill-creator\scripts\quick_validate.py .codex\skills\forma-background`
- `git diff --check`
- `rg -n "ComfyUI|generate_background|Local ComfyUI|fallback|imagegen" .codex\skills\forma-background docs\OVERVIEW.md docs\plan.md docs\delta\DR-20260628-forma-background-no-comfyui.md`

---

# delta-archive

## Archive Status
- PASS

## Summary
- 背景画像作成では ComfyUI を使わず、`imagegen` による base 生成と fixed-composition edit variants を正規方針として確定した。
- `forma-background` repo-local skill から背景用 ComfyUI 実行 script を削除した。
