---
title: Issue 126 RAI evidence register implementation evidence
ms.date: 2026-10-18
---

Task 126; slug issue-126-rai-evidence-register; full plan scope.
Base ab0613f3336109ff9b96560a16758ee842232715.
Status: ordered RPI and publication complete; stopping for coordinator exact-head
inspection. No implementation workers.

## P01: Core/API

Baseline command `python3 -m unittest discover -s src/core/tests -p test_governance.py -q`
failed with missing zava_forward distribution. Then created owned .venv and pip
installed editable src/core[dev,sql], src/agents, src/api[dev]. Repeated baseline:
23 tests passed. No private data read. No PYTHONPATH=mvp or uv.

Sole critique Complete/Revise, PC-001/002 applied in plan/details before source edits.
Original SHA256 4e24e7e0cc8cf21081c4e5823cbbfbd8fbf0d1d0a8e904220ecd5b0e3235c8bb.
Correction count: 0. Sole original implementation Review now completed below.

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

Sole original Review:
.copilot-tracking/reviews/2026-10-18/issue-126-rai-evidence-register-review.md.
Execution Complete; outcome Conformant for bounded engineering; no actionable
RV findings. Assessed source d0bb02df6a0e8ea52fe56f409b24cfcf6db2ea90 and all
28 candidate files/receipts. Fresh read-only semantic/integrity checks are recorded
in that original; SQL/image/HTTP receipts were inspected, not rerun by reviewer.
Original SHA256 12788d8f7f81279012b54ba3902255f2eabe436d61d97fda3a0ae701bb6b6c24.
Original critique SHA256 remains
4e24e7e0cc8cf21081c4e5823cbbfbd8fbf0d1d0a8e904220ecd5b0e3235c8bb.
Neither original was modified. No post-Review source changes, corrections or
second Review. All remaining human/live gates remain explicit and unmet.

Publication: https://github.com/jmservera/ama/pull/409, main target.
Pinned implementation base ab0613f3336109ff9b96560a16758ee842232715.
Observed live PR base at creation 9403dc6a8f52f1f04c5ad910faab11a57c29ee78,
not the pinned base; main moved independently. No rebase, merge or lineage rewrite.
Authenticated gh account id8036360/login jmservera supplied repo-local noreply
author/committer identity. Source/initial artifacts commit d0bb02df6a0e8ea52fe56f409b24cfcf6db2ea90.
Final handoff commit adds original Review, full inventory and lifecycle bookkeeping
only; source/docs remain identical to the assessed source commit.
PR creation verified closingIssuesReferences empty. No issue/board/acceptance
action or merge occurred. Coordinator owns integration of concurrent work.

### Actual Ordered Phase Log

1. Research executed focused Wider -> Deeper -> Contrarian, synthesized Ready.
2. Plan and separate phase details authored from verified source.
3. Exactly one final-candidate critique executed Complete / Revise; PC-001/002
   dispositioned directly in plan/details, original retained.
4. Implement executed failing-first -> bounded source -> local/SQL/HTTP/image/
   preservation/quality checks -> supported current documentation.
5. Exactly one original Review executed Complete / Conformant; findings none.
6. Published non-closing PR #409; final owned evidence handoff; explicit caller Stop.

Every phase uses date 2026-10-18 and slug issue-126-rai-evidence-register.
Full changed inventory is the adjacent `issue-126-rai-evidence-register-inventory.txt`.
Session: .copilot-tracking/rpi-sessions/2026-10-18/issue-126-rai-evidence-register-state.json.
No implementation blockers; required human/live acceptance is explicitly unmet.
No issue acceptance or closure. Stop for independent coordinator inspection of
the final exact head, all source/artifacts and retained raw logs.

## Amendments and Divergences

Ordinary tightly coupled discovery: existing governance GET was unreachable because
generic projection.STAFF_GET does not list governance. Moved only governance read
integration ahead of that generic guard, retaining its fresh registered manager
guard. No generic role or endpoint grants changed. HTTP failed first (403 manager)
and passes after. JSON removed login identity correctly returns 401, not 403;
test oracle corrected, not a source authority change.

