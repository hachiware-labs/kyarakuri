# ComfyUI / Blender 統合 Skill パック 要件定義

## 1. 目的

ローカル環境にインストール済みの **ComfyUI** と **Blender** を、軽量な Skill パックから一括利用できるようにし、以下の 3 点を効率よく実現する。

1. キャラクター画像の作成
2. キャラクター画像に基づく 3D VRM の作成
3. モーションの適用・確認

本要件では、**MCP や常駐対話制御を前提にしない**。  
ComfyUI は API 実行、Blender は CLI / background mode 実行を基本とし、Codex などから利用可能な Skill パックとして構成する。

---

## 2. 背景

ComfyUI は画像生成ワークフローの再利用に強く、Blender は CLI から Python スクリプト実行が可能である。  
一方で、MCP ベースの常駐接続は柔軟である反面、構成が重くなりやすい。

今回の主目的は、Blender や ComfyUI を対話的に細かく操作することではなく、以下のような **制作パイプラインの自動化** である。

- キャラ画像を作る
- 必要な表情差分を用意する
- ベース 3D に反映して VRM を整備する
- 既存モーションを適用し、確認用出力を得る

したがって、最初の実装は **軽量・再現性・ローカル完結** を優先する。

---

## 3. スコープ

### 3.1 対象範囲

本 Skill パックが対象とするのは、以下の機能である。

#### A. キャラクター画像生成
- ComfyUI workflow を用いたキャラクター画像生成
- 正面立ち絵の生成
- 表情差分シートの生成
- 再生成しやすい入力管理

#### B. VRM 作成支援
- Blender background mode による処理実行
- ベース素体または既存メッシュへの素材適用
- 表情用 shape key / expression 準備
- レビュー用レンダ画像出力
- VRM 化の前段階整理

#### C. モーション適用支援
- 既存モーションデータの読み込み
- キャラクターへの適用
- 確認用レンダまたはプレビュー出力
- 将来的な VRMA 対応を見据えた設計

### 3.2 対象外

初版では以下を対象外とする。

- Blender のリアルタイム遠隔操作
- viewport 常時監視
- MCP サーバーの必須化
- 完全自動の 3D モデル生成品質保証
- 完全自動の高品質モーション生成
- Unity 依存の正式 VRMA 書き出し自動化
- 商用品質の rig 自動作成保証

---

## 4. 想定ユーザー

### 4.1 主対象
- ローカルに ComfyUI / Blender を導入済みの開発者
- キャラクター制作を半自動化したい個人開発者
- VRM アバター制作フローを Skill 化したいユーザー

### 4.2 前提知識
- ComfyUI の workflow JSON を保存・利用できる
- Blender を CLI から実行できる
- 基本的なファイル操作と Python 実行が可能

---

## 5. ゴール

### 5.1 MVP ゴール

以下が通れば MVP とする。

1. Skill から ComfyUI workflow を呼び出せる
2. キャラクター画像と表情シートを生成できる
3. Blender background mode でレビュー用レンダを出せる
4. 既存モーションを適用して確認できる
5. 一連の成果物が決まったディレクトリに整理される

### 5.2 成果物

最低限、以下の成果物を出力する。

- キャラクター画像
- 表情差分画像
- Blender 作業ファイル
- レビュー用レンダ画像
- モーション確認用出力
- 実行ログ
- 設定ファイル

---

## 6. システム方針

### 6.1 基本方針

- **ComfyUI は API 実行専用** とする
- **Blender は CLI / background mode 専用** とする
- **Skill は手順と実行入口を提供** する
- **MCP は必須にしない**
- **ローカル完結を優先** する

### 6.2 全体構成

```text
Skill Pack
 ├─ ComfyUI 実行ラッパ
 ├─ Blender 実行ラッパ
 ├─ 設定確認ツール
 ├─ workflow テンプレート
 ├─ Blender Python スクリプト
 └─ 要件 / 手順ドキュメント

ローカル環境
 ├─ ComfyUI
 ├─ Blender
 ├─ workflow JSON
 ├─ 素体 / 資産
 └─ 出力ディレクトリ
```

---

## 7. Skill パック要件

### 7.1 配布形態

Skill パックは、以下のような形で導入できること。

