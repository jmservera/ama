---
title: Issue 570 RPI rerun research
ms.date: 2026-11-01
---

## Findings

* Cause (criterion 1): the recorded cause was the runner's display-email gate, which compared `account.email` with the expected email. It was not a roster or display-name comparison; roster binding stays diagnostic (historical predicate in `.copilot-tracking/changes/2026-10-30/live-acceptance-1030c/acceptance.py:42-50`; `src/api/README.md`). The historical account and the missing or different claim were not established, so this evidence does not imply an application mapping defect. The API binds the role from authoritative Entra claims. Evidence: research/2026-10-31 identity-check artifacts and merged #574, #601 and #644.
* Fix (criterion 2): merged on main. Regression evidence for the identity predicate is `src/api/tests/test_employee_identity_check.py`, including `test_correct_rosterless_account_needs_no_display_email` and `test_same_display_email_cannot_admit_another_account`. The four tests in `test_employee_live_acceptance.py` were rerun here, but they stub `verify_employee`, so they verify only the CLI behaviour, not the identity predicate.
* Criterion 3 (live chat, map filters, case view with the test user): owner comments on #616 and #617 record both fixes deployed on revision `ca-cutover-test-demo-api--emp-main-ac0c9968` on 1 November, so deployment is no longer a pending prerequisite. The strict live acceptance run remains outstanding and is routed to a later task; criterion 3 is not complete. This task must not touch live Azure or handle credentials.
* Research disposition: reused. Planning Readiness: Ready (evidence-only slice).

## Validation observed

* src/api employee live acceptance tests OK; ruff check and ruff format --check clean.
* mypy: 11 pre-existing environment errors (missing azure.eventhub/iot stubs, agents modules not installed); none in touched files because no source changed.
