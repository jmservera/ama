---
title: Issue 122 register release remediation correction ONE receipt
description: RV-001-only source correction and exact-base parity, publication blocked by main movement
ms.date: 2026-10-18
---

## Disposition and Exact Boundary

SAME task issue-122-register-release-remediation, owner-authorized correction
ONE of maximum two. Implementation evidence only, not self-Pass or independent
acceptance. Original Review Complete / Not accepted remains immutable.
RV-002 malformed metadata echo is excluded and remains a distinct non-blocking
follow-up. The older historical adverse assessments and two exhausted correction
cycles remain untouched. No new task, critique or Review.

| Boundary | Exact value |
| --- | --- |
| Expected original local/remote head | e00c521573501a4ed84dab7ec0ccf66ef57a7053 |
| Prior base | 9c648b2006e8b2e563823ea7d5aabdf7f1ac7096 |
| Authorized new base | a86282c4badebc58eabbf9e441410d930a201ac2 |
| Pre-rebase intake commit | 5a7f8c48, committed authorized scope only |
| Integrated pre-correction candidate | e188b47d2b8a583cdaf601caad038278a077f473 |
| Validated source candidate | 72cf28b057dbb57e1599367dded1345a4c26c054 |
| Subsequently observed remote main | ab0613f3336109ff9b96560a16758ee842232715 |
| Publication | BLOCKED; no push, no PR metadata update |

Owner explicitly directed report/wait if main moved again. Remote main movement
was observed during validation. No second rebase or broader source correction
followed. This local receipt and source are persisted pending coordinator base
direction. The ONLY authorized history-publication lease remains
refs/heads/fix/continuity-epoch-export-122:e00c521573501a4ed84dab7ec0ccf66ef57a7053;
it was NOT exercised. PR398 remains draft at the old published head. No other
branch, main, issue or board write, merge, or ready transition.

## Source Candidate Delta

Relative to integrated e188b47d, production changes ONLY
src/core/src/zava_forward/core/continuity.py: retain exact int/float type
acceptance and bool exclusion, catch only OverflowError around math.isfinite,
and return the existing invalid task-release event envelope problem.
No fallback timestamp, coercion, calendar-date policy, lifecycle/count/
association/chronology/source relaxation or metadata-echo fix.

One new semantic test method in src/api/tests/test_continuity_epoch_export.py
executes 17 cases at each of producer/offline-verifier boundaries. JSON round-trip
includes positive and negative 10**400, zero/negative/fractional/large finite
positives, both booleans, null, numeric text and nonfinite negatives. NaN/Infinity
use Python's existing permissive JSON encoder/decoder extension; the oversized
integers use ordinary JSON numbers. Producer returns complete=false with the
explicit problem. Offline test starts from a valid bundle, forces complete=true,
clears incomplete reasons, recomputes the ordinary digest and serializes/parses;
it returns valid=false/complete=false with the event problem, unchanged original
external head and byte-equivalent canonical ledger. No digest/head mismatch is
used as a proxy for the numeric rejection.

Each producer call captures its own separately held emitted head because the
normal export operation appends an audit entry. Existing register GET/mutation
privacy, recorded need, safe operational fields and immutable full canonical
proof remain exercised by the unchanged focused methods. API README documents
the conversion-safe numeric contract without new date bounds.

## Integration Parity and Immutable Evidence

Exact rebase command completed with no conflicts:

```bash
git fetch origin
git rebase --onto a86282c4badebc58eabbf9e441410d930a201ac2 \
  9c648b2006e8b2e563823ea7d5aabdf7f1ac7096
```

All 43 upstream changed paths match authorized main exactly except the additive
API README. Both README contributions remain; no manual conflict resolution
was needed. PR407 queue production/tests/contracts and PR406 recorder code/tests
are preserved. The inherited projection delta remains exactly the two continuity
STAFF_GET kinds; recorder-identity projection is otherwise exact upstream.
The historical knowledge-log body is an unchanged prefix and the entire log is
exact upstream. Pre-correction owned runtime/test source matches the old head.
Machine-readable companion correction-one-parity.json records all upstream and
frozen path hashes, the exact candidate source delta and full PR boundary.

