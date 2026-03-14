# 仕様

入口は `docs/OVERVIEW.md`。Given/When/Then（前提/条件/振る舞い）で番号付きに整理する。

## SP-DOCTOR-001 `doctor`

### Public alias
- `forma-character-prepare-environment` は `forma-character` の canonical public command である
- `doctor` は `forma-character` 内の internal implementation command である

### 1. 設定解決
- Given: ユーザーが `python .codex/skills/forma-character/scripts/prepare_environment.py` または `python .codex/skills/forma-character/scripts/doctor.py` を実行し、必要に応じて `--config <path>` を指定する
- When: `doctor` が起動する
- Then: `config/forma-character.json` を既定設定として扱い、`comfyui_url`、`blender_path`、`workflow_dir`、`output_dir` の解決結果を個別に表示する

### 2. パス解決
- Given: 設定内に相対パスが含まれる
- When: `doctor` が `blender_path`、`workflow_dir`、`output_dir` を解決する
- Then: 相対パスはリポジトリルート基準で絶対パスに解決する

### 3. ComfyUI 確認
- Given: `comfyui_url` が設定されている
- When: `doctor` が疎通確認を行う
- Then: `/system_stats` を優先し、失敗時は `/queue` を代替 probe として確認する

### 4. Blender 確認
- Given: `blender_path` が設定されている
- When: `doctor` が環境確認を行う
- Then: 指定先が存在するファイルであることを確認する

### 5. workflow / output 確認
- Given: `workflow_dir` と `output_dir` が設定されている
- When: `doctor` が環境確認を行う
- Then: `workflow_dir` は存在必須として確認し、`output_dir` は未作成なら生成を試みる

### 6. 失敗時の終了
- Given: 1 件以上の確認失敗がある
- When: `doctor` が終了する
- Then: 項目ごとに次の行動が分かるメッセージを表示し、非 0 で終了する

### 7. 成功時の終了
- Given: 全確認が成功している
- When: `doctor` が終了する
- Then: 成功結果を一覧表示し、終了コード 0 で終了する

## SP-GCS-001 `generate-character-sheet`

### 1. 入力
- Given: ユーザーが workflow JSON パスと `character_prompt` を指定し、必要に応じて `seed`、reference image、config パスを指定する
- When: `generate-character-sheet` が起動する
- Then: workflow JSON、config、出力先を解決する

### 2. workflow 形式
- Given: workflow JSON が指定されている
- When: `generate-character-sheet` が workflow を読む
- Then: API-format prompt JSON のみを受け付け、UI export JSON は拒否する

### 2a. bundled workflow
- Given: base image 生成の既知 workflow をすぐ使いたい
- When: skill の workflow dir を確認する
- Then: `neta-yume-lumina-base.api.json` があり、`NetaYumev35_pretrained_all_in_one.safetensors` と `{{character_prompt}}`、`{{seed}}`、`{{run_id}}` を前提に使える

### 2b. transparent bundled workflow
- Given: base image を transparent PNG で使いたい
- When: skill の workflow dir を確認する
- Then: `neta-yume-lumina-base-transparent.api.json` があり、ComfyUI 標準ノードだけで white background keying を行い、alpha 付き PNG を `SaveImage` に渡す

### 3. プレースホルダ解決
- Given: workflow JSON にプレースホルダが含まれている
- When: `generate-character-sheet` が submitted workflow を生成する
- Then: `character_prompt`、`seed`、`run_id`、reference image 系の値を解決し、未解決プレースホルダが残る場合は失敗にする

### 4. ComfyUI 実行
- Given: submitted workflow が生成できている
- When: `generate-character-sheet` が ComfyUI API を呼ぶ
- Then: `POST /prompt` で送信し、`/history/<prompt_id>` を polling して完了を待つ

### 5. 成果物保存
- Given: ComfyUI の画像出力が取得できている
- When: `generate-character-sheet` が保存処理を行う
- Then: `output_dir/<project-name>/images/base/<run-id>/images/` に画像を保存し、submitted workflow と history を同 run 配下へ保存し、`output_dir/<project-name>/logs/` に実行メタ情報を保存する

### 6. 失敗時の終了
- Given: workflow ファイル不足、workflow JSON 不正、未解決プレースホルダ、ComfyUI API エラー、画像ダウンロード失敗のいずれかがある
- When: `generate-character-sheet` が終了する
- Then: 次の行動が分かるメッセージを表示し、非 0 で終了する

### 7. 成功時の終了
- Given: 画像保存まで成功している
- When: `generate-character-sheet` が終了する
- Then: `run_id`、`prompt_id`、保存先を表示し、終了コード 0 で終了する

## SP-GCFB-001 `generate-character-from-brief`

### Public alias
- `forma-character-generate-base-image` は `forma-character` の canonical public command である
- `generate-character-from-brief` は `forma-character` 内の internal implementation command である

