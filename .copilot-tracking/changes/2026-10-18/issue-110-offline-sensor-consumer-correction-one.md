---
title: Issue 110 offline consumer correction ONE and integration receipt
description: Same-task authorized RV-001 and RV-002 correction followed by pinned integration only
ms.date: 2026-10-18
---

## Authority and intake

Same task issue-110 / issue-110-offline-sensor-consumer, session
350bfa26-8783-4b1f-81b7-0434d2d93881. Coordinator authorized later rpi-implement
correction ONE of maximum TWO for RV-001 Medium and RV-002 Low only, then
integration-only onto 6fbdcee18413e9f7366e5f9ec53f68f053681096.
No Research, critique or original Review rerun; no new task or implementation
worker. RV-003 remains separate baseline browser-import residual.

Before any edit: clean worktree; branch feat/offline-sensor-consumer-110;
local HEAD, remote branch and PR411 head all exactly
43ef35655b5a01f2a07a2d09eaef5415cc27c1dd. PR411 is Draft, closing refs empty.
Fetched origin/main equals authorized target
6fbdcee18413e9f7366e5f9ec53f68f053681096. No unexpected advancement.
Integration remote lease remains exactly intake unless a normal correction
push is explicitly recorded; preferred local correction then single exact lease.

Original critique SHA-256:
ad56b59a8df472fff31ed3ae906eca63505ea76fca0f63a457dda4acf540942b.
Original Review SHA-256:
5ae9cb33e5d46a5a486cfbce0e824ab012efd8b6b4fccf9b4e73546e772b07cc.
Both verified at intake and immutable. Original outcome Defects found remains.

## Bounded implementation and verification contract

Validate retained accepted reading against its historical accepted witness,
not current consent/calibration/window. Refuse malformed persisted time/numbers/
inconsistent source explicitly with bounded ConsumerError. Ensure later-row
failure preserves API committed-prefix receipts, no duplicate or overwrite,
no sensitive error diagnostics. Preserve rejected historical replay, current
transaction fencing, exact-generator loader and shared SQL stores.
RV-002 is reconciled by labelling historical contradictory handoff and appending
an accurate present handoff, never pretending original evidence was correct.

Use existing actual SQLite/disposable SQL Server harness and hardened image.
Record red before production edit, green after. Integration may union additive
documentation only, not add another fix. Compare complete normalized owned
patch and protected upstream blob/modes, not a sample. No browser, UI, private
data, live Hub/Azure/AI, service or approval authority.

## Actual transcript and results

Intake command: `git status --short; git branch --show-current; git rev-parse
HEAD; git ls-remote origin refs/heads/feat/offline-sensor-consumer-110;
gh pr view 411 --json headRefOid,isDraft,baseRefOid,closingIssuesReferences;
sha256sum <original critique> <original Review>; git fetch origin main;
git rev-parse origin/main; git cat-file -t <authorized target>`.
Result: all exact checks above passed; no source edited before intake.

`python3` import first failed `No module named zava_forward`; only then created
the session-owned `files/venv-correction-one` with `--system-site-packages` and
installed local editable core/agents/API using `pip --quiet --no-deps`.
Tool probe failed `No module named ruff`; only then installed repository-pinned
ruff 0.17.1 / mypy 2.4.0. No browser dependency was installed.

`PY` below is the exact session executable
`/home/azureuser/.copilot/session-state/350bfa26-8783-4b1f-81b7-0434d2d93881/files/venv-correction-one/bin/python`.

Failing-first production remained identical to intake while tests ran:

