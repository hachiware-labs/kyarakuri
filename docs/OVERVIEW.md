# docs/OVERVIEW.md（入口 / 運用の正本）

この文書は **プロジェクト運用の正本**です。`AGENTS.md` は最小ルールのみで、詳細はここに集約します。
ユーザー要件の変更実行は **delta-first（request → apply → verify → archive）** で運用します。
運用文書間で矛盾がある場合、実行中の Delta ID（In Scope / Out of Scope / AC）を優先します。
文書スキル（concept/spec/architecture）は正本整備に限定し、delta の作成/実行は行いません。
Delta ID が未提示の要件実装は開始せず、先に delta request を作成します。
plan.md の実装アイテム1件は delta request 1件の seed として扱います（原則 1:1）。
実装アイテムが大きい場合は複数 delta に分割して進めます（1:N）。
delta 記録は Markdown（docs/delta/*.md）を正本とし、JSON/YAML の副管理を要求しません。
delta-archive が PASS のときのみ、正本へ最小差分で同期します。
大機能が一段落したら `review delta` を起票し、`docs/delta/REVIEW_CHECKLIST.md` を使って点検します。
ユーザーは `review deltaを回して` といつでも言ってよく、Codex は 1つの plan item が 3 delta 以上になった時や REVIEW 以外の delta が 5件続いた時に review delta を提案してよいです。
通常のソースコードは 500 行超でレビュー対象、800 行超は原則分割、1000 行超は例外扱いとします。
`docs/plan.md` は current / review timing / future / archive summary / archive index だけを置き、archive の詳細は monthly archive に分離します。
ユーザーは `planをシュリンクして` といつでも言ってよく、その場合は `plan-archive-shrinker` skill を使います。Codex は plan の archive 領域が 100行を超えたら slim 化してよいです。
plan.md の archive は計画タスクの完了記録であり、delta archive（差分確定）とは別です。

---

## 現在地（必ず更新）
- 現在フェーズ: P0
- 今回スコープ（1〜5行）:
  - Active Delta: なし
  - 直近完了: `DR-20260413-background-transparent-script` を archive 済み
  - internal / repo-local の既定 config は `http://127.0.0.1:8000` に揃った
  - `doctor` と `forma-character-prepare-environment` は現行ローカル環境で PASS する
  - 実 ComfyUI は主要機能の smoke verify に使う方針を正本 docs に反映した
  - bundled workflow `neta-yume-lumina-base.api.json` と `neta-yume-lumina-expressions.api.json` を internal / repo-local workflow dir に追加した
  - 2026-03-14 に実 ComfyUI で `forma-character-generate-base-image` と `forma-character-generate-expressions` の成功を確認した
  - transparent workflow `neta-yume-lumina-base-transparent.api.json` と `neta-yume-lumina-expressions-transparent.api.json` を internal / repo-local workflow dir に追加した
  - 2026-03-14 に実 ComfyUI で transparent base / expressions PNG の alpha 出力を確認した
  - 新規の base / expressions は `outputs/<project-name>/images/...` と `outputs/<project-name>/logs/` に保存し、base image brief は `outputs/<project-name>/brief.json` にも保存する
  - `Forma Character` (`forma-character`) は repo 内 canonical implementation skill pack である
  - legacy compatibility layer と `config/comfy-blender-vrm.json` は repo から削除済みである
  - `forma-character-generate-base-image` は standing full-body / backgroundless / no text overlay の defaults を prompt 合成時に常に入れ、interactive input では background を聞かない
  - `forma-character/SKILL.md` には loader 互換の YAML frontmatter が入っている
  - `background-transparent` は既存画像の背景透明化用 repo-local skill として追加し、white/checker/auto mode の Pillow script で deterministic に背景透明化できる
  - 次の seed は `review delta` または提供用 skill への移行 delta
- 非ゴール（やらないこと）:
  - FBX 対応、複雑な retargeting、動画出力
  - VRM 正式 export、rig 自動生成、shape key 自動作成
  - internal implementation command 名の rename
- 重要リンク:
  - concept: `./concept.md`
  - spec: `./spec.md`
  - architecture: `./architecture.md`
  - plan: `./plan.md`

---

## レビューゲート（必ず止まる）
共通原則：**自己レビュー → 完成と判断できたらユーザー確認 → 合意で次へ**

## Verify 方針
- 日常 verify は mock ComfyUI / fake Blender を主力に使う。
- 実 ComfyUI は主要機能が使えることを確認する smoke verify に使う。
- 実 ComfyUI smoke verify は repo-local skill を提供用 skill へ移す前の最終確認として扱ってよい。

---

## 更新の安全ルール（判断用）
### 合意不要
- 誤字修正、リンク更新、意味を変えない追記
- plan のチェック更新
- 小さな明確化（既存方針に沿う）

### 提案→合意→適用（必須）
- 大量削除、章構成変更、移動/リネーム
- Spec ID / Error ID の変更
- API/データモデルの形を変える設計変更
- セキュリティ/重大バグ修正で挙動が変わるもの
