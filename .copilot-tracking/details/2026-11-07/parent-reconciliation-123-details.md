<!-- markdownlint-disable-file -->
# Details: discovery parent reconciliation (#123), 2026-11-07

Plan: [plan](../../plans/2026-11-07/parent-reconciliation-123-plan.md).

## Merges

* Pins: parent `9bacb87dc04fb51ba747b35ec78061b05af184be`, main `b284d0d3e8ebed24d40bf9eb1e23de1ae9101d01`; verify `rev-parse` equality before each merge and merge the SHA.
* Success: both are ancestors of HEAD; first-parent history keeps `dec700c7` and the planning commit.
* Conflict rule for `docs/architecture/cutover-evidence-pack.md`: keep all parent sections and main's trailing #73 section; frontmatter `ms.date` takes 2026-11-07; remove markers only. Verify with a script that every non-marker line of each side's added text appears in the result in the same relative order.

## Scope

* `git diff --stat origin/main HEAD`; list paths outside `.copilot-tracking`; expect only `paired_equity.py`, `test_paired_equity.py`, `src/core/README.md`, the pack, KB index and log.

## Checks

* `PYTHONDONTWRITEBYTECODE=1`, `XDG_CACHE_HOME`, `RUFF_CACHE_DIR`, `MYPY_CACHE_DIR` under `/tmp`; interpreter and tool versions from the existing external environment; explicit `PYTHONPATH=<worktree>/src/core/src:<worktree>/src/core/tests` with `__file__` assertions. Use the configured core commands from `src/README.md` and `src/core`.
* Focused gate per Plan Phase 7 only.