- npm パッケージ等による一括追加
- 指定ディレクトリへ Skill 一式を展開
- ローカル設定ファイルを生成
- AGENTS.md への追記またはテンプレート提供

### 7.2 Skill の役割

Skill は以下を行う。

- ComfyUI workflow 実行の呼び出し
- Blender background 実行の呼び出し
- 入出力ファイルの規約統一
- 処理順のガイド
- 失敗時の確認ポイント提示

### 7.3 Skill の非役割

Skill 自体は以下を持たない。

- ComfyUI 本体のインストール
- Blender 本体のインストール
- GPU ドライバの構成管理
- 高度な自動 rig 品質保証

---

## 8. 機能要件

## 8.1 環境確認

### 要件
- ComfyUI の接続先 URL を確認できること
- Blender 実行ファイルの場所を確認できること
- 必要なディレクトリを確認・生成できること
- 不足時に分かりやすいメッセージを出せること

### 入力
- 設定ファイル
- CLI 引数

### 出力
- 環境確認結果
- 不足項目一覧

---

## 8.2 キャラクター画像生成

### 要件
- ComfyUI workflow JSON を指定して実行できること
- キャラクター立ち絵を生成できること
- 同一キャラ向けの再生成がしやすいこと
- seed や主要パラメータを記録できること

### 入力
- workflow JSON
- キャラ設定文
- 参考画像（任意）
- 出力先

### 出力
- 立ち絵画像
- 実行ログ
- 実行時パラメータ

---

## 8.3 表情差分生成

### 要件
- 同一キャラの表情差分を複数生成できること
- 以下の最低限の表情候補を扱えること
  - neutral
  - smile
  - angry
  - sad
  - surprised
  - blink
- 将来的に lip sync 用口形へ拡張しやすい構成であること

### 入力
- ベースキャラ画像
- expression 用 workflow JSON
- 表情種別一覧

### 出力
- 表情差分画像群
- 表情一覧メタ情報

---

## 8.4 Blender ベース構築

### 要件
- Blender を background mode で起動できること
- ベース素体または既存 blend を読み込めること
- テクスチャや素材を適用できること
- レビュー用に静止画レンダを出力できること

### 入力
- blend ファイルまたは素体データ
- テクスチャ画像
- 設定ファイル

### 出力
- 更新済み blend
- レビュー用レンダ画像
- 処理ログ

---

## 8.5 表情データ準備

### 要件
- 表情用 shape key / expression 作業の補助ができること
- 必要表情一覧をレポートできること
- 手動調整が必要な箇所を明示できること

### 備考
初版では、完全自動の高品質生成を必須としない。  
まずは「必要な表情一覧を整理し、反映対象を明確にする」ことを優先する。

---

## 8.6 モーション適用

### 要件
- 既存モーションを読み込めること
- 既存の humanoid 系モーションを対象とすること
- キャラクターに適用して確認用出力を得られること
- モーション確認のための静止画または簡易アニメ出力ができること

### 初版方針
- 初版では **既存モーションの適用** を対象とする
- モーション生成は対象外とする
- まずは確認可能なことを重視する

### 想定入力
- BVH
- FBX
- 既存アニメーションクリップ相当の資産

### 想定出力
- モーション適用後の review render
- 確認用ログ

---

## 8.7 出力整理

### 要件
- 出力先ディレクトリを統一できること
- 画像、blend、ログ、設定を分けて保存できること
- 実行日時ベースの整理ができること
- 再現実行のための情報を保存できること

### 推奨ディレクトリ例

```text
outputs/
  character/
  expressions/
  blender/
  motion/
  review/
  logs/
```

---

## 9. 非機能要件

### 9.1 軽量性
- MCP 常駐を前提としないこと
- ローカルスクリプトベースで完結可能であること
- 不要な依存を増やしすぎないこと

### 9.2 再現性
- workflow JSON を版管理できること
- Blender スクリプトを再実行可能であること
- 入力パラメータを保存できること

### 9.3 可搬性
- Windows を優先する
- 将来的に macOS / Linux にも展開しやすい構造であること

### 9.4 拡張性
- 将来的に VRMA、lip sync、MCP、追加 workflow を組み込みやすいこと

