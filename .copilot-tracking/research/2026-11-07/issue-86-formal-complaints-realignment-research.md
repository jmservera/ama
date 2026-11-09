# Issue 86 formal-complaints parent re-alignment: research

Scope: jmservera/ama#86 only (`Refs #86`). Dated 2026-11-07. Alignment preparation only; no source feature scope. Preserved unchanged: the original research, plan, critique, changes, review and alignment records, the typing records, the R1 refusal, the R2 failed receipt (14 strict-mypy errors) and the R3 passing receipt.

## Evidence at start

* Child head `6ff492adf9d897c81ae666e71696f5a10ed1573d`, tree `b4a3af5d217f4cb60fd8c30cab9b810a6d2dcbcc`; ignored-inclusive status clean. Child is 3 original source/evidence commits, 1 alignment record, 2 typing commits (`7cc0d461f`, `6ff492adf`) on parent `c5edb320ad10d3d73bb985bfb82b2d0bee94381a`. Open PR 1243 head is this commit; the remote parent branch still reads `c5edb320`.
* Current `origin/main` is `0f420dc9514db22081cb48fa733267d9d33a0d24` (previously `56eec736`, an ancestor). Main moved by #1241 (checklist export), #1245 (#891 chat disclaimer) and scorer commits.
* The local parent branch `feat/controlled-lifecycle-integration-81` is now `ad72384f3` and is MOVING: it holds rpi-81's records (`2e3ca0d41`, `9da4ee89f`, `ad72384f3`) over earlier work; the original rpi-81 session is still running (PID `4160383` family, log `/tmp/rpi-81-post891-align-1107.log`) in `/home/azureuser/source/ama-wt/parent-81`. Its state is not final and is not a base.
* Verified after critique: `0f420dc95` (current main) IS an ancestor of `ad72384f3`; `c5edb320` is NOT an ancestor (parent history was rewritten, so the old boundary must stay `c5edb320`, never the merge-base `56eec736`). The child-versus-parent merge-base is `56eec736`. Parent diff from `c5edb320` does not touch `store.py`, `resident_decisions.py` or the core README, so conflict overlap must be reassessed against the final parent.
* Focused checks at the frozen head (own scratch `/mnt/ama-gates/restart-1107-86-align/`, R3 core venv tools read-only, `PYTHONPATH=src:tests`, import origin is this worktree): strict mypy 267 files no issues; `ruff check .` pass; `ruff format --check .` 214 files formatted; `unittest test_resident_decisions` 281 run OK, 101 skipped (SQL-backed, no service). These are pre-alignment results at the old head, not evidence for the aligned head.

## Alignment approach

* Do not replay by name. Child-only patches are exactly the six commits after `c5edb320` (`git rev-list c5edb320..6ff492adf`); verify with `range-diff` and the 11-file slice diff before and after.
* Only align after the parent is a clean, frozen outcome: rpi-81 absent, parent worktree clean, and the parent head resolved from both the branch ref and the worktree HEAD agreeing, with current main as an ancestor. Maximum wait 15 minutes; otherwise return an explicit no-alignment result.
* Rebase locally with `git rebase --onto <parent> c5edb320 HEAD` after creating a backup branch of `6ff492adf`. Prefer rebase (prior alignment used it, patch-equal); fall back to a documented merge only if conflicts show duplicated parent patches.
* Conflict policy: genuine minimal resolution only; likely files `store.py` and `resident_decisions.py`. No invented intent.

## Gates

FULL tier remains required for publication. `tools/rpi-checks.py --all` requires the base to be current `origin/main`; `--stack-member` does not relax it. No heavy gate is started here (#1231 is the sole heavy lane). Old g86 receipts at base `56eec736` are historical, not current.

Planning readiness: Ready, conditional on the parent outcome.