All 27 frozen artifacts match original-head blobs, including all 16 older
historical artifacts and all immutable new-task research, assessments and prior
validation/integration receipts. Current plan/details/changes/state are the only
pre-existing issue-122 artifacts intentionally updated.

| Original assessment | SHA-256, unchanged |
| --- | --- |
| New original Review Complete / Not accepted | e43d6ec67d83b788e97d68fd2be20523ef962f7ac5aeb544fabc0886adbf93e4 |
| New single critique Complete / Revise | 343c3e14ecebe3fa813b2bb8c0a0a914b555a786996dd987c583356798d36ca7 |
| Historical original Review | 9d9d0bff0fdda5a8d163967c4ba8a997ee1bc315ae5a896611fc331aff200abc |
| Historical critique | 4eeda2d60235f571916a83de65fa9cda8d73e2159291a50286e8055328fc77be |
| Original coordinator findings content | a873595246e3d7ce212589e93ed1ccb0b8bea2bf489a931030805549b74650d9 |
| Original coordinator Not accepted content | efc5e52e98b0984e8609ba519716e89e420c6b85fb811ea948f10aad6fd467e2 |

## Actual Commands and Results

All host commands use the existing installed editable distributions and venv.
No dependency installation or private environment/data access was needed.
Raw logs are companion files with this task's correction-one prefix and are
hashed in correction-one-parity.json.

```bash
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest \
  test_continuity_epoch_export.OfflineTests.test_json_numeric_timestamps_fail_closed_without_conversion_errors -q
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest \
  test_continuity_epoch_export.EpochTests test_continuity_epoch_export.LegacyTests \
  test_continuity_epoch_export.OfflineTests test_continuity_epoch_export.HttpTests \
  test_continuity test_role_endpoint_inventory -q
```

First new-test red run on unchanged integrated source: 1 method, 4 OverflowErrors
plus 15 oracle failures from incorrectly reusing an earlier producer ledger head.
Corrected oracle red run on unchanged source: 1 method, exactly 4 OverflowErrors,
no failures (both integer signs at both boundaries). Both logs are preserved.
Final focused run: 66/66 pass, zero skips; this includes the new numeric method.

The integrated host and installed-image selectors add test_taskqueues,
test_sqlqueues, test_task_queue_api and test_progress_event_capture to the
focused command above. Each result is 151 run, 133 pass, 18 opt-in skips.
They overlap the focused run, not additional unique tests.

```bash
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest \
  test_ai_tasks test_assistants test_assistant_release test_assistants_dispatch \
  test_workflows test_role_matrix test_procurement_api test_quality_procurement \
  test_resident_decisions test_resident_api test_progress_event_capture \
  test_hazard_referral test_recovery -q
PYTHONPATH=src/api:src/api/tests:src/core/tests:src/agents/tests .venv/bin/python \
  -m unittest tests.test_resident_api -q
```

First coupled command: FAILED, 547 runner entries, 432 pass, 114 skips and
1 import error. test_resident_api imports tests.test_mvp and needs src/api on
the path. Corrected independent resident command: 9 run, 8 pass, 1 opt-in skip.
The other 546 coupled entries have no failures; the failed command is not
relabelled as a passing suite. Expected injected recovery failures and explicit
Unknown rule checks without a synthetic law store remain in logs.

Actual SQL used the unchanged committed remediation-owned-sql.py runner loaded
with importlib.util; only NAME was overridden to the unique
zf-122-correction-one-sql-28a50b1e, and sys.argv selected:
test_continuity_epoch_export.MssqlEpochTests, MssqlLegacyTests, MssqlOfflineTests
and MssqlHttpTests (all fully qualified under test_continuity_epoch_export).
PYTHONPATH was src/api/tests:src/core/tests:src/agents/tests; interpreter
.venv/bin/python. Actual SQL Server 16.0.4305.5: 32/32 pass, zero skips.
UUID-owned databases were dropped and the exact loopback container removed.
This covers producer/verifier parity through the MSSQL store, not a claim that
normal SQL writers emit oversized timestamps or an Azure drill.

