# アーキテクチャ

入口は `docs/OVERVIEW.md`。レイヤー責務・依存方向・主要I/Fを明文化する。

## レイヤー責務
- Skill entry:
  - `.codex/skills/comfy-blender-vrm/SKILL.md`
  - 実行方法、既定 config、相対パス解決ルールを示す
- Repo-local public skill entry:
  - `.codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md`
  - `kyarakuri-*` 名の wrapper command と repo-local trial 用 config を示す
- CLI/application:
  - `.codex/skills/comfy-blender-vrm/scripts/doctor.py`
  - 引数解決、設定読込、チェック実行、標準出力、終了コードを担当する
- Local adapters:
  - ComfyUI HTTP probe
  - Blender executable path check
  - workflow / output directory check

## 依存方向
- Skill entry -> CLI/application -> Local adapters -> ローカルファイルシステム / ローカル HTTP
- Repo-local public skill entry -> wrapper scripts -> existing CLI/application -> Local adapters
- ComfyUI と Blender は `doctor` から直接利用確認するだけとし、相互依存を持たせない

## 主要 I/F
- Command:
  - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/prepare_environment.py`
  - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py --workflow <path> [--brief-file <path>]`
  - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expressions.py --workflow <path> --base-image <path> --character-prompt <text>`
  - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/build_vrm.py --blend-file <path> [--texture-image <path>]`
  - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/apply_motion_preview.py --blend-file <path> --motion-file <path>`
  - `python .codex/skills/comfy-blender-vrm/scripts/doctor.py`
  - `python .codex/skills/comfy-blender-vrm/scripts/doctor.py --config <path>`
  - `python .codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py --workflow <path> --character-prompt <text>`
  - `python .codex/skills/comfy-blender-vrm/scripts/generate_character_from_brief.py --workflow <path> [--brief-file <path>]`
  - `python .codex/skills/comfy-blender-vrm/scripts/generate_expression_sheet.py --workflow <path> --base-image <path> --character-prompt <text>`
  - `python .codex/skills/comfy-blender-vrm/scripts/build_vrm_base.py --blend-file <path> [--texture-image <path>]`
  - `python .codex/skills/comfy-blender-vrm/scripts/apply_motion_preview.py --blend-file <path> --motion-file <path>`
- Config keys:
  - `comfyui_url`
  - `blender_path`
  - `workflow_dir`
  - `output_dir`

## `kyarakuri-comfy-blender-vrm` 構成
- Skill entry:
  - `.codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md`
  - public command 名、repo-local trial の位置づけ、既定 config を定義する
- Wrapper scripts:
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/_wrapper_common.py`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/prepare_environment.py`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expressions.py`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/build_vrm.py`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/apply_motion_preview.py`
  - `--config` 未指定時に `config/kyarakuri-comfy-blender-vrm.json` を注入し、既存実装へ委譲する
- Repo-local config:
  - `config/kyarakuri-comfy-blender-vrm.json`
  - new skill pack 用の既定 path を保持する

## `generate-character-sheet` 構成
- CLI/application:
  - `.codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py`
  - 引数解決、run_id 生成、submitted workflow 作成、成果物保存、および再利用可能な生成経路 `run_character_sheet_generation()` を担当する
- Local adapters:
  - `.codex/skills/comfy-blender-vrm/scripts/comfy_helpers.py`
  - config 読込、workflow 検証、placeholder 展開、ComfyUI HTTP 通信、polling、画像ダウンロードを担当する
- Workflow contract:
  - `.codex/skills/comfy-blender-vrm/workflows/README.md`
  - API-format workflow とサポート対象プレースホルダを定義する

## `generate-character-from-brief` 構成
- CLI/application:
  - `.codex/skills/comfy-blender-vrm/scripts/generate_character_from_brief.py`
  - brief JSON 読込または CLI 対話入力、brief 検証、`character_prompt` 合成、brief / prompt preview 保存指定を担当する
- Shared application path:
  - `.codex/skills/comfy-blender-vrm/scripts/generate_character_sheet.py`
  - 既存の ComfyUI submit / polling / image download / metadata 保存経路を再利用する
- Brief contract:
  - `.codex/skills/comfy-blender-vrm/references/character_brief.md`
  - brief の必須 / 任意フィールドと保存成果物を定義する

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

## `build-vrm-base` 構成
- CLI/application:
  - `.codex/skills/comfy-blender-vrm/scripts/build_vrm_base.py`
  - config 読込、`.blend` / texture 解決、run dir 作成、Blender background process 起動、metadata 保存を担当する
- Blender script:
  - `.codex/skills/comfy-blender-vrm/blender/build_vrm_base.py`
  - scene 内の first mesh material 更新、camera / light 補完、updated `.blend` 保存、review render 出力を担当する
- Public wrapper:
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/build_vrm.py`
  - repo-local public 名 `kyarakuri-build-vrm` と既定 config 注入を担当する

## `apply-motion-preview` 構成
- CLI/application:
  - `.codex/skills/comfy-blender-vrm/scripts/apply_motion_preview.py`
  - config 読込、`.blend` / `BVH` 解決、run dir 作成、Blender background process 起動、metadata 保存を担当する
- Blender script:
  - `.codex/skills/comfy-blender-vrm/blender/apply_motion_preview.py`
  - first armature への action 割当、camera / light 補完、updated `.blend` 保存、preview render 出力を担当する
- Public wrapper:
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/apply_motion_preview.py`
  - repo-local public 名 `kyarakuri-apply-motion-preview` と既定 config 注入を担当する

## 状態遷移
- config load
- setting resolve
- environment checks
- summary output
- exit 0 / non-0
- brief collect
- brief validate
- character prompt synthesize
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
- blender subprocess launch
- blend save
- review render save
- motion import
- action assign
- preview render save

## エラー設計
- 設定ファイル不足
- JSON 不正
- ComfyUI 未到達
- Blender パス不正
- workflow ディレクトリ不足
- output ディレクトリ作成失敗
- brief ファイル不足
- brief JSON 不正
- brief 必須項目不足
- workflow ファイル不足
- workflow 形式不正
- 未解決プレースホルダ
- prompt API 失敗
- image download 失敗
- `.blend` 不足
- `BVH` 不足
- texture image 不足
- Blender 実行失敗
- review render 不足
- preview render 不足
