# delta-request

## Delta ID
- DR-20260412-background-transparent-skill

## Delta Type
- FEATURE

## 目的
- ユーザーが「画像の背景を透明化して」と依頼した時に使える repo-local skill を追加する。

## 変更対象（In Scope）
- `.codex/skills/background-transparent/` に repo-local skill を作成する。
- skill は raster image の background removal / transparent PNG cutout を対象にする。
- skill は入力画像を非破壊で扱い、出力先を明示する手順を持つ。
- `docs/OVERVIEW.md` と `docs/plan.md` に current state を最小反映する。
- delta 記録を `docs/delta/DR-20260412-background-transparent-skill.md` に残す。

## 非対象（Out of Scope）
- ComfyUI の新規 workflow 実装。
- `forma-character` の既存 public command 追加や rename。
- 実画像の背景透明化実行。
- Python 画像処理依存の導入。
- 提供用 skill への移行。

## Candidate Files/Artifacts
- `.codex/skills/background-transparent/SKILL.md`
- `.codex/skills/background-transparent/agents/openai.yaml`
- `docs/OVERVIEW.md`
- `docs/plan.md`
- `docs/delta/DR-20260412-background-transparent-skill.md`

## 差分仕様
- DS-01:
  - Given: Codex が background removal / transparent PNG cutout の依頼を受ける。
  - When: skill 一覧から `background-transparent` を判定する。
  - Then: skill description が背景透明化依頼で発火できる内容になっている。
- DS-02:
  - Given: skill 本文を読む。
  - When: 背景透明化を実施する。
  - Then: 入力画像の役割確認、対象保持、背景のみ透明化、非破壊保存、出力パス報告の手順が分かる。
- DS-03:
  - Given: repo docs を読む。
  - When: 現在地を確認する。
  - Then: background transparent skill が repo-local に追加済みであることが分かる。

## 受入条件（Acceptance Criteria）
- AC-01: `.codex/skills/background-transparent/SKILL.md` が存在し、YAML frontmatter の `name` と `description` を持つ。
- AC-02: skill 本文に背景透明化の最小 workflow と保存方針がある。
- AC-03: `agents/openai.yaml` が存在し、UI 用の最小 metadata を持つ。
- AC-04: `docs/OVERVIEW.md` と `docs/plan.md` が current state に同期されている。
- AC-05: skill validation が PASS する。

## Verify Profile
- static check: Required
- targeted unit: Not Required
- targeted integration / E2E: Not Required
- skill validation: `skill-creator/scripts/quick_validate.py`

## Canonical Sync Mode
- mode: post-archive sync
- reason: repo state 反映は verify PASS 後に閉じる。

## 制約
- 新 skill は `background-transparent` に限定する。
- 実画像編集や ComfyUI workflow 追加は今回行わない。
- skill は簡潔に保ち、不要な README / INSTALLATION_GUIDE などを作らない。

## Review Gate
- required: No
- reason: repo-local skill の小規模追加であり、既存 command / data model を変更しない。

## 未確定事項
- 実画像編集で使う具体 workflow は、ユーザーが画像を渡した時か follow-up delta で決める。

## Step 2: delta-apply
- changed files:
  - `.codex/skills/background-transparent/SKILL.md`
  - `.codex/skills/background-transparent/agents/openai.yaml`
  - `docs/OVERVIEW.md`
  - `docs/plan.md`
  - `docs/delta/DR-20260412-background-transparent-skill.md`
- applied AC:
  - AC-01:
    - 変更: `background-transparent/SKILL.md` を作成し、`name` と `description` を持つ YAML frontmatter を置いた。
  - AC-02:
    - 変更: 背景透明化の workflow、prompt pattern、quality check、非破壊保存方針を本文に追加した。
  - AC-03:
    - 変更: `agents/openai.yaml` に `display_name`、`short_description`、`default_prompt` を追加した。
  - AC-04:
    - 変更: `docs/OVERVIEW.md` と `docs/plan.md` に delta の current state を同期した。
  - AC-05:
    - 変更: verify step で実行する。
- non-goal kept:
  - ComfyUI workflow 追加なし: Yes
  - `forma-character` command 変更なし: Yes
  - 実画像編集実行なし: Yes
- code split check:
  - file over 500 lines: No
  - file over 800 lines: No
  - file over 1000 lines: No
- status: APPLIED

## Step 3: delta-verify
- verify profile:
  - static check: Required
  - targeted unit: Not Required
  - targeted integration / E2E: Not Required
  - skill validation: `skill-creator/scripts/quick_validate.py`
- executed verify:
  - skill validation:
    - command: `$env:PYTHONUTF8='1'; uv run --with pyyaml python C:/Users/naruhide/.codex/skills/.system/skill-creator/scripts/quick_validate.py .codex/skills/background-transparent`
    - result: `Skill is valid!`
    - note: `PYTHONUTF8=1` は Windows 既定 encoding で日本語 description を読む validator 失敗を避けるために指定した。
  - static check:
    - command: inline parser で `SKILL.md` frontmatter の `name`、日本語 trigger、本文 section を確認
    - result: `skill-static-ok`
  - UI metadata check:
    - command: `agents/openai.yaml` を YAML parse し、`display_name`、`short_description`、`default_prompt` を確認
    - result: `openai-yaml-ok`
  - template residue check:
    - command: `rg -n "TODO|Structuring This Skill|Resources \\(optional\\)|Use -transparent" .codex/skills/background-transparent docs/delta/DR-20260412-background-transparent-skill.md`
    - result: no matches
  - whitespace check:
    - command: `git diff --check -- .codex/skills/background-transparent/SKILL.md .codex/skills/background-transparent/agents/openai.yaml docs/OVERVIEW.md docs/plan.md docs/delta/DR-20260412-background-transparent-skill.md`
    - result: PASS
- AC result table:
  - AC-01: PASS
    - 根拠: `SKILL.md` に `name: background-transparent` と description 付き frontmatter がある。
  - AC-02: PASS
    - 根拠: workflow、prompt pattern、quality check、非破壊保存方針がある。
  - AC-03: PASS
    - 根拠: `agents/openai.yaml` が UI metadata と `$background-transparent` を含む default prompt を持つ。
  - AC-04: PASS
    - 根拠: `docs/OVERVIEW.md` と `docs/plan.md` に current state を同期した。
  - AC-05: PASS
    - 根拠: `quick_validate.py` が `Skill is valid!` を返した。
- scope deviation:
  - Out of Scope 変更あり: No
- validator note:
  - `delta-project-validator` は `C:/Users/naruhide/.codex/skills/delta-project-validator/` に存在しなかったため未実行。
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
  - 目的: 既存画像の背景透明化用 repo-local skill を追加する
  - 変更対象: `background-transparent` skill、overview、plan、delta record
  - 非対象: ComfyUI workflow 追加、`forma-character` command 変更、実画像編集、Python 画像処理依存導入、提供用 skill 移行
- unresolved items:
  - 実画像編集で使う具体 workflow は、ユーザーが画像を渡した時か follow-up delta で決める。
