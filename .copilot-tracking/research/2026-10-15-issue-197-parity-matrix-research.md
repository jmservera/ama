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
