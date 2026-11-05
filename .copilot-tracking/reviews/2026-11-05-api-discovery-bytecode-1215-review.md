---
title: Review - API discovery bytecode policy move (#1215)
description: Single independent Review of the uncommitted candidate and its routing
ms.date: 2026-11-05
ms.topic: reference
---

## Execution

* Executed once, by an independent read-only code-review agent, on the uncommitted working tree against base c6d5a8f3c3a35892322300be27b9747f7b11362d (files: `tools/rpi-checks.py`, `tools/test_rpi_checks.py`, `src/README.md`, `docs/reference/log.md`).
* The reviewer ran `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tools.test_rpi_checks`: 86 tests passed.

## Outcome

No significant issues found; overall outcome pass. Reviewer statements preserved:

* The move covers `project-api` and `setup-api`; the policy exists before API discovery.
* The browser-group copy is removed; the receipt still requires `browser-bytecode-policy.pth` when the browser group ran; `environment_identity` is computed at receipt time, so no resume path breaks.
* No weakening of environment scrubbing, the dirty-snapshot guard, cleanup or receipt acceptance.
* Research claims are labelled as inferred where the producer process was not traced.

## Reviewer limitations (recorded, not resolved here)

* The reviewer did not re-run the new regression against the old code. The "fails before" result rests on the main session's recorded run in the changes artifact (three `__pycache__` directories created, exit failure).
* The reviewer did not open the `.copilot-tracking` research files beyond the log entry.
* Non-blocking critique note (setup-api/sealed-receipt/resume test) remains unaddressed.

## Routing

No open defects. Later user-selected work: optional sealed-receipt/resume coverage for `setup-api`; independent exact-head assessment, hosted CI and human approval remain required. No second Review is run in this task. The focused gate run follows the candidate commit and is recorded externally and in the handoff, not in this artifact.
