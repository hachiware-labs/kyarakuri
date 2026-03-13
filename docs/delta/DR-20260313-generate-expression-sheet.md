# delta-request

## Delta ID
- DR-20260313-generate-expression-sheet

## Delta Type
- FEATURE

## 目的
- ベースキャラクター画像と API-format ComfyUI workflow を使って、複数表情の差分画像を 1 コマンドで生成できるようにする。
- expression ごとの画像だけでなく、再実行に必要な expression list / seed / workflow 情報も保存できるようにする。

## 変更対象（In Scope）
- `generate-expression-sheet` コマンドの最小インターフェースを定義する。
- API-format workflow JSON を読み込み、`base_image`、`character_prompt`、`expression_name`、`seed` 系のプレースホルダを解決できるようにする。
- ベース画像を ComfyUI へアップロードし、表情一覧ごとに prompt を送信、完了待ち、画像ダウンロード、成果物保存までを行う。
- 画像群、submitted workflow 群、実行メタ情報を `output_dir` 配下に整理して保存する。
- 失敗時に次の行動が分かるメッセージと終了ステータスの要件を定義する。

## 非対象（Out of Scope）
- 画像を 1 枚の contact sheet に合成する処理。
- lip sync 用口形、VRM expression、Blender 連携、モーション適用。
- UI 形式 workflow JSON から API 形式への変換。
- ComfyUI 本体の起動代行やモデル不足の自動解決。

## Candidate Files/Artifacts
- docs/delta/DR-20260313-generate-expression-sheet.md
- docs/OVERVIEW.md
- docs/plan.md
- .codex/skills/comfy-blender-vrm/SKILL.md
- .codex/skills/comfy-blender-vrm/references/pipeline.md
- .codex/skills/comfy-blender-vrm/scripts/comfy_helpers.py
- .codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py
- .codex/skills/comfy-blender-vrm/workflows/README.md

## 差分仕様
- DS-01:
  - Given: ユーザーが workflow JSON、base image、`character_prompt`、任意の `seed`、任意の expression list を指定する。
  - When: `generate-expression-sheet` を実行する。
  - Then: workflow JSON を読み込み、ベース画像 upload 結果と expression ごとの placeholder を解決した submitted workflow を生成する。
- DS-02:
  - Given: submitted workflow が expression ごとに生成できている。
  - When: コマンドが ComfyUI API を実行する。
  - Then: expression ごとに prompt を送信し、完了まで polling して、出力画像を取得する。
- DS-03:
  - Given: 画像取得が成功している。
  - When: コマンドが成果物を保存する。
  - Then: `output_dir/expressions/<run-id>/<expression>/` に画像と submitted workflow を保存し、`output_dir/logs/` に実行メタ情報を保存する。
- DS-04:
  - Given: workflow JSON 不正、base image 不足、未解決プレースホルダ、ComfyUI API 失敗、画像ダウンロード失敗のいずれかがある。
  - When: コマンドが終了する。
  - Then: 次の行動が分かるメッセージを出し、非 0 の終了ステータスを返す。

## 受入条件（Acceptance Criteria）
- AC-01: `generate-expression-sheet` の入力として workflow JSON パス、base image、`character_prompt`、任意の `seed`、任意の expression list、任意の config パスが Skill ドキュメント上で定義されている。
- AC-02: workflow JSON は API 形式を前提とし、`{{character_prompt}}`、`{{expression_name}}`、`{{seed}}`、`{{base_image}}` 系のプレースホルダを解決できる。
- AC-03: ComfyUI 実行成功時に、expression ごとの生成画像、submitted workflow 群、実行メタ情報が `output_dir` 配下へ保存される。
- AC-04: workflow ファイル不足、workflow JSON 不正、base image 不足、未解決プレースホルダ、ComfyUI API エラー、画像ダウンロード失敗の少なくとも 6 種の失敗に対して、次の行動が分かるメッセージが定義される。
- AC-05: 成功時は終了コード 0、失敗時は非 0 で終了する。

## Verify Profile
- static check: Required
- targeted unit: Not Required
- targeted integration / E2E: Required
- delta-project-validator: links-only

## Canonical Sync Mode
- mode: post-archive sync
- reason: request 時点では scope と AC を固定し、正本への仕様同期は verify PASS 後に最小差分で行う。

