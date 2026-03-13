# delta-request

## Delta ID
- DR-20260313-doctor-command

## Delta Type
- FEATURE

## 目的
- ComfyUI / Blender / 必須ディレクトリの利用可否を、Skill から 1 コマンドで確認できるようにする。
- Phase 1 の着手点として、ローカル環境の前提不足を先に可視化する。

## 変更対象（In Scope）
- `doctor` コマンドの最小インターフェースを定義する。
- 設定ファイルから `comfyui_url`、`blender_path`、`workflow_dir`、`output_dir` を解決する。
- ComfyUI 接続可否、Blender 実行ファイルの存在、必須ディレクトリの存在または生成可否を確認する。
- 失敗時に次の行動が分かるメッセージと終了ステータスの要件を定義する。

## 非対象（Out of Scope）
- `generate-character-sheet`、`generate-expression-sheet`、`build-vrm-base`、`apply-motion-preview` の実装。
- ComfyUI 本体、Blender 本体、GPU ドライバのインストールや起動代行。
- workflow JSON の内容検証や画像生成実行。
- VRM 生成、モーション適用、レビュー画像出力。

## Candidate Files/Artifacts
- docs/delta/DR-20260313-doctor-command.md
- docs/OVERVIEW.md
- docs/plan.md
- .codex/skills/comfy-blender-vrm/SKILL.md
- .codex/skills/comfy-blender-vrm/scripts/doctor.py
- .codex/skills/comfy-blender-vrm/references/pipeline.md
- config/comfy-blender-vrm.json

## 差分仕様
- DS-01:
  - Given: `doctor` コマンドが設定ファイルパス、または既定設定パスを受け取れる。
  - When: ユーザーが `doctor` を実行する。
  - Then: `comfyui_url`、`blender_path`、`workflow_dir`、`output_dir` の解決結果を表示し、未設定キーがあれば不足項目として列挙する。
- DS-02:
  - Given: 設定値が解決できている。
  - When: `doctor` が環境確認を実行する。
  - Then: ComfyUI の到達可否、Blender 実行ファイルの存在、`workflow_dir` の存在、`output_dir` の存在または生成可否を項目ごとに判定する。
- DS-03:
  - Given: 1 件以上の確認失敗がある。
  - When: `doctor` が終了する。
  - Then: 失敗項目ごとに次の行動が分かるメッセージを出し、非 0 の終了ステータスを返す。
- DS-04:
  - Given: 全項目が確認済みである。
  - When: `doctor` が終了する。
  - Then: 成功項目の一覧を表示し、0 の終了ステータスを返す。

## 受入条件（Acceptance Criteria）
- AC-01: `doctor` の入力として設定ファイルパスの明示指定、または既定設定パスの利用方法が Skill ドキュメント上で定義されている。
- AC-02: `doctor` 実行時に `comfyui_url`、`blender_path`、`workflow_dir`、`output_dir` の確認結果が個別に出力される。
- AC-03: `output_dir` が未作成でも、作成可能な場合は作成して成功として扱う。
- AC-04: ComfyUI 未起動、Blender パス不正、workflow ディレクトリ不足、出力先作成失敗の少なくとも 4 種の失敗に対して、次の行動が分かるメッセージが定義される。
- AC-05: 全項目成功時は終了コード 0、1 件以上失敗時は非 0 で終了する。

## Verify Profile
- static check: Required
- targeted unit: Not Required
- targeted integration / E2E: Required
- delta-project-validator: links-only

## Canonical Sync Mode
- mode: post-archive sync
- reason: request 時点では Scope と AC のみを固定し、正本の詳細同期は apply/verify 完了後に最小差分で行う。

## 制約
- ローカル導入済みの ComfyUI / Blender を前提にし、インストール処理は追加しない。
- Windows 優先のパス解決を前提にするが、将来の他 OS 展開を阻害する固定実装は避ける。
- 追加依存は最小限にし、可能なら標準ライブラリ中心で構成する。
- `doctor` は環境を確認するだけとし、ComfyUI workflow 実行や Blender の本処理起動は行わない。

## Review Gate
- required: No
- reason: Phase 1 の単一コマンドに閉じた最小機能であり、現時点ではレイヤー横断の大規模変更を伴わない。

