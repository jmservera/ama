---
title: Issue 126 RAI evidence register implementation evidence
ms.date: 2026-10-18
---

Task 126; slug issue-126-rai-evidence-register; full plan scope.
Base ab0613f3336109ff9b96560a16758ee842232715.
Status: P01/P02 complete; ready for sole original Review. No implementation workers.

## P01: Core/API

Baseline command `python3 -m unittest discover -s src/core/tests -p test_governance.py -q`
failed with missing zava_forward distribution. Then created owned .venv and pip
installed editable src/core[dev,sql], src/agents, src/api[dev]. Repeated baseline:
23 tests passed. No private data read. No PYTHONPATH=mvp or uv.

Sole critique Complete/Revise, PC-001/002 applied in plan/details before source edits.
Original SHA256 4e24e7e0cc8cf21081c4e5823cbbfbd8fbf0d1d0a8e904220ecd5b0e3235c8bb.
Correction count: 0 (no original implementation Review yet).

Fail-before: added first tests on unchanged source, 50 tests executed, 59 errors
(subtests included), 10 MSSQL opt-in skips; missing rai_evidence_record and old view
signature. Exact output retained as fail-before receipt.
Pass-after current focused suite: 107 tests, 16 MSSQL opt-in skips, no failure.
Ten actual local HTTP cases exercise JSON/SQLite with real login and loopback app.
Expected injected error logs are synthetic failures, not test failures.

Implementation uses existing governance checked meta document, no new source
module/table/service. Existing change_validation rechecks authenticated manager
inside SQL writer transaction; immediate post-COMMIT witness also covers refresh/
hook/lock-exit acknowledgement failures. Replay returns exact prior record, no
additional success audit. Inert owner references remain unverified.

## P02: Validation and documentation

Core Ruff and strict mypy (124 files) passed; API Ruff, new harness format and
strict mypy (57 files) passed. Existing project typing exemptions preserved;
new typed HTTP harness uses established untyped-Store-call exemption only.
Initial local SQL run: 12/12 actual disposable SQL tests passed, container removed.
Final expanded SQL run: 16/16 actual tests passed, no skips, fresh UUID database
per test, owned loopback container removed. Hardened image focused suite: 107 tests, 16 opt-in
SQL skips, passed as UID10001 with read-only root, all capabilities dropped,
no-new-privileges and tmpfs writable state. Image rebuild contains current source.
Image ID sha256:f3d12ecda16385484b187038aa254ec3ed07f59e5f826b2a66f0877afbf01056.
Additional existing provenance/finance/resident/procurement/continuity preservation
suite: 288 tests, 46 skips (resident opt-in MSSQL and SQL's JSON-only restoration
case), passed. Expected injected
failure tracebacks remain in receipts; they are not evidence of actual failures.

Commands (repository root unless noted):

```bash
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest test_governance test_governance_evidence_api test_assistant_release -q
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest test_change_provenance test_finance_signoffs test_resident_decisions test_quality_procurement test_continuity -q
PYTHONPATH=src/core/tests .venv/bin/python .copilot-tracking/changes/2026-10-18/issue-126-rai-evidence-register-sql-check.py
(cd src/core && ../../.venv/bin/ruff check . && ../../.venv/bin/mypy)
(cd src/api && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check tests/test_governance_evidence_api.py && ../../.venv/bin/mypy)
docker build -q -t zf-rai126-api:20261018 -f src/api/Dockerfile src
docker run --rm --read-only --cap-drop=ALL --security-opt=no-new-privileges --tmpfs /tmp:rw,nosuid,size=512m --tmpfs /state:rw,nosuid,uid=10001,gid=10001,size=128m -v "$PWD/src/core/tests:/checks/core:ro" -v "$PWD/src/api/tests:/checks/api:ro" -v "$PWD/src/agents/tests:/checks/agents:ro" -e PYTHONPATH=/checks/api:/checks/core:/checks/agents zf-rai126-api:20261018 python -c 'import os,unittest; print("image uid",os.getuid(),flush=True); assert os.getuid()==10001; r=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromNames(["test_governance","test_governance_evidence_api","test_assistant_release"])); raise SystemExit(not r.wasSuccessful())'
git diff --check
```

Receipts share this directory and stable slug: fail-before.log, local-tests.log,
image-build.log, image-tests.log, preservation-tests.log, sql.log. SQL runner is
owned evidence, not a runtime service. Password is randomly generated process-only,
never logged or committed. No owned running container remains.

Documentation updated: existing core/API guides, addendum, PRD implementation-status
note, ADR 0002, KB index and appended log. Original log byte prefix verified;
original case, memory and baseline report remain byte-identical. New relative
links resolve; git diff whitespace check passes. No web/UI change or Playwright.

Unperformed and not waived: actual Azure deployment, real model/Graph/IAM calls,
billable inference, witnessed restore/erasure, qualified human/privacy/legal/
operational review and current PRD acceptance. Local SQL is not application
acceptance. Whole issue 126 and all 22 baseline findings remain open.

## P03: Original Review/publication

Implementation review-ready: P01/P02 markers complete and details/current
validation reconciled. P03-T01 original Review and P03-T02 publication remain.
No implementation blockers; required human/live acceptance is explicitly unmet.
No issue acceptance or closure.

## Amendments and Divergences

Ordinary tightly coupled discovery: existing governance GET was unreachable because
generic projection.STAFF_GET does not list governance. Moved only governance read
integration ahead of that generic guard, retaining its fresh registered manager
guard. No generic role or endpoint grants changed. HTTP failed first (403 manager)
and passes after. JSON removed login identity correctly returns 401, not 403;
test oracle corrected, not a source authority change.

Caller-declared assessment context, not server build attestation, is an
explicit planned limitation; no additional config or authority fabricated.
