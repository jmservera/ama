---
title: "#521 unified evidence pack details"
ms.date: 2026-11-13
---

* Cherry-pick with `git cherry-pick`; resolve log.md conflicts by keeping both entries.
* Link check: script resolving every Markdown link target in files changed vs 8ca5685b7.
* Inventory: `python3 -m zava_forward.core.synthetic.cutover_audit` (inspect module for CLI), then `test_cutover_audit`, `test_bicep_policy`, `pytest tools/capstone/test_build_assets.py`, validation.json hash check.
* Validation tier: Focused (documentation plus inventory regeneration).

## Critique dispositions (applied directly)

* PC-001: Markdown-aware link check with anchors over all changed .md files, including hidden tracking files.
* PC-002: Run tests unconditionally; locate the existing capstone test (`tools/capstone/test_build_assets.py` may be absent) and run what exists.
* PC-003: Set PYTHONPATH to this worktree's `src/core/src` and verify the imported module path.
* PC-004: Commit cherry-picks first so files are tracked, run cutover_audit with `--write` then check mode, inspect both generated TSVs.
