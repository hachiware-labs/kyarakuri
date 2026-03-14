# delta-request

## Delta ID
- DR-20260314-root-bilingual-readme

## Delta Type
- DOCS-SYNC

## 目的
- repo root に英語版 `README.md` と日本語版 `README_ja.md` を追加し、プロジェクトの入口を分かる状態にする。
- 現在の canonical skill pack、主要コマンド、outputs レイアウト、参照先 docs を root から辿れるようにする。

## 変更対象（In Scope）
- repo root に `README.md` を追加する。
- repo root に `README_ja.md` を追加する。
- `docs/OVERVIEW.md` と `docs/plan.md` に active delta と archive 状態を反映する。
- delta 記録を `docs/delta/DR-20260314-root-bilingual-readme.md` に残す。

## 非対象（Out of Scope）
- skill docs や canonical docs の大規模再構成。
- command 名、config、workflow、outputs レイアウトの仕様変更。
- 提供用 skill への移行。
- code / script の変更。

## Candidate Files/Artifacts
- README.md
- README_ja.md
- docs/OVERVIEW.md
- docs/plan.md
- docs/delta/DR-20260314-root-bilingual-readme.md

## 差分仕様
- DS-01:
  - Given: リポジトリを初めて開いたユーザーがいる。
  - When: root の `README.md` を読む。
  - Then: プロジェクトの目的、現状の実装範囲、主要コマンド、outputs 配置、参照 docs が英語で分かる。
- DS-02:
  - Given: 日本語で root 入口を読みたいユーザーがいる。
  - When: root の `README_ja.md` を読む。
  - Then: プロジェクトの目的、現状の実装範囲、主要コマンド、outputs 配置、参照 docs が日本語で分かる。
- DS-03:
  - Given: root README から詳細 docs を辿りたい。
  - When: README 内リンクを確認する。
  - Then: `docs/OVERVIEW.md` と canonical skill pack などの主要導線へ辿れる。

## 受入条件（Acceptance Criteria）
- AC-01: repo root に `README.md` が追加される。
- AC-02: repo root に `README_ja.md` が追加される。
- AC-03: 両 README にプロジェクト概要、canonical skill pack、主要コマンド、outputs レイアウト、詳細 docs への導線が含まれる。
- AC-04: README の内容は現在の実装状態と矛盾しない。
- AC-05: `delta-project-validator` の `links-only` が PASS する。

## Verify Profile
- static check: Not Required
- targeted unit: Not Required
- targeted integration / E2E: Not Required
- delta-project-validator: links-only

## Canonical Sync Mode
- mode: post-archive sync
- reason: root README 追加と current status の同期を verify PASS 後に閉じる。

## 制約
- root README は現在の repo-local / canonical skill 構成だけを説明し、将来想定を事実のように書かない。
- README は既存 docs とリンク整合を保つ。

## Review Gate
- required: No
- reason: root 入口 docs の追加に閉じた差分であり、仕様変更や実装変更は伴わない。

## 未確定事項
- Q-01: release 用の配布 README へ再編する場合は follow-up delta に切り分ける。

## Step 2: delta-apply
- changed files:
  - `README.md`
  - `README_ja.md`
  - `docs/OVERVIEW.md`
  - `docs/plan.md`
  - `docs/delta/DR-20260314-root-bilingual-readme.md`
- applied AC:
  - AC-01:
    - 変更: repo root に英語版 `README.md` を追加した。
    - 根拠: project overview、主要コマンド、outputs、docs 導線を記載した。
  - AC-02:
    - 変更: repo root に日本語版 `README_ja.md` を追加した。
    - 根拠: project overview、主要コマンド、outputs、docs 導線を日本語で記載した。
  - AC-03:
    - 変更: 両 README に project summary、canonical skill pack、主要コマンド、output layout、詳細 docs への導線を追加した。
    - 根拠: `Status` / `Available Commands` / `Quick Start` / `Output Layout` / `Documentation` 節を追加した。
  - AC-04:
    - 変更: README の記述を現行の canonical / legacy 構成と current outputs layout に合わせた。
    - 根拠: `kyarakuri-comfy-blender-vrm` を canonical、`comfy-blender-vrm` を compatibility layer として記載した。
  - AC-05:
    - 変更: links-only verify が通る形に current status docs を更新した。
    - 根拠: `docs/OVERVIEW.md` と `docs/plan.md` に active delta / archive 状態を反映した。
- non-goal kept:
  - Out of Scope への変更なし: Yes
- canonical sync:
  - mode: post-archive sync
  - action: verify PASS 後に current status docs を同期する
  - status: DONE
- status: APPLIED

## Step 3: delta-verify
- verify profile:
  - static check: Not Required
  - targeted unit: Not Required
  - targeted integration / E2E: Not Required
  - delta validator: links-only
- executed verify:
  - README link check:
    - `README.md` の markdown link を解決して missing なし
    - `README_ja.md` の markdown link を解決して missing なし
  - delta validator:
    - `node C:/Users/naruhide/.codex/skills/delta-project-validator/scripts/validate_delta_links.js --dir C:/Users/naruhide/workspace/kyarakuri`
- AC result table:
  - AC-01: PASS
    - 根拠: repo root に `README.md` が存在する。
  - AC-02: PASS
    - 根拠: repo root に `README_ja.md` が存在する。
  - AC-03: PASS
    - 根拠: 両 README に project 概要、canonical skill pack、主要コマンド、outputs、docs 導線が含まれる。
  - AC-04: PASS
    - 根拠: README 記述は現行の canonical / legacy skill 構成と outputs layout に一致する。
  - AC-05: PASS
    - 根拠: `validate_delta_links.js` が `OK` を返した。
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
    - overview: `docs/OVERVIEW.md`
    - plan: `docs/plan.md`
- closed scope:
  - 目的: repo root に英語版 / 日本語版 README を追加して project 入口を整える
  - 変更対象: `README.md`、`README_ja.md`、current status docs、delta record
  - 非対象: skill docs 再構成、command / config / workflow 仕様変更、コード変更
- unresolved items:
  - Q-01: release 用の配布 README への再編は follow-up delta に切り分ける
- follow-up delta seeds:
  - `review delta`
  - `distributable-skill migration`
