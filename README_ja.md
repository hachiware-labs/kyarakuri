# kyarakuri

`kyarakuri` は、Forma 系のアセット作成スキルを repo 内で育てるための workspace です。

現在の中心は `Forma Character` です。ローカル ComfyUI と Blender を使ってキャラクター画像、表情差分、Blender 作業土台、モーション preview を作ります。あわせて背景作成と背景透明化の helper skill も含みます。

## この repo でできること

- `forma-character`: キャラクターのベース画像、表情差分、Blender 作業土台、モーション preview を作る。
- `forma-background`: `imagegen` で背景 base を作り、同じ構図のまま時間・天気・光だけを変える。
- `background-transparent`: 既存画像の背景を抜き、透明 PNG cutout を保存する。

## 現在地

- フェーズ: `P0`
- メイン skill pack: [`.codex/skills/forma-character/SKILL.md`](./.codex/skills/forma-character/SKILL.md)
- 背景 skill: [`.codex/skills/forma-background/SKILL.md`](./.codex/skills/forma-background/SKILL.md)
- 背景透明化 skill: [`.codex/skills/background-transparent/SKILL.md`](./.codex/skills/background-transparent/SKILL.md)
- 既定 config: [`config/forma-character.json`](./config/forma-character.json)
- docs 入口: [`docs/OVERVIEW.md`](./docs/OVERVIEW.md)

## 必要なローカルアプリ

- ローカル ComfyUI。通常は `http://127.0.0.1:8000`。
- Blender。Blender 系 command で使います。
- repo-local skills を有効にした Codex。

例外として、背景生成は ComfyUI を使いません。`forma-background` は `imagegen` を使います。背景では構図品質と固定レイアウト編集が重要で、ローカル checkpoint の再現性よりも優先されます。

## Skill と用途

### Forma Character

キャラクター画像と Blender アセットを作るときに使います。

public command 名:

- `forma-character-prepare-environment`
- `forma-character-generate-base-image`
- `forma-character-generate-expressions`
- `forma-character-build-vrm`
- `forma-character-apply-motion-preview`

実体の script は `.codex/skills/forma-character/scripts/` にあります。

### Forma Background

背景・環境画像を作るときに使います。

想定フロー:

1. 背景 brief を聞く、または推定する。
2. `imagegen` で背景 base を作る。
3. 採用した base を `outputs/<project-name>/backgrounds/<location-name>/base.png` に保存する。
4. その base を入力画像にして、時間・天気差分を image edit で作る。
5. カメラ位置、パース、トリミング、レイアウト、オブジェクト位置、スケールを維持する。

この repo では背景生成に ComfyUI を使いません。雨、雪、夜、朝、霧などを作る場合は、採用済み base image を編集し、光・天気・表面状態だけを変えます。

### Background Transparent

既存画像を透明 PNG にしたいときに使います。

キャラクター画像では、インストール済みなら ComfyUI-RMBG が最優先です。単純な白背景・チェッカー背景なら Pillow fallback script も使えます。

## クイックスタート

### 1. 環境確認

```powershell
python .codex/skills/forma-character/scripts/prepare_environment.py
```

ComfyUI URL、Blender path、workflow directory、output directory を確認します。

既定 config:

```text
config/forma-character.json
```

### 2. キャラクター brief を用意する

再現しやすい生成のため、brief JSON を用意します。最小例:

```json
{
  "character_name": "toko",
  "core_concept": "成人女性。廃校を改装したクリエイター住居の管理人兼大家。",
  "visual_traits": "短い茶髪、琥珀色の目、落ち着いた表情",
  "outfit": "白いブラウス、茶色のベスト、ロングスカート、控えめなペンダント",
  "personality": "親切、実務的、静かに頼れる",
  "pose": "立ち姿、リラックスした姿勢"
}
```

例:

```text
outputs/toko/brief.json
```

### 3. キャラクターのベース画像を生成する

透明背景向け workflow:

```powershell
python .codex/skills/forma-character/scripts/generate_base_image.py `
  --workflow .codex/skills/forma-character/workflows/neta-yume-lumina-base-transparent.api.json `
  --brief-file outputs/toko/brief.json
```

通常 workflow:

```powershell
python .codex/skills/forma-character/scripts/generate_base_image.py `
  --workflow .codex/skills/forma-character/workflows/neta-yume-lumina-base.api.json `
  --brief-file outputs/toko/brief.json
```

ベース画像 prompt は常に次を狙います。

- 全身立ち姿
- 背景なし
- 説明文字・ラベルなし

出力先:

```text
outputs/<project-name>/images/base/<run-id>/
outputs/<project-name>/logs/
```

### 4. 表情差分を生成する

保存済み base image を入力にします。

```powershell
python .codex/skills/forma-character/scripts/generate_expressions.py `
  --workflow .codex/skills/forma-character/workflows/neta-yume-lumina-expressions.api.json `
  --base-image outputs/<project-name>/images/base/<run-id>/images/<image>.png `
  --character-prompt "<同じ character prompt>" `
  --expressions neutral,smile,thinking,concerned
```

透明背景向け表情 workflow:

```powershell
python .codex/skills/forma-character/scripts/generate_expressions.py `
  --workflow .codex/skills/forma-character/workflows/neta-yume-lumina-expressions-transparent.api.json `
  --base-image outputs/<project-name>/images/base/<run-id>/images/<image>.png `
  --character-prompt "<同じ character prompt>" `
  --expressions neutral,smile
```

出力先:

```text
outputs/<project-name>/images/expressions/<run-id>/<expression>/
outputs/<project-name>/logs/
```

### 5. 背景を作る

