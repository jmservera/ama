---
title: Issue 80 r12 plan, harness test isolation and current preservation proof
description: Plan and one-pass critique before any test or README edit
ms.date: 2026-11-06
---

* Research: [research](../research/2026-11-06-excel-transition-80-r12-test-isolation-research.md). Details: [details](../details/2026-11-06-excel-transition-80-r12-test-isolation-details.md).
* [ ] Phase 1: isolate the default-scratch test in an owned temporary ROOT via `patch.object`; the test must not create `.venv` in the real checkout.
* [ ] Phase 2: correct the README paragraph to current tense.
* [ ] Phase 3: focused checks (four harness tests, Ruff, format, mypy on the test), source-status and byte-identity of production and harness files against 5fa44964.
* [ ] Phase 4: Changes, state, validation; commit; separate later Review; commit.
* [ ] Phase 5: after the final commit, external current-head preservation proof under a new `/mnt/ama-gates/e80-r12-r65-1106`; no deletion.

## Critique (one pass, applied directly)

* Risk: patching `ROOT` could also be hit by the other tests that read `harness.ROOT`; scope the patch to the one test only. Applied.
* Risk: the test should still prove the legacy result. It asserts `scratch_parent() == tmp / ".venv"` and that the real checkout gained no `.venv` entry in this test's execution is shown by the temp root holding it. Applied.
* Risk: preservation snapshot taken before the Review commit would again be stale. Phase 5 runs strictly after the last commit. Applied.
* Risk: a proof helper that only checks inventory rows misses deleted originals. The helper compares against `git ls-tree` of the frozen head and the current directory walk in both directions. Applied.
* No finding conflicts with a confirmed decision; no user decision needed.
