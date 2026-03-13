# delta-request

## Delta ID
- DR-20260313-generate-character-from-brief

## Delta Type
- FEATURE

## 目的
- ユーザーのキャラクター要件を聞き取り、ベース画像生成用の prompt に落として、既存の `generate-character-sheet` へ接続できるようにする。
- 聞き取り内容そのものも保存し、生成画像と一緒に再利用可能な brief を残せるようにする。

## 変更対象（In Scope）
- `generate-character-from-brief` コマンドの最小インターフェースを定義する。
- 対話入力、または brief JSON ファイルからキャラクター要件を収集できるようにする。
- 収集内容から `character_prompt` を合成し、既存の `generate-character-sheet` 相当処理へ渡してベース画像を生成する。
- brief JSON と合成 prompt を `output_dir` 配下へ保存する。
- 失敗時に次の行動が分かるメッセージと終了ステータスの要件を定義する。

## 非対象（Out of Scope）
- 自然言語会話の自由対話エージェント化。
- 画像評価の自動フィードバックループ。
- 複数候補の比較ランキング。
- Blender 連携、表情生成、モーション適用。

## Candidate Files/Artifacts
- docs/delta/DR-20260313-generate-character-from-brief.md
- docs/OVERVIEW.md
- docs/plan.md
- .codex/skills/comfy-blender-vrm/SKILL.md
- .codex/skills/comfy-blender-vrm/references/pipeline.md
- .codex/skills/comfy-blender-vrm/references/character_brief.md
- .codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py
- .codex/skills/comfy-blender-vrm/scripts/generate_character_from_brief.py

## 差分仕様
- DS-01:
  - Given: ユーザーが workflow JSON と、対話入力または brief JSON を指定する。
  - When: `generate-character-from-brief` を実行する。
  - Then: キャラクター brief を収集し、ベース画像生成用の `character_prompt` を合成する。
- DS-02:
  - Given: `character_prompt` が合成できている。
  - When: コマンドが既存の生成処理を呼ぶ。
  - Then: `generate-character-sheet` と同等の出力を行い、brief と prompt も保存する。
- DS-03:
  - Given: brief JSON 不正、brief 必須項目不足、workflow 失敗のいずれかがある。
  - When: コマンドが終了する。
  - Then: 次の行動が分かるメッセージを出し、非 0 の終了ステータスを返す。

## 受入条件（Acceptance Criteria）
- AC-01: `generate-character-from-brief` の入力として workflow JSON、任意の brief JSON、対話入力モード、任意の seed、任意の config パスが Skill ドキュメント上で定義されている。
- AC-02: 対話入力または brief JSON から `character_prompt` を合成でき、brief JSON と prompt preview を成果物として保存できる。
- AC-03: ベース画像生成成功時に、既存の character sheet 成果物に加えて brief 情報が `output_dir` 配下へ保存される。
- AC-04: brief ファイル不足、brief JSON 不正、brief 必須項目不足、workflow / ComfyUI 側の生成失敗の少なくとも 4 種の失敗に対して、次の行動が分かるメッセージが定義される。
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
- 生成本体は既存の `generate-character-sheet` と同じ workflow 実行経路を使う。
- brief の質問数は最小限に保ち、標準ライブラリ中心で構成する。
- brief 収集は CLI 対話か JSON 読込に限定し、GUI は追加しない。

## Review Gate
- required: No
- reason: Phase 1.5 の単一コマンドに閉じた差分であり、既存生成処理の前段ラッパに留まる。

## 未確定事項
- Q-01: Resolved. brief の必須項目は `core_concept` のみとした。
- Q-02: Resolved. prompt は full-body / front-facing / base sheet 用の既定文言を付与し、optional fields を追加する形にした。
- Q-03: Resolved. `brief.json` と `prompt-preview.txt` は character output 配下へ保存し、metadata にも brief 情報を残す形にした。

## Step 2: delta-apply
- changed files:
  - .codex/skills/comfy-blender-vrm/SKILL.md
  - .codex/skills/comfy-blender-vrm/references/pipeline.md
  - .codex/skills/comfy-blender-vrm/references/character_brief.md
  - .codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py
  - .codex/skills/comfy-blender-vrm/scripts/generate_character_from_brief.py
  - docs/delta/DR-20260313-generate-character-from-brief.md
- applied AC:
  - AC-01:
    - 変更: `SKILL.md` に `generate-character-from-brief` の interactive 実行例と `--brief-file` 実行例を追加した。
    - 根拠: workflow JSON、brief JSON、対話入力モード、seed、config の入口を明示した。
  - AC-02:
    - 変更: `generate_character_from_brief.py` で brief JSON 読込または CLI 対話入力を受け、`character_prompt` を合成し、`brief.json` と `prompt-preview.txt` を保存するようにした。
    - 根拠: 必須 `core_concept` と定義済み optional fields から prompt を組み立て、成功 run の character output 配下へ成果物を残す。
  - AC-03:
    - 変更: `generate_character_sheet.py` を関数化し、同一 workflow 実行経路をラッパから再利用できるようにした。
    - 根拠: `run_character_sheet_generation()` を通して既存の submitted workflow / history / image / metadata 保存経路を共有し、brief 情報を metadata にも追記する。
  - AC-04:
    - 変更: brief ファイル不足、brief JSON 不正、brief 必須項目不足、unsupported field、ComfyUI 失敗に対する `detail` / `next` を定義した。
    - 根拠: すべて `GenerationError(detail, next_action)` で扱い、次の行動が分かるメッセージを返す。
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
  - `generate_character_sheet.py`: 258 lines
  - `generate_character_from_brief.py`: 263 lines
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
  - static check: `python -m py_compile .codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py .codex/skills/comfy-blender-vrm/scripts/generate_character_from_brief.py`
  - targeted integration / E2E:
    - success case: `--brief-file` で prompt 合成、画像 download、brief / prompt preview / metadata 保存
    - success case: interactive input で prompt 合成、画像 download、brief / prompt preview 保存
    - failure case: brief file missing
    - failure case: brief JSON invalid
    - failure case: brief required field missing
    - failure case: ComfyUI prompt API HTTP 500
  - delta validator: `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- review delta outcome:
  - pass: Yes
  - follow-up delta seeds:
    - `build-vrm-base` request
- AC result table:
  - AC-01: PASS
    - 根拠: `SKILL.md` に interactive 実行と `--brief-file` 実行の両方を記載した。
  - AC-02: PASS
    - 根拠: success case で `brief.json` と `prompt-preview.txt` が character output 配下に保存され、submitted workflow に合成 prompt が反映された。
  - AC-03: PASS
    - 根拠: success case で既存の character sheet 成果物に加え、brief 情報と metadata 追記が保存された。
  - AC-04: PASS
    - 根拠: missing brief file、invalid brief JSON、missing required field、ComfyUI HTTP 500 の 4 種で `detail` と `next` を確認した。
  - AC-05: PASS
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
  - success case では mock ComfyUI への prompt submit が 2 回行われ、brief-file run と interactive run の両方が完了した。
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
  - 目的: ユーザー brief から `character_prompt` を合成し、既存生成経路でベース画像を作れるようにする
  - 変更対象: brief 収集、prompt 合成、character sheet 実行経路の再利用、brief / prompt preview / metadata 保存
  - 非対象: 自由対話エージェント、画像評価ループ、比較ランキング、Blender 連携、表情生成、モーション適用
- unresolved items:
  - なし
- follow-up delta seeds:
  - `build-vrm-base` request
