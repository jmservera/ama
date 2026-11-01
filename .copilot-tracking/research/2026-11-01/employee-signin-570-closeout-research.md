---
title: Issue 570 closeout research
ms.date: 2026-11-01
---

## Findings

* Cause: the runner compared against a roster/name style expected identity while Entra authoritatively binds the immutable identity. Fixed and merged in #574, #601 and #644 (see 2026-10-31 research/changes artifacts in this folder tree).
* Main (efebfc6d) contains the fix; branch fix/employee-signin-identity-check has no unmerged commits.
* Criteria 1 and 2 are proven by merged PRs; criterion 3 (live chat, map filters, case view with the test user) needs credentials and an independent identity attestation that this session does not have.
* Planning Readiness: Ready (evidence-only closeout).

## Validation observed

* src/api: 23 employee_* unit tests OK (discover, PYTHONPATH core/agents tests); ruff check, ruff format --check, mypy clean.
