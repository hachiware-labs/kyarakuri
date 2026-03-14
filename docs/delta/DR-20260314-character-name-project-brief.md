# delta-request

## Delta ID
- DR-20260314-character-name-project-brief

## Delta Type
- FEATURE

## 目的
- `generate-base-image` の対話入力で最初にキャラクター名を聞けるようにする。
- brief を run 配下だけでなく `outputs/<project-name>/brief.json` にも保存し、project 入口として使えるようにする。

## 変更対象（In Scope）
- `generate_character_from_brief.py` に `character_name` の対話入力と project 直下 brief 保存を追加する。
- brief schema / docs に `character_name` と project 直下 `brief.json` を反映する。
- canonical docs に project 名導出と brief 保存先の更新を反映する。
- delta 記録を `docs/delta/DR-20260314-character-name-project-brief.md` に残す。

## 非対象（Out of Scope）
- command 名や CLI 引数の変更。
- expression / Blender / motion コマンドの保存仕様変更。
- project root への `prompt-preview.txt` 追加。
- 既存 brief-file の全面互換性破壊。

## Candidate Files/Artifacts
- `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_character_from_brief.py`
- `.codex/skills/kyarakuri-comfy-blender-vrm/references/character_brief.md`
- `.codex/skills/comfy-blender-vrm/references/character_brief.md`
- `docs/concept.md`
- `docs/spec.md`
- `docs/architecture.md`
- `docs/OVERVIEW.md`
- `docs/plan.md`
- `docs/delta/DR-20260314-character-name-project-brief.md`

## 差分仕様
- DS-01:
  - Given: ユーザーが `generate-base-image` を interactive に使う。
  - When: brief 入力が始まる。
  - Then: 最初に `character_name` を聞き、その後に `core_concept` と optional brief を聞く。
- DS-02:
  - Given: brief に `character_name` がある。
  - When: base image 生成を実行する。
  - Then: project 名導出は `character_name` を優先し、なければ既存どおり `core_concept` を使う。
- DS-03:
  - Given: base image 生成が成功する。
  - When: brief 保存を行う。
  - Then: 既存の run 配下 `brief.json` に加えて `outputs/<project-name>/brief.json` が保存される。

## 受入条件（Acceptance Criteria）
- AC-01: interactive brief input で `character_name` を最初に入力できる。
- AC-02: brief schema が `character_name` を受け付ける。
- AC-03: `character_name` がある場合、project 名導出はそれを優先する。
- AC-04: 生成成功時に `outputs/<project-name>/brief.json` が保存される。
- AC-05: `character_name` を持たない既存 brief JSON でも `generate-base-image` は引き続き実行できる。
- AC-06: `delta-project-validator` の `links-only` が PASS する。

## Verify Profile
- static check: Required
- targeted unit: Not Required
- targeted integration / E2E: Required
- delta-project-validator: links-only

## Canonical Sync Mode
- mode: post-archive sync
- reason: 実装と brief docs / canonical docs の同期を verify PASS 後に閉じる。

## 制約
- `character_name` は後方互換のため brief-file では optional にする。
- 既存の run 配下 `brief.json` は残す。

## Review Gate
- required: No
- reason: brief 入力と保存先に閉じた差分であり、command I/F の追加や大規模設計変更はない。

## 未確定事項
- Q-01: project root に `prompt-preview.txt` も保存するかは別 delta に切り分ける。

## Step 2: delta-apply
- changed files:
  - `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_character_from_brief.py`
  - `.codex/skills/kyarakuri-comfy-blender-vrm/references/character_brief.md`
  - `.codex/skills/comfy-blender-vrm/references/character_brief.md`
  - `docs/concept.md`
  - `docs/spec.md`
  - `docs/architecture.md`
  - `docs/OVERVIEW.md`
  - `docs/plan.md`
  - `docs/delta/DR-20260314-character-name-project-brief.md`
