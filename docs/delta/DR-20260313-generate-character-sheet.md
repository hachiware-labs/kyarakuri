# delta-request

## Delta ID
- DR-20260313-generate-character-sheet

## Delta Type
- FEATURE

## 目的
- ComfyUI の API-format workflow JSON を使って、キャラクター立ち絵を 1 コマンドで生成できるようにする。
- 生成画像だけでなく、再実行に必要な prompt / seed / workflow 情報も保存できるようにする。

## 変更対象（In Scope）
- `generate-character-sheet` コマンドの最小インターフェースを定義する。
- API-format workflow JSON を読み込み、`character_prompt`、`seed`、`reference_image` 系のプレースホルダを解決できるようにする。
- ComfyUI に prompt を送信し、完了待ち、画像ダウンロード、成果物保存までを行う。
- 画像、submitted workflow、実行メタ情報を `output_dir` 配下に整理して保存する。
- 失敗時に次の行動が分かるメッセージと終了ステータスの要件を定義する。

## 非対象（Out of Scope）
- UI 形式 workflow JSON から API 形式への変換。
- 複数 workflow の一括実行、expression sheet 生成、Blender 連携、モーション適用。
- negative prompt、モデル切替、複雑なノードマッピング UI の提供。
- ComfyUI 本体の起動代行やモデル不足の自動解決。

## Candidate Files/Artifacts
- docs/delta/DR-20260313-generate-character-sheet.md
- docs/OVERVIEW.md
- docs/plan.md
- .codex/skills/comfy-blender-vrm/SKILL.md
- .codex/skills/comfy-blender-vrm/references/pipeline.md
- .codex/skills/comfy-blender-vrm/scripts/comfy_helpers.py
- .codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py
- .codex/skills/comfy-blender-vrm/workflows/README.md

## 差分仕様
- DS-01:
  - Given: ユーザーが workflow JSON パス、`character_prompt`、任意の `seed`、任意の reference image を指定する。
  - When: `generate-character-sheet` を実行する。
  - Then: workflow JSON を読み込み、プレースホルダを解決した submitted workflow を生成する。
- DS-02:
  - Given: submitted workflow が生成できている。
  - When: コマンドが ComfyUI API を実行する。
  - Then: prompt を送信し、完了まで polling して、出力画像を取得する。
- DS-03:
  - Given: 画像取得が成功している。
  - When: コマンドが成果物を保存する。
  - Then: `output_dir/character/<run-id>/` に画像と submitted workflow を保存し、`output_dir/logs/` にメタ情報を保存する。
- DS-04:
  - Given: workflow JSON 不正、未解決プレースホルダ、ComfyUI API 失敗、画像ダウンロード失敗のいずれかがある。
  - When: コマンドが終了する。
  - Then: 次の行動が分かるメッセージを出し、非 0 の終了ステータスを返す。

## 受入条件（Acceptance Criteria）
- AC-01: `generate-character-sheet` の入力として workflow JSON パス、`character_prompt`、任意の `seed`、任意の reference image、任意の config パスが Skill ドキュメント上で定義されている。
- AC-02: workflow JSON は API 形式を前提とし、`{{character_prompt}}`、`{{seed}}`、`{{reference_image}}` 系のプレースホルダを解決できる。
- AC-03: ComfyUI 実行成功時に、生成画像、submitted workflow、実行メタ情報が `output_dir` 配下へ保存される。
- AC-04: workflow ファイル不足、workflow JSON 不正、未解決プレースホルダ、ComfyUI API エラー、画像ダウンロード失敗の少なくとも 5 種の失敗に対して、次の行動が分かるメッセージが定義される。
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
- 出力保存とメタ保存は `output_dir` 配下で完結させる。
- 追加依存は最小限にし、可能なら標準ライブラリ中心で構成する。

## Review Gate
- required: No
- reason: Phase 1 の単一コマンドに閉じた差分であり、Blender 連携や多機能化を含まない。

## 未確定事項
- Q-01: Resolved. `character_prompt` / `seed` / `run_id` / `reference_image` / `reference_image_name` / `reference_image_subfolder` / `reference_image_type` をサポートする。
- Q-02: Resolved. run ディレクトリ命名は `timestamp-output_name_slug` とした。
- Q-03: Resolved. reference image upload のレスポンスは `name` と `filename` を許容し、workflow には `reference_image*` 系 placeholder へ反映する。

## Step 2: delta-apply
- changed files:
  - .codex/skills/comfy-blender-vrm/SKILL.md
  - .codex/skills/comfy-blender-vrm/references/pipeline.md
  - .codex/skills/comfy-blender-vrm/scripts/comfy_helpers.py
  - .codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py
  - .codex/skills/comfy-blender-vrm/workflows/README.md
  - docs/delta/DR-20260313-generate-character-sheet.md
- applied AC:
  - AC-01:
    - 変更: `SKILL.md` に `generate-character-sheet` の実行方法、主要引数、reference image 付きの例を記載した。
    - 根拠: `--workflow`、`--character-prompt`、`--reference-image`、`--seed`、`--config` を使用例として明示した。
  - AC-02:
    - 変更: API-format workflow だけを受け付け、placeholder 展開と未解決 token 検出を実装した。
    - 根拠: `generate_character_sheet.py` と `comfy_helpers.py` で UI export JSON を拒否し、`reference_image*` を含む placeholder を解決する。
  - AC-03:
    - 変更: ComfyUI prompt submit、history polling、画像 download、submitted workflow / history / metadata の保存を実装した。
    - 根拠: `output_dir/character/<run-id>/images/` と `output_dir/logs/` へ成果物を出力する。
  - AC-04:
    - 変更: workflow 不足、workflow JSON 不正、未解決 placeholder、ComfyUI API エラー、画像 download 失敗の各失敗分岐に `next` メッセージを定義した。
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
  - static check: `python -m py_compile .codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py .codex/skills/comfy-blender-vrm/scripts/comfy_helpers.py`
  - targeted integration / E2E:
    - success case with mock ComfyUI server, reference image upload, image download, metadata save
    - failure case: missing workflow file
    - failure case: invalid workflow JSON
    - failure case: unresolved placeholder
    - failure case: ComfyUI prompt API HTTP 500
    - failure case: image download HTTP 404
  - delta validator: `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- review delta outcome:
  - pass: Yes
  - follow-up delta seeds:
    - `generate-expression-sheet` request
- AC result table:
  - AC-01: PASS
    - 根拠: `SKILL.md` に workflow / prompt / reference image / seed / config の使用例を記載した。
  - AC-02: PASS
    - 根拠: success case で `character_prompt`、`seed`、`reference_image` が展開され、unresolved placeholder case で検出して失敗した。
  - AC-03: PASS
    - 根拠: success case で画像 1 枚、metadata 1 件、submitted workflow と history を保存した。
  - AC-04: PASS
    - 根拠: missing workflow、invalid JSON、unresolved placeholder、API error、download error の 5 種で `detail` と `next` を確認した。
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
  - success case では submitted prompt に `hero front pose`, `4242`, `uploaded-ref.png` が入った。
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
  - 目的: API-format ComfyUI workflow から立ち絵を生成し、画像と再現メタを保存する
  - 変更対象: workflow 読込、placeholder 展開、ComfyUI API 実行、画像 download、metadata 保存
  - 非対象: UI workflow 変換、expression sheet、Blender 連携、モーション適用
- unresolved items:
  - なし
- follow-up delta seeds:
  - `generate-expression-sheet` request
