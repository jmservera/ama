---
title: Issue 122 new register and release remediation changes
description: Separate implementation and validation evidence for the newly authorized task
ms.date: 2026-10-18
---

## Task and Execution Boundary

issue-122-register-release-remediation, 2026-10-18, automatic full bounded scope.
Owner explicitly authorized this new task; previous independent Not accepted
and both exhausted historical correction cycles remain unchanged.
New critique executed once, Complete / Revise; PC-001 through PC-005 accepted
directly in plan/details. No second critique or original Review has run yet.

## P01 Exact Integration

Expected local and remote source head verified
1144647c8d539716e8ddddf9daa47407c9bd00ac. Fetched exact authorized main
9c648b2006e8b2e563823ea7d5aabdf7f1ac7096. Intake/plan evidence is committed
before the owner-authorized rebase; no source/test implementation before integration.
Authenticated gh api user: id 8036360, login jmservera; repository-local
8036360+jmservera@users.noreply.github.com for author and committer.
All ten prior task artifacts frozen by SHA-256 in session manifest.

Integration completed without any conflict at
08dd12762e1789bc3dd387b37b1d572716b3d810, tree
0c4c5047873aedaaaa909bf0b902055895c42c25. The complete 148-file upstream delta
matches exact new base except inherited additive API README and exact two
STAFF_GET names. Upstream recorder_identity projection is retained.
Every inherited owned source is byte-identical except those explained upstream
compositions. All ten historical artifacts match their frozen hashes.
Machine-readable full parity/hashes: adjacent remediation-integration.json.

An initial parity script assumed the ENTIRE old log, including frontmatter date,
was an unchanged prefix; that assertion failed because upstream updated metadata.
Corrected verification separately proves the historical log BODY is an unchanged
prefix and the WHOLE current log is byte-identical to exact upstream. No log or
source was edited to satisfy parity; no unexpected conflict was resolved.

## P01-T02 Failing Acceptance Controls

Six new semantic methods (within <=12, none removed) ran against unchanged
integrated continuity source before implementation. Actual result: see adjacent
red.log: six methods, 49 failing subtests and 11 errors, preserving all failures.
Both original exact
reproductions had already been independently rerun at 1144647c. The broader red
matrix also exposed malformed-input exceptions and invalid lifecycle acceptance,
as anticipated by PC-001/PC-003. A nullable envelope in an otherwise pending
proposal is legitimate absence, not a malformed envelope; that one test input
was changed to a scalar before fixed validation. Shared fixture bytes unchanged.

## P02 Source and Test Changes

Production changes are ONLY core continuity.py: control_record projects every
same-document read/mutation return under existing can_see_reason, retaining safe
operation IDs/status/epochs/flags and holding arbitrary text. Full recorded-need
users keep canonical records. Source validation precedes traversal; missing SQL
evidence is not defaulted to empty. Actual unsupported JSON is explicit and
source-scoped. All retained releases undergo count/type/snapshot/lifecycle checks,
independent of proposal references. Reference digest/version/task checks remain.
Repeated suspension and possible ordering within timestamp ties are allowed;
strictly impossible initial/terminal chronology rejects. Invalid proof now reports
complete=false even if a caller forces complete=true and recomputes the digest.
Canonical ledger/head and serving/late-result/accounting/publication code remain.

Full-proof test setup locally replaces every bare synthetic release BEFORE
constructing evidence through real record_release APIs. Shared installer unchanged;
explicit bare-history and missing-source negatives remain. Manual historical
event backfill was removed from the legacy positive. No production synthesis of
missing events, exported-record omission or retrospective evidence is introduced.

An initial focused fixed run failed (65 run, two failures/17 errors): an overly
broad edit accidentally projected the INTERNAL _suspension helper, causing
NameError and dependent failures. Fixed before Review by retaining raw internal
lookup and projecting restart_decide's actual response. Preserved first-truncation
reason ordering for existing regression. Subsequent focused run: 65/65 pass.
Initial API static checks found one unused variable, one typing annotation and a
format change; resolved locally. No original Review has run at this point.

## P03 Validation In Progress

* Focused host: 65 run, 65 pass, zero skips.
* Coupled current-domain/assistant suites: 546 run, 432 pass, 114 opt-in/platform
  skips, zero failures. Rule evaluation without the synthetic law store remains
  explicit Unknown; injected recovery errors are intentional exercised controls.
* Actual owned SQL Server 2022 version 16.0.4305.5: 31 run, 31 pass, zero skips,
  including inherited new role/proof matrices and independent epoch/legacy races.
  UUID databases dropped, exact owned container removed.
* Installed hardened rebuilt API: 65 run, 65 pass, zero skips; image
  sha256:5a20c9a27d90398aaeb166d12dc0815f8612a68cbbaeb60a276d8e7b7a7b2a08,
  UID/GID10001, read-only, zero capabilities and no-new-privileges. Existing
  check-container.py controls, negative probes and responsive startup passed.
