# delta-request

## Delta ID
- DR-20260413-background-transparent-script

## Delta Type
- FEATURE

## 目的
- `background-transparent` skill を、手順書だけでなく deterministic な Pillow script 付きで再利用しやすい状態にする。

## 変更対象（In Scope）
- `.codex/skills/background-transparent/scripts/` に背景透明化用の Pillow script を追加する。
- script は `--out`、`--replace`、`--mode white/checker/auto`、preview 生成、alpha 統計出力を持つ。
- `.codex/skills/background-transparent/SKILL.md` に script 優先の利用手順と semantic fallback を追記する。
- `docs/OVERVIEW.md` と `docs/plan.md` に current state を最小反映する。
- delta 記録を `docs/delta/DR-20260413-background-transparent-script.md` に残す。

## 非対象（Out of Scope）
- ComfyUI の新規 workflow 実装。
- 生成AI / imagegen の CLI fallback 実装。
- 任意の複雑背景を完全自動で semantic segmentation すること。
- `forma-character` の既存 public command 追加や rename。
- 提供用 skill への移行。

## Candidate Files/Artifacts
- `.codex/skills/background-transparent/SKILL.md`
- `.codex/skills/background-transparent/scripts/remove_background.py`
- `docs/OVERVIEW.md`
- `docs/plan.md`
- `docs/delta/DR-20260413-background-transparent-script.md`

## 差分仕様
- DS-01:
  - Given: 背景が白または checkerboard 風の raster image がある。
  - When: `remove_background.py` を `--mode white/checker/auto` のいずれかで実行する。
  - Then: border-connected な背景候補を透明化した PNG を保存できる。
- DS-02:
  - Given: 透明化結果を確認したい。
  - When: `--preview <path>` を指定する。
  - Then: 透明部分を色背景で確認できる preview PNG が保存される。
- DS-03:
  - Given: 実行結果を機械的に確認したい。
  - When: script が完了する。
  - Then: input/output/mode/size/alpha count/removed pixels を JSON で stdout に出す。
- DS-04:
  - Given: skill 本文を読む。
  - When: 背景透明化を実施する。
  - Then: deterministic script を優先し、複雑背景では semantic background extraction へ fallback する判断が分かる。

## 受入条件（Acceptance Criteria）
- AC-01: `.codex/skills/background-transparent/scripts/remove_background.py` が存在する。
- AC-02: script が `--out`、`--replace`、`--mode white/checker/auto`、`--preview` を受け付ける。
- AC-03: script が完了時に alpha 統計と removed pixels を JSON で出力する。
- AC-04: synthetic image で white / checker の背景透明化 smoke test が PASS する。
- AC-05: `SKILL.md` が script 優先の利用手順と fallback 方針を説明している。
- AC-06: skill validation が PASS する。

## Verify Profile
- static check: Required
- targeted unit/smoke: Required
- skill validation: `skill-creator/scripts/quick_validate.py`
- targeted integration / E2E: Not Required

## Canonical Sync Mode
- mode: post-archive sync
- reason: repo state 反映は verify PASS 後に閉じる。

## 制約
- 追加 script は Pillow 以外の外部依存を増やさない。
- 既存の `forma-character` skill pack には触らない。
- skill は簡潔に保ち、不要な README / INSTALLATION_GUIDE などを作らない。

## Review Gate
- required: No
- reason: repo-local skill の小規模 script 追加であり、既存 command / data model を変更しない。

## 未確定事項
- 複雑背景向けの semantic extraction は、必要になった時に別 delta で扱う。

## Step 2: delta-apply
- changed files:
  - `.codex/skills/background-transparent/SKILL.md`
  - `.codex/skills/background-transparent/scripts/remove_background.py`
  - `docs/OVERVIEW.md`
  - `docs/plan.md`
  - `docs/delta/DR-20260413-background-transparent-script.md`
- applied AC:
  - AC-01:
    - 変更: `scripts/remove_background.py` を追加した。
  - AC-02:
    - 変更: `--out`、`--replace`、`--mode auto|white|checker`、`--preview`、`--preview-color` を実装した。
  - AC-03:
    - 変更: 完了時に input/output/preview/mode/size/removed_pixels/alpha_before/alpha_after を JSON 出力するようにした。
  - AC-04:
    - 変更: verify step で synthetic white / checker image の smoke test を実行する。
  - AC-05:
    - 変更: `SKILL.md` に bundled script の優先利用、mode 選択、preview、replace の使い分けを追記した。
  - AC-06:
    - 変更: verify step で実行する。
- non-goal kept:
  - ComfyUI workflow 追加なし: Yes
  - 生成AI / imagegen CLI fallback 実装なし: Yes
  - `forma-character` command 変更なし: Yes
  - 提供用 skill への移行なし: Yes
- code split check:
  - file over 500 lines: No
  - file over 800 lines: No
  - file over 1000 lines: No
- status: APPLIED

## Step 3: delta-verify
- verify profile:
  - static check: Required
  - targeted unit/smoke: Required
  - skill validation: `skill-creator/scripts/quick_validate.py`
  - targeted integration / E2E: Not Required
- executed verify:
  - python compile:
    - command: `uv run --with pillow python -m py_compile .codex/skills/background-transparent/scripts/remove_background.py`
    - result: PASS
  - skill validation:
    - command: `$env:PYTHONUTF8='1'; uv run --with pyyaml C:/Users/naruhide/.codex/skills/.system/skill-creator/scripts/quick_validate.py C:/Users/naruhide/workspace/kyarakuri/.codex/skills/background-transparent`
    - result: `Skill is valid!`
  - synthetic white smoke:
    - command: `uv run --with pillow python .codex/skills/background-transparent/scripts/remove_background.py <temp>/white.png --mode white --out <temp>/white-out.png --preview <temp>/white-preview.png`
    - result: PASS
    - observed: `removed_pixels=8192`, `alpha_after.transparent=8192`, center subject alpha remained 255
  - synthetic checker smoke:
    - command: `uv run --with pillow python .codex/skills/background-transparent/scripts/remove_background.py <temp>/checker.png --mode checker --out <temp>/checker-out.png --preview <temp>/checker-preview.png`
    - result: PASS
    - observed: `removed_pixels=7903`, `alpha_after.transparent=7903`, center subject alpha remained 255
- AC result table:
  - AC-01: PASS
    - 根拠: `scripts/remove_background.py` が存在する。
  - AC-02: PASS
    - 根拠: argparse で `--out`、`--replace`、`--mode auto|white|checker`、`--preview` を受け付ける。
  - AC-03: PASS
    - 根拠: 実行結果に alpha 統計と removed pixels の JSON が出力された。
  - AC-04: PASS
    - 根拠: synthetic white / checker の smoke test が PASS した。
  - AC-05: PASS
    - 根拠: `SKILL.md` に bundled script の使い方と semantic fallback 方針がある。
  - AC-06: PASS
    - 根拠: `quick_validate.py` が `Skill is valid!` を返した。
- scope deviation:
  - Out of Scope 変更あり: No
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
  - 目的: `background-transparent` skill を deterministic な Pillow script 付きで再利用しやすい状態にする
  - 変更対象: `background-transparent` script、skill 本文、overview、plan、delta record
  - 非対象: ComfyUI workflow 追加、生成AI / imagegen CLI fallback 実装、任意の複雑背景の完全自動 semantic segmentation、`forma-character` command 変更、提供用 skill 移行
- unresolved items:
  - 複雑背景向けの semantic extraction は、必要になった時に別 delta で扱う。
