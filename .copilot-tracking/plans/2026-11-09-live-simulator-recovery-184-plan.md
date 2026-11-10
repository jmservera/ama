---
title: "#184 recovery plan: merge main, reconcile ten-test contract, targeted validation"
ms.date: 2026-11-09
---

Ordering disclosure: the diagnosis (steps 1 to 3) was done interactively before these records were written, so research, plan and details are retrospective for those steps and prospective only for the validation tier. They were not backfilled as earlier dates.

Details: [details](../details/2026-11-09-live-simulator-recovery-184-details.md).

* [x] 1. Fetch origin/main and merge it locally preserving both intents (no rebase, no push).
* [x] 2. Fix the stale default-selection unit test (six selectors).
* [x] 3. Reconcile the analysis contract to ten tests: harness ANALYSIS_TESTS, main gate SENSOR_MSSQL_REQUIRED_TESTS (two added names) and the count-literal tests derived from the pinned tuple; README sentence.
* [x] 4. Run the owner-selected demo-targeted tier (details), owned SQL under the shared nonblocking heavy lock.
* [ ] 5. Write changes, one author review, state and handoff; commit a clean frozen candidate.

## Critique (author critique, executed once; recorded after the source edits, not before)

* Risk: weakening the gate. Mitigation: the pinned tuple grows by exactly the two named tests; exact-count and zero-skip checks stay and are tested by derived counts.
* Risk: duplicating #1297. Mitigation: only the two extra test names and count literals change; no runner logic.
* Risk: browser claim. Mitigation: none made; no web surface changed.
Verdict: proceed. No conflict with confirmed owner decisions.
