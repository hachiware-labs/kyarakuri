# delta-request

## Delta ID
- DR-20260628-forma-background-skill

## Delta Type
- ADD

## 目的
- 背景画像を作成し、背景の位置・構図を変えずに時間帯や照明だけを変える repo-local skill を追加する。

## 変更対象（In Scope）
- `.codex/skills/forma-background/SKILL.md` を追加する。
- 背景 brief / base background / time variation の成果物保存ルールを定義する。
- ComfyUI を使う場合の prompt 方針と、構図固定のための img2img / low denoise / seed 管理方針を定義する。
- `docs/OVERVIEW.md` と `docs/plan.md` に current state を最小反映する。
- delta 記録を `docs/delta/DR-20260628-forma-background-skill.md` に残す。

## 非対象（Out of Scope）
- 実 ComfyUI workflow JSON の追加。
- 背景画像の実生成。
- React / hidamari 側の表示コード変更。
- 3D scene、depth map、camera tracking の実装。
- character skill の改名や統合。

## Candidate Files/Artifacts
- `.codex/skills/forma-background/SKILL.md`
- `docs/OVERVIEW.md`
- `docs/plan.md`
- `docs/delta/DR-20260628-forma-background-skill.md`

## 差分仕様
- DS-01:
  - Given: ユーザーが背景を作りたいと依頼する。
  - When: `forma-background` skill が使われる。
  - Then: 背景 brief を整理し、`outputs/<project-name>/backgrounds/` 配下に保存する前提で進める。
- DS-02:
  - Given: ユーザーが「位置は変えず、時間変化を作る」と依頼する。
  - When: time variation を作る。
  - Then: camera angle / object positions / room layout / horizon / perspective を固定し、time of day / weather / lighting / window color / shadow direction だけを変える。
- DS-03:
  - Given: ComfyUI img2img を使う。
  - When: variation を生成する。
  - Then: low denoise と同一 seed 系の管理を優先し、構図変更や物体追加を negative に入れる。

## 受入条件（Acceptance Criteria）
- AC-01: `forma-background/SKILL.md` に YAML frontmatter があり、skill loader validation を通る。
- AC-02: skill が「背景生成」と「構図固定の時間帯差分」の手順を区別している。
- AC-03: 保存先と成果物命名が定義されている。
- AC-04: 既存 skill への破壊的変更がない。
- AC-05: docs current / archive が delta と整合している。

## Verify Profile
- static check: Required
- skill validation: `skill-creator/scripts/quick_validate.py`
- real ComfyUI smoke: Not required

## Canonical Sync Mode
- mode: post-archive sync
- reason: repo-local skill 追加と docs 更新を verify PASS 後に閉じる。

## 制約
- repo-local skill として作る。
- 背景にキャラクター、説明文字、ロゴ、看板文字を入れる前提にはしない。
- 構図固定の variation では、背景内オブジェクトの位置変更を禁止する。

## Review Gate
- required: No
- reason: 新規 repo-local skill の手順定義に閉じ、既存 workflow や public command の破壊を伴わない。

---

## Step 2: delta apply
- `skill-creator/scripts/init_skill.py` で `.codex/skills/forma-background` を初期化した。
- `forma-background/SKILL.md` に、背景 brief、base background、time variants、ComfyUI img2img 推奨値、variant presets、quality check を定義した。
- `agents/openai.yaml` を初期化し、skill list 用の表示名・短い説明・default prompt を追加した。
- `docs/OVERVIEW.md` と `docs/plan.md` に本 delta の current state を反映した。

## Step 3: delta verify
- PASS: `$env:PYTHONUTF8='1'; uv run --with pyyaml python C:\Users\naruhide\.codex\skills\.system\skill-creator\scripts\quick_validate.py .codex\skills\forma-background`
- PASS: `forma-background/SKILL.md` は YAML frontmatter を持ち、背景生成と固定構図 time variation の手順を分離している。
- PASS: 保存先 `outputs/<project-name>/backgrounds/<location-name>/...` と成果物命名を定義している。
- PASS: 既存 skill への破壊的変更はない。

## Step 4: delta archive
- status: PASS
- archived_at: 2026-06-28
- sync:
  - `docs/OVERVIEW.md` の Active Delta をなしに戻し、直近完了を本 delta に更新した。
  - `docs/plan.md` の current checkbox と archive summary を更新した。