## 未確定事項
- Q-01: Resolved. 既定の設定ファイル配置は `config/comfy-blender-vrm.json` とした。
- Q-02: Resolved. ComfyUI の疎通確認は `/system_stats` を優先し、失敗時は `/queue` を代替 probe とする。
- Q-03: Resolved. `workflow_dir` は存在必須とし、自動生成は行わない。

## Step 2: delta-apply
- changed files:
  - .codex/skills/comfy-blender-vrm/SKILL.md
  - .codex/skills/comfy-blender-vrm/references/pipeline.md
  - .codex/skills/comfy-blender-vrm/scripts/doctor.py
  - config/comfy-blender-vrm.json
  - docs/delta/DR-20260313-doctor-command.md
- applied AC:
  - AC-01:
    - 変更: `SKILL.md` に `doctor` の実行方法、既定設定パス、相対パス解決ルールを記載した。
    - 根拠: `python .codex/skills/comfy-blender-vrm/scripts/doctor.py` と `--config` の利用方法を明示した。
  - AC-02:
    - 変更: `doctor.py` で `comfyui_url`、`blender_path`、`workflow_dir`、`output_dir` の解決結果と個別チェック結果を出力するようにした。
    - 根拠: `Resolved settings` と `Checks` の 2 セクションで設定解決と実行結果を分離して表示する。
  - AC-03:
    - 変更: `output_dir` が未作成の場合に `mkdir(parents=True, exist_ok=True)` で作成し、成功として扱う処理を追加した。
    - 根拠: `check_output_dir` で生成成功時に `Created output directory` を返す。
  - AC-04:
    - 変更: ComfyUI 未起動、Blender パス不正、workflow ディレクトリ不足、出力先作成失敗/不正の各ケースに次の行動を含むメッセージを定義した。
    - 根拠: `CheckResult.next_action` を各失敗分岐に設定した。
  - AC-05:
    - 変更: 失敗件数を集計し、失敗 0 件で 0、それ以外で 1 を返す終了コード判定を実装した。
    - 根拠: `main()` の `failures` 集計と `return 0 if failures == 0 else 1`。
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
  - longest source file: `.codex/skills/comfy-blender-vrm/scripts/doctor.py` = 322 lines
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
  - static check: `python -m py_compile .codex/skills/comfy-blender-vrm/scripts/doctor.py`
  - targeted integration / E2E:
    - `python .codex/skills/comfy-blender-vrm/scripts/doctor.py`
    - temporary failure config with invalid ComfyUI / Blender / workflow_dir / output_dir target
    - temporary success config with mock HTTP server, valid Blender path, existing workflow_dir, and auto-created output_dir
  - delta validator: `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- review delta outcome:
  - pass: Yes
  - follow-up delta seeds:
    - `generate-character-sheet` request
    - `generate-expression-sheet` request
- AC result table:
  - AC-01: PASS
    - 根拠: `SKILL.md` に既定 config と `--config` 指定の両方を記載した。
  - AC-02: PASS
    - 根拠: 既定 config 実行と temporary config 実行で 4 設定の解決結果と個別チェック結果を確認した。
  - AC-03: PASS
    - 根拠: success config 実行で未作成 `output_dir` が生成され、`Created output directory` と exit code 0 を確認した。
  - AC-04: PASS
    - 根拠: failure config 実行で ComfyUI 未起動、Blender パス不正、workflow ディレクトリ不足、output path が directory ではないケースの `next` メッセージを確認した。
  - AC-05: PASS
    - 根拠: failure config 実行は exit code 1、success config 実行は exit code 0 を確認した。
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
  - default config execution currently fails on ComfyUI not running and missing workflow directory, which is expected and produces actionable guidance.
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
  - 目的: `doctor` でローカル環境の前提不足を 1 コマンドで可視化する
  - 変更対象: config 解決、ComfyUI / Blender / workflow / output の確認、終了コードと案内メッセージ
  - 非対象: 画像生成、VRM 構築、モーション適用、インストール代行
- unresolved items:
  - なし
- follow-up delta seeds:
  - `generate-character-sheet` request
  - `generate-expression-sheet` request
