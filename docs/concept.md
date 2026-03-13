# コンセプト

入口は `docs/OVERVIEW.md`。ここには機能一覧（Spec ID）とフェーズをまとめる。

## 現在フェーズ
- P0

## 機能一覧
- SP-DOCTOR-001:
  - 名称: `doctor`
  - 目的: ローカルの ComfyUI / Blender / workflow / output 設定の利用可否を、実装前に 1 コマンドで確認する。
  - 状態: 実装済み / archive 済み
- SP-GCS-001:
  - 名称: `generate-character-sheet`
  - 目的: API-format ComfyUI workflow からキャラクター立ち絵を生成し、画像と再現メタを保存する。
  - 状態: 実装済み / archive 済み
- SP-GES-001:
  - 名称: `generate-expression-sheet`
  - 目的: ベース画像から複数表情を生成し、expression ごとの画像群と再現メタを保存する。
  - 状態: 実装済み / archive 済み

## Phase 1 の到達点
- `doctor`: 実装済み
- `generate-character-sheet`: 実装済み
- `generate-expression-sheet`: 実装済み

## 非ゴール
- ComfyUI や Blender 本体のインストール代行
- workflow 実行や VRM 生成そのもの