## 制約
- ComfyUI はローカル HTTP API のみを使い、MCP や常駐制御は追加しない。
- workflow JSON は API 形式のみを対象とし、UI export 変換は行わない。
- base image は必須入力とし、同一アップロード結果を expression ごとに再利用する。
- 追加依存は最小限にし、可能なら標準ライブラリ中心で構成する。

## Review Gate
- required: No
- reason: Phase 1 の単一コマンドに閉じた差分であり、ComfyUI 呼び出しの拡張に留まる。

## 未確定事項
- Q-01: Resolved. expression list 未指定時の既定値は `neutral,smile,angry,sad,surprised,blink` とした。
- Q-02: Resolved. expression ごとの seed は `base_seed + index` とした。
- Q-03: Resolved. 保存先は `outputs/expressions/<run-id>/<expression>/images/` とした。

## Step 2: delta-apply
- changed files:
  - .codex/skills/comfy-blender-vrm/SKILL.md
  - .codex/skills/comfy-blender-vrm/references/pipeline.md
  - .codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py
  - .codex/skills/comfy-blender-vrm/workflows/README.md
  - docs/delta/DR-20260313-generate-expression-sheet.md
- applied AC:
  - AC-01:
    - 変更: `SKILL.md` に `generate-expression-sheet` の実行方法、主要引数、expression list 指定例を記載した。
    - 根拠: `--workflow`、`--base-image`、`--character-prompt`、`--expressions`、`--seed`、`--config` を使用例として明示した。
  - AC-02:
    - 変更: API-format workflow だけを受け付け、`expression_name` と `base_image*` を含む placeholder 展開を実装した。
    - 根拠: `generate_expression_sheet.py` が base image upload 結果と expression ごとの seed を placeholder に埋める。
  - AC-03:
    - 変更: expression ごとの prompt submit、history polling、画像 download、submitted workflow / history / metadata の保存を実装した。
    - 根拠: `output_dir/expressions/<run-id>/<expression>/images/` と `output_dir/logs/` へ成果物を出力する。
  - AC-04:
    - 変更: workflow 不足、workflow JSON 不正、base image 不足、未解決 placeholder、ComfyUI API エラー、画像 download 失敗の各失敗分岐に `next` メッセージを定義した。
    - 根拠: すべて `GenerationError(detail, next_action)` で扱う。
  - AC-05:
    - 変更: 成功時 0、失敗時 1 の終了コードを実装した。
    - 根拠: `main()` が正常終了で `0`、例外処理で `1` を返す。
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
  - longest source file: `.codex/skills/comfy-blender-vrm/scripts/comfy_helpers.py` = 355 lines
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
  - static check: `python -m py_compile .codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py`
  - targeted integration / E2E:
    - success case with mock ComfyUI server, base image upload reuse, 2 expressions, image download, metadata save
    - failure case: missing workflow file
    - failure case: invalid workflow JSON
    - failure case: missing base image
    - failure case: unresolved placeholder
    - failure case: ComfyUI prompt API HTTP 500
    - failure case: image download HTTP 404
  - delta validator: `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- review delta outcome:
  - pass: Yes
  - follow-up delta seeds:
    - `build-vrm-base` request
    - `review delta` request
- AC result table:
  - AC-01: PASS
    - 根拠: `SKILL.md` に workflow / base-image / expression list / seed / config の使用例を記載した。
  - AC-02: PASS
    - 根拠: success case で `expression_name`、`seed`、`base_image` が展開され、unresolved placeholder case で検出して失敗した。
  - AC-03: PASS
    - 根拠: success case で 2 expression の画像 2 枚、metadata 1 件、expression ごとの submitted workflow と history を保存した。
  - AC-04: PASS
    - 根拠: missing workflow、invalid JSON、missing base image、unresolved placeholder、API error、download error の 6 種で `detail` と `next` を確認した。
  - AC-05: PASS
    - 根拠: success case は exit code 0、各 failure case は exit code 1 を確認した。
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
  - success case では base image upload が 1 回、prompt submit が 2 回で、`neutral` と `smile` に対して seed `700` と `701` が使われた。
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
  - 目的: ベース画像から複数表情を生成し、expression ごとの画像群と再現メタを保存する
  - 変更対象: base image upload、expression loop、placeholder 展開、ComfyUI API 実行、画像 download、metadata 保存
  - 非対象: contact sheet 合成、lip sync、Blender 連携、モーション適用
- unresolved items:
  - なし
- follow-up delta seeds:
  - `review delta` request
  - `build-vrm-base` request
