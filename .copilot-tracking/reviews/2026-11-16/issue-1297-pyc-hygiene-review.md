---
title: "Issue 1297 gate bytecode hygiene review"
ms.date: 2026-11-16
---

## Execution and outcome

Review executed once by the RPI worker over the uncommitted diff at head 2e9bd4ab6a84492da704f068ecf5e7fc65ebcd1b (tools/rpi-checks.py, tools/test_rpi_checks.py). Outcome: conformant for the reviewed boundary; this is self-review and does not replace the coordinator's independent exact-head review, human approval or hosted CI. Full gate evidence is not yet claimed.

## Checks

* Root cause evidence reproduced: scrubbed core discovery-demo child writes exactly the six retained `.pyc` names; Runner bytecode variables never reached it.
* Fix scope: interpreter-level policy in every gate venv; api-only out-dir receipt file unchanged; no change to `clean_identity`, snapshot inputs, skip allowlists, SQL dispatch or the retained receipt.
* Regression test failed before the fix (5/5 venv subtests) and passes after; `tools.test_rpi_checks` 108 OK; gate-equivalent ruff clean.
* The venv `.pth` is hashed (not executed) in the environment startup identity; no test depended on its absence.

## Findings routed to later work

* A scrubbed child using a non-venv interpreter, or a venv whose site-packages path is not `lib/python3.12`, is not covered. Hosted/browser prerequisite results and the full receipt remain pending.
* Prior follow-up (wire ZF_RESIDENT_MSSQL classes into the SQL group) is unchanged.
