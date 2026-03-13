# アーキテクチャ

入口は `docs/OVERVIEW.md`。レイヤー責務・依存方向・主要I/Fを明文化する。

## レイヤー責務
- Skill entry:
  - `.codex/skills/comfy-blender-vrm/SKILL.md`
  - 実行方法、既定 config、相対パス解決ルールを示す
- CLI/application:
  - `.codex/skills/comfy-blender-vrm/scripts/doctor.py`
  - 引数解決、設定読込、チェック実行、標準出力、終了コードを担当する
- Local adapters:
  - ComfyUI HTTP probe
  - Blender executable path check
  - workflow / output directory check

## 依存方向
- Skill entry -> CLI/application -> Local adapters -> ローカルファイルシステム / ローカル HTTP
- ComfyUI と Blender は `doctor` から直接利用確認するだけとし、相互依存を持たせない

## 主要 I/F
- Command:
  - `python .codex/skills/comfy-blender-vrm/scripts/doctor.py`
  - `python .codex/skills/comfy-blender-vrm/scripts/doctor.py --config <path>`
  - `python .codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py --workflow <path> --character-prompt <text>`
  - `python .codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py --workflow <path> --base-image <path> --character-prompt <text>`
- Config keys:
  - `comfyui_url`
  - `blender_path`
  - `workflow_dir`
  - `output_dir`

## `generate-character-sheet` 構成
- CLI/application:
  - `.codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py`
  - 引数解決、run_id 生成、submitted workflow 作成、成果物保存を担当する
- Local adapters:
  - `.codex/skills/comfy-blender-vrm/scripts/comfy_helpers.py`
  - config 読込、workflow 検証、placeholder 展開、ComfyUI HTTP 通信、polling、画像ダウンロードを担当する
- Workflow contract:
  - `.codex/skills/comfy-blender-vrm/workflows/README.md`
  - API-format workflow とサポート対象プレースホルダを定義する

## `generate-expression-sheet` 構成
- CLI/application:
  - `.codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py`
  - expression list 解決、base seed 展開、expression ごとの submitted workflow 作成、成果物保存を担当する
- Local adapters:
  - `.codex/skills/comfy-blender-vrm/scripts/comfy_helpers.py`
  - base image upload、ComfyUI HTTP 通信、polling、画像ダウンロードを担当する
- Workflow contract:
  - `.codex/skills/comfy-blender-vrm/workflows/README.md`
  - `expression_name` と `base_image*` placeholder を含む workflow 契約を定義する

## 状態遷移
- config load
- setting resolve
- environment checks
- summary output
- exit 0 / non-0
- workflow load
- placeholder render
- prompt submit
- history poll
- image download
- metadata write
- exit 0 / non-0
- base image upload
- per-expression loop
- per-expression save

## エラー設計
- 設定ファイル不足
- JSON 不正
- ComfyUI 未到達
- Blender パス不正
- workflow ディレクトリ不足
- output ディレクトリ作成失敗
- workflow ファイル不足
- workflow 形式不正
- 未解決プレースホルダ
- prompt API 失敗
- image download 失敗
