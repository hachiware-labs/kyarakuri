# delta-request

## Delta ID
- DR-20260313-build-vrm-base

## Delta Type
- FEATURE

## 目的
- Blender background mode を使って既存 `.blend` を処理し、VRM 作業の土台となる更新済み `.blend` と review render を出力できるようにする。
- repo-local public 名 `kyarakuri-build-vrm` からも同じ処理を呼べるようにする。

## 変更対象（In Scope）
- `build-vrm-base` コマンドの最小インターフェースを定義する。
- Blender background mode を起動する Python CLI と Blender 実行用 script を追加する。
- 入力として既存 `.blend`、任意の texture image、任意の config path を受け取り、更新済み `.blend` と review render を `output_dir` 配下へ保存できるようにする。
- `kyarakuri-build-vrm` wrapper を repo-local skill pack に追加する。
- 失敗時に次の行動が分かるメッセージと終了ステータスの要件を定義する。

## 非対象（Out of Scope）
- VRM 正式 export。
- humanoid rig 自動生成。
- shape key / expression の自動作成。
- motion preview の実装。
- 既存 `comfy-blender-vrm` skill pack の全面 rename。

## Candidate Files/Artifacts
- docs/delta/DR-20260313-build-vrm-base.md
- docs/OVERVIEW.md
- docs/plan.md
- .codex/skills/comfy-blender-vrm/SKILL.md
- .codex/skills/comfy-blender-vrm/references/pipeline.md
- .codex/skills/comfy-blender-vrm/scripts/build_vrm_base.py
- .codex/skills/comfy-blender-vrm/blender/build_vrm_base.py
- .codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md
- .codex/skills/kyarakuri-comfy-blender-vrm/references/pipeline.md
- .codex/skills/kyarakuri-comfy-blender-vrm/scripts/build_vrm.py

## 差分仕様
- DS-01:
  - Given: ユーザーが既存 `.blend` と、任意の texture image を指定する。
  - When: `build-vrm-base` を実行する。
  - Then: Blender background mode を起動し、入力 `.blend` を処理する。
- DS-02:
  - Given: Blender script が処理を開始している。
  - When: texture image が指定されている。
  - Then: 最初の mesh object に対して texture を適用または差し替えし、更新済み `.blend` を保存する。
- DS-03:
  - Given: Blender script の処理が完了している。
  - When: review render を出力する。
  - Then: `output_dir/blender/<run-id>/` に更新済み `.blend`、review render、実行メタ情報を保存する。
- DS-04:
  - Given: `.blend` 不足、texture image 不足、Blender 実行失敗、render 出力失敗のいずれかがある。
  - When: コマンドが終了する。
  - Then: 次の行動が分かるメッセージを出し、非 0 の終了ステータスを返す。
- DS-05:
  - Given: repo-local skill pack を使う。
  - When: `kyarakuri-build-vrm` wrapper を実行する。
  - Then: `build-vrm-base` と同じ処理を `config/kyarakuri-comfy-blender-vrm.json` 既定で呼べる。

## 受入条件（Acceptance Criteria）
- AC-01: `build-vrm-base` の入力として `.blend` path、任意の texture image、任意の config path が Skill ドキュメント上で定義されている。
- AC-02: Blender background mode を起動し、入力 `.blend` から更新済み `.blend` と review render を保存できる。
- AC-03: 成功時に `output_dir/blender/<run-id>/` と `output_dir/logs/` に成果物と metadata を保存できる。
- AC-04: `.blend` 不足、texture image 不足、Blender path 不正または実行失敗、review render 出力失敗の少なくとも 4 種の失敗に対して、次の行動が分かるメッセージが定義される。
- AC-05: repo-local `kyarakuri-build-vrm` wrapper が追加され、既存 config 既定値で同じ処理を呼べる。
- AC-06: 成功時は終了コード 0、失敗時は非 0 で終了する。

## Verify Profile
- static check: Required
- targeted unit: Not Required
- targeted integration / E2E: Required
- delta-project-validator: links-only

## Canonical Sync Mode
- mode: post-archive sync
- reason: build-vrm の最小実装を verify PASS で確定した後、正本 docs に最小差分で同期する。

## 制約
- Blender は config の `blender_path` を使って CLI / background mode で起動する。
- texture 適用対象は最初の mesh object に限定し、複雑な material graph 編集は今回の対象外とする。
- review render は静止画 1 枚を対象とし、turntable や動画出力は今回の対象外とする。

## Review Gate
- required: No
- reason: 単一コマンドの最小実装であり、VRM export や rigging を含まない。

## 未確定事項
- Q-01: Resolved. review render の既定 camera / light は Blender script 側で不足時のみ補う形にした。
- Q-02: Resolved. texture image 未指定時は material を保持したまま render のみ実行する形にした。

## Step 2: delta-apply
- changed files:
  - .codex/skills/comfy-blender-vrm/SKILL.md
  - .codex/skills/comfy-blender-vrm/references/pipeline.md
  - .codex/skills/comfy-blender-vrm/scripts/build_vrm_base.py
  - .codex/skills/comfy-blender-vrm/blender/build_vrm_base.py
  - .codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md
  - .codex/skills/kyarakuri-comfy-blender-vrm/references/pipeline.md
  - .codex/skills/kyarakuri-comfy-blender-vrm/scripts/build_vrm.py
  - docs/delta/DR-20260313-build-vrm-base.md
