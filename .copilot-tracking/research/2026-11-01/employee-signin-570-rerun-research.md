---
title: Issue 570 RPI rerun research
ms.date: 2026-11-01
---

## Findings

* Cause (criterion 1): the runner compared the Entra login with a roster or display-name style expected identity, while the API binds the role from authoritative Entra claims (immutable object id) with no roster binding. Evidence: research/2026-10-31 identity-check artifacts and merged #574, #601 and #644.
* Fix (criterion 2): merged on main with regression tests in src/api/tests/test_employee_live_acceptance.py (4 tests pass on this branch head).
* Criterion 3 (live chat, map filters, case view with the test user): not provable here. The 2026-10-31 owner decision unblocks live checks only after #616 and #617 are deployed, and this task must not touch live Azure or handle credentials.
* Research disposition: reused. Planning Readiness: Ready (evidence-only slice).

## Validation observed

* src/api employee live acceptance tests OK; ruff check and ruff format --check clean.
* mypy: 11 pre-existing environment errors (missing azure.eventhub/iot stubs, agents modules not installed); none in touched files because no source changed.