* Configured core/agents Ruff/format/mypy passed (124/23 files). Final API static
  rerun passed (57 files). Final source/test freeze checks remain before Review.

The legacy publication race barrier was strengthened to observe a NEW record
at the actual save boundary, not a publication_fence implementation detail.
Installed exact-main image
sha256:206f61a94ff00b765745f4eefe748efa83f48df173389a01be1b4504539cf476
was built from git archive of exact authorized main. The SAME final oracle
failed all three subcases: summary raised ConflictError instead of a retained
local retry; document remained Not reviewed; priority remained Proposed.
No timeout/missing-method proxy is counted. Same oracle on installed fixed image:
one method/three subcases passed. An earlier baseline attempt had one priority
barrier timeout; it is not the final semantic adverse evidence.
Final strengthened oracle will also rerun on owned SQL and host.

## Final P03-T01 Evidence and Commands

Final source/test hashes and raw-log SHA-256/actual runner summaries are in adjacent
remediation-validation.json; full installed-vs-worktree hash parity established
for eight core modules. Atomicity.log retains the entire final base-red/fixed-green
output. Static.log retains all configured gate output. No test method removed;
six new methods, not counting inherited SQL execution. Exact owned containers and
both task image tags removed after all checks. No application source was mounted
into the installed images.

| Final execution | Actual result |
| --- | --- |
| Focused host, final tests | 65 run, 65 pass, zero skips |
| Coupled current-domain suites | 546 run, 432 pass, 114 skips, zero failures |
| Actual task-owned loopback SQL | 31 run, 31 pass, zero skips |
| Final strengthened SQL atomicity + known-empty source | 2 run, 2 pass, zero skips (overlapping selectors, not 33 distinct tests) |
| Hardened installed API image, final tests | 65 run, 65 pass, zero skips |
| Exact-main installed semantic publication race | 1 method, all 3 subcases fail on actual persisted/returned outcomes |
| Same fixed installed publication race | 1 method, all 3 subcases pass |
| Existing container controls/negative probes/startup | Pass |
| Core/API/agents configured Ruff, format, mypy | All pass; 124/57/23 files |

Executed from repository root with installed src distributions (no installation
was needed; the existing venv imports the editable src packages):

```bash
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest \
  test_continuity_epoch_export.EpochTests test_continuity_epoch_export.LegacyTests \
  test_continuity_epoch_export.OfflineTests test_continuity_epoch_export.HttpTests \
  test_continuity test_role_endpoint_inventory -q
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest \
  test_ai_tasks test_assistants test_assistant_release test_assistants_dispatch \
  test_workflows test_role_matrix test_procurement_api test_quality_procurement \
  test_resident_decisions test_progress_event_capture test_hazard_referral test_recovery -q
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python \
  /home/azureuser/.copilot/session-state/fdcaa8b0-3c35-4010-90df-06be900c5b6b/files/run_owned_sql.py \
  test_continuity_epoch_export.MssqlEpochTests test_continuity_epoch_export.MssqlLegacyTests \
  test_continuity_epoch_export.MssqlOfflineTests test_continuity_epoch_export.MssqlHttpTests
```

Final SQL selectors with the same runner:
MssqlLegacyTests.test_legacy_text_document_priority_publication_race and
MssqlOfflineTests.test_release_source_absence_and_unsupported_are_not_full_evidence.
The committed owned-sql.py receipt is the exact sanitized runner used, copied
without changing its bytes; ephemeral credentials were generated only in memory.
It creates no shared database and never loads deployment settings.

```bash
docker build -q -f src/api/Dockerfile -t zf-122-remediation-api-fdcaa8b0:local src
.venv/bin/python src/check-container.py api zf-122-remediation-api-fdcaa8b0:local
docker run --rm --name zf-122-remediation-final-image-fdcaa8b0 \
  --read-only --cap-drop=ALL --security-opt=no-new-privileges \
  --tmpfs /tmp:rw,nosuid,nodev,uid=10001,gid=10001 \
  --tmpfs /state:rw,nosuid,nodev,uid=10001,gid=10001 \
  -e PYTHONPATH=/tests/api:/tests/core:/tests/agents \
  --mount type=bind,source="$PWD/src/api/tests",target=/tests/api,readonly \
  --mount type=bind,source="$PWD/src/core/tests",target=/tests/core,readonly \
  --mount type=bind,source="$PWD/src/agents/tests",target=/tests/agents,readonly \
  --entrypoint python zf-122-remediation-api-fdcaa8b0:local -m unittest \
  test_continuity_epoch_export.EpochTests test_continuity_epoch_export.LegacyTests \
  test_continuity_epoch_export.OfflineTests test_continuity_epoch_export.HttpTests \
  test_continuity test_role_endpoint_inventory -q
```

Baseline image uses the exact authorized main's `git archive ... src` contents
as its src build context and the same hardening/test mounts. Final atomicity
selectors run the identical method in both installed images. The test barrier
does not depend on the feature's fence field. Configured static commands from
each of src/core, src/api and src/agents:

