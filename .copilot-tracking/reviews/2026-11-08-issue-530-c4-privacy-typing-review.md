---
title: Issue 530 C4 chat privacy typing review
ms.date: 2026-11-08
---

* Execution: one authored Review after implementation. Outcome: conformant for the bounded typing correction and LIGHT scope. Not acceptance of #530.
* Conformance: plan phases 1 to 4 executed in order; critique F1 and F2 applied (Callable import; verbose id comparison and load-only MSSQL class check). Scope held to one test helper plus records.
* Cause finding: not an existing Main failure. Main's own snapshot passes API strict mypy (190 files, exit 0); the candidate import `test_chat_privacy` in `test_mssqlstore.py` exposed the untyped helper. Unchanged file identity alone was not used as evidence.
* Deviations: a first Main baseline attempt failed on missing `playwright` (45 import errors) until the `dev` extra was installed; the first candidate api install was non-editable and was reinstalled editable (recorded in changes). Four ignored generated paths from this task's installs were relocated with hash proof.
* Limitations: no 21-method actual SQL result, no three-state Chromium/axe result, no eligible receipt. The failed r1 receipt remains failed; a fresh admitted focused run on the final head is still required. Behaviour equivalence relies on AST equality and identical 29-test results, not on SQL execution.
* Follow-ups: 1. Separately admitted single-holder focused run for the actual SQL and chat browser states on the final source. 2. Fresh exact-head hosted CI and independent review. 3. Native CI parity for the chat browser check.
* Still unmet and not claimed: real sign-in, private-runner authority, model price and budget, real-model grounded answer, serving attestation, named agent confirmation, AT, resident, legal and professional approvals. #530 stays open (Refs only).