### 9.5 保守性
- 各処理を小さなコマンド単位に分けること
- ComfyUI / Blender を疎結合に保つこと

---

## 10. 推奨コマンドセット

初版 Skill パックは、少なくとも以下の 4 コマンドを持つこと。

### 10.1 generate-character-sheet
- キャラクター画像を生成する
- 正面や参考角度を出力する

### 10.2 generate-expression-sheet
- 表情差分を生成する
- 表情一覧をメタ情報として保存する

### 10.3 build-vrm-base
- Blender background mode で素材を反映する
- レビュー用レンダを出す

### 10.4 apply-motion-preview
- 既存モーションを適用する
- 確認用出力を生成する

必要に応じて以下を追加する。

### 10.5 doctor
- 環境確認

### 10.6 export-review-renders
- 節目のレビュー画像をまとめて出力

---

## 11. モーション要件の整理

### 11.1 初版の方針

モーションは最初から生成しない。  
まずは **既存モーションを正しく適用し、確認できること** を優先する。

### 11.2 理由

- キャラクター画像生成と 3D 化だけでも負荷が高い
- モーション生成まで同時に自動化すると設計が重くなる
- 既存モーション適用だけでも価値が高い
- VRMA などへの拡張は後から追加できる

### 11.3 将来拡張

将来的には以下を検討する。

- BVH から VRMA への変換
- expression animation の組み込み
- gaze 制御
- lip sync 用口形との連携
- 動画参照からのモーション抽出

---

## 12. 想定ディレクトリ構成

```text
project-root/
├─ AGENTS.md
├─ .codex/
│  └─ skills/
│     └─ comfy-blender-vrm/
│        ├─ SKILL.md
│        ├─ scripts/
│        │  ├─ doctor.py
│        │  ├─ run_comfy.py
│        │  └─ run_blender.py
│        ├─ workflows/
│        │  ├─ character_sheet.json
│        │  └─ expression_sheet.json
│        ├─ blender/
│        │  ├─ build_vrm_base.py
│        │  └─ apply_motion_preview.py
│        └─ references/
│           └─ pipeline.md
├─ assets/
├─ outputs/
└─ config/
```

---

## 13. 設定ファイル要件

最低限、以下を設定可能とする。

- ComfyUI URL
- Blender 実行ファイルパス
- workflow ディレクトリ
- 出力先
- デフォルトモデル名やテンプレート

例:

```json
{
  "comfyui_url": "http://127.0.0.1:8188",
  "blender_path": "C:/Program Files/Blender Foundation/Blender 4.2/blender.exe",
  "workflow_dir": "./.codex/skills/comfy-blender-vrm/workflows",
  "output_dir": "./outputs"
}
```

---

## 14. エラー時の要件

以下を分かりやすく表示すること。

- ComfyUI 未起動
- Blender パス不正
- workflow JSON 不正
- 入力画像不足
- 出力先作成失敗
- モーション適用失敗

エラー表示は、単なる失敗通知ではなく、次の行動が分かることが望ましい。

---

## 15. MVP 実装順

### Phase 1
- doctor
- generate-character-sheet
- generate-expression-sheet

### Phase 2
- build-vrm-base
- export-review-renders

### Phase 3
- apply-motion-preview

### Phase 4
- 実行ログ整理
- テンプレート充実
- UX 改善

---

## 16. 将来拡張候補

- VRM 正式書き出しの自動化
- Unity / UniVRM 連携
- VRMA 書き出し
- lip sync 支援
- motion extraction
- キャラ設定からの一括自動生成
- 品質評価レポート生成
- ComfyUI / Blender の追加テンプレート配布

---

## 17. 意思決定まとめ

本要件定義における意思決定は以下の通り。

1. **MCP は必須にしない**
2. **ComfyUI は API 実行に限定する**
3. **Blender は CLI / background mode を基本にする**
4. **モーションは初版では既存資産適用を対象とする**
5. **Skill パックは一括導入可能な形で配布する**
6. **重い対話制御より、軽量で再現性のある制作フローを優先する**

---

## 18. 付録: MVP の一文要約

**ComfyUI と Blender がローカルに導入済みの環境に対し、キャラクター画像生成・VRM 作成支援・既存モーション適用を軽量に自動化する Skill パックを提供する。**
