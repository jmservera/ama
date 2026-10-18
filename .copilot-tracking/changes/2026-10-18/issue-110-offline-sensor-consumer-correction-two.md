---
title: Issue 110 final correction TWO
description: Separately authorized final same-task implementation of four independent findings
ms.date: 2026-10-18
---

## Authority, immutable intake and scope

Same issue-110 / issue-110-offline-sensor-consumer, retained session
350bfa26-8783-4b1f-81b7-0434d2d93881. Coordinator authorizes correction TWO,
FINAL permitted source correction, for independent assessment
eb350bd7-aad7-4696-a364-efc436f25fa9: one High and three Medium findings.
No Research, critique or original Review rerun; no implementation workers.
No rebase/integration/base change; normal commits/pushes only.

Before any edit, verified clean local/remote/PR411 head
4723f0a19eb6741079dfec638303f9a3d009d05c, branch
feat/offline-sensor-consumer-110, Draft and no closing references.
PR base and remote main both 6fbdcee18413e9f7366e5f9ec53f68f053681096.
Original critique and original adverse Review hashes match:
ad56b59a8df472fff31ed3ae906eca63505ea76fca0f63a457dda4acf540942b and
5ae9cb33e5d46a5a486cfbce0e824ab012efd8b6b4fccf9b4e73546e772b07cc.
Historical correction-one artifacts will remain byte-for-byte unchanged.

Original actual streams verified in session files before work:
coordinator-complete-rpi-110-original.log: 1273 lines, 66993 bytes,
SHA256 f0a6c47b4ba4df75cf183b83880dc6228732b0367e4cf523dfc84ce14f70d56c.
coordinator-complete-rpi-110-correction-one.log: 998 lines, 59545 bytes,
SHA256 eafe164f93cd2c928f1118e00b0ae2519cfacc0db8cc2099089a46be8a886af2.
These are actual worker streams, not JSON event summaries. Exact copies are
retained in correction-two-workerfiles with the same filenames.

## Findings-to-change and execution checklist

| Finding | Authorized change | Required evidence |
| --- | --- | --- |
| High: full API strict mypy fails | Remove only obsolete dependent import ignore; restore declared dev dependencies locally | Intake full configured mypy fails with declared deps, final full API/core static passes |
| Medium: signed zero seed | Semantic validated integer comparison, preserve observation/digest contract | SQLite/MSSQL admit -0, reopen exact replay, later reading; integer bounds |
| Medium: unchecked SQL MAX hides corrupt rows | Validate complete per-sensor ordering boundary including equal maxima before selecting latest | Actual red/green low-sorting corrupt later timestamp and duplicate-max, API prefix1/no target or trailing writes |
| Medium: stale ADR owner status | Dated scoped current reconciliation against actual owner comment, preserve proposal history | Source comment retrieved; narrow ADR/guides/addendum/index and append-only log |

## Implementation and validation intent

Starting C2-T01: add focused fail-before regressions on unchanged intake
production; actual SQLite and uniquely owned disposable SQL Server.
Then fix all four together in C2-T02, preserving historical replay independence,
current-authority fencing, privacy, exact loader and shared stores.
C2-T03 runs full relevant configured static gates/local CI unit jobs, focused
actual SQL, preservation, hardened nonroot image/adapter restart. No UI/browser
execution or new manifest dependencies. C2-T04 binds hashes/inventory and normal
publication to the same base, cleans exact owned resources and stops.

System Python import failed No module named zava_forward before dependency
restoration. Prior missing declared browser/dev dependencies are already proven.
Use a task-owned venv and pip local src distributions/dev extras only.

## Dated owner evidence

Fetched via gh API comment6194409951 on 2026-10-18:
created_at 2026-10-15T14:24:33Z,
https://github.com/jmservera/ama/issues/129#issuecomment-6194409951.
Owner decision: ADR 0003 accepted with amendment; Basic IoT Hub enough for
exercise, no cloud-to-device messages, device twins or device management.
This is not live provisioning, network/cost/credentials, privacy, real AI,
Azure acceptance or whole-issue closure authority.