### 1. 入力
- Given: ユーザーが workflow JSON を指定し、必要に応じて brief JSON、seed、config パスを指定する
- When: `generate-character-from-brief` が起動する
- Then: `--brief-file` がある場合は brief JSON を読み、ない場合は CLI 対話入力で brief を収集する

### 2. brief 形式
- Given: brief 情報が入力される
- When: `generate-character-from-brief` が brief を検証する
- Then: `core_concept` を必須とし、`character_name` を追加フィールドとして受け付け、`background` は後方互換用 field として受け付け続け、定義済み fields 以外は拒否し、不正 JSON や必須項目不足は失敗にする

### 2a. interactive 入力順
- Given: `--brief-file` を指定せずに実行する
- When: `generate-character-from-brief` が対話入力を始める
- Then: 最初に `character_name` を聞き、その後に `core_concept` と optional fields を聞き、background の自由入力は聞かず、pose は standing detail として聞く

### 3. prompt 合成
- Given: brief が検証済みである
- When: `generate-character-from-brief` がベース画像生成用 prompt を作る
- Then: `core_concept` と optional fields を使って `character_prompt` を合成し、standing full-body、backgroundless、no text overlay の defaults を常に含め、`background` field は prompt に反映せず、`character_name` は project 名導出に使い、`prompt-preview.txt` を保存する

### 4. 既存生成経路の再利用
- Given: `character_prompt` が合成できている
- When: `generate-character-from-brief` が画像生成を実行する
- Then: `generate-character-sheet` と同じ workflow 実行経路を使い、ComfyUI submit / polling / image download / metadata 保存を行う

### 5. 成果物保存
- Given: 画像生成が成功している
- When: `generate-character-from-brief` が保存処理を行う
- Then: `output_dir/<project-name>/brief.json` と `output_dir/<project-name>/images/base/<run-id>/brief.json` の両方に brief を保存し、`output_dir/<project-name>/images/base/<run-id>/prompt-preview.txt` を保存し、`output_dir/<project-name>/logs/` の metadata に brief 情報を残す

### 6. 失敗時の終了
- Given: brief file 不足、brief JSON 不正、brief 必須項目不足、ComfyUI API エラーのいずれかがある
- When: `generate-character-from-brief` が終了する
- Then: 次の行動が分かるメッセージを表示し、非 0 で終了する

### 7. 成功時の終了
- Given: brief 保存と画像保存まで成功している
- When: `generate-character-from-brief` が終了する
- Then: `run_id`、`prompt_id`、保存先、brief 保存先を表示し、終了コード 0 で終了する

## SP-GES-001 `generate-expression-sheet`

### Public alias
- `forma-character-generate-expressions` は `forma-character` の canonical public command である
- `generate-expression-sheet` は `forma-character` 内の internal implementation command である

### 1. 入力
- Given: ユーザーが workflow JSON パス、base image、`character_prompt` を指定し、必要に応じて `seed`、expression list、config パスを指定する
- When: `generate-expression-sheet` が起動する
- Then: workflow JSON、base image、config、出力先を解決する

### 2. workflow 形式
- Given: workflow JSON が指定されている
- When: `generate-expression-sheet` が workflow を読む
- Then: API-format prompt JSON のみを受け付け、UI export JSON は拒否する

### 2a. bundled workflow
- Given: expression 生成の既知 workflow をすぐ使いたい
- When: skill の workflow dir を確認する
- Then: `neta-yume-lumina-expressions.api.json` があり、`NetaYumev35_pretrained_all_in_one.safetensors` と `{{character_prompt}}`、`{{expression_name}}`、`{{seed}}`、`{{run_id}}`、`{{base_image_name}}` を前提に使える

### 2b. transparent bundled workflow
- Given: expression image を transparent PNG で使いたい
- When: skill の workflow dir を確認する
- Then: `neta-yume-lumina-expressions-transparent.api.json` があり、ComfyUI 標準ノードだけで white background keying を行い、alpha 付き PNG を `SaveImage` に渡す

### 3. base image とプレースホルダ解決
- Given: workflow JSON にプレースホルダが含まれている
- When: `generate-expression-sheet` がベース画像を upload し、submitted workflow を生成する
- Then: `character_prompt`、`expression_name`、`seed`、`run_id`、base image 系の値を解決し、未解決プレースホルダが残る場合は失敗にする

### 3a. project 名の引継ぎ
- Given: base image path が `output_dir/<project-name>/images/...` 配下にある
- When: `generate-expression-sheet` が保存先を決める
- Then: 同じ `<project-name>` を引き継いで expression 出力先と metadata 保存先を決める

