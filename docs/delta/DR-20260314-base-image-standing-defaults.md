# delta-request

## Delta ID
- DR-20260314-base-image-standing-defaults

## Delta Type
- FEATURE

## 目的
- `forma-character-generate-base-image` の既定 prompt を、背景なし・説明文字なし・立ち姿のベース画像向けに固定する。
- interactive brief と docs を同じ前提に揃え、ベース画像用途のずれを減らす。

## 変更対象（In Scope）
- `.codex/skills/forma-character/scripts/generate_character_from_brief.py` の base image prompt 合成既定を更新する。
- interactive brief 入力文言を standing / no-background base image 前提に寄せる。
- brief schema / skill docs / root README / canonical docs に新しい base image 既定を反映する。
- delta 記録を `docs/delta/DR-20260314-base-image-standing-defaults.md` に残す。

## 非対象（Out of Scope）
- `forma-character-generate-expressions` の prompt / workflow 挙動変更。
- bundled workflow JSON 自体の変更。
- CLI 引数や config schema の追加・削除。
- Blender / motion 系コマンドの仕様変更。
- 画像品質そのものを視覚評価で保証すること。

## Candidate Files/Artifacts
- `.codex/skills/forma-character/scripts/generate_character_from_brief.py`
- `.codex/skills/forma-character/references/character_brief.md`
- `.codex/skills/forma-character/SKILL.md`
- `README.md`
- `README_ja.md`
- `docs/concept.md`
- `docs/spec.md`
- `docs/architecture.md`
- `docs/OVERVIEW.md`
- `docs/plan.md`
- `docs/delta/DR-20260314-base-image-standing-defaults.md`

## 差分仕様
- DS-01:
  - Given: brief に pose や background を入れずに `forma-character-generate-base-image` を実行する。
  - When: base image 用 `character_prompt` を合成する。
  - Then: standing full-body、backgroundless、no text overlay を明示する既定 prompt が必ず入る。
- DS-02:
  - Given: `--brief-file` なしで interactive 実行する。
  - When: brief を聞く。
  - Then: background の自由入力は聞かず、pose は standing detail として聞く。
- DS-03:
  - Given: 既存 brief JSON が `background` を持つ。
  - When: brief を検証して base image prompt を合成する。
  - Then: brief 読込自体は後方互換で受け付けるが、base image prompt は backgroundless defaults を優先する。

## 受入条件（Acceptance Criteria）
- AC-01: `generate_character_from_brief.py` の synthesized prompt に standing full-body、backgroundless、no text overlay の base-image defaults が常に含まれる。
- AC-02: interactive input は background の自由入力を聞かず、pose を standing detail として案内する。
- AC-03: `background` field は brief schema 上は後方互換のため受け付け続けるが、docs に「base image prompt では使わない」ことが明記される。
- AC-04: 実 ComfyUI で `forma-character-generate-base-image` を transparent bundled workflow と brief-file で実行し、生成が成功し、保存された `prompt-preview.txt` から新しい defaults を確認できる。
- AC-05: `delta-project-validator` の `links-only` が PASS する。

## Verify Profile
- static check: Required
- targeted unit: Not Required
- targeted integration / E2E: Required
- delta-project-validator: links-only

## Canonical Sync Mode
- mode: post-archive sync
- reason: 実装と brief / skill / canonical docs の同期を verify PASS 後に閉じる。

## 制約
- `background` field は既存 brief-file 互換のため削除しない。
- 画像の見た目そのものではなく、skill が合成する prompt と実行成功を主証跡にする。
- 既存 workflow 選択はユーザー指定のままとし、今回は workflow JSON を直接編集しない。

## Review Gate
- required: No
- reason: base image brief/prompt と docs に閉じた差分であり、レイヤー追加や I/F 変更を伴わない。

## 未確定事項
- Q-01: 将来的に `background` field 自体を brief schema から外すかは別 delta で判断する。

## Step 2: delta-apply
- changed files:
  - `.codex/skills/forma-character/scripts/generate_character_from_brief.py`
  - `.codex/skills/forma-character/references/character_brief.md`
  - `.codex/skills/forma-character/SKILL.md`
  - `README.md`
  - `README_ja.md`
  - `docs/concept.md`
  - `docs/spec.md`
  - `docs/architecture.md`
  - `docs/OVERVIEW.md`
  - `docs/plan.md`
  - `docs/delta/DR-20260314-base-image-standing-defaults.md`