## Current status

C2-T01 and C2-T02 completed; expanded C2-T03 checks follow.
No independent acceptance claim; correction TWO is final.

## Actual red and first green

`PY` means
`/home/azureuser/.copilot/session-state/350bfa26-8783-4b1f-81b7-0434d2d93881/files/venv-correction-two/bin/python`.
Created an isolated venv (not global); restored declared dev dependencies with
`PY -m pip install --quiet -e 'src/core[dev]' -e src/agents -e 'src/api[dev]'`
only after the missing distribution/dev dependency failures already recorded.
No manifest expansion, browser install or browser execution.

| Run against unchanged intake production | Command | Actual result |
| --- | --- | --- |
| SQLite red | `PYTHONPATH=src/core/tests:src/api/tests PY -m unittest <seven focused methods below> -q` | 7 tests, 6 failures; seed semantics already valid on SQLite |
| Actual SQL Server red | `PY src/api/checks/sensor_sql_check.py` | Responsive real engine, 40 tests, 7 failures/5 errors; container removed |
| Full API strict mypy red with declared dev deps | From src/api: `PY -m mypy` | 1 introduced unused-ignore error, 61 checked; prior 9 missing browser imports gone after dependency restoration |

Seven SQLite selectors: core
`SensorConsumerTests.test_seed_integer_semantics_reopen_replay_and_later_admission`,
`test_low_sorting_retained_timestamp_refused`,
`test_invalid_month_retained_timestamp_refused`,
`test_duplicate_maximum_witness_mismatch_refused`;
API `ApiSensorTests.test_low_sorting_corruption_preserves_prefix`,
`test_invalid_month_corruption_preserves_prefix`,
`test_duplicate_maximum_corruption_preserves_prefix`.
Each ordering variant is a separate fresh-store test, not a contaminated retry.
Two target readings are genuinely admitted before only the later timestamp is
corrupted; the low-sorting values and duplicate maximum are not simulated digest
failures. MSSQL native DATETIME2 is deliberately altered to NVARCHAR to construct
otherwise unrepresentable persistence corruption; both original timestamps are
normalized before altering the later value. No fake connection.

The SQL seed test first admits -0 then exact reopen replay raises bounded
malformed on intake. Subsequent seed subcases are blocked by that same retained
-0 row, producing four consequential errors and the final count failure.
Those are preserved, not misreported as five independently isolated seed bugs.
Six actual SQL ordering/prefix cases fail because the intake code skips the
corrupt later row; all six SQLite variants likewise fail before production edits.

First green after the authorized batch:
`PYTHONPATH=src/core/tests:src/api/tests PY -W ignore::ResourceWarning -m unittest
test_sensor_consumer test_sensor_ingestion -q`: 70 passed.
`PY src/api/checks/sensor_sql_check.py`: actual SQL Server 40 passed, container
removed. Full configured API `PY -m mypy`: all61 passed.
Changed-file Ruff/formatter: four files pass, no lint/type exemptions added.

## Implemented findings

High: removed exactly the obsolete import-not-found ignore on release_support
in unchanged upstream continuity test. Core fixture lookup and strict mypy remain;
no blanket ignore or warning disable. Declared Playwright package is restored
for types only; browser runtime remains unexecuted.

Seed: retained values must still match integer grammar and signed bounds, then
compare as integers to the validated historical witness. -0 and BIGINT0 are
semantically equal; observation strings and delivery fingerprint are unchanged.
Tests cover -0, zero, negative one and both accepted magnitude boundaries,
closed/reopened exact replay, no duplicate write and subsequent admission.
Existing out-of-bound input tests remain.