Caller-declared assessment context, not server build attestation, is an
explicit planned limitation; no additional config or authority fabricated.

## Authorized Same-Task Integration-Only Continuation

The original publication/no-rebase statements above remain historical. Coordinator
subsequently authorized exact owned-topic rebase from original base ab0613f3 and
head `4a23f750f1ea943bb4aaf989256e7bd019a57d12` onto exact
`9403dc6a8f52f1f04c5ad910faab11a57c29ee78`, PR #389 consultation merge.
Expected clean local/remote heads were verified before mutation. Rebase replayed
the two owned commits; only manual conflict was the append-only KB log. Its exact
upstream prefix and original issue-126 addition were retained in that order.

Rebased original source/handoff head:
`93b7450c823d80765d869e533788662f3c61f94a`. All original 30-path normalized
patches match, SHA256
`bb16f170463c1b3fffc075262db4b33e6f2ac8bdf63cf423792694af4e9c6548`.
Six-source/config/test patch SHA256
`2c94988bd6b03e082cd553038beb677855bf1a3b46c1bb4f91ed6ffecbe48026`.
Every nonowned target file/mode (2599 paths), consultation route, procurement/
tests, UX links, additive README/index content and original immutable evidence
were preserved. Only current plan/details/changes/state receive descriptive
bookkeeping; research, adverse critique, original Review and prior logs do not.
Original inventory remains 30 paths; separate integration additions are inventoried.

Fresh integration checks, not another Review:

* Governance/actual local HTTP/assistant release: 107 run, 91 passes, 16 explicit
  MSSQL opt-in skips. Expected injected failure traces are retained in raw output.
* Consultation controls and procurement/API: 64 run, 51 passes, 13 explicit skips.
* Configured core/API Ruff and mypy pass, 125/57 source files.
* Configured formatter checks pass, 72 core/25 API files. Existing exclusions
  cover governance/sqlstore/test_governance/server; explicit stdin diagnostics
  show those four would reformat both before and after integration. No bulk
  formatting, new exception or source correction was performed.

The complete actual original CLI log (846 lines, 39413 bytes) was read and copied
byte-identically to the resumed session's files directory; SHA256
`918e07c62d006a4c4034ca16a036f540710149ad5f5af453651a6a11aa8e0072`.
This supports the actual ordered phase history, together with original detailed
raw receipts; artifact presence alone is not execution evidence.

Separate integration receipt, commands, raw logs and full path/hash manifests:
issue-126-rai-evidence-register-integration/receipt.md.
Original SQL16/16 and hardened image107/skip16 are historical, not freshly repeated.
No persistence/packaging conflict or production intent change justified a broad
rerun in this integration-only scope. Original critique/Review hashes unchanged;
source correction count 0, additional critiques 0, additional original Reviews 0.
Publish with the exact authorized lease only, subsequent receipts normal; preserve
Refs #126 and empty closing issue references. All human/live acceptance remains
unmet. Stop for independent coordinator full exact-head source/artifact/log inspection.

Exact authorized first lease succeeded, publishing integration metadata
`b38067293741c5667dd07f5e15e8b2ee39abd823`; remote and PR #409 verified that head,
exact base9403dc6a and empty closing references. First immediate PR cache was stale,
then converged without another branch write. Final receipt is normal-pushed;
full final inventory is original30 plus integration27 paths. Final exact head is
bound by the normal-push output and PR body, not a recursive self-commit claim.
Automatic Follow-up remains completed/stopped, with coordinator independent
exact-head inspection next. No additional original Review, critique or correction.

Final-manifest repeat initially stopped before commit/push on a mixed
absolute/workspace-relative path assertion after the first receipt became tracked.
Corrected only the new integration utility's root normalization and regenerated
workspace-relative inventory/hashes. Raw failed attempt remains in the final
session publication log. No production source or original assessment was changed;
source correction count stays 0.
