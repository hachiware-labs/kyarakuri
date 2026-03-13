# 仕様

入口は `docs/OVERVIEW.md`。Given/When/Then（前提/条件/振る舞い）で番号付きに整理する。

## SP-DOCTOR-001 `doctor`

### 1. 設定解決
- Given: ユーザーが `python .codex/skills/comfy-blender-vrm/scripts/doctor.py` または `--config <path>` を実行する
- When: `doctor` が起動する
- Then: `config/comfy-blender-vrm.json` を既定設定として扱い、`comfyui_url`、`blender_path`、`workflow_dir`、`output_dir` の解決結果を個別に表示する

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
- Then: `output_dir/character/<run-id>/images/` に画像を保存し、submitted workflow と history を同 run 配下へ保存し、`output_dir/logs/` に実行メタ情報を保存する

### 6. 失敗時の終了
- Given: workflow ファイル不足、workflow JSON 不正、未解決プレースホルダ、ComfyUI API エラー、画像ダウンロード失敗のいずれかがある
- When: `generate-character-sheet` が終了する
- Then: 次の行動が分かるメッセージを表示し、非 0 で終了する

### 7. 成功時の終了
- Given: 画像保存まで成功している
- When: `generate-character-sheet` が終了する
- Then: `run_id`、`prompt_id`、保存先を表示し、終了コード 0 で終了する

## SP-GES-001 `generate-expression-sheet`

### 1. 入力
- Given: ユーザーが workflow JSON パス、base image、`character_prompt` を指定し、必要に応じて `seed`、expression list、config パスを指定する
- When: `generate-expression-sheet` が起動する
- Then: workflow JSON、base image、config、出力先を解決する

### 2. workflow 形式
- Given: workflow JSON が指定されている
- When: `generate-expression-sheet` が workflow を読む
- Then: API-format prompt JSON のみを受け付け、UI export JSON は拒否する

### 3. base image とプレースホルダ解決
- Given: workflow JSON にプレースホルダが含まれている
- When: `generate-expression-sheet` がベース画像を upload し、submitted workflow を生成する
- Then: `character_prompt`、`expression_name`、`seed`、`run_id`、base image 系の値を解決し、未解決プレースホルダが残る場合は失敗にする

### 4. ComfyUI 実行
- Given: submitted workflow が expression ごとに生成できている
- When: `generate-expression-sheet` が ComfyUI API を呼ぶ
- Then: expression ごとに `POST /prompt` で送信し、`/history/<prompt_id>` を polling して完了を待つ

### 5. 成果物保存
- Given: expression ごとの画像出力が取得できている
- When: `generate-expression-sheet` が保存処理を行う
- Then: `output_dir/expressions/<run-id>/<expression>/images/` に画像を保存し、同 expression 配下に submitted workflow と history を保存し、`output_dir/logs/` に実行メタ情報を保存する

### 6. 失敗時の終了
- Given: workflow ファイル不足、workflow JSON 不正、base image 不足、未解決プレースホルダ、ComfyUI API エラー、画像ダウンロード失敗のいずれかがある
- When: `generate-expression-sheet` が終了する
- Then: 次の行動が分かるメッセージを表示し、非 0 で終了する

### 7. 成功時の終了
- Given: expression ごとの画像保存まで成功している
- When: `generate-expression-sheet` が終了する
- Then: `run_id`、保存先、expression 一覧を表示し、終了コード 0 で終了する