- applied AC:
  - AC-01:
    - 変更: `SKILL.md` に `build-vrm-base` の実行例と `.blend` / `texture-image` / `config` の入口を追加した。
    - 根拠: user-facing 実行方法として `.blend` path と optional texture image を明示した。
  - AC-02:
    - 変更: `build_vrm_base.py` と Blender script `blender/build_vrm_base.py` を追加し、background mode で `.blend` を開いて review render を出せるようにした。
    - 根拠: Blender CLI を起動し、更新済み `.blend` と静止画 render を保存する。
  - AC-03:
    - 変更: `outputs/blender/<run-id>/` と `outputs/logs/` に result `.blend`、`review.png`、`blender-result.json`、metadata を保存するようにした。
    - 根拠: internal CLI が run dir と log metadata を作成する。
  - AC-04:
    - 変更: `.blend` 不足、texture image 不足、Blender path 不正、Blender 実行失敗、review render 不足に対する `detail` / `next` を定義した。
    - 根拠: すべて `BuildVrmError(detail, next_action)` で扱う。
  - AC-05:
    - 変更: repo-local wrapper `kyarakuri-build-vrm` を追加した。
    - 根拠: `build_vrm.py` が `build-vrm-base` を既定 config 付きで呼ぶ。
  - AC-06:
    - 変更: 成功時 0、失敗時 1 の終了コードを実装した。
    - 根拠: internal CLI が正常終了で `0`、例外処理で `1` を返す。
- non-goal kept:
  - Out of Scope への変更なし: Yes
- canonical sync:
  - mode: post-archive sync
  - action: 正本 docs の追加同期は未実施
  - status: NOT STARTED
- code split check:
  - file over 500 lines: No
  - file over 800 lines: No
  - file over 1000 lines: No
  - `build_vrm_base.py`: 282 lines
  - `blender/build_vrm_base.py`: 128 lines
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
  - static check: `python -m py_compile .codex/skills/comfy-blender-vrm/scripts/build_vrm_base.py .codex/skills/comfy-blender-vrm/blender/build_vrm_base.py .codex/skills/kyarakuri-comfy-blender-vrm/scripts/build_vrm.py`
  - targeted integration / E2E:
    - success case: internal `build_vrm_base.py` with fake Blender executable, `.blend`, texture image, updated `.blend` / review render / metadata save
    - success case: wrapper `kyarakuri-build-vrm` with default config injection and fake Blender executable
    - failure case: missing `.blend`
    - failure case: missing texture image
    - failure case: invalid Blender executable path
    - failure case: Blender execution non-zero exit
    - failure case: review render output missing after Blender success
  - delta validator: `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- review delta outcome:
  - pass: Yes
  - follow-up delta seeds:
    - `apply-motion-preview` request
- AC result table:
  - AC-01: PASS
    - 根拠: internal skill docs に `.blend` と optional texture image の利用例を記載した。
  - AC-02: PASS
    - 根拠: fake Blender success case で updated `.blend` と review render を保存できた。
  - AC-03: PASS
    - 根拠: success case で `outputs/blender/<run-id>/` と `outputs/logs/` に成果物と metadata を保存した。
  - AC-04: PASS
    - 根拠: missing `.blend`、missing texture image、invalid Blender path、Blender execution failure、review render missing の 5 種で `detail` と `next` を確認した。
  - AC-05: PASS
    - 根拠: wrapper success case で `--config` 未指定の `kyarakuri-build-vrm` が同じ処理を完了した。
  - AC-06: PASS
    - 根拠: success cases は exit code 0、failure cases は exit code 1 を確認した。
- scope deviation:
  - Out of Scope 変更あり: No
- review findings:
  - layer integrity: PASS
  - docs sync: PASS
  - data size: PASS
  - code split health: PASS
  - file-size threshold: PASS
- canonical sync:
  - mode: post-archive sync
  - status: NOT STARTED
  - result: PASS
- references:
  - fake Blender integration では wrapper default config 注入を含めて internal / wrapper の両経路を確認した。
  - `validate_delta_links.js` returned `OK: errors=0, warnings=0`.
- overall: PASS

## Step 4: delta-archive
- verify result: PASS
- review gate: NOT REQUIRED
- archive status: archived
- canonical sync:
  - mode: post-archive sync
  - status: DONE
  - synced docs:
    - concept: `docs/concept.md`
    - spec: `docs/spec.md`
    - architecture: `docs/architecture.md`
    - overview: `docs/OVERVIEW.md`
    - plan: `docs/plan.md`
- closed scope:
  - 目的: Blender background mode で `.blend` を処理し、review render まで出せる最小 `build-vrm-base` を追加する
  - 変更対象: internal CLI、Blender script、repo-local wrapper、関連 docs
  - 非対象: VRM export、rig 自動生成、shape key 自動作成、motion preview
- unresolved items:
  - なし
- follow-up delta seeds:
  - `apply-motion-preview` request
