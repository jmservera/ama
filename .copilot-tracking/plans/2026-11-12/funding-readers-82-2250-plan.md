---
title: Issue 82 funding readers fail-closed plan (follow-up RV01)
ms.date: 2026-11-12
task_id: funding-readers-82-2250
---

## Objective

Make the three remaining readers of `funding_ok` use the delivered canonical definition: only an explicit `True` is confirmed. Non-boolean, `None` and absent values then never read as confirmed or as "no funding blocker", and an absent key no longer raises `KeyError` in the home case view. Research: [research](../../research/2026-11-12/funding-readers-82-2250-research.md). Details: [details](../../details/2026-11-12/funding-readers-82-2250-details.md). Refs #82 only; parent task `server-gate-readiness-82-1112`.

## Phases

* [ ] Phase 1: one independent critique of this final candidate plan in [critique](funding-readers-82-2250-critique.md); apply compatible findings.
* [ ] Phase 2: add failing-first regressions in existing tests, record failing output, then apply the three one-expression changes.
* [ ] Phase 3: focused validation of modified and impacted tests, ruff and mypy on touched files.
* [ ] Phase 4: changes record, one original Review, local frozen commit with repository-local privacy-safe identity.

## Boundaries and stop rules

* Write surface: `chat_case_answers.py`, `taskqueues.py`, `home_case.py` and directly related existing tests only (plus dated RPI evidence).
* No change to `gates.py`, `store.py`, any gate, role, consent, safety hold or independent-review logic; no new helper, rule, finance gate, template or approval. `True` stays confirmed.
* The original 1490 head and worktree are not touched. No push, PR, merge, issue creation or edit, tick, human approval, full gate, cleanup, cloud, model or spend call, and no private data.
* Local frozen follow-up only; prospective child of the UX parent with explicit dependency on 1490 and #82 reaching that parent first. One candidate; Review findings become later work.
