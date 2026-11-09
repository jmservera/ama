# Research: issue 144 current-main integration (2026-11-09, Refs #144)

Task: `issue-144-current-main-2026-11-09`. Parent: `issue-144-hosted-conflict-2026-11-09`. Research disposition: executed (fresh fetch, main delta, import closure) and reused (approved queue adapter evidence). Planning Readiness: Ready.

## Pins (fetched 2026-11-09, fetch only)

* Start HEAD d2d9560694622441fc8b2ad146cccd9c765535c4, tree 27d750e510dc3ef66205fa34888cf945733c1923, clean, branch `fix/demo-recovery-144-1109`.
* origin/main is df8e858b2150198e5e22c73d224a0d3592c73daa. The brief named 23e944c1fccf0c4578e7beb0740ddd55c3f935b2 (PR 1304, IoT recovery); main has since advanced by one automated rubric score commit (`df8e858b`, only `.github/rubric/scores/latest.json`). The integration target is the actual current main, df8e858b, which contains 23e944c1.
* Merge-base HEAD to main: d4d6827fe60be651cd922ab9656688c18c978e1d (PR 1222, already merged into HEAD).

## Main delta since d4d6827f (observed)

* 211 paths: 179 under `.copilot-tracking/` (main's own records), 32 elsewhere.
* Source and tests: `src/api` live control, receiver and simulator (new `live_control.py`, `live_receiver.py`; changed `live_simulator.py`, `sensor_handover_verify.py`, `checks/sensor_sql_check.py`; tests); `src/core` sensor modules (`sensor_sql.py`, `sensor_consumer.py`, `sensor_analysis_store.py`, `synthetic/device_provision.py`, `synthetic/live_readings.py`, `synthetic/sensor_consistency.py`; tests); `tools/rpi-checks.py` and `tools/test_rpi_checks.py` (+2 and a 13-line test change); `infra/live-receiver-job.bicep` (new), `infra/live-simulator-job.bicep`.
* Docs: `docs/reference/log.md`, `docs/reference/README.md`, `docs/reference/research/iot-sensor-analytics-research-plan.md`, `infra/README.md`, `src/api/README.md`, `src/core/README.md`, `.github/rubric/scores/latest.json`.
* `git diff d4d6827f origin/main -- src/agents` is empty: main does not touch the Agents queue adapter or its tests.

## Overlap and import closure

* Paths changed on both sides since d4d6827f: `docs/reference/log.md` (both append) and `infra/README.md` (this branch edits one table row at line 1333; main adds a section elsewhere). `git merge-tree --write-tree HEAD origin/main` is clean, predicted tree 464ce9646f8c7ebc29a1a17d419fce6cc99e02c9 (prediction only, not an execution result).
* Agents imports `zava_forward.core` only via `store`, `synthetic.scale_fixture`, `synthetic.output_dir`, `synthetic.privacy` and AI/chat modules. None of these files changed on main (changed core synthetic files are `live_readings`, `sensor_consistency`, `device_provision`, none imported by Agents). `queue_azure.py` imports no core module.
* Impact derivation: Agents queue tests (`test_queue_azure`, `test_worker`, `test_dispatch`, `test_dependency_rule`) remain the affected set; Core tests changed by main for non-SQL sensor modules (`test_live_readings`, `test_device_provision`, `test_sensor_analysis_store`, `test_sensor_consumer_live`, `test_paired_equity`) are the impacted Core set, run as a confirmation that the merge result equals main for them. API live and SQL tests (`test_live_receiver_sql`, SQL checks) are main's own, need SQL or are unrelated to the queue slice, and are not selected; no SQL, browser or cloud run.

## Date and ownership contracts

* Source `src/agents/src/zava_forward/agents/queue_azure.py:124` sends `x-ms-date` from `email.utils.formatdate(usegmt=True)`; it is byte-identical to approved 63d7f8c180ee995121144cf593e8eca7cb94bd4d (`git diff 63d7f8c1 HEAD -- src/agents` empty before the merge).
* Positive contract: `RequestDateTests` (every operation carries a current RFC 1123 UTC `x-ms-date`). Negative contract: `DateContractTransport` refuses a missing or stale date with 403; this run adds a mutation check on a copy outside the repository (header removed) that must fail the positive tests, so the contract is genuinely exercised on the current tree rather than inferred from earlier runs.
* Log ancestry: the header `## 2026-11-09` entries for issue 144 and main's entries must both survive; the diff HEAD to merge for `docs/reference/log.md` must be additions only.

## Unknowns kept open

* Hosted conflict cause for PR 1141 is not established; local clean is not hosted mergeability. All five live acceptance criteria stay unproven. No product change is planned; any real conflict needing a material product fix stops and reports scope and the remaining budget (no review-correction cycle is consumed by unchanged-source validation).
