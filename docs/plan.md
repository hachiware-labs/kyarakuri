# plan.md（必ず書く：最新版）

このファイルは入口だけを置く。`current` は 1〜5 件、archive の詳細は monthly archive に分離する。
ユーザーは `planをシュリンクして` といつでも指示してよく、その場合は `plan-archive-shrinker` skill を使う。Codex は plan の archive 領域が 100行を超えたら slim 化してよい。

# current
- [ ] 次の active delta を起票する
- [ ] 同一 plan item が 3 delta 以上になったら review delta を検討する
- [ ] REVIEW 以外の delta が 5 件続いたら review delta を検討する

# review timing
- 手動: `review deltaを回して`
- 手動: `設計レビューして`
- 自動: 大機能が一段落した時
- 自動: 同一 plan item が 3 delta 以上になった時
- 自動: REVIEW 以外の delta が 5 件続いた時

# future
- 将来計画を粗く列挙する

# archive
- [x] `DR-20260313-doctor-command`: `doctor` を実装し、verify PASS で archive した
- [x] `DR-20260313-generate-character-sheet`: API-format workflow から立ち絵生成、画像保存、実行メタ保存を実装し archive した
- [x] `DR-20260313-generate-expression-sheet`: ベース画像から複数表情を生成し、expression ごとの画像群と実行メタ保存を実装し archive した

# archive index
- `./plan_archive_YYYY_MM.md`