| Run | Actual command | Result |
| --- | --- | --- |
| Initial SQLite | `PYTHONPATH=src/core/tests:src/api/tests PY -m unittest <nine correction methods> -q` | 9 tests, 28 failures / 6 errors |
| Initial real SQL Server | `PY src/api/checks/sensor_sql_check.py` | 33 tests, 13 failures / 4 errors; owned container removed |
| Isolated SQLite red | Same nine methods after fixture isolation corrections | 9 tests, 32 failures / 2 errors |
| Isolated real SQL red | Same SQL command after fixture isolation corrections | 33 tests, 17 failures / 1 error; owned container removed |
| First corrected SQLite | `PYTHONPATH=src/core/tests:src/api/tests PY -m unittest test_sensor_consumer test_sensor_ingestion -q` | 59 tests passed |
| First corrected real SQL | `PY src/api/checks/sensor_sql_check.py` | 33 tests passed; owned container removed |
| First correction static | `PY -m ruff check --fix <three changed Python files>` then formatter | 1 initial E501; formatter corrected it |
| First correction types | From core: `PY -m mypy src/zava_forward/core/sensor_consumer.py tests/test_sensor_consumer.py` | 2 files passed |

The nine selected methods are the four core methods
`test_retained_reading_replay_refuses_malformed_and_inconsistent_values`,
`test_retained_witness_must_match_reading_and_digest`,
`test_new_admission_refuses_malformed_latest_without_raw_parse_error`,
`test_truthful_historical_replay_ignores_withdrawn_current_authority`,
their four inherited API equivalents and API
`test_later_corrupt_reading_preserves_committed_prefix`.

Initial red test errors included contamination between corruption subcases
because restoration followed a deliberately failing assertion, plus SQL fixture
configuration after intentional schema corruption. `finally` restoration and
trusted second-sensor configuration before corruption fixed only the test setup.
The isolated red errors are the actual raw timestamp ValueError escape.
Assertions expose absent bounded refusals for malformed numerics, source/witness
mismatch and lost prefix, not successful acceptance. Full raw outputs retained.

## C1-T01 implementation

Only core sensor_consumer production source changed. `_reference` reuses the
existing exact delivery digest. Accepted replay validates closed historical body,
digest and complete retained reading, with semantic Decimal equality across
SQLite strings and SQL Server decimals and exact whole-second UTC timestamps.
Units and calibration claims are historical witness data, not current control
authority. No present-day consent/window/calibration check is reapplied.

Latest consumer reading receives the same historical consistency validation
before timestamp ordering. JSON-valid guarded SQL extraction finds its accepted
witness on both actual engines; no new table or shared-store hook. Legacy
generator rows without a consumer witness retain their separate contract and
receive bounded timestamp/numeric validation. Null latest timestamps are selected
for explicit refusal, not treated as an empty store. No parse errors or raw
values escape to BatchStopped, whose existing completed-prefix mechanism remains.

Tests snapshot all reading/delivery/DQ rows before refusal and assert no mutation;
prefix cases prove exactly one earlier new commit, no trailing admission or
overwrite and no raw identifiers/numeric contents in exception metadata.
Historical replay after simultaneous policy/mapping/consent/calibration withdrawal
passes on both engines. Existing independent connections, rollback,
postcommit reconciliation and privacy cases remain in the actual suites.

## C1-T02 evidence reconciliation

The contradictory final original changes line is retained verbatim and labelled
historical, then followed by a truthful current handoff. Original Review bytes,
execution Complete and outcome Defects found are unchanged. Narrow core/API
guides, KB index and append-only log explain the persistence safeguard without
claiming operational authority. No ADR status, case-study or memory change.

## Final correction validation before integration

All commands use PY above; PYTHONPATH names only existing public test fixtures.
No source edit followed these checks. Generated raw logs are committed alongside
this receipt with prefix `issue-110-offline-sensor-consumer-correction-one-`.

