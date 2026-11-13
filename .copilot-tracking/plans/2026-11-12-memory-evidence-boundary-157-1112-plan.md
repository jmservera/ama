---
title: Issue 157 memory-as-evidence boundary plan
ms.date: 2026-11-12
task_id: memory-evidence-boundary-157-1112
---

## Objective

Add one end-to-end boundary test to the existing `ApiTests` harness in `src/api/tests/test_assistants.py` proving that active synthetic chat memory cannot become evidence on the chat -> registered-assistant proposal path. Research: [research](../research/2026-11-12-memory-evidence-boundary-157-1112-research.md). Details: [details](../details/2026-11-12-memory-evidence-boundary-157-1112-details.md). Refs #157 only; the criterion stays unticked.

## Phases

* [x] Phase 1: one independent critique of the final candidate plan; apply compatible findings.
* [x] Phase 2: add the test method (and only the imports it needs) to `ApiTests`.
* [x] Phase 3: focused validation: the new test, `test_assistants`, `test_chat_isolation`, `test_chat_panel`, core `test_chat_memory`; ruff check, ruff format --check and mypy on the touched test file as the repository configures them.
* [x] Phase 4: changes record, one original Review, local commit with repo-local privacy-safe identity.

## Boundaries and stop rules

* Tests only, one existing test file plus RPI evidence. No production edit, no new invariant, registry assistant, administrator policy or personal-data processing.
* Do not touch `test_assistant_release.py`, `assistant_process_worker.py` (#107), `app.js` or its copy tests (#153), `store.py` (#82). If overlap becomes necessary, stop and return an ordering requirement.
* If the test exposes a real promotion path, preserve the failing output, stop, and report it as a distinct defect with its evidence; do not patch within this candidate without reconciling scope.
* Local only: no push, PR, merge, tick or board mutation. The provider is a local test double: simulated evidence, not model, human or production acceptance.
