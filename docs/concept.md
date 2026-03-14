# コンセプト

入口は `docs/OVERVIEW.md`。ここには機能一覧（Spec ID）とフェーズをまとめる。

## 現在フェーズ
- P0

## Repo-local public skill pack
- 名称: `kyarakuri-comfy-blender-vrm`
- 役割: repo 内で `kyarakuri-*` の public name を試し、そのまま release seed にする canonical implementation skill pack
- output layout:
  - `outputs/<project-name>/brief.json`
  - `outputs/<project-name>/images/base/<run-id>/...`
  - `outputs/<project-name>/images/expressions/<run-id>/<expression>/...`
- bundled workflow:
  - `neta-yume-lumina-base.api.json`
  - 2026-03-04 のローカル成功 PNG metadata 由来の base-image 用 workflow
  - `neta-yume-lumina-base-transparent.api.json`
  - 2026-03-14 に repo 内へ追加した transparent PNG 向け base-image workflow
  - `neta-yume-lumina-expressions.api.json`
  - 2026-03-14 のローカル成功 expression run 由来の image-to-image workflow
  - `neta-yume-lumina-expressions-transparent.api.json`
  - 2026-03-14 に repo 内へ追加した transparent PNG 向け expression workflow
- 実装済み public commands:
  - `kyarakuri-prepare-environment`
  - `kyarakuri-generate-base-image`
  - `kyarakuri-generate-expressions`
  - `kyarakuri-build-vrm`
  - `kyarakuri-apply-motion-preview`

## Legacy compatibility skill pack
- 名称: `comfy-blender-vrm`
- 役割: 旧 CLI 名と `config/comfy-blender-vrm.json` を維持する compatibility layer
- 実装方式: `.codex/skills/kyarakuri-comfy-blender-vrm/` の canonical 実装を呼び出す

## 機能一覧
- SP-DOCTOR-001:
  - 名称: `doctor`
  - 目的: ローカルの ComfyUI / Blender / workflow / output 設定の利用可否を、実装前に 1 コマンドで確認する。
  - 状態: 実装済み / archive 済み
- SP-GCS-001:
  - 名称: `generate-character-sheet`
  - 目的: API-format ComfyUI workflow からキャラクター立ち絵を生成し、画像と再現メタを保存する。
  - 状態: 実装済み / archive 済み
- SP-GCFB-001:
  - 名称: `generate-character-from-brief`
  - 目的: ユーザー brief を収集し、ベース画像生成用の `character_prompt` を合成して、画像と brief を一緒に保存する。
  - 状態: 実装済み / archive 済み
- SP-GES-001:
  - 名称: `generate-expression-sheet`
  - 目的: ベース画像から複数表情を生成し、expression ごとの画像群と再現メタを保存する。
  - 状態: 実装済み / archive 済み
- SP-BVB-001:
  - 名称: `build-vrm-base`
  - 目的: Blender background mode で既存 `.blend` を処理し、更新済み `.blend` と review render を保存する。
  - 状態: 実装済み / archive 済み
- SP-AMP-001:
  - 名称: `apply-motion-preview`
  - 目的: Blender background mode で既存 `.blend` に既存 `BVH` motion を適用し、更新済み `.blend` と preview render を保存する。
  - 状態: 実装済み / archive 済み

## Phase 1 の到達点
- `doctor`: 実装済み
- `generate-character-sheet`: 実装済み
- `generate-character-from-brief`: 実装済み
- `generate-expression-sheet`: 実装済み

## Phase 2 の現在地
- `build-vrm-base`: 実装済み
- `apply-motion-preview`: 実装済み

## 非ゴール
- ComfyUI や Blender 本体のインストール代行
- workflow 実行や VRM 生成そのもの