| Directory | Actual command | Actual result |
| --- | --- | --- |
| src/core | `PY -m ruff check . && PY -m ruff format --check . && PY -m mypy` | Pass; 75 formatted files, 128 typed files |
| src/api | `PY -m ruff check . && PY -m ruff format --check . && PY -m mypy src/zava_forward/api/sensor_ingestion.py tests/test_sensor_ingestion.py checks/sensor_sql_check.py` | Pass; 27 formatted files, 3 selected typed files |
| src/api | `PY -m mypy` | FAIL, 9 existing missing playwright.sync_api imports in 9 files/60 checked; RV-003 remains |
| src/core | `PYTHONPATH=tests PY -W ignore::ResourceWarning -m unittest test_sensor_consumer test_sensor_backfill test_sensor_faults test_sensor_plausibility test_sensor_privacy test_sensor_stock test_sqlstore test_buildings test_chat_privacy test_regulatory_privacy test_governance test_rai_release -q` | 202 tests, 17 existing explicit/opt-in skips, no failures |
| src/api | `PYTHONPATH=tests:../core/tests:../agents/tests PY -W ignore::ResourceWarning -m unittest test_sensor_ingestion test_auth test_role_matrix test_role_endpoint_inventory test_chat_isolation test_continuity test_governance_evidence_api test_buildings test_mssqlstore -q` | 329 tests, 169 existing opt-in SQL skips, no failures |
| repository | `PY src/api/checks/sensor_sql_check.py` | Actual responsive loopback SQL Server, API33 passed; container finally removed |
| repository | `docker build --quiet -f src/api/Dockerfile -t ama-sensor110-api:correction-one-350bfa26 src` | sha256:03e34bd68f4848c7d8ba14bb294a40dc3d19828dbfe77d8a42f9f6d2f995344f |
| repository | Hardened command below | 75 tests, 1 existing opt-in sensor112 skip; separate actual API accepted2/reopened replay2, two rows retained |

Image runtime command:

```bash
docker run --rm --name ama-sensor110-c1-image-350bfa26 --network none \
  --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp:rw,mode=1777 --tmpfs /state:rw,uid=10001,gid=10001,mode=700 \
  --mount type=bind,src="$PWD/src/core/tests",dst=/tests/core,readonly \
  --mount type=bind,src="$PWD/src/api/tests",dst=/tests/api,readonly \
  -e PYTHONPATH=/tests/core:/tests/api -e ZF_DATA=/tmp/no-default-dataset.json \
  ama-sensor110-api:correction-one-350bfa26 python -W ignore::ResourceWarning -c \
  'import os,unittest; assert os.getuid()==10001; print("UID10001; read-only root; network none", flush=True); result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromNames(["test_sensor_consumer","test_sensor_ingestion","test_sensor_privacy"])); assert result.wasSuccessful(); import tempfile; from sensor_consumer_fixture import store_at, POLICY, CONTROL, RECEIVED, observations; from zava_forward.api.sensor_ingestion import SensorIngestion; directory=tempfile.TemporaryDirectory(); store=store_at(directory.name); adapter=SensorIngestion(store); adapter.consumer.configure(POLICY,[CONTROL]); rows=observations(); first=adapter.consume(rows,received_at=RECEIVED); assert len(first)==2 and all(r.status=="accepted" and not r.replay for r in first); store.db.close(); reopened=store_at(directory.name); second=SensorIngestion(reopened).consume(rows,received_at=RECEIVED); assert len(second)==2 and all(r.replay for r in second); assert reopened.db.execute("SELECT COUNT(*) FROM sensor_reading").fetchone()[0]==2; reopened.db.close(); directory.cleanup(); print("Actual finite API adapter accepted2/reopened replay2; no duplicate append", flush=True)'
```

The inline assertions ran, not a mocked container acceptance. The exact runtime
output is committed. ResourceWarning suppression affects noise only. Preservation
logs include deliberately injected recovery and unloaded-law-store tracebacks
with passing assertions, not a hidden SQL fallback. Skipped remote SQL fixtures
are not counted as executed SQL acceptance; API33 separately runs actual MSSQL.

Correction source/config SHA-256 manifest is committed as
`issue-110-offline-sensor-consumer-correction-one-source.sha256`.
Identity resolved afresh with `gh api user`: id 8036360/login jmservera; local
author and committer noreply set before commit, no global configuration change.
Remote lease rechecked exact intake; fetched main still exact authorized target.
Next action is authorized integration-only, no further source correction.
