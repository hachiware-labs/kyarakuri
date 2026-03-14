# アーキテクチャ

入口は `docs/OVERVIEW.md`。レイヤー責務・依存方向・主要I/Fを明文化する。

## レイヤー責務
- Skill entry:
  - `.codex/skills/forma-character/SKILL.md`
  - `forma-character-*` 名の canonical command、既定 config、相対パス解決ルールを示す
- CLI/application:
  - `.codex/skills/forma-character/scripts/doctor.py`
  - 引数解決、設定読込、チェック実行、標準出力、終了コードを担当する
- Local adapters:
  - ComfyUI HTTP probe
  - Blender executable path check
  - workflow / output directory check

## 依存方向
- Canonical skill entry -> same-pack CLI/application -> Local adapters -> ローカルファイルシステム / ローカル HTTP
- ComfyUI と Blender は `doctor` から直接利用確認するだけとし、相互依存を持たせない

## 主要 I/F
- Command:
  - `python .codex/skills/forma-character/scripts/prepare_environment.py`
  - `python .codex/skills/forma-character/scripts/generate_base_image.py --workflow <path> [--brief-file <path>]`
  - `python .codex/skills/forma-character/scripts/generate_expressions.py --workflow <path> --base-image <path> --character-prompt <text>`
  - `python .codex/skills/forma-character/scripts/build_vrm.py --blend-file <path> [--texture-image <path>]`
  - `python .codex/skills/forma-character/scripts/apply_motion_preview.py --blend-file <path> --motion-file <path>`
- Config keys:
  - `comfyui_url`
  - `blender_path`
  - `workflow_dir`
  - `output_dir`

## `forma-character` 構成
- Skill entry:
  - `.codex/skills/forma-character/SKILL.md`
  - public command 名、canonical 実装、既定 config を定義する
- Public entry scripts:
  - `.codex/skills/forma-character/scripts/_wrapper_common.py`
  - `.codex/skills/forma-character/scripts/prepare_environment.py`
  - `.codex/skills/forma-character/scripts/generate_base_image.py`
  - `.codex/skills/forma-character/scripts/generate_expressions.py`
  - `.codex/skills/forma-character/scripts/build_vrm.py`
  - `--config` 未指定時に `config/forma-character.json` を注入し、同 skill pack 内の canonical 実装を呼ぶ
- Canonical implementation:
  - `.codex/skills/forma-character/scripts/doctor.py`
  - `.codex/skills/forma-character/scripts/generate_character_sheet.py`
  - `.codex/skills/forma-character/scripts/generate_character_from_brief.py`
  - `.codex/skills/forma-character/scripts/generate_expression_sheet.py`
  - `.codex/skills/forma-character/scripts/build_vrm_base.py`
  - `.codex/skills/forma-character/scripts/apply_motion_preview.py`
  - `.codex/skills/forma-character/scripts/comfy_helpers.py`
  - `.codex/skills/forma-character/blender/build_vrm_base.py`
  - `.codex/skills/forma-character/blender/apply_motion_preview.py`
- Repo-local config:
  - `config/forma-character.json`
  - new skill pack 用の既定 path を保持する

## `generate-character-sheet` 構成
- CLI/application:
  - `.codex/skills/forma-character/scripts/generate_character_sheet.py`
  - 引数解決、project 名導出、run_id 生成、submitted workflow 作成、成果物保存、および再利用可能な生成経路 `run_character_sheet_generation()` を担当する
- Local adapters:
  - `.codex/skills/forma-character/scripts/comfy_helpers.py`
  - config 読込、workflow 検証、placeholder 展開、ComfyUI HTTP 通信、polling、画像ダウンロードを担当する
- Workflow contract:
  - `.codex/skills/forma-character/workflows/README.md`
  - API-format workflow とサポート対象プレースホルダを定義する
  - `.codex/skills/forma-character/workflows/neta-yume-lumina-base.api.json`
  - 2026-03-04 のローカル成功 PNG metadata 由来の bundled base-image workflow を保持する
  - `.codex/skills/forma-character/workflows/neta-yume-lumina-base-transparent.api.json`
  - 既存 base workflow に white background keying を追加した transparent PNG 向け bundled workflow を保持する