- applied AC:
  - AC-01:
    - 変更: base image prompt の固定 positive / negative defaults を追加し、standing full-body、backgroundless、no text overlay を常に含めるようにした。
    - 根拠: `BASE_IMAGE_PROMPT_PARTS` と `BASE_IMAGE_NEGATIVE_CONSTRAINTS` を追加し、`synthesize_character_prompt()` で常時マージする形にした。
  - AC-02:
    - 変更: interactive brief から background の自由入力を外し、pose prompt を standing detail に変更した。
    - 根拠: `collect_interactive_brief()` の質問列から `background` を外し、`Standing pose detail (optional):` を使うようにした。
  - AC-03:
    - 変更: `background` field は brief schema 上受け付けたまま、docs に「base image prompt では使わない」ことを明記した。
    - 根拠: `character_brief.md`、`spec.md`、`architecture.md`、README 群に後方互換と prompt 反映なしを追記した。
  - AC-04:
    - 変更: real ComfyUI verify を前提に、transparent bundled workflow を quick start / skill docs でも優先例として示した。
    - 根拠: `SKILL.md` と `README*.md` の base image 例を transparent workflow 優先に揃えた。
  - AC-05:
    - 変更: plan / overview / delta record を validator が通る状態に揃えた。
    - 根拠: `validate_delta_links.js` が `OK` を返した。
- non-goal kept:
  - Out of Scope への変更なし: Yes
- canonical sync:
  - mode: post-archive sync
  - action: verify PASS 後に skill / root / canonical docs を同期した
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
    - `python -m py_compile .codex/skills/forma-character/scripts/generate_character_from_brief.py`
  - targeted integration / E2E:
    - interactive run:
      - `python .codex/skills/forma-character/scripts/generate_base_image.py --workflow .codex/skills/forma-character/workflows/neta-yume-lumina-base-transparent.api.json --output-name standing-defaults-interactive --timeout-seconds 600`
      - stdin prompts did not include `Background (optional):`
      - stdout included `Standing pose detail (optional):`
      - project output: `outputs/standing-prompt-verify/`
      - prompt preview: `outputs/standing-prompt-verify/images/base/20260314-071750-standing-defaults-interactive/prompt-preview.txt`
    - brief-file run:
      - `python .codex/skills/forma-character/scripts/generate_base_image.py --workflow .codex/skills/forma-character/workflows/neta-yume-lumina-base-transparent.api.json --brief-file outputs/tmp/base-image-standing-defaults-brief.json --output-name standing-defaults-brief-file --timeout-seconds 600`
      - brief file contained `background = "abandoned school hallway with signs"`
      - project output: `outputs/background-ignore-verify/`
      - prompt preview: `outputs/background-ignore-verify/images/base/20260314-071920-standing-defaults-brief-file/prompt-preview.txt`
    - post-run health check:
      - `http://127.0.0.1:8000/system_stats` returned `200`
  - delta validator:
    - `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- AC result table:
  - AC-01: PASS
    - 根拠: 2 本の `prompt-preview.txt` ともに `full body standing character concept illustration`、`no background scene`、`no text, no caption, no watermark, no logo` を含む。
  - AC-02: PASS
    - 根拠: interactive run の stdout は `Standing pose detail (optional):` を表示し、`Background (optional):` を表示しなかった。
  - AC-03: PASS
    - 根拠: brief-file run の保存 brief には `background` が残り、合成 prompt には `background:` 行が入らず、docs に後方互換 / prompt 非反映が記載された。
  - AC-04: PASS
    - 根拠: real ComfyUI brief-file run が成功し、`outputs/background-ignore-verify/images/base/20260314-071920-standing-defaults-brief-file/prompt-preview.txt` で新 defaults を確認できた。
  - AC-05: PASS
    - 根拠: `validate_delta_links.js` が `OK: errors=0, warnings=0` で終了した。
- scope deviation:
  - Out of Scope 変更あり: No
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
    - skill: `.codex/skills/forma-character/SKILL.md`
    - root readme: `README.md`
    - root readme ja: `README_ja.md`
    - concept: `docs/concept.md`
    - spec: `docs/spec.md`
    - architecture: `docs/architecture.md`
    - overview: `docs/OVERVIEW.md`
    - plan: `docs/plan.md`
- closed scope:
  - 目的: base image prompt を背景なし・説明文字なし・立ち姿の前提へ固定する
  - 変更対象: `generate_character_from_brief.py`、brief docs、skill docs、root README、canonical docs、delta record
  - 非対象: expressions / workflow JSON / CLI I/F / Blender / motion 変更、画像品質の視覚保証
- unresolved items:
  - Q-01: `background` field 自体を brief schema から外すかは別 delta で判断する
- follow-up delta seeds:
  - `review delta`
  - `brief-schema cleanup`
