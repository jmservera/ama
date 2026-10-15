---
title: Issue 197 parity matrix research
ms.date: 2026-10-15
---

* Task: build `docs/architecture/mvp-to-src-parity-matrix.md` (issue #197, epic #195). Research disposition: executed. Planning readiness: Ready.
* Read: copilot instructions, case study and addendum, knowledge base index and memory, ADRs 0001 to 0005, issues #195 to #203, PRs 235 to 287 (bodies, file lists, linked issues).
* Inventory: `git ls-files mvp prototype` is 125 files (42 modules, 46 test files, 11 web, 4 evals, 1 law, 1 policy, build files, 10 prototype files).
* Import graph (top-level and lazy imports): `store` imports 18 siblings; cluster `store`, `sqlstore`, `assistants`, `ai_registry`, `continuity`, `ledger` cannot be split.
* ADR 0001: agents app has no database access and is queue driven; `assistants.py` leases tasks in SQL in the API process. Rebuild under #107.
* Baseline: 703 tests, 92 skipped on `main` at `1ffcfbc` (run 2026-10-15).
* Closed issues checked against acceptance criteria: #151 and #175 have unmet criteria; #210 caveat (Azure deployment unverified).
* PR 287 (open) commits 72 `.assistant-test-*` sandbox files.
* Owner decisions applied: src layout, `zava_forward` namespace, several isolated packages, `zavaforward_mvp` dropped, rubric dip accepted, prototype first, tag `v<BRD version>`.
* Unknowns: ADR 0006 (draft on another branch); no Azure use needed.

## Fix iteration 2026-10-15 (PR #291 review)

* Research disposition: executed (delta). ADR 0006 is Accepted and merged; PR 287 merged. `git ls-files mvp prototype` is now 578 files: 128 real (adds `assistant_release.py`, `release_support.py`, `test_assistant_release.py`) and 450 sandbox files in 225 `mvp/.assistant-test-*` directories.
* Baseline: 719 tests, 92 skipped (703 plus 16 in test_assistant_release), run 2026-10-15 on the branch merged with `main` at `736b387`.
* ADR 0006 module mapping read in full: no `devtools` package; `scale_fixture`, `sensor_backfill`, `loadcheck` to `core.synthetic`; `ai_eval`, `ai_registry`, `assistants` and their evals to `agents`; `digest_blob`, `token_store` to `orchestrator`; form fixtures to `importer`.
* Import graph check found core lazily importing `ai_registry` and `assistants` (agents), which the dependency rule forbids; `assistant_release` is unmapped. Recorded as proposed ADR amendments A1 to A5, not silent deviations.
* Owner answers of 2026-10-15 recorded: old check names until after cut-over, then one rename PR (#200); GitHub release with the archive tag (#202); agents image without the `sql` extra; no soak period.
* Planning readiness: Ready.
