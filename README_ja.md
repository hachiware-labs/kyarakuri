# kyarakuri

ローカルに導入した ComfyUI と Blender を使って、キャラクター作成フローを組み立てる repo です。

現在は `kyarakuri-comfy-blender-vrm` を canonical skill pack として使い、次の処理を repo 内で実行できます。

- 環境確認
- brief からのベース画像生成
- ベース画像からの表情差分生成
- Blender を使った VRM 作業土台の作成
- Blender を使ったモーション preview

旧 `comfy-blender-vrm` skill pack は、従来の CLI 名を維持する compatibility layer として残しています。

## 現在地

- フェーズ: `P0`
- canonical skill pack: [`./.codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md`](./.codex/skills/kyarakuri-comfy-blender-vrm/SKILL.md)
- legacy compatibility layer: [`./.codex/skills/comfy-blender-vrm/SKILL.md`](./.codex/skills/comfy-blender-vrm/SKILL.md)
- repo-local 既定 config: [`./config/kyarakuri-comfy-blender-vrm.json`](./config/kyarakuri-comfy-blender-vrm.json)
- 正本 docs の入口: [`./docs/OVERVIEW.md`](./docs/OVERVIEW.md)

## 利用できるコマンド

- `kyarakuri-prepare-environment`
- `kyarakuri-generate-base-image`
- `kyarakuri-generate-expressions`
- `kyarakuri-build-vrm`
- `kyarakuri-apply-motion-preview`

## クイックスタート

1. まずローカル環境を確認します。

```powershell
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/prepare_environment.py
```

2. brief からベース画像を生成します。

```powershell
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py `
  --workflow .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-base.api.json `
  --brief-file outputs/tmp/real-comfyui-brief.json
```

3. 保存済みのベース画像から表情差分を生成します。

```powershell
python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_expressions.py `
  --workflow .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-expressions.api.json `
  --base-image outputs/<project-name>/images/base/<run-id>/images/<image>.png `
  --character-prompt "<同じ prompt>" `
  --expressions neutral,smile
```

## Bundled Workflow

canonical skill pack には、repo 内でそのまま使える bundled workflow を含めています。

- `neta-yume-lumina-base.api.json`
- `neta-yume-lumina-base-transparent.api.json`
- `neta-yume-lumina-expressions.api.json`
- `neta-yume-lumina-expressions-transparent.api.json`

workflow の前提や placeholder は [`./.codex/skills/kyarakuri-comfy-blender-vrm/workflows/README.md`](./.codex/skills/kyarakuri-comfy-blender-vrm/workflows/README.md) を参照してください。

## 出力レイアウト

ベース画像と表情差分は project 名ごとに [`./outputs`](./outputs) 配下へ保存されます。

- `outputs/<project-name>/images/base/<run-id>/`
- `outputs/<project-name>/images/expressions/<run-id>/<expression>/`
- `outputs/<project-name>/logs/`

Blender / motion 系の出力先は、現状ではコマンド別です。

- `outputs/blender/<run-id>/`
- `outputs/motion/<run-id>/`

## 参照ドキュメント

- 入口: [`./docs/OVERVIEW.md`](./docs/OVERVIEW.md)
- concept: [`./docs/concept.md`](./docs/concept.md)
- spec: [`./docs/spec.md`](./docs/spec.md)
- architecture: [`./docs/architecture.md`](./docs/architecture.md)
- plan: [`./docs/plan.md`](./docs/plan.md)

## 補足

- この repo は ComfyUI と Blender がローカル導入済みである前提です。
- 現在は repo-local での検証を主目的としており、提供用 skill への移行は次段です。
- 実 ComfyUI は主要な生成フローの smoke verify に使います。