```bash
../../.venv/bin/ruff check .
../../.venv/bin/ruff format --check .
../../.venv/bin/mypy
```

The 114 broader skips are opt-in MSSQL/Azure/platform exclusions, not passes.
Actual local SQL selectors do not convert the unrelated skips to passes.
Fixture rule evaluation stays explicit Unknown without a law store. Recovery
fault logs are expected assertions, not hidden product failures.

## Baseline Adverse Evidence

Installed actual HTTP at original head: PSO and Quality Inspector GET register
200 with synthetic protected canary. Record an unreferenced release through API,
export(event_limit=0): event_total=1/events=[]/truncated=true, producer complete=true;
serialized verifier with unchanged separately retained head returned
valid=true/problems=[]/complete=true, also after ordinary digest recomputation.
These observations reproduce defects, not successful acceptance controls.

Original coordinator messages were extracted unchanged from original events,
including provenance/content hashes in new research coordinator-evidence.json.
Original findings content a873595246e3d7ce212589e93ed1ccb0b8bea2bf489a931030805549b74650d9;
original completion/Not accepted efc5e52e98b0984e8609ba519716e89e420c6b85fb811ea948f10aad6fd467e2.

## Remaining Work and Unmet Gates

Integration, implementation and local validation complete. One original Review
has completed below; publication remains. Source is frozen after Review.
No bounded correction of this new task has been used. Coordinator retains final
independent acceptance. Genuine authority, witnessed drill, immutable external
Azure head, Azure SQL drill and enforceable pre-gate-image exclusion remain unmet;
whole #122 stays open. No private inputs, live inference, Azure/IAM/Graph,
issue/board/merge action, shared server/web/queue/procurement edit is authorized.

## ONE Original Review: Complete / Not Accepted

Independent new Review at frozen c5e329c588fa68ab6a7199ddcfa5977be94fe6f3:
.copilot-tracking/reviews/logs/2026-10-18/issue-122-register-release-remediation-review.md.
SHA-256 e43d6ec67d83b788e97d68fd2be20523ef962f7ac5aeb544fabc0886adbf93e4.
The reviewer independently reran focused 65/65 and coupled 546/432 pass/114 skips,
reconciled all new source and canonical artifacts, preserved all ten historical
files, and separately classified supplied SQL/image/static evidence.

Both original coordinator reproductions are fixed in exercised normal paths,
but the complete bounded acceptance contract is NOT accepted:

* RV-001 Medium: a parseable JSON integer timestamp 10**400 raises OverflowError
  in math.isfinite during producer and recomputed-digest offline verification
  instead of an explicit incomplete/invalid result.
* RV-002 Low: malformed source count/flag metadata can echo arbitrary values into
  limited export despite correct incomplete status. This is inherited conditional
  defensive hardening; the actual unchanged exporter supplies typed counts, not a
  demonstrated ordinary HTTP disclosure. Separate later follow-up.

No correction is performed here. This is NOT coordinator full published-head
acceptance. New-task correction count is zero; at most two may occur only after
coordinator review/authorization, as the owner directed. No source or test changes
after this original Review, no repeat Review and no self-Pass. The prior original
Not accepted and all historical receipts remain byte-identical.

Authorized next action: commit this assessment/state and publish only the owned
branch with the exact expected-head lease, update PR 398 while retaining draft,
Refs-only/empty closing references, and STOP for full coordinator review.

## Publication and Owner-Requested STOP

Authorized exact-lease push actually completed:
1144647c8d539716e8ddddf9daa47407c9bd00ac ->
916c1b0800d2a9b8d092e5eded2f996d75a73b9b. Fresh remote check immediately before
push matched expected old head; no alternative lease or branch was used.
PR 398 body updated with owner decision, new task/history separation,
exact source/base/boundary, commands/results, adverse new original Review and
unmet gates. Its ENTIRE previous body is preserved under an explicitly historical
heading. Actual live read: OPEN, draft=true, main-based, head=916c1b08,
closingIssuesReferences=[].

Final receipt/state is documentation-only, published by NORMAL push. No source
change, correction, repeated assessment, self-approval, ready flag, issue/board
mutation, other-branch/main write or merge follows the original Review.
Final exact head is the commit containing this receipt (discoverable in Git/PR),
not a fabricated self-referential hash. All 34 full-PR changed paths are in
remediation-boundary.json; all 16 historical issue-122 artifacts remain equal to
original-head blobs. Both original assessment hashes and new independent
assessment hashes are in that manifest/PR. Final acceptance remains blocked by
RV-001 and coordinator review. New task correction count stays ZERO.

The bounded automatic loop is complete and the session stops as the owner
explicitly directed. This is completion of execution/publication, NOT acceptance
of the implementation or the whole issue. Coordinator must review the final
published head before deciding a later correction; no follow-up starts here.