Codex に自然言語で `forma-background` 相当の依頼をします。

例:

```text
Forma で無人の児童公園背景を作って。ブランコと滑り台があります。まず晴れの base を1枚作り、そのあと全く同じ構図で雨天 variant を作って。
```

想定出力:

```text
outputs/<project-name>/backgrounds/<location-name>/brief.json
outputs/<project-name>/backgrounds/<location-name>/base.png
outputs/<project-name>/backgrounds/<location-name>/base.prompt.json
outputs/<project-name>/backgrounds/<location-name>/variants/<variant-name>.png
outputs/<project-name>/backgrounds/<location-name>/variants/<variant-name>.prompt.json
outputs/<project-name>/backgrounds/<location-name>/logs/
```

variant では構図維持が最重要です。カメラ位置、トリミング、パース、オブジェクト位置、スケール、レイアウトを維持し、変えるのは天気・時間・光・空・濡れ・雪・霧などの表面状態だけにします。

### 6. 既存画像の背景を透明にする

キャラクター画像向け ComfyUI-RMBG:

```powershell
uv run --with pillow python .codex/skills/background-transparent/scripts/comfyui_rmbg.py `
  image.png `
  --model BiRefNet-portrait `
  --out image-transparent.png `
  --preview image-preview.png
```

白背景・チェッカー背景向け Pillow fallback:

```powershell
uv run --with pillow python .codex/skills/background-transparent/scripts/remove_background.py `
  image.png `
  --mode auto `
  --out image-transparent.png `
  --preview image-preview.png
```

## Bundled Workflow

`forma-character` には ComfyUI API-format workflow を同梱しています。

- `neta-yume-lumina-base.api.json`
- `neta-yume-lumina-base-transparent.api.json`
- `neta-yume-lumina-expressions.api.json`
- `neta-yume-lumina-expressions-transparent.api.json`

workflow の前提や placeholder は [`.codex/skills/forma-character/workflows/README.md`](./.codex/skills/forma-character/workflows/README.md) を参照してください。

## 出力レイアウトまとめ

キャラクター:

```text
outputs/<project-name>/brief.json
outputs/<project-name>/images/base/<run-id>/
outputs/<project-name>/images/expressions/<run-id>/<expression>/
outputs/<project-name>/logs/
```

背景:

```text
outputs/<project-name>/backgrounds/<location-name>/base.png
outputs/<project-name>/backgrounds/<location-name>/variants/<variant-name>.png
outputs/<project-name>/backgrounds/<location-name>/logs/
```

Blender / motion:

```text
outputs/blender/<run-id>/
outputs/motion/<run-id>/
```

## 参照ドキュメント

- 入口: [`docs/OVERVIEW.md`](./docs/OVERVIEW.md)
- concept: [`docs/concept.md`](./docs/concept.md)
- spec: [`docs/spec.md`](./docs/spec.md)
- architecture: [`docs/architecture.md`](./docs/architecture.md)
- plan: [`docs/plan.md`](./docs/plan.md)

## ComfyUI の追加モデル・Custom Node 詳細手順

この repo は ComfyUI、Blender、checkpoint、ComfyUI custom node を自動インストールしません。先にローカル ComfyUI 側を準備してください。

### Forma Character に必須の checkpoint

同梱 character workflow には次の checkpoint が必要です。

```text
NetaYumev35_pretrained_all_in_one.safetensors
```

アクティブな ComfyUI の checkpoint directory に配置します。現在の Windows desktop 構成では、想定パスは次です。

```text
C:\Users\<you>\Documents\ComfyUI\models\checkpoints\NetaYumev35_pretrained_all_in_one.safetensors
```

ComfyUI の model directory が別の場合は、その ComfyUI の `models/checkpoints/` に置くか、ComfyUI の extra model paths config に登録してください。

checkpoint をコピーした後:

1. ComfyUI を再起動します。UI に model refresh がある場合は refresh でも構いません。
2. `CheckpointLoaderSimple` から `NetaYumev35_pretrained_all_in_one.safetensors` を選べることを確認します。
3. 次を実行します。

```powershell
python .codex/skills/forma-character/scripts/prepare_environment.py
```

生成時に checkpoint-not-found が出る場合、workflow は読めていますが ComfyUI が model を見つけられていません。ファイル名と配置先を確認してください。

### 透明キャラクター cutout に推奨の ComfyUI-RMBG

高品質な背景除去を使いたい場合は、アクティブな ComfyUI の `custom_nodes` に `ComfyUI-RMBG` を入れます。

想定パス:

```text
C:\Users\<you>\Documents\ComfyUI\custom_nodes\ComfyUI-RMBG
```

custom node を配置したら、ComfyUI が使っている Python 環境に requirements を入れてから ComfyUI を再起動します。

ComfyUI の `.venv` を使う例:

```powershell
C:\Users\<you>\Documents\ComfyUI\.venv\Scripts\python.exe -m pip install -r C:\Users\<you>\Documents\ComfyUI\custom_nodes\ComfyUI-RMBG\requirements.txt
```

RMBG node が ComfyUI に登録されているか確認します。

```powershell
$json = Invoke-RestMethod http://127.0.0.1:8000/object_info
$json | ConvertTo-Json -Depth 4 | Select-String "RMBG"
```

キャラクター画像では次を優先します。

```text
BiRefNet-portrait
```

一般物体や fringe が強い場合の fallback:

```text
RMBG-2.0
```

### 背景作成には追加 ComfyUI モデル不要

背景生成は意図的に ComfyUI を使いません。`forma-background` のためだけに背景 checkpoint を追加する必要はありません。背景 base は `imagegen`、天気・時間差分は `imagegen` edit で作ります。
