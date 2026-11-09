---
title: "#184 post-policy validation research: current main, impact and check selection"
ms.date: 2026-11-09
---

Prospective second recovery record. It is written before the main merge, the checks and any edit of this validation pass, and it does not rewrite the original C1 to C5 records or the earlier recovery records (14ce74544), whose disclosure stands: that diagnosis preceded their records.

## Start identity (observed 2026-11-09)

* Branch feat/demo-recovery-sensors-184-1109, clean, HEAD 14ce745448bf0b63d80e89af3bd952ddb48c7c81, local only (no parent PR open; no remote branch is touched).
* Fetched origin/main 76db469b16e7ac0ae862e8c9b19873fc66b04f0e. Merge base with HEAD is b46a9ad9a (#1299). Main is two commits ahead: 9814cf6b2 (#1301, validation policy) and 76db469b1 (bot rubric score).
* The brief said main adds only the rubric score; the diff shows more. Excluding 84 added tracking records, main changes: `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `.github/copilot-instructions.md`, `.github/rubric/README.md`, `.github/rubric/scores/latest.json`, `docs/reference/log.md`, `docs/reference/method/tracking-retention-policy.md`, `docs/reference/research/delivery-bottleneck-analysis-2026-10-31.md`, `src/README.md`. `src/README.md` is policy text for the local gate, not source code. The merge brings no source, infra or tool change.
* Overlap with the parent's non-tracking paths: only `docs/reference/log.md`. `git merge-tree --write-tree HEAD origin/main` completes with no conflict (tree 5afd0cf39).
* `tools/rpi-checks.py`, `tools/test_rpi_checks.py` and every src/ and infra/ path are untouched by main since the merge base, so the parent's two-name SENSOR_MSSQL_REQUIRED_TESTS growth does not collide with #1301.

## Policy impact (#1301 as merged)

* The default local tier is planned targeted checks plus hosted CI. Big features, releases, infrastructure, deployment, SQL and security-sensitive work still require the complete gate; size cannot downgrade them, mixed changes take the strictest tier, and workflow, gate-tool, dependency and Dockerfile edits are classified by actual impact.
* This parent is higher-risk by that classification (SQL contract, infra templates, gate tool). The owner's explicit demo authorization for 2026-11-09 permits modified and impacted module checks without the blanket local gate. That authorization is demo-scoped, is not a downgrade of the permanent tier, and is not a full-gate or receipt claim. Hosted CI and independent exact-head review stay mandatory.

## Actual affected surface (parent versus main, 29 non-tracking source, doc, tool and infra paths)

* core: sensor_consumer, sensor_sql, sensor_analysis_store, device_provision, live_readings, sensor_consistency, and their tests and fixture.
* api: live_control (cohort at most 100, 14 day reader bound), live_receiver, live_simulator, sensor_handover_verify, checks/sensor_sql_check.py and tests test_live_control, test_live_receiver_sql, test_iot_stream, test_sensor_consistency, test_sensor_sql_check.
* infra: new live-receiver-job.bicep, one added env var in live-simulator-job.bicep, README steps. Existing Hub module infra/modules/iothub*.bicep and iot-hub-live.bicep are present and unchanged; no Hub or template family is added.
* tools: rpi-checks.py (two names added to the required tuple) and test_rpi_checks.py.
* No web asset, route or template changes. Admin control is the live_control CLI plus Azure RBAC; no browser surface, so no web skill or browser check applies. If a web route is discovered during validation this is revisited.

## Prior evidence status (not inherited)

* The earlier handoff-184 reports test counts and exits. They are historical context only; every count in this pass is re-run. The earlier handoff recorded that ruff and mypy were not run; this pass runs them on modified and impacted files and does not claim a prior pass.
* Opt-in SQL tests skip offline. Skips in an offline unit run are reported separately and are not SQL proof. SQL proof is only the owned disposable SQL Server run.
* Original adverse evidence is preserved: the 2026-11-08 full-gate failure and receipt (issue comments 2026-11-08T20:52Z and 23:41Z), the C4 full-gate addendum, and the earlier analysis run that passed ten tests but was rejected by the harness (exit 1) before the corrected harness accepted it (exit 0).
* Original C5 Low gaps (exact-grant live_receiver.main entrypoint and rejected data-quality SQL coverage): the C3 to C5 records and the earlier recovery review kept them open. This pass re-reads the tests to confirm status and does not claim independent closure.

## Environment

* /home/azureuser/venv-184 holds editable installs of this worktree's src/core, src/agents and src/api (pth paths read: this worktree). Verified again by import before any test.
* ruff 0.17.1 and mypy 2.4.0 are not present in that venv. Per instruction they are installed (pinned, venv only) only after a failed attempt to run them.
* Azure CLI with Bicep 0.48.1 is available; no Azure login, deployment or what-if is used.
* Shared heavy lock /tmp/ama-rpi-heavy.lock was observed held at 2026-11-09 (about 08:55 UTC) by another lane (e1-sql-run.sh, container zf-1288-e1-sql). Admission is non-queued: heavy SQL is attempted with `flock -n` only, non-heavy work proceeds meanwhile, and the other lane's SQL is never stopped.

## Gaps kept open

Children #185, #188, #140 and #110 acceptance, credential and log lifecycle evidence, actual simulator to Hub to SQL to UI to Quality model proof, human acceptance, qualified live walkthrough and the #440 integrated checkpoint. Mocked source tests and diagrams are not that proof. Receiver cap stays 100 bindings, never 60000.

Planning readiness: Ready. Disposition: executed (fresh source, diff and environment investigation).