The actual runner invocation was:

```bash
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python - <<'PY'
import importlib.util,sys
p='.copilot-tracking/changes/2026-10-18/issue-122-register-release-remediation-owned-sql.py'
spec=importlib.util.spec_from_file_location('owned_sql',p)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.NAME='zf-122-correction-one-sql-28a50b1e'
sys.argv=[p,'test_continuity_epoch_export.MssqlEpochTests','test_continuity_epoch_export.MssqlLegacyTests','test_continuity_epoch_export.MssqlOfflineTests','test_continuity_epoch_export.MssqlHttpTests']
raise SystemExit(m.main())
PY
```

```bash
docker build -q -f src/api/Dockerfile -t zf-122-correction-one-28a50b1e:local src
.venv/bin/python src/check-container.py api zf-122-correction-one-28a50b1e:local
docker run --rm --name zf-122-correction-one-tests-28a50b1e \
  --read-only --cap-drop=ALL --security-opt=no-new-privileges \
  --tmpfs /tmp:rw,nosuid,nodev,uid=10001,gid=10001 \
  --tmpfs /state:rw,nosuid,nodev,uid=10001,gid=10001 \
  -e PYTHONPATH=/tests/api:/tests/core:/tests/agents \
  --mount type=bind,source="$PWD/src/api/tests",target=/tests/api,readonly \
  --mount type=bind,source="$PWD/src/core/tests",target=/tests/core,readonly \
  --mount type=bind,source="$PWD/src/agents/tests",target=/tests/agents,readonly \
  --entrypoint python zf-122-correction-one-28a50b1e:local -m unittest \
  test_continuity_epoch_export.EpochTests test_continuity_epoch_export.LegacyTests \
  test_continuity_epoch_export.OfflineTests test_continuity_epoch_export.HttpTests \
  test_continuity test_role_endpoint_inventory test_taskqueues test_sqlqueues \
  test_task_queue_api test_progress_event_capture -q
```

Installed image SHA-256:
0937579bb90f6505e544df379ab36112348d4d128b049cebd90414b53e0ac95b.
151 run/133 pass/18 skips; checker controls, negative probes and responsive
startup pass. Independent installed parity probe reports UID/GID10001,
CapEff=0000000000000000, NoNewPrivs=1 and installed continuity SHA-256
4afcabd0cfbc495dc71d6b4869f42da5c8db500909c6aab129d20194586883ad,
exact worktree match. Only tests were mounted, not application source.
Both --rm named test/parity containers exited and the exact owned image tag
was removed. No long-lived service remains.

Configured commands from each of src/core, src/api and src/agents:

```bash
../../.venv/bin/ruff check .
../../.venv/bin/ruff format --check .
../../.venv/bin/mypy
```

All pass; formatted files 71/25/19, mypy source files 124/57/23.
No web change; no browser/conformance acceptance is asserted. Remote CI and
rubric checks have not run for this unpublished candidate.

## Stop and Remaining Boundary

P04-T01/T02/T03 execution complete on the exact authorized base; P04-T04 blocked
by the owner's main-movement condition. Local source/evidence commits only.
Authenticated gh api user resolved id 8036360/login jmservera; repository-local
8036360+jmservera@users.noreply.github.com is used for author and committer,
with Conventional Commit and required Copilot trailer.

Full source/artifact independent coordinator review remains pending; original
Not accepted is not superseded by these green checks. RV-002 remains separate.
Genuine OQ-017 authority, witnessed authorized drill, immutable externally held
Azure head, Azure SQL drill and enforceable pre-gate-image exclusion remain
unmet. No private .env/ZF_DATA, live inference, Azure/IAM/Graph/spend, issue or
board mutation, merge or operational approval occurred.

STOP and wait for coordinator base/publication direction. No further source
correction or assessment is started.
