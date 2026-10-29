<!-- markdownlint-disable-file -->
# RPI Phase Details: Refresh IoT PR #508

## Metadata

* Task ID: pr-508-refresh-2026-10-29
* Task slug: iot-consumer-110-refresh
* Plan: .copilot-tracking/plans/2026-10-29/iot-consumer-110-refresh-plan.md
* Evidence: .copilot-tracking/research/2026-10-29/iot-consumer-110-refresh-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Integrate main | Complete | P01-T01, P01-T02 |
| P02 | Validate | Complete | P02-T01 |
| P03 | Review and local handoff | Review complete; local commit pending | P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Integrate main

Current branch is clean except this task's newly created evidence, and matches the open draft. Four existing topic commits replay onto fetched b0364e4b. No stash, discard, branch switch, force push or merge is authorized.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Rebase and resolve

Before replay: resolve gh api user and derive its id+login noreply identity, configure repository-local name/email, verify effective committer, run git fetch origin main, capture git rev-parse HEAD origin/main and use that fetched base. Research SHA b0364e4b is historical, not an execution-time freshness promise.

Resolve conflicts by inspecting base/main/topic sections. Preserve appended logs and both relevant index/README sections, retaining main's current context and topic's bounded streaming constraints. Combine nonoverlapping mypy overrides and SDK dependencies. Main alone owns rubric and scenario manifest. Complete when rebase finishes and git merge-base --is-ancestor origin/main HEAD succeeds.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Reconcile contracts and pins

Use main manifest's fixed source allowlist, recompute actual SHA-256 values only if mismatch remains. Run test_scenario_manifest and test_needs_inventory. Preserve dynamic sensor_backfill.VERSION and main's bounded-noise semantics. No UI edits intended; if required, web skill/review requirements apply first. Compare rubric bytes to main and preserve original dated evidence.

<!-- rpi:phase id=P02 -->
## P02: Validate integrated source

Test ownership/removal/addition budget is locked in the plan: no removals, at most two justified integration regressions. Use installed distributions and explicit sibling paths rather than legacy imports.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run lint, types and units

Verify installed distributions using /tmp/mv/bin/python -m pip show zava-forward-core zava-forward-agents zava-forward-api. After the observed missing IoT SDK result, restore declared editable distributions using /tmp/mv/bin/python -m pip install -e 'src/core[dev,sql,blob]' -e src/agents -e 'src/api[dev]'. Keep manifests/lock pins unchanged unless an actual integration defect requires correction.

Copyable core commands, working directory src/core:

```bash
/tmp/mv/bin/python -m ruff check .
/tmp/mv/bin/python -m ruff format --check .
/tmp/mv/bin/python -m mypy
PYTHONPATH=src:tests:../agents/src:../agents/tests /tmp/mv/bin/python -m unittest -q test_sensor_stream test_sensor_consumer test_sensor_faults test_sensor_stock test_sensor_privacy test_sensor_backfill test_historical_backfill test_scenario_manifest test_needs_inventory
```

Copyable API commands, working directory src/api:

```bash
/tmp/mv/bin/python -m ruff check .
/tmp/mv/bin/python -m ruff format --check .
/tmp/mv/bin/python -m mypy
PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests /tmp/mv/bin/python -m unittest -q test_iot_stream test_sensor_ingestion
flock -n /tmp/ama-rpi-heavy.lock env PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests /tmp/mv/bin/python -m unittest discover -s tests -q
```

PYTHONPATH is runtime fixture/source resolution; mypy uses each project's configured mypy_path. Failed heavy admission means do not start full discovery.

From each owning directory use /tmp/mv/bin/python -m ruff check ., ruff format --check . and mypy. Core paths: src:tests:../agents/src:../agents/tests. API paths: src:tests:../core/src:../core/tests:../agents/src:../agents/tests. Cover sensor_stream, sensor_consumer, sensor faults/stock/privacy, historical backfill and scenario manifest/inventory, plus API iot_stream and sensor_ingestion. Main generator behavior is the reference, not historical bytes. Run full API discovery only inside successful nonblocking flock, holding it for the command. Do not read private data or call real SDK services. Record original failures and rerun evidence.

<!-- rpi:phase id=P03 -->
## P03: Review, commit and hand off

No hosted CI claim is possible before coordinator push. Review source once; later metadata closeout is not a second assessment.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Freeze source and perform one Review

Completed exactly once: independent record .copilot-tracking/reviews/logs/2026-10-29/iot-consumer-110-refresh-review.md, execution Complete, outcome Conformant with justified divergence. No source defects; RV-001 complete publication gate and RV-002 fresh hosted results remain coordinator-owned. Source unchanged after assessment; no repeated original Review.

Reconcile completed phase markers, details, changes/results and remaining blockers. Fresh reviewer reads plan/research/changes and actual diff against main, checks conflict preservation and focused tests, writes only the designated review file. Record execution separately from outcome; findings become later work.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Commit and publication-gate handoff

Use gh api user to derive privacy-safe repository-local author/committer. Include required co-author trailer. Keep numeric paid-Hub cost only in local PR notes for the coordinator, with region/currency/date/source/exclusions. Do not edit remote PR or push.

Static inspection during P02 proved the full runner invokes az bicep version/build/lint, which is outside the task's az cost-lookup-only permission. Therefore do not attempt it in this execution; record the blocker and coordinator ownership. No runner patch, wrapper, skip token, substituted status or receipt is permitted. Missing prerequisites or lock contention block publication, not evidence preservation. Keep exact-head receipt external; no fabricated status, cloud fallback, protection change or rewritten original outcome. Coordinator must fetch/verify fresh base and receipt before publication.

The coordinator must additionally obtain independent exact-head assessment after fetching main and verifying the external receipt, immediately before its separately authorized push. This is a separate publication control, not a second original implementation Review. Missing/adverse original Review, failed/missing full receipt or missing exact-head assessment blocks publication. Later commits, base/source/tool/image or dirty/untracked/ignored input changes invalidate gate evidence. Missing prerequisites or lock contention block publication, not evidence preservation. Keep exact-head receipt external; no fabricated status, cloud fallback, protection change or rewritten original outcome. Coordinator must fetch/verify fresh base and receipt before publication.
