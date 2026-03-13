# delta-request

## Delta ID
- DR-20260313-apply-motion-preview

## Delta Type
- FEATURE

## 目的
- Blender background mode を使って既存モーションをキャラクターへ適用し、確認用 preview render を出力できるようにする。
- repo-local public 名 `kyarakuri-apply-motion-preview` からも同じ処理を呼べるようにする。

## 変更対象（In Scope）
- `apply-motion-preview` コマンドの最小インターフェースを定義する。
- Blender background mode を起動する Python CLI と Blender 実行用 script を追加する。
- 入力として既存 `.blend`、既存 `BVH` motion file、任意の config path を受け取り、preview 用 render と更新済み `.blend` を `output_dir` 配下へ保存できるようにする。
- `kyarakuri-apply-motion-preview` wrapper を repo-local skill pack に追加する。
- 失敗時に次の行動が分かるメッセージと終了ステータスの要件を定義する。

## 非対象（Out of Scope）
- FBX や複数 motion format の同時対応。
- 高度な retargeting、bone mapping GUI、motion cleanup。
- 動画出力や turntable animation。
- VRMA export。
- 既存 skill pack の全面 rename。

## Candidate Files/Artifacts
- docs/delta/DR-20260313-apply-motion-preview.md
- docs/OVERVIEW.md
- docs/plan.md
- .codex/skills/comfy-blender-vrm/SKILL.md
- .codex/skills/comfy-blender-vrm/references/pipeline.md
- .codex/skills/comfy-blender-vrm/scripts/apply_motion_preview.py
- .codex/skills/comfy-blender-vrm/blender/apply_motion_preview.py
- .codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md
- .codex/skills/kyarakuri-comfy-blender-vrm/references/pipeline.md
- .codex/skills/kyarakuri-comfy-blender-vrm/scripts/apply_motion_preview.py

## 差分仕様
- DS-01:
  - Given: ユーザーが既存 `.blend` と既存 `BVH` motion file を指定する。
  - When: `apply-motion-preview` を実行する。
  - Then: Blender background mode を起動し、入力 `.blend` と motion file を処理する。
- DS-02:
  - Given: Blender script が処理を開始している。
  - When: motion file が import できる。
  - Then: 最初の armature object に motion を割り当て、preview 用の 1 フレーム render を出力する。
- DS-03:
  - Given: Blender script の処理が完了している。
  - When: 成果物を保存する。
  - Then: `output_dir/motion/<run-id>/` に更新済み `.blend`、preview render、実行メタ情報を保存する。
- DS-04:
  - Given: `.blend` 不足、`BVH` 不足、Blender 実行失敗、preview render 出力失敗のいずれかがある。
  - When: コマンドが終了する。
  - Then: 次の行動が分かるメッセージを出し、非 0 の終了ステータスを返す。
- DS-05:
  - Given: repo-local skill pack を使う。
  - When: `kyarakuri-apply-motion-preview` wrapper を実行する。
  - Then: `apply-motion-preview` と同じ処理を `config/kyarakuri-comfy-blender-vrm.json` 既定で呼べる。

## 受入条件（Acceptance Criteria）
- AC-01: `apply-motion-preview` の入力として `.blend` path、`BVH` motion file、任意の config path が Skill ドキュメント上で定義されている。
- AC-02: Blender background mode を起動し、入力 `.blend` と `BVH` から更新済み `.blend` と preview render を保存できる。
- AC-03: 成功時に `output_dir/motion/<run-id>/` と `output_dir/logs/` に成果物と metadata を保存できる。
- AC-04: `.blend` 不足、`BVH` 不足、Blender path 不正または実行失敗、preview render 出力失敗の少なくとも 4 種の失敗に対して、次の行動が分かるメッセージが定義される。
- AC-05: repo-local `kyarakuri-apply-motion-preview` wrapper が追加され、既定 config で同じ処理を呼べる。
- AC-06: 成功時は終了コード 0、失敗時は非 0 で終了する。

## Verify Profile
- static check: Required
- targeted unit: Not Required
- targeted integration / E2E: Required
- delta-project-validator: links-only

## Canonical Sync Mode
- mode: post-archive sync
- reason: motion preview の最小実装を verify PASS で確定した後、正本 docs に最小差分で同期する。

## 制約
- Blender は config の `blender_path` を使って CLI / background mode で起動する。
- motion input は初版では `BVH` のみに限定する。
- preview output は静止画 1 枚を対象とし、動画や複数カメラ出力は今回の対象外とする。