### 4. ComfyUI 実行
- Given: submitted workflow が expression ごとに生成できている
- When: `generate-expression-sheet` が ComfyUI API を呼ぶ
- Then: expression ごとに `POST /prompt` で送信し、`/history/<prompt_id>` を polling して完了を待つ

### 5. 成果物保存
- Given: expression ごとの画像出力が取得できている
- When: `generate-expression-sheet` が保存処理を行う
- Then: `output_dir/<project-name>/images/expressions/<run-id>/<expression>/images/` に画像を保存し、同 expression 配下に submitted workflow と history を保存し、`output_dir/<project-name>/logs/` に実行メタ情報を保存する

### 6. 失敗時の終了
- Given: workflow ファイル不足、workflow JSON 不正、base image 不足、未解決プレースホルダ、ComfyUI API エラー、画像ダウンロード失敗のいずれかがある
- When: `generate-expression-sheet` が終了する
- Then: 次の行動が分かるメッセージを表示し、非 0 で終了する

### 7. 成功時の終了
- Given: expression ごとの画像保存まで成功している
- When: `generate-expression-sheet` が終了する
- Then: `run_id`、保存先、expression 一覧を表示し、終了コード 0 で終了する

## SP-BVB-001 `build-vrm-base`

### Public alias
- `forma-character-build-vrm` は `forma-character` の canonical public command である
- `build-vrm-base` は `forma-character` 内の internal implementation command である

### 1. 入力
- Given: ユーザーが `.blend` path を指定し、必要に応じて texture image と config path を指定する
- When: `build-vrm-base` が起動する
- Then: `.blend`、texture image、config、出力先を解決する

### 2. Blender 実行
- Given: Blender executable と source `.blend` が利用可能である
- When: `build-vrm-base` が処理を開始する
- Then: Blender background mode を起動し、bundled Blender script に引数を渡して scene を処理する

### 3. texture 適用
- Given: texture image が指定されている
- When: Blender script が scene を更新する
- Then: 最初の mesh object の material に texture image を接続する

### 4. review render
- Given: Blender script が scene を保存できる
- When: `build-vrm-base` が review render を生成する
- Then: camera / light を補い、静止画 1 枚を render する

### 5. 成果物保存
- Given: Blender background mode の処理が成功している
- When: `build-vrm-base` が保存処理を行う
- Then: `output_dir/blender/<run-id>/` に更新済み `.blend`、`review.png`、Blender result JSON を保存し、`output_dir/logs/` に metadata を保存する

### 6. 失敗時の終了
- Given: `.blend` 不足、texture image 不足、Blender path 不正、Blender 実行失敗、review render 不足のいずれかがある
- When: `build-vrm-base` が終了する
- Then: 次の行動が分かるメッセージを表示し、非 0 で終了する

### 7. 成功時の終了
- Given: updated `.blend` と review render の保存まで成功している
- When: `build-vrm-base` が終了する
- Then: `run_id`、保存先、updated `.blend`、review render を表示し、終了コード 0 で終了する

## SP-AMP-001 `apply-motion-preview`

### Public alias
- `forma-character-apply-motion-preview` は `forma-character` の canonical public command である
- `apply-motion-preview` は `forma-character` 内の internal implementation command である

### 1. 入力
- Given: ユーザーが `.blend` path と `BVH` motion file を指定し、必要に応じて config path を指定する
- When: `apply-motion-preview` が起動する
- Then: `.blend`、`BVH`、config、出力先を解決する

### 2. Blender 実行
- Given: Blender executable、source `.blend`、`BVH` motion file が利用可能である
- When: `apply-motion-preview` が処理を開始する
- Then: Blender background mode を起動し、bundled Blender script に引数を渡して scene を処理する

### 3. motion 適用
- Given: Blender script が `BVH` を import できる
- When: scene 内の armature を更新する
- Then: import した action を最初の armature object に割り当て、action の開始フレームを preview frame に使う

### 4. preview render
- Given: Blender script が scene を保存できる
- When: `apply-motion-preview` が preview render を生成する
- Then: camera / light を補い、静止画 1 枚を render する

### 5. 成果物保存
- Given: Blender background mode の処理が成功している
- When: `apply-motion-preview` が保存処理を行う
- Then: `output_dir/motion/<run-id>/` に更新済み `.blend`、`preview.png`、Blender result JSON を保存し、`output_dir/logs/` に metadata を保存する

### 6. 失敗時の終了
- Given: `.blend` 不足、`BVH` 不足、Blender path 不正、Blender 実行失敗、preview render 不足のいずれかがある
- When: `apply-motion-preview` が終了する
- Then: 次の行動が分かるメッセージを表示し、非 0 で終了する

### 7. 成功時の終了
- Given: updated `.blend` と preview render の保存まで成功している
- When: `apply-motion-preview` が終了する
- Then: `run_id`、保存先、updated `.blend`、preview render を表示し、終了コード 0 で終了する
