# delta-request

## Delta ID
- DR-20260628-background-transparent-multipass-refine

## Delta Type
- IMPROVE

## 目的
- `background-transparent` の背景除去を複数 pass に分け、白い服や淡色被写体を守りながら背景残りを減らす。
- hidamari の管理人さん画像 4 枚で multi-pass 出力を比較できるようにする。

## 変更対象（In Scope）
- `.codex/skills/background-transparent/scripts/remove_background.py` に、初回の安全な border-connected 除去後、透明領域からのみ背景候補へ広げる refinement pass を追加する。
- `.codex/skills/background-transparent/scripts/remove_background.py` に、cropped portrait 用の corner-start flood fill を追加する。
- `.codex/skills/background-transparent/scripts/verify_remove_background.py` に multi-pass が白い服を大きく透明化しない検証を追加する。
- `.codex/skills/background-transparent/SKILL.md` に multi-pass の使い方を追記する。
- hidamari の対象画像 4 枚を再処理し、`transparent-v3` に `*-transparent.png` と `*-preview.png` を保存する。
- `docs/OVERVIEW.md` と `docs/plan.md` に current state を最小反映する。
- delta 記録を `docs/delta/DR-20260628-background-transparent-multipass-refine.md` に残す。

## 非対象（Out of Scope）
- hidamari の React コード変更。
- 元画像、既存 `transparent/`、既存 `transparent-v2/` の上書き。
- ML / semantic segmentation 依存の追加。
- 背景以外の画像補正、リペイント、輪郭追加。

## Candidate Files/Artifacts
- `.codex/skills/background-transparent/SKILL.md`
- `.codex/skills/background-transparent/scripts/remove_background.py`
- `.codex/skills/background-transparent/scripts/verify_remove_background.py`
- `docs/OVERVIEW.md`
- `docs/plan.md`
- `docs/delta/DR-20260628-background-transparent-multipass-refine.md`
- `C:/Users/naruhide/workspace/hidamari/docs/assets/manager/transparent-v3/manager-neutral-transparent.png`
- `C:/Users/naruhide/workspace/hidamari/docs/assets/manager/transparent-v3/manager-neutral-preview.png`
- `C:/Users/naruhide/workspace/hidamari/docs/assets/manager/transparent-v3/manager-happy-transparent.png`
- `C:/Users/naruhide/workspace/hidamari/docs/assets/manager/transparent-v3/manager-happy-preview.png`
- `C:/Users/naruhide/workspace/hidamari/docs/assets/manager/transparent-v3/manager-thinking-transparent.png`
- `C:/Users/naruhide/workspace/hidamari/docs/assets/manager/transparent-v3/manager-thinking-preview.png`
- `C:/Users/naruhide/workspace/hidamari/docs/assets/manager/transparent-v3/manager-concerned-transparent.png`
- `C:/Users/naruhide/workspace/hidamari/docs/assets/manager/transparent-v3/manager-concerned-preview.png`

## 差分仕様
- DS-01:
  - Given: 背景残りがある白系背景の画像がある。
  - When: `remove_background.py --mode auto --refine-passes 2` を実行する。
  - Then: 2 pass 目は既に背景として除去された領域から隣接する背景候補へだけ広がる。
- DS-02:
  - Given: 袖や胴体の白い服が画像端に触れている cropped portrait がある。
  - When: `remove_background.py --mode auto --flood-source corners` を実行する。
  - Then: corner 以外の border に触れた白い服は flood fill の開始点にならない。
- DS-03:
  - Given: 白い服や淡色の被写体内部がある。
  - When: refinement pass を実行する。
  - Then: enclosed protection に該当する領域は refinement pass でも保持される。
- DS-04:
  - Given: hidamari の管理人さん画像 4 枚がある。
  - When: multi-pass 修正版 script で再処理する。
  - Then: `transparent-v3` に transparent PNG と preview PNG が非破壊で保存される。

## 受入条件（Acceptance Criteria）
- AC-01: refinement pass は border-connected / already-background-connected の連結条件を維持し、グローバルに白系 pixel を消さない。
- AC-02: synthetic regression で、multi-pass 実行時も白い服領域の alpha が大きく透明化されない。
- AC-03: hidamari の 4 枚について `transparent-v3` に `*-transparent.png` と `*-preview.png` が生成される。
- AC-04: `SKILL.md` に multi-pass 推奨 option が追記される。
- AC-05: `SKILL.md` に cropped portrait 用の `--flood-source corners` 推奨が追記される。
- AC-06: `py_compile`、regression、skill validation が PASS する。

## Verify Profile
- static check: Required
- targeted unit/smoke: Required
- targeted integration / E2E: Required
- skill validation: `skill-creator/scripts/quick_validate.py`

## Canonical Sync Mode
- mode: post-archive sync
- reason: script option、skill docs、再現出力を verify PASS 後に閉じる。

## 制約
- 元画像は上書きしない。
- hidamari の React コードには触らない。
- Pillow 以外の外部依存を追加しない。
- multi-pass は opt-in とし、既存の 1 pass 既定動作を壊さない。

## Review Gate
- required: No
- reason: 既存 script の追加 option と検証追加に閉じ、既存 command の破壊を伴わない。

---

## Step 2: delta apply
- `remove_background.py` に `--refine-passes` / `--refine-*` を追加し、2 pass 目以降は既に選択された背景領域からのみ背景候補へ広げるようにした。
- `remove_background.py` に `--flood-source corners|border` を追加し、既定を `corners` にした。
- `verify_remove_background.py` で enclosed white clothing case を `--refine-passes 2` でも検証するようにした。
- `SKILL.md` に `--refine-passes 2` と `--flood-source corners` の使い方を追記した。
- hidamari 管理人さん画像 4 枚を `transparent-v3` に非破壊で再出力した。

## Step 3: delta verify
- PASS: `uv run --with pillow python -m py_compile .codex\skills\background-transparent\scripts\remove_background.py .codex\skills\background-transparent\scripts\verify_remove_background.py`
- PASS: `uv run --with pillow python .codex\skills\background-transparent\scripts\verify_remove_background.py`
- PASS: `$env:PYTHONUTF8='1'; uv run --with pyyaml python C:\Users\naruhide\.codex\skills\.system\skill-creator\scripts\quick_validate.py .codex\skills\background-transparent`
- PASS: `C:\Users\naruhide\workspace\hidamari\docs\assets\manager\transparent-v3\` に 4 枚分の `*-transparent.png` と `*-preview.png` が存在することを確認した。
- Visual check: `transparent-v3` は袖・白ブラウスの大きな抜けを抑えた。髪や肩の後ろに白い背景島が残る箇所はある。

## Step 4: delta archive
- status: PASS
- archived_at: 2026-06-28
- sync:
  - `docs/OVERVIEW.md` の Active Delta をなしに戻し、直近完了を本 delta に更新した。
  - `docs/plan.md` の current checkbox と archive summary を更新した。