## `generate-character-from-brief` 構成
- CLI/application:
  - `.codex/skills/forma-character/scripts/generate_character_from_brief.py`
  - brief JSON 読込または CLI 対話入力、`character_name` を含む brief 検証、standing full-body / backgroundless / no text overlay default を含む `character_prompt` 合成、project 直下 brief と run 配下 brief / prompt preview 保存指定を担当する
- Shared application path:
  - `.codex/skills/forma-character/scripts/generate_character_sheet.py`
  - 既存の ComfyUI submit / polling / image download / metadata 保存経路を再利用する
- Brief contract:
  - `.codex/skills/forma-character/references/character_brief.md`
  - brief の必須 / 任意フィールドと保存成果物を定義する
  - `character_name` がある場合は project 名導出に優先し、なければ `core_concept` を使う
  - `background` field は後方互換のため保持するが、base image prompt には反映しない

## `generate-expression-sheet` 構成
- CLI/application:
  - `.codex/skills/forma-character/scripts/generate_expression_sheet.py`
  - expression list 解決、base image path からの project 名引継ぎ、base seed 展開、expression ごとの submitted workflow 作成、成果物保存を担当する
- Local adapters:
  - `.codex/skills/forma-character/scripts/comfy_helpers.py`
  - base image upload、ComfyUI HTTP 通信、polling、画像ダウンロードを担当する
- Workflow contract:
  - `.codex/skills/forma-character/workflows/README.md`
  - `expression_name` と `base_image*` placeholder を含む workflow 契約を定義する
  - `.codex/skills/forma-character/workflows/neta-yume-lumina-expressions.api.json`
  - 2026-03-14 のローカル成功 expression run 由来の bundled image-to-image workflow を保持する
  - `.codex/skills/forma-character/workflows/neta-yume-lumina-expressions-transparent.api.json`
  - 既存 expression workflow に white background keying を追加した transparent PNG 向け bundled workflow を保持する

## `build-vrm-base` 構成
- CLI/application:
  - `.codex/skills/forma-character/scripts/build_vrm_base.py`
  - config 読込、`.blend` / texture 解決、run dir 作成、Blender background process 起動、metadata 保存を担当する
- Blender script:
  - `.codex/skills/forma-character/blender/build_vrm_base.py`
  - scene 内の first mesh material 更新、camera / light 補完、updated `.blend` 保存、review render 出力を担当する
- Public wrapper:
  - `.codex/skills/forma-character/scripts/build_vrm.py`
  - repo-local public 名 `forma-character-build-vrm` と既定 config 注入を担当する

## `apply-motion-preview` 構成
- CLI/application:
  - `.codex/skills/forma-character/scripts/apply_motion_preview.py`
  - config 読込、`.blend` / `BVH` 解決、run dir 作成、Blender background process 起動、metadata 保存を担当する
- Blender script:
  - `.codex/skills/forma-character/blender/apply_motion_preview.py`
  - first armature への action 割当、camera / light 補完、updated `.blend` 保存、preview render 出力を担当する
- Public entry:
  - `.codex/skills/forma-character/scripts/apply_motion_preview.py`
  - repo-local public 名 `forma-character-apply-motion-preview` の canonical 実装を担当する

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
- project output infer
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

## Verify Strategy
- 主力 verify:
  - mock ComfyUI / fake Blender を使い、差分単位の成功系と失敗系を再現可能に確認する
- smoke verify:
  - 実 ComfyUI を使い、主要機能が現行ローカル環境で通ることを確認する
  - 初期対象は `generate-character-from-brief` と `generate-expression-sheet` を想定する
  - `generate-character-from-brief` の smoke verify seed には bundled workflow `neta-yume-lumina-base.api.json` を使える
  - `generate-expression-sheet` の smoke verify seed には bundled workflow `neta-yume-lumina-expressions.api.json` を使える
  - transparent background smoke verify seed には `neta-yume-lumina-base-transparent.api.json` と `neta-yume-lumina-expressions-transparent.api.json` を使える
  - 実 ComfyUI smoke verify の固定 workflow / fixed prompt / 出力確認は follow-up delta で定義する
