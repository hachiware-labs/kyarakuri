# plan.md（必ず書く：最新版）

このファイルは入口だけを置く。`current` は 1〜5 件、archive の詳細は monthly archive に分離する。
ユーザーは `planをシュリンクして` といつでも指示してよく、その場合は `plan-archive-shrinker` skill を使う。Codex は plan の archive 領域が 100行を超えたら slim 化してよい。

# current
- [x] `DR-20260628-background-transparent-comfyui-rmbg` を起票する
- [x] `DR-20260628-background-transparent-comfyui-rmbg` を archive まで完了する
- [x] `DR-20260628-background-transparent-multipass-refine` を起票する
- [x] `DR-20260628-background-transparent-multipass-refine` を archive まで完了する
- [x] `DR-20260628-background-transparent-protect-subject-whites` を起票する
- [x] `DR-20260628-background-transparent-protect-subject-whites` を archive まで完了する
- [x] `DR-20260413-background-transparent-script` を起票する
- [x] `DR-20260413-background-transparent-script` を archive まで完了する
- [x] `DR-20260412-background-transparent-skill` を起票する
- [x] `DR-20260412-background-transparent-skill` を archive まで完了する
- [x] `DR-20260315-forma-skill-frontmatter` を起票する
- [x] `DR-20260315-forma-skill-frontmatter` を archive まで完了する
- [x] `DR-20260314-rename-to-forma-character` を起票する
- [x] `DR-20260314-rename-to-forma-character` を archive まで完了する
- [x] `DR-20260314-remove-legacy-compat-layer` を起票する
- [x] `DR-20260314-remove-legacy-compat-layer` を archive まで完了する
- [x] `DR-20260314-character-name-project-brief` を起票する
- [x] `DR-20260314-character-name-project-brief` を archive まで完了する
- [x] `DR-20260314-base-image-standing-defaults` を起票する
- [x] `DR-20260314-base-image-standing-defaults` を archive まで完了する
- [x] `DR-20260314-root-bilingual-readme` を起票する
- [x] `DR-20260314-root-bilingual-readme` を archive まで完了する
- [x] `DR-20260314-release-skill-consolidation` を起票する
- [x] `DR-20260314-release-skill-consolidation` を archive まで完了する
- [x] `DR-20260314-transparent-background-workflows` を起票する
- [x] `DR-20260314-transparent-background-workflows` を archive まで完了する
- [x] `DR-20260314-project-output-layout` を起票する
- [x] `DR-20260314-project-output-layout` を archive まで完了する
- [x] `DR-20260314-bundle-known-good-expression-workflow` を起票する
- [x] `DR-20260314-bundle-known-good-expression-workflow` を archive まで完了する
- [x] `DR-20260314-bundle-known-good-base-workflow` を起票する
- [x] `DR-20260314-bundle-known-good-base-workflow` を archive まで完了する
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
- `review delta`: repo-local canonical skill pack への集約後に layer / docs / verify coverage を横断点検する
- `distributable-skill migration`: repo 内 canonical skill pack が安定したら提供用 skill へ移す

# archive
- [x] `DR-20260628-background-transparent-comfyui-rmbg`: `background-transparent` に ComfyUI-RMBG API wrapper を追加し、人物向け既定を `BiRefNet-portrait`、Pillow script を fallback とする運用へ更新した
- [x] `DR-20260628-background-transparent-multipass-refine`: `background-transparent` に corner-start flood fill と multi-pass refinement を追加し、cropped portrait の白い服を守りながら hidamari 管理人さん画像の `transparent-v3` 出力を生成した
- [x] `DR-20260628-background-transparent-protect-subject-whites`: `background-transparent` の auto mode を corner seed / border-connected background 基準へ寄せ、白い服や淡色被写体を保護する検証と hidamari 管理人さん画像の `transparent-v2` 出力を追加した
- [x] `DR-20260413-background-transparent-script`: `background-transparent` に Pillow script `scripts/remove_background.py` を追加し、white/checker/auto mode、preview 生成、alpha 統計 JSON 出力を使えるようにした
- [x] `DR-20260412-background-transparent-skill`: 既存画像の背景透明化用 repo-local skill `background-transparent` を追加し、非破壊保存と transparent PNG cutout の手順を定義した
- [x] `DR-20260315-forma-skill-frontmatter`: `forma-character/SKILL.md` に YAML frontmatter を追加し、skill loader が読める構造へ戻した
- [x] `DR-20260314-rename-to-forma-character`: canonical skill pack / config / public command 名を `Forma Character` / `forma-character-*` へ揃え、renamed pack で real ComfyUI / fake Blender verify を通した
- [x] `DR-20260314-remove-legacy-compat-layer`: legacy compatibility skill pack と old config を削除し、`kyarakuri-comfy-blender-vrm` 単独で real ComfyUI / fake Blender verify を通した
- [x] `DR-20260314-character-name-project-brief`: base image の対話入力で `character_name` を追加し、`outputs/<project-name>/brief.json` を保存するようにした
- [x] `DR-20260314-base-image-standing-defaults`: base image prompt に standing full-body / backgroundless / no text overlay defaults を固定し、interactive brief は background を聞かない形へ揃えた
- [x] `DR-20260314-root-bilingual-readme`: repo root に `README.md` と `README_ja.md` を追加し、project 入口を bilingual 化した
- [x] `DR-20260314-release-skill-consolidation`: `kyarakuri-comfy-blender-vrm` を canonical implementation skill pack に昇格し、旧 `comfy-blender-vrm` を compatibility wrapper layer に整理した
- [x] `DR-20260314-transparent-background-workflows`: local-only / standard-node の transparent workflow を base / expressions 用に追加し、real ComfyUI で alpha 付き PNG verify を通した
- [x] `DR-20260314-project-output-layout`: base / expressions の保存先を `outputs/<project-name>/images/...` と `outputs/<project-name>/logs/` に変更し、real ComfyUI で新レイアウトの verify を通した
- [x] `DR-20260314-bundle-known-good-expression-workflow`: 2026-03-14 の成功 expression run 由来の `neta-yume-lumina-expressions.api.json` を internal / repo-local workflow dir に追加し、real ComfyUI で 2 表情の verify を通した
- [x] `DR-20260314-bundle-known-good-base-workflow`: 2026-03-04 の成功 PNG metadata 由来の `neta-yume-lumina-base.api.json` を internal / repo-local workflow dir に追加し、bundled workflow として docs に同期した
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
