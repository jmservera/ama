---
title: Critique of the SQL wiring plan for the unleased revocation test
description: Single actual critique before changes, produced by a read-only reviewer subagent; not human or independent-assessment approval
ms.date: 2026-11-07
---

Executed once on 2026-11-07 by a read-only `rubber-duck` subagent over the research, plan and details. The first author-only critique stays unchanged and is not retroactively relabelled. This critique is model-produced and is not human approval, independent exact-head assessment or hosted evidence. Verdict: proceed with one test-only correction.

## Findings and dispositions

* Blocking: `src/api/tests/test_assistants.py` (around line 1263) creates and revokes a UUID release, the fixture does not drop `assistant_releases`, and `release_support.install` deletes only `fx-%` rows. On actual SQL the final exact `["revoked"]` assertion could see extra rows. Disposition: accepted. Compatible and applied directly: the mixin gets a `setUp` that, after the base setup, deletes only non-`fx-` rows from `assistant_releases` in the disposable database, and the final assertion filters to `fx-CAP`. Test-only, no production change.
* Non-blocking: the runner rejects unexpected integration skips but does not require this test's success line, so tuple membership alone does not prove execution. Disposition: accepted as a recorded limit. No extra tool logic is added; the coordinator and the later review confirm the verbose log shows `test_independent_worker_revocation_denial_is_durable_for_an_unleased_task` as `ok` and not skipped.
* Confirmed: the runner supplies `ZF_TEST_MSSQL=1`, loopback host and test paths; the fixture overrides `ZF_SQL_DATABASE`; no hash, receipt or workflow-parity break was found from appending the selector. Hosted workflows still omit the class (disclosed gap).
* Egg-info relocation looks safe; verify imports, editable metadata and `pip check` afterwards.

No significant or divergent issue needed an owner decision.
