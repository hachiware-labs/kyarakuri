# delta-request

## Delta ID
- DR-20260315-forma-skill-frontmatter

## Delta Type
- REPAIR

## 目的
- `forma-character` の `SKILL.md` に YAML frontmatter を追加し、skill loader が invalid 扱いしない状態へ戻す。

## 変更対象（In Scope）
- `.codex/skills/forma-character/SKILL.md` の先頭に loader 互換の YAML frontmatter を追加する。
- delta 記録を `docs/delta/DR-20260315-forma-skill-frontmatter.md` に残す。
- `docs/OVERVIEW.md` と `docs/plan.md` に current state を最小反映する。

## 非対象（Out of Scope）
- skill 本文のコマンド仕様変更。
- 他 skill pack の構文修正。
- spec / concept / architecture の仕様変更。
- 実装コードや workflow の変更。

## Candidate Files/Artifacts
- `.codex/skills/forma-character/SKILL.md`
- `docs/OVERVIEW.md`
- `docs/plan.md`
- `docs/delta/DR-20260315-forma-skill-frontmatter.md`

## 差分仕様
- DS-01:
  - Given: skill loader が `.codex/skills/forma-character/SKILL.md` を読む。
  - When: ファイル先頭を確認する。
  - Then: `---` で囲まれた YAML frontmatter があり、`name` と `description` を持つ。
- DS-02:
  - Given: frontmatter 追加後の `SKILL.md` を開く。
  - When: 本文を読む。
  - Then: 既存の usage / references / defaults の本文内容は維持される。

## 受入条件（Acceptance Criteria）
- AC-01: `.codex/skills/forma-character/SKILL.md` が YAML frontmatter で始まる。
- AC-02: frontmatter は `name` と `description` を持つ。
- AC-03: 本文の既存 scope / usage / reference セクションは残る。
- AC-04: `delta-project-validator` の `links-only` が PASS する。

## Verify Profile
- static check: Required
- targeted unit: Not Required
- targeted integration / E2E: Not Required
- delta-project-validator: links-only

## Canonical Sync Mode
- mode: post-archive sync
- reason: repo state 反映は verify PASS 後に閉じる。

## 制約
- 修正は `forma-character/SKILL.md` に限定し、loader 警告の原因だけを直す。
- frontmatter は ASCII ベースで書く。

## Review Gate
- required: No
- reason: loader 互換の小修正であり、仕様やレイヤー構造は変えない。

## 未確定事項
- なし

## Step 2: delta-apply
- changed files:
  - `.codex/skills/forma-character/SKILL.md`
  - `docs/OVERVIEW.md`
  - `docs/plan.md`
  - `docs/delta/DR-20260315-forma-skill-frontmatter.md`
- applied AC:
  - AC-01:
    - 変更: `SKILL.md` の先頭に `---` で囲まれた frontmatter を追加した。
    - 根拠: 1 行目から `name` / `description` を持つ YAML frontmatter が始まる。
  - AC-02:
    - 変更: frontmatter に `name: forma-character` と description を追加した。
    - 根拠: loader が要求する最小メタ情報を本文前に置いた。
  - AC-03:
    - 変更: 既存の scope / usage / references 本文はそのまま残した。
    - 根拠: frontmatter 追加以外の本文セクション削除や仕様変更はしていない。
  - AC-04:
    - 変更: delta 記録と current state を同期し、validator が通る状態にした。
    - 根拠: `docs/OVERVIEW.md` と `docs/plan.md` を current delta に合わせて更新した。
- non-goal kept:
  - Out of Scope への変更なし: Yes
- canonical sync:
  - mode: post-archive sync
  - action: verify PASS 後に overview / plan を archive 状態へ戻した
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
  - targeted integration / E2E: Not Required
  - delta validator: links-only
- executed verify:
  - static check:
    - `Get-Content .codex/skills/forma-character/SKILL.md -TotalCount 8`
    - inline parser:
      - opening delimiter exists
      - second delimiter exists
      - `name = forma-character`
      - `description` exists
  - delta validator:
    - `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- AC result table:
  - AC-01: PASS
    - 根拠: `SKILL.md` の先頭 4 行が YAML frontmatter になっている。
  - AC-02: PASS
    - 根拠: inline parser が `name` と `description` を検出し、`frontmatter-ok` を返した。
  - AC-03: PASS
    - 根拠: frontmatter の下に従来どおり `# Forma Character` から本文が続いている。
  - AC-04: PASS
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
    - overview: `docs/OVERVIEW.md`
    - plan: `docs/plan.md`
- closed scope:
  - 目的: `forma-character/SKILL.md` を loader 互換の frontmatter 付き構造へ戻す
  - 変更対象: `SKILL.md`、overview、plan、delta record
  - 非対象: skill 仕様変更、他 skill 修正、spec / concept / architecture 更新、実装コード変更
- unresolved items:
  - なし
