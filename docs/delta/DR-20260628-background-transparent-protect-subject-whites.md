# delta-request

## Delta ID
- DR-20260628-background-transparent-protect-subject-whites

## Delta Type
- REPAIR

## 目的
- `background-transparent` の `auto` 背景除去で、白い服や淡色の被写体内部が透明化される問題を修正する。
- hidamari の管理人さん画像 4 枚を再現ケースとして使い、`transparent-v2` に修正版 PNG / preview を生成する。

## 変更対象（In Scope）
- `.codex/skills/background-transparent/scripts/remove_background.py` の `auto` 背景判定を、外周からの flood fill と外周代表色への近さを基本に修正する。
- `.codex/skills/background-transparent/SKILL.md` に、白い服や淡色被写体を守るための推奨 mode / option を追記する。
- `.codex/skills/background-transparent/scripts/verify_remove_background.py` を追加し、白い服が大きく透明化されない回帰検証を行う。
- hidamari の対象画像 4 枚を再処理し、`transparent-v2` に `*-transparent.png` と `*-preview.png` を保存する。
- `docs/OVERVIEW.md` と `docs/plan.md` に current state を最小反映する。
- delta 記録を `docs/delta/DR-20260628-background-transparent-protect-subject-whites.md` に残す。

## 非対象（Out of Scope）
- hidamari の React コード変更。
- 元画像や既存 `transparent/` 出力の上書き。
- semantic segmentation や ML 依存の追加。
- ComfyUI workflow 追加。
- 任意の複雑背景の完全自動切り抜き保証。

## Candidate Files/Artifacts
- `.codex/skills/background-transparent/SKILL.md`
- `.codex/skills/background-transparent/scripts/remove_background.py`
- `.codex/skills/background-transparent/scripts/verify_remove_background.py`
- `docs/OVERVIEW.md`
- `docs/plan.md`
- `docs/delta/DR-20260628-background-transparent-protect-subject-whites.md`
- `C:/Users/naruhide/workspace/hidamari/docs/assets/manager/transparent-v2/manager-neutral-transparent.png`
- `C:/Users/naruhide/workspace/hidamari/docs/assets/manager/transparent-v2/manager-neutral-preview.png`
- `C:/Users/naruhide/workspace/hidamari/docs/assets/manager/transparent-v2/manager-happy-transparent.png`
- `C:/Users/naruhide/workspace/hidamari/docs/assets/manager/transparent-v2/manager-happy-preview.png`
- `C:/Users/naruhide/workspace/hidamari/docs/assets/manager/transparent-v2/manager-thinking-transparent.png`
- `C:/Users/naruhide/workspace/hidamari/docs/assets/manager/transparent-v2/manager-thinking-preview.png`
- `C:/Users/naruhide/workspace/hidamari/docs/assets/manager/transparent-v2/manager-concerned-transparent.png`
- `C:/Users/naruhide/workspace/hidamari/docs/assets/manager/transparent-v2/manager-concerned-preview.png`

## 差分仕様
- DS-01:
  - Given: 背景と同じく明るい白系の服が画像内にある。
  - When: `remove_background.py --mode auto` を実行する。
  - Then: 背景判定は外周代表色に近い border-connected pixels を基本とし、外周色から離れた白い服を透明化しない。
- DS-02:
  - Given: plain white background の画像がある。
  - When: `remove_background.py --mode auto` を実行する。
  - Then: 外周代表色が白の場合は、従来どおり白背景を透明化できる。
- DS-03:
  - Given: hidamari の管理人さん画像 4 枚がある。
  - When: 修正版 script で再処理する。
  - Then: `transparent-v2` に transparent PNG と preview PNG が非破壊で保存される。

## 受入条件（Acceptance Criteria）
- AC-01: `auto` mode は外周代表色への近さを使い、外周色と無関係な bright neutral pixel を無条件に背景扱いしない。
- AC-02: synthetic regression で、白い服領域の alpha が大きく透明化されない。
- AC-03: synthetic white background smoke で、背景が透明化され、中心 subject は保持される。
- AC-04: hidamari の 4 枚について `transparent-v2` に `*-transparent.png` と `*-preview.png` が生成される。
- AC-05: `SKILL.md` に白い服 / 淡色被写体を守る推奨が追記される。
- AC-06: `py_compile` と skill validation が PASS する。

## Verify Profile
- static check: Required
- targeted unit/smoke: Required
- targeted integration / E2E: Required
- skill validation: `skill-creator/scripts/quick_validate.py`

## Canonical Sync Mode
- mode: post-archive sync
- reason: script 修正、skill docs、再現出力、repo state を verify PASS 後に閉じる。

## 制約
- 元画像は上書きしない。
- hidamari の React コードには触らない。
- Pillow 以外の外部依存を追加しない。
- 既存の `white` / `checker` mode は維持する。

## Review Gate
- required: No
- reason: 単一 skill の script 判定改善と検証追加に閉じた修正であり、既存 command / data model の破壊を伴わない。

## 未確定事項
- 複雑背景や被写体と背景が同色で境界がないケースは、今後 semantic extraction delta が必要になる可能性がある。

---

## Step 2: delta apply
- `remove_background.py` の `auto` mode を、corner seed を既定にした外周代表色近傍の border-connected background 判定へ変更した。
- 白い服や淡色ハイライトが背景候補になった場合に、強い前景ストロークに囲まれた領域を保持する `--protect-enclosed-radius` 系 option を追加した。
- `verify_remove_background.py` を追加し、白い subject / plain white background / enclosed white clothing の synthetic regression を実行できるようにした。
- `SKILL.md` に、白い服や淡色被写体では `--mode auto --seed-source corners` と preview 確認を優先する説明を追加した。
- hidamari 管理人さん画像 4 枚を `transparent-v2` に非破壊で再出力した。

## Step 3: delta verify
- PASS: `uv run --with pillow python -m py_compile .codex\skills\background-transparent\scripts\remove_background.py .codex\skills\background-transparent\scripts\verify_remove_background.py`
- PASS: `uv run --with pillow python .codex\skills\background-transparent\scripts\verify_remove_background.py`
- PASS: `$env:PYTHONUTF8='1'; uv run --with pyyaml python C:\Users\naruhide\.codex\skills\.system\skill-creator\scripts\quick_validate.py .codex\skills\background-transparent`
- PASS: `C:\Users\naruhide\workspace\hidamari\docs\assets\manager\transparent-v2\` に 4 枚分の `*-transparent.png` と `*-preview.png` が存在することを確認した。
- NOTE: deterministic script のため、背景と被写体が同色で境界が弱い部分には小さな残りや過剰抜けがあり得る。

## Step 4: delta archive
- status: PASS
- archived_at: 2026-06-28
- sync:
  - `docs/OVERVIEW.md` の Active Delta をなしに戻し、直近完了を本 delta に更新した。
  - `docs/plan.md` の current checkbox と archive summary を更新した。
