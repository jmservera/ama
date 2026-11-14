# Plan: C1 correction of the #80 list-export candidate

Research: [research](../../research/2026-11-13/80-c1-rebase-fix-2250-research.md). Details: [details](../../details/2026-11-13/80-c1-rebase-fix-2250-details.md).

## Phases

* [x] Phase 1: fetch and rebase onto current origin/main; resolve the role-inventory conflict keeping `proposal-freshness` and the new CSV routes.
* [x] Phase 2: fix the vacuous regex and tautology; align importer `safe_cell` with core; add focused unit tests.
* [x] Phase 3: enrich law and proposal export rows (Criterion 4 metadata) with tests.
* [x] Phase 4: Focused-tier validation in `/tmp/venv-80-c1` (pip only), recorded by actually running it.
* [x] Phase 5: remove the venv, commit with Conventional Commits and the Copilot trailer; no push, no PR.

## Decisions

* Validation tier: Focused (owner-selected for C1); the full gate and external receipt are not claimed.
* Original `80-every-list-export-2035-*` artifacts are left untouched.
