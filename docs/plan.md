# plan.md（必ず書く：最新版）

このファイルは入口だけを置く。`current` は 1〜5 件、archive の詳細は monthly archive に分離する。
ユーザーは `planをシュリンクして` といつでも指示してよく、その場合は `plan-archive-shrinker` skill を使う。Codex は plan の archive 領域が 100行を超えたら slim 化してよい。

# current
- [x] `DR-20260313-generate-character-from-brief` を起票する
- [x] `DR-20260313-generate-character-from-brief` を archive まで完了する
- [x] `DR-20260313-repo-local-kyarakuri-skill-pack` を起票する
- [x] `DR-20260313-repo-local-kyarakuri-skill-pack` を archive まで完了する
- [x] `DR-20260313-build-vrm-base` を起票する
- [x] `DR-20260313-build-vrm-base` を archive まで完了する
- [x] `DR-20260313-apply-motion-preview` を起票する
- [x] `DR-20260313-apply-motion-preview` を archive まで完了する
- [x] `DR-20260313-align-comfyui-url-8000` を起票する
- [x] `DR-20260313-align-comfyui-url-8000` を archive まで完了する
- [x] `DR-20260313-real-comfyui-smoke-policy` を起票する
- [x] `DR-20260313-real-comfyui-smoke-policy` を archive まで完了する
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
- `DR-20260313-real-comfyui-smoke-verify`: 実 ComfyUI を使って `generate-base-image` / `generate-expressions` の smoke verify を定義し、repo-local skill の提供前確認を行う

# archive
- [x] `DR-20260313-doctor-command`: `doctor` を実装し、verify PASS で archive した
- [x] `DR-20260313-generate-character-sheet`: API-format workflow から立ち絵生成、画像保存、実行メタ保存を実装し archive した
- [x] `DR-20260313-generate-character-from-brief`: brief の対話入力 / JSON 読込、prompt 合成、既存 character sheet 経路の再利用、brief / prompt preview 保存を実装し archive した
- [x] `DR-20260313-generate-expression-sheet`: ベース画像から複数表情を生成し、expression ごとの画像群と実行メタ保存を実装し archive した
- [x] `DR-20260313-repo-local-kyarakuri-skill-pack`: `kyarakuri-comfy-blender-vrm` を repo-local wrapper skill pack として追加し、public name で既存実装を呼べるようにして archive した
- [x] `DR-20260313-build-vrm-base`: Blender background mode で `.blend` を処理し、updated `.blend` と review render を保存する最小 build-vrm を実装して archive した
- [x] `DR-20260313-apply-motion-preview`: Blender background mode で `.blend` に `BVH` motion を適用し、updated `.blend` と preview render を保存する最小 motion preview を実装して archive した
- [x] `DR-20260313-align-comfyui-url-8000`: internal / repo-local の既定 config の `comfyui_url` を `http://127.0.0.1:8000` に揃え、環境確認コマンドが PASS する状態へ修正した
- [x] `DR-20260313-real-comfyui-smoke-policy`: mock / fake を主力 verify とし、実 ComfyUI は主要機能の smoke verify に使う方針を正本 docs に同期した
- [x] `DR-20260313-phase1-review`: review checklist と validator full を実行し、Phase 1 review を PASS で archive した

# archive index
- `./plan_archive_YYYY_MM.md`