## Review Gate
- required: No
- reason: 単一コマンドの最小実装であり、format 拡張や高度な retargeting を含まない。

## 未確定事項
- Q-01: Resolved. target は opened `.blend` 内の first armature とし、import した `BVH` action を copy して割り当てる形にした。
- Q-02: Resolved. preview frame は copied action の開始フレームを使う形にした。

## Step 2: delta-apply
- changed files:
  - .codex/skills/comfy-blender-vrm/SKILL.md
  - .codex/skills/comfy-blender-vrm/references/pipeline.md
  - .codex/skills/comfy-blender-vrm/scripts/apply_motion_preview.py
  - .codex/skills/comfy-blender-vrm/blender/apply_motion_preview.py
  - .codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md
  - .codex/skills/kyarakuri-comfy-blender-vrm/references/pipeline.md
  - .codex/skills/kyarakuri-comfy-blender-vrm/scripts/apply_motion_preview.py
  - docs/delta/DR-20260313-apply-motion-preview.md
- applied AC:
  - AC-01:
    - 変更: internal / repo-local `SKILL.md` に `.blend`、`BVH`、optional `config` の実行例を追加した。
    - 根拠: user-facing 実行方法として required inputs を明示した。
  - AC-02:
    - 変更: `apply_motion_preview.py` と Blender script `blender/apply_motion_preview.py` を追加し、background mode で `.blend` を開いて motion preview を出せるようにした。
    - 根拠: Blender CLI を起動し、updated `.blend` と静止画 preview を保存する。
  - AC-03:
    - 変更: `outputs/motion/<run-id>/` と `outputs/logs/` に result `.blend`、`preview.png`、`blender-result.json`、metadata を保存するようにした。
    - 根拠: internal CLI が run dir と log metadata を作成する。
  - AC-04:
    - 変更: `.blend` 不足、`BVH` 不足、Blender path 不正、Blender 実行失敗、preview render 不足に対する `detail` / `next` を定義した。
    - 根拠: すべて `MotionPreviewError(detail, next_action)` で扱う。
  - AC-05:
    - 変更: repo-local wrapper `kyarakuri-apply-motion-preview` を追加した。
    - 根拠: wrapper script が `apply-motion-preview` を既定 config 付きで呼ぶ。
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
  - `apply_motion_preview.py`: 314 lines
  - `blender/apply_motion_preview.py`: 158 lines
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
  - static check: `python -m py_compile .codex/skills/comfy-blender-vrm/scripts/apply_motion_preview.py .codex/skills/comfy-blender-vrm/blender/apply_motion_preview.py .codex/skills/kyarakuri-comfy-blender-vrm/scripts/apply_motion_preview.py`
  - targeted integration / E2E:
    - success case: internal `apply_motion_preview.py` with fake Blender executable, `.blend`, `BVH`, updated `.blend` / preview render / metadata save
    - success case: wrapper `kyarakuri-apply-motion-preview` with default config injection and fake Blender executable
    - failure case: missing `.blend`
    - failure case: missing `BVH`
    - failure case: invalid Blender executable path
    - failure case: Blender execution non-zero exit
    - failure case: preview render output missing after Blender success
  - delta validator: `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- review delta outcome:
  - pass: Yes
  - follow-up delta seeds:
    - `review delta`
- AC result table:
  - AC-01: PASS
    - 根拠: internal / repo-local skill docs に `.blend` と `BVH` の利用例を記載した。
  - AC-02: PASS
    - 根拠: fake Blender success case で updated `.blend` と preview render を保存できた。
  - AC-03: PASS
    - 根拠: success case で `outputs/motion/<run-id>/` と `outputs/logs/` に成果物と metadata を保存した。
  - AC-04: PASS
    - 根拠: missing `.blend`、missing `BVH`、invalid Blender path、Blender execution failure、preview render missing の 5 種で `detail` と `next` を確認した。
  - AC-05: PASS
    - 根拠: wrapper success case で `--config` 未指定の `kyarakuri-apply-motion-preview` が同じ処理を完了した。
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
  - 目的: Blender background mode で `.blend` に `BVH` motion を適用し、preview render まで出せる最小 `apply-motion-preview` を追加する
  - 変更対象: internal CLI、Blender script、repo-local wrapper、関連 docs
  - 非対象: FBX、複雑な retargeting、動画出力、VRMA export
- unresolved items:
  - なし
- follow-up delta seeds:
  - `review delta`