Ordering: replace pre-validation MAX with two target-sensor SQL reads, one
accepted-witness index, complete retained reading validation and only then
derive latest from validated timestamps. This is linear in per-sensor history,
avoids per-row SQL lookup/whole-store snapshots and stays inside the existing
writer transaction. Every equal-maximum row is validated; missing, mismatched or
duplicate witness and malformed time/numbers refuse explicitly. Legacy generator
rows keep their existing witness-free contract. No new table/store or policy.
Exact historical replay still validates only its historical row/witness, never
present-day consent/calibration/window authority. The new API tests prove
exactly one genuinely new independent-sensor prefix commit, zero target/trailing
writes, unchanged target rows and bounded metadata without identifiers/raw values.

Docs: current ADR status, guides, addendum and KB index reconcile the actual
2026-10-15 owner acceptance/amendment. ADR retains the original Proposed paragraph
under explicitly superseded proposal history. Basic exercise tier and excluded
cloud-to-device/twins/device management are distinguished from all unexecuted
operational gates. KB log appends, never rewrites prior status evidence.
No original case/memory, historic correction-one receipt/log, original critique
or original Review changed.

## Final local-first CI and preservation execution

All checks below ran before any push on the unchanged pinned base. Logs use
prefix `issue-110-offline-sensor-consumer-correction-two-` beside this receipt;
static/preservation/image logs include shell-traced exact executable commands.
API discovery's launcher records the exact command and exit status. The isolated
venv's full dependency freeze is retained; `PY -m pip check` passed.
No `PYTHONPATH=mvp`, global installation or manifest expansion.

| Directory | Actual command | Result |
| --- | --- | --- |
| src/core | `PY -m ruff check . && PY -m ruff format --check . && PY -m mypy` | Pass, 75 formatted files / 128 typed |
| src/api | `PY -m ruff check . && PY -m ruff format --check . && PY -m mypy` | Pass, 28 formatted files / ALL61 typed |
| src/api | `PY -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 checks/design_system_browser_check.py checks/regulatory_ux_check.py` and matching isolated format check | Pass, static only, no browser execution |
| src/core | `PYTHONPATH=tests PY -W ignore::ResourceWarning -m unittest test_sensor_consumer test_sensor_backfill test_sensor_faults test_sensor_plausibility test_sensor_privacy test_sensor_stock test_sqlstore test_buildings test_chat_privacy test_regulatory_privacy test_governance test_rai_release test_sqlqueues test_taskqueues -q` | 236 tests in 69.785s, 17 existing opt-in skips, no failures |
| src/api | `PYTHONPATH=../core/tests:../agents/tests PY -W ignore::ResourceWarning -m unittest discover -s tests -v` | Complete CI unit discovery: 935 tests in 394.261s, 300 explicit opt-in skips, no failures |
| repository | `PY src/api/checks/sensor_sql_check.py` | Actual disposable SQL Server API40 in 19.408s passed, container removed |
| repository | `docker build --quiet -f src/api/Dockerfile -t ama-sensor110-api:correction-two-350bfa26 src` | Image165ebd0d6577ce9e363fe8843bd6fc1c77bacf3a04afeda2237255072b26c1b9 |
| repository | Hardened image command below | 86 tests in 1.295s, 1 existing opt-in skip; actual signed-zero adapter accepted2/reopened replay2/later1, rows3 |
| repository | `PY src/check-container.py api ama-sensor110-api:correction-two-350bfa26` | Existing CI Docker controls, negative probes and hardened/plain loopback startup PASS |

API unit discovery explicitly removes inherited ZF_* options before launching,
so no SQL/live/browser opt-in or private data path is inherited. Existing tests
use their own constructed fixtures. The reported 60000-case timing in that
suite is in-memory generated test cases, not the original private dataset.
No support/private dataset was opened. Core deliberately runs relevant bounded
selectors rather than unrelated generator/private-path suites.
Existing injected recovery/unloaded-law-store tracebacks are assertion-tested
failures, not hidden sensor failures. ResourceWarning suppression is noise only.
Skipped external/browser/other-SQL fixtures are not executed acceptance claims.

Hardened actual runtime command:

```bash
docker run --rm -i --name ama-sensor110-c2-runtime-350bfa26 --network none \
  --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp:rw,mode=1777 --tmpfs /state:rw,uid=10001,gid=10001,mode=700 \
  --mount type=bind,src="$PWD/src/core/tests",dst=/tests/core,readonly \
  --mount type=bind,src="$PWD/src/api/tests",dst=/tests/api,readonly \
  -e PYTHONPATH=/tests/core:/tests/api -e ZF_DATA=/tmp/no-default-dataset.json \
  ama-sensor110-api:correction-two-350bfa26 python -W ignore::ResourceWarning - \
  < correction-two-image-check.py
```

The exact executed input script is committed as
`issue-110-offline-sensor-consumer-correction-two-image-check.py`.
It asserts UID/GID10001, read-only root, all capability sets zero and
NoNewPrivs, then actual suites and signed-zero adapter reopen/later admission.
A separate equally hardened source-binding container SHA-256 hashes every
runtime core/agents/API Python file: all83 exactly match source; committed image
hash manifest binds those bytes. No runtime source edits followed the image.

Local reproduction covers CI's API unit/lint/type/static-harness/build/container
steps and relevant core gates. CI's actual browser/axe execution is explicitly
not run under this scope; no browser binaries installed. Trivy/remote deployment
and Azure/real-model acceptance are not claimed. This is not a claim that every
remote CI job or whole application is accepted.

## Preservation and candidate binding

The correction-two proof lists every one of 2792 protected intake blob/modes,
including all historical correction-one receipts/logs/integration patches and
original adverse assessments. Zero changes outside the 14 authorized existing
paths (four current lifecycle files plus ten source/docs files). The dependent
continuity test changes only one import line; its other contents are preserved.
Shared sqlstore/mssqlstore, exact synthetic loader, governance/roles/queue/recorder/
DPIA and original case/memory remain unchanged.

`correction-two-source.sha256` binds all ten changed src/docs files. Full delta
inventory and per-file hashes include raw red/green streams and input script;
Git's candidate tree binds the manifest itself. Original actual streams retain
their exact 1273/66993 and 998/59545 line/byte counts and supplied SHA256 values.
No new independent Review or Pass verdict is claimed; original adverse outcomes
are unchanged. Correction count TWO, no third source correction authorized.

Main and remote topic were rechecked after checks: main still6fbdcee1, remote
topic still exact intake4723f0a1. No fetch/rebase/integration/base change occurred.
Publication will use normal commits/pushes only. Exact frozen head and cleanup
are recorded after publication; coordinator owns independent accumulated-delta
and previously incomplete unchanged-document semantic coverage.

## Verified resource cleanup

All actual SQL containers were owned and removed by exact generated name in the
existing harness finally, including the red attempt. Hardened runtime/binding
containers used exact unique names with --rm. Existing Docker startup harness
captures each generated container ID and removes that exact ID in finally.
After checks, removed only tag ama-sensor110-api:correction-two-350bfa26 and image
165ebd0d6577ce9e363fe8843bd6fc1c77bacf3a04afeda2237255072b26c1b9.
Removed only the exact session files/venv-correction-two directory after
dependency check. Filtered owned-container/image listings are empty and venv
absence asserted. Raw cleanup output retained; no shared base image, unrelated
resource, global environment or dataset modified.

## Remaining gates

Local implementation evidence addresses all four findings, not independent Pass.
The coordinator must independently assess the accumulated final delta and
previously incomplete unchanged-doc semantic coverage at the frozen head.
Correction count TWO is the final permitted source correction; no third source
cycle, second original Review, issue/AC tick, board action, ready or merge.

ADR0003 owner acceptance and Basic exercise amendment are recorded facts, not
unmet gates. Distinct Hub identities/live transport, remaining unit/sizing/cost,
network/provisioning/device credential decisions, OD-43/privacy/human review,
real AI and Azure SQL/application acceptance remain unexecuted/unmet.
No live Hub, new SDK/public route/service, AI/task/priority mutation, Azure/
Graph/IAM/spend or original private dataset was involved.
