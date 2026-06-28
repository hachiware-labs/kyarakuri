# delta-request

## Delta ID
- DR-20260628-forma-background-weather-variants

## Delta Type
- IMPROVE

## 目的
- `forma-background` skill で、時間帯だけでなく雨・雪・霧などの天候差分も固定構図 variation として扱うことを明確化する。

## 変更対象（In Scope）
- `.codex/skills/forma-background/SKILL.md` の description / brief / variation / preset を weather variants 対応へ更新する。
- `.codex/skills/forma-background/agents/openai.yaml` の短い説明と default prompt を weather variants に合わせる。
- `docs/OVERVIEW.md` と `docs/plan.md` に current state を最小反映する。
- delta 記録を `docs/delta/DR-20260628-forma-background-weather-variants.md` に残す。

## 非対象（Out of Scope）
- 実 ComfyUI workflow JSON の追加。
- 背景画像の実生成。
- 既存 skill のリネームや統合。
- 天候エフェクト専用 script の追加。

## 受入条件（Acceptance Criteria）
- AC-01: `forma-background/SKILL.md` が rain / snow / fog / storm などの weather variation を明示している。
- AC-02: weather variation でも camera / layout / object positions を固定するルールが明記されている。
- AC-03: agents metadata が weather variation を反映している。
- AC-04: skill validation が PASS する。

## Verify Profile
- skill validation: `skill-creator/scripts/quick_validate.py`

## Review Gate
- required: No
- reason: 既存 repo-local skill の説明拡張に閉じ、破壊的変更を伴わない。

---

## Step 2: delta apply
- `forma-background/SKILL.md` の description を time / weather / lighting variants 対応へ更新した。
- `weather_variants` brief field を追加し、rain / heavy-rain / after-rain / snow / heavy-snow / fog / storm / snowy-night の preset を追加した。
- weather variation でも camera / layout / object positions / scene identity を固定し、天候エフェクトで主要形状を隠しすぎない negative 制約を追加した。
- `agents/openai.yaml` の short description と default prompt を weather variants 対応へ更新した。

## Step 3: delta verify
- PASS: `$env:PYTHONUTF8='1'; uv run --with pyyaml python C:\Users\naruhide\.codex\skills\.system\skill-creator\scripts\quick_validate.py .codex\skills\forma-background`
- PASS: `SKILL.md` に雨・雪・霧・嵐などの weather variation が明記されている。
- PASS: weather variation でも構図固定ルールが維持されている。

## Step 4: delta archive
- status: PASS
- archived_at: 2026-06-28
- sync:
  - `docs/OVERVIEW.md` の Active Delta をなしに戻し、直近完了を本 delta に更新した。
  - `docs/plan.md` の current checkbox と archive summary を更新した。
