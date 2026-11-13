---
title: 1530 c3 TSV rebase plan
ms.date: 2026-11-13
---

Details: all steps inline.

1. Rebase paused at b1d4bc59d; take base TSV (`--ours` in rebase), regenerate with `cutover_audit --write`, check mode passes, `git add`, `rebase --continue` without editing the message.
2. Verify `git diff origin/main..HEAD -- src docs/reference` equals the original `git diff 2c71e2c21..b1d4bc59d` for src and design-system.md (patch-id / byte equality of blobs).
3. Run test_cutover_audit, test_safety_panel_ux, test_scenario_manifest, test_needs_inventory, ruff check, ruff format --check, mypy in the pinned venv.
4. Independent code-review, commit tracking artifacts, remove venv, verify clean tree and `git diff --check`.

Risk: the 3 commits are replayed; the TSV regeneration must also cover later commits' references, so regenerate again at the final HEAD (the TSV is only touched at b1d4bc59d but check-mode must pass at the end).