- applied AC:
  - AC-01:
    - 変更: interactive brief input の最初に `character_name` を追加した。
    - 根拠: `collect_interactive_brief()` が `Character name (required):` から始まる。
  - AC-02:
    - 変更: brief schema が `character_name` を受け付けるようにした。
    - 根拠: `STRING_FIELDS` / `ALLOWED_BRIEF_KEYS` に `character_name` を追加した。
  - AC-03:
    - 変更: project 名導出は `character_name` を優先し、なければ `core_concept` を使うようにした。
    - 根拠: `project_name_hint = brief.get("character_name") or brief["core_concept"]` にした。
  - AC-04:
    - 変更: project 直下にも `brief.json` を保存するようにした。
    - 根拠: 生成成功後に `result.project_dir / "brief.json"` へ保存する処理を追加した。
  - AC-05:
    - 変更: `character_name` を持たない既存 brief JSON でも実行できる形を維持した。
    - 根拠: `character_name` は brief-file では optional のままとした。
  - AC-06:
    - 変更: docs link 整合が通る形に brief docs / canonical docs / delta record を更新した。
    - 根拠: `validate_delta_links.js` が `OK` を返した。
- non-goal kept:
  - Out of Scope への変更なし: Yes
- canonical sync:
  - mode: post-archive sync
  - action: verify PASS 後に brief docs と canonical docs を同期する
  - status: DONE
- status: APPLIED

## Step 3: delta-verify
- verify profile:
  - static check: Required
  - targeted unit: Not Required
  - targeted integration / E2E: Required
  - delta validator: links-only
- executed verify:
  - static check:
    - `py_compile` for `.codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_character_from_brief.py`
  - targeted integration / E2E:
    - interactive run:
      - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py --workflow .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-base.api.json --output-name interactive-character-name --timeout-seconds 600`
      - stdin answers started with `character_name = "Airi Brief Verify"`
      - project output: `outputs/airi-brief-verify/`
      - project brief: `outputs/airi-brief-verify/brief.json`
      - run brief: `outputs/airi-brief-verify/images/base/20260314-020733-interactive-character-name/brief.json`
    - backward-compatible brief-file run:
      - `python .codex/skills/kyarakuri-comfy-blender-vrm/scripts/generate_base_image.py --workflow .codex/skills/kyarakuri-comfy-blender-vrm/workflows/neta-yume-lumina-base.api.json --brief-file outputs/tmp/real-comfyui-brief.json --output-name compat-no-character-name --timeout-seconds 600`
      - project output: `outputs/future-inspired-japanese-idol-mechanic/`
      - project brief: `outputs/future-inspired-japanese-idol-mechanic/brief.json`
    - post-run health check:
      - `http://127.0.0.1:8000/system_stats` returned `200`
  - delta validator:
    - `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- AC result table:
  - AC-01: PASS
    - 根拠: interactive verify で最初に `Character name (required):` が表示され、入力を受け付けた。
  - AC-02: PASS
    - 根拠: `outputs/airi-brief-verify/brief.json` に `character_name` が保存された。
  - AC-03: PASS
    - 根拠: interactive verify の project 名は `airi-brief-verify` になり、`core_concept` 由来ではなかった。
  - AC-04: PASS
    - 根拠: project 直下の `brief.json` と run 配下の `brief.json` の両方が保存された。
  - AC-05: PASS
    - 根拠: `character_name` を持たない既存 `outputs/tmp/real-comfyui-brief.json` でも generation が成功した。
  - AC-06: PASS
    - 根拠: `validate_delta_links.js` が `OK: errors=0, warnings=0` で終了した。
- scope deviation:
  - Out of Scope 変更あり: No
- canonical sync:
  - mode: post-archive sync
  - status: DONE
  - result: PASS
- overall: PASS

## Step 4: delta-archive
- verify result: PASS
- review gate: NOT REQUIRED
- archive status: archived
- canonical sync:
  - mode: post-archive sync
  - status: DONE
  - synced docs:
    - concept: `docs/concept.md`
    - spec: `docs/spec.md`
    - architecture: `docs/architecture.md`
    - overview: `docs/OVERVIEW.md`
    - plan: `docs/plan.md`
- closed scope:
  - 目的: base image interactive 入力で `character_name` を聞き、project 直下にも `brief.json` を保存する
  - 変更対象: `generate_character_from_brief.py`、brief refs、canonical docs、delta record
  - 非対象: command 名 / CLI 引数変更、expression / Blender / motion の保存仕様変更、project root `prompt-preview.txt` 追加
- unresolved items:
  - Q-01: project root `prompt-preview.txt` 追加は別 delta に切り分ける
- follow-up delta seeds:
  - `review delta`
  - `project-root prompt-preview`
