# delta-request

## Delta ID
- DR-20260628-forma-background-imagegen-fixed-variants

## Delta Type
- CHANGE

## 目的
- `forma-background` を、背景 base 生成は `imagegen` に任せ、同じ構図を保ったまま光・時間・天気だけを変える背景作成スキルとして整理する。
- ComfyUI は主経路ではなく、ローカル実験・fallback として扱う。

## 変更対象（In Scope）
- `.codex/skills/forma-background/SKILL.md` の workflow を `imagegen` 主経路に更新する。
- base image と variant image の作成ルールに「構図・カメラ・画角・オブジェクト位置を変えない」を明記する。
- ComfyUI / Animagine / local script は fallback / experimental として位置付け直す。
- `docs/OVERVIEW.md` と `docs/plan.md` に current state を最小反映する。
- delta 記録を `docs/delta/DR-20260628-forma-background-imagegen-fixed-variants.md` に残す。

## 非対象（Out of Scope）
- 実際の新規背景画像生成。
- imagegen の wrapper script 実装。
- ComfyUI script の削除。
- Animagine モデルファイルの削除。
- ControlNet / depth / canny の導入。

## 受入条件（Acceptance Criteria）
- AC-01: `SKILL.md` が base background の主経路を `imagegen` として説明する。
- AC-02: `SKILL.md` が variants を base image からの fixed-composition edit として説明する。
- AC-03: `SKILL.md` が変えてよい要素と変えてはいけない要素を明確に分ける。
- AC-04: ComfyUI script は fallback / experimental として整理され、主経路として推奨されない。
- AC-05: skill validation が PASS する。

## Verify Profile
- static check: Required
- skill validation: Required
- real image generation: Not Required

## Review Gate
- required: No
- reason: repo-local skill の運用説明変更であり、既存 script の破壊を伴わない。

---

# delta-apply

## 実装
- `.codex/skills/forma-background/SKILL.md` の description と workflow を、`imagegen` base 生成を主経路にする形へ更新した。
- variants は approved `base.png` を入力画像にした `imagegen` edit として作成し、text-only regeneration を禁止する方針を明記した。
- `Allowed changes` と `Forbidden changes` を分け、変えてよいのは time/weather/light/surface condition に限定した。
- local ComfyUI script は `Local ComfyUI Fallback` として残し、high-quality base background art の推奨経路ではないと明記した。

---

# delta-verify

## 結果
- PASS: AC-01 `SKILL.md` が base background の主経路を `imagegen` として説明する。
- PASS: AC-02 `SKILL.md` が variants を base image からの fixed-composition edit として説明する。
- PASS: AC-03 `SKILL.md` が変えてよい要素と変えてはいけない要素を明確に分ける。
- PASS: AC-04 ComfyUI script は fallback / experimental として整理され、主経路として推奨されない。
- PASS: AC-05 skill validation が PASS した。

## 実行した検証
- `$env:PYTHONUTF8='1'; uv run --with pyyaml python C:\Users\naruhide\.codex\skills\.system\skill-creator\scripts\quick_validate.py .codex\skills\forma-background`
- `uv run python -m py_compile .codex\skills\forma-background\scripts\generate_background.py`
- `git diff --check`

---

# delta-archive

## Archive Status
- PASS

## Summary
- `forma-background` は、背景 base を `imagegen` で作り、同じ構図を保ったまま光・時間・天気だけを変える fixed-composition variant 作成スキルとして整理された。
- ComfyUI は local-only / fallback / smoke verify 用に残すが、主経路ではない。
