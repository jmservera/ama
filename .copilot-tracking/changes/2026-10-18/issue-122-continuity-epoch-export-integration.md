---
title: Issue 122 authorized post-397 integration receipt
description: Exact-base ancestry integration, not a third source correction or Review
ms.date: 2026-10-18
---

## Authorization and Ancestry

Same session 33f480bb-395e-4492-8a02-d3a84c5a7a89, PR #398, owned branch
fix/continuity-epoch-export-122. Clean published head independently verified:
a40fdd3623eae4ee23712f474909d58cdbcb7bfc. Old base
99056cae7bc679d2ace3e42c75f28577cfce8887; tested original source
0067f2a1cacf2bd7f821ea13988566b8b4af0b71. Coordinator explicitly authorized
rebase onto exact merged #397 base 3104bb69ddc26c81e0e9d2f57000dac1d99a419a
and only this remote update lease:
refs/heads/fix/continuity-epoch-export-122:a40fdd3623eae4ee23712f474909d58cdbcb7bfc.
No main force push, domain changes, third correction or Review.

## Textual Integration and Parity

Rebase completed. Sole conflict: both branches inserted a section at the top of
src/api/README.md. Retained upstream appointment section followed by the unchanged
continuity section; no prose dropped. Projection merged without conflict,
retaining #87 appointment_evidence_visible/type annotations and the two continuity
STAFF_GET entries.

| Old commit | Rebased commit |
| --- | --- |
| 441da95000318b9b13c928717aba069c5f748487 | ca46d172 (original source/artifacts) |
| 649d242c3b6fb6236d2f039fd0eeee50daf77af3 | 08be1ba3 (correction ONE) |
| 0067f2a1cacf2bd7f821ea13988566b8b4af0b71 | 24ee7034 (tested source correction TWO) |
| a40fdd3623eae4ee23712f474909d58cdbcb7bfc | 61e04f8a865c4bbf7eee1336c83b2c93a4b2ebd0 (publication receipt) |

Pre/post source patches saved in session files as integration-before.patch and
integration-after.patch. Programmatic blob comparison proved:

* Own assistants/continuity/ai_tasks/store, focused tests and API pyproject exactly
  byte-identical to published source; no feature logic edits.
* Projection equals exact upstream blob after removing only the two authorized
  continuity names.
* Own README continuity section byte-identical; removing it yields exact upstream
  README, including all appointment content.
* All 35 upstream changed files match exact upstream bytes except these two
  explained additive overlaps. docs/reference/log.md retains its old prefix.
* range-diff shows only README insertion context/frontmatter already supplied by
  upstream; final source correction and receipt patches equivalent.

Frozen critique SHA-256:
4eeda2d60235f571916a83de65fa9cda8d73e2159291a50286e8055328fc77be.
Frozen original Not accepted Review SHA-256:
9d9d0bff0fdda5a8d163967c4ba8a997ee1bc315ae5a896611fc331aff200abc.
Both verified unchanged after rebase.

## Integration Validation

Completed on integrated runtime at 61e04f8a865c4bbf7eee1336c83b2c93a4b2ebd0.
Only documentation/tracking metadata changed afterward. Existing merged #87
fixtures/runtime were used, not old source mounts. No test/source repair or
new domain behavior was needed; no new failure was observed in these checks.

| Boundary | Actual result |
| --- | --- |
| Targeted host epoch/export/legacy/roles/appointment/procurement/quality/resident/progress/hazard | 563 run, 455 pass, 108 skips, no failures |
| Actual task-owned local SQL Server 2022 16.0.4305.5 | 81 run, 81 pass, no skips; independent connections and cross-domain cases |
| Rebuilt installed hardened API image targeted cross-domain suites | 329 run, 271 pass, 58 opt-in/platform skips, no failures |
| API/core/agents configured Ruff, format --check, mypy | All pass; mypy 57 / 123 / 23 source files (core now includes upstream appointment module) |
| Source-context Docker build and existing check-container.py | Image sha256:e36a4789f259d1b9b497c23e49903333483b1cc6a9cfe8dab85216288a063c2f; controls, negative probes and compatible startup pass |
| Installed runtime parity | assistants, continuity, projection, ai_tasks, store, appointments, procurement, sqlstore and server exactly match worktree |
| Scope / historical evidence / cleanup | Own source parity and 35 upstream files preserved; frozen hashes unchanged; exact owned containers removed |

Host command:

```bash
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest \
  test_continuity_epoch_export.EpochTests test_continuity_epoch_export.LegacyTests \
  test_continuity_epoch_export.OfflineTests test_continuity_epoch_export.HttpTests \
  test_continuity test_ai_tasks test_assistants test_assistant_release \
  test_assistants_dispatch test_workflows test_role_endpoint_inventory \
  test_procurement_api test_quality_procurement test_resident_decisions \
  test_progress_event_capture test_hazard_referral -q
```

Host skips remain actual skips, not passes: opt-in MSSQL suites, explicitly
unperformed isolated Azure SQL test and test-environment preconditions. Static
discovery reports 49 disposable-MSSQL, 38 resident-MSSQL, 18 capture-MSSQL and one
Azure opt-in marker; two further tests skip at runtime. Dedicated local SQL
selectors below execute affected cases but do not convert all host skips into
passes or supply Azure evidence.

Static commands from each component:

```bash
../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy
```

Actual SQL command:

```bash
ZF_CAPTURE_MSSQL=1 ZF_RESIDENT_MSSQL=1 .venv/bin/python -c \
  "import runpy; runpy.run_path('/home/azureuser/.copilot/session-state/33f480bb-395e-4492-8a02-d3a84c5a7a89/files/run_owned_sql.py', run_name='__main__')" \
  test_continuity_epoch_export.MssqlEpochTests \
  test_continuity_epoch_export.MssqlLegacyTests \
  test_continuity_epoch_export.MssqlOfflineTests \
  test_continuity_epoch_export.MssqlHttpTests \
  test_assistants.MssqlContractTests test_assistants.MssqlReviewTests \
  test_assistants.MssqlDurabilityTests test_assistants.MssqlApiTests \
  integration_sql_boundaries.MssqlProcurementApi.test_appointment_controls_http_provenance_denials_and_committed_response \
  integration_sql_boundaries.MssqlProcurementApi.test_appointment_http_serialized_canaries_follow_existing_roles \
  integration_sql_boundaries.MssqlProcurementApi.test_human_home_case_closure_http_evidence_denials_reset_and_committed_retry \
  integration_sql_boundaries.MssqlQualityAppointments.test_appointment_concurrent_confirmations_and_outcomes_are_not_lost \
  integration_sql_boundaries.MssqlQualityAppointments.test_human_closure_wins_against_stale_event_without_count_or_history_loss \
  integration_sql_boundaries.MssqlQualityAppointments.test_return_fix_reinspect_handover_aftercare \
  test_progress_event_capture.MssqlCapture.test_actual_forward_return_pause_and_reopen \
  test_progress_event_capture.MssqlCapture.test_actual_quality_remediation_and_independent_handover_versions \
  test_resident_decisions.MssqlResidentControls.test_response_reassignment_status_clock_follows_responsibility_not_shared_person
```

Session-only integration_sql_boundaries.py subclasses existing tests to replace
only SQLite fixture creation/reopen with actual MssqlStore on UUID-named owned
databases. Test assertions and production source are unchanged. It is not a mock,
SQL adapter refactor or new committed test policy. Runner temporarily includes
the session helper directory on test PYTHONPATH. Exact owned container
zf-issue122-sql-33f480bb uses local loopback, private ephemeral credentials,
3GB limit and finally stop/remove. No shared database or Azure is touched.

Image commands:

```bash
docker build -q -f src/api/Dockerfile -t zf-issue122-api:local src
.venv/bin/python src/check-container.py api zf-issue122-api:local
docker run --rm --name zf-issue122-image-33f480bb --read-only --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --tmpfs /tmp:rw,nosuid,nodev,uid=10001,gid=10001 \
  --tmpfs /state:rw,nosuid,nodev,uid=10001,gid=10001 \
  -e PYTHONPATH=/tests/api:/tests/core:/tests/agents \
  --mount type=bind,source="$PWD/src/api/tests",target=/tests/api,readonly \
  --mount type=bind,source="$PWD/src/core/tests",target=/tests/core,readonly \
  --mount type=bind,source="$PWD/src/agents/tests",target=/tests/agents,readonly \
  --entrypoint python zf-issue122-api:local -m unittest \
  test_continuity_epoch_export.EpochTests test_continuity_epoch_export.LegacyTests \
  test_continuity_epoch_export.OfflineTests test_continuity_epoch_export.HttpTests \
  test_role_endpoint_inventory test_procurement_api test_quality_procurement \
  test_resident_decisions test_progress_event_capture -q
```

No application source mount; installed runtime is rebuilt after upstream runtime
changes. UID/GID10001, read-only root, no capabilities, no-new-privileges; actual
HTTP manager full/limited proof and denials, nested canaries, appointment audience
projection, resident/progress/quality paths exercised. Manual hazard/authority
tests remain real transactions. Synthetic App rule evaluation is explicitly
Unknown without its law store, not compliance acceptance. Local SQL is not Azure;
no live inference, notices, private inputs or real authority.

Logs are in the same session files directory: integration-host.log,
integration-sql.log and integration-image.log. No new independent Review ran.
Before/after patch artifacts and session SQL harness remain local supporting
evidence, not new repository source files.

## Current Source and Metadata

New exact integration base: 3104bb69ddc26c81e0e9d2f57000dac1d99a419a.
Rebased final correction source: 24ee70347064886a1847b1fea8b5219ad6323e6d.
Integrated tested tree: 61e04f8a865c4bbf7eee1336c83b2c93a4b2ebd0.
Subsequent tracking commit updates plan/details/changes/correction-two/state and
adds a README integration-base note, preserving both original README sections.
Original research, critique, Review and correction-one receipt are not rewritten.
Knowledge log prefix and all #87 artifacts remain unchanged.

Projection composed hash:
1b412fe1cc870dea21a017f861e4a129b6234a974c8b95ef5f071710cc7eef91.
Own continuity hash remains:
0616465f7da75c04acceb6cd0da4e6fa2f69e6e9ce40781c0b8ba1c13983a9c8.
Source parity is an integration property, not a new acceptance verdict.

## Publication Gate

Before tracking commit, remote branch still independently matched exact expected
a40fdd3623eae4ee23712f474909d58cdbcb7bfc and remote main exact new base.
All validation and frozen hashes passed. Final tracking commit is documentation
only; fresh gh api user supplies privacy-safe local author/committer email and
required Copilot trailer. Authorized publication command, used only if both
remote invariants still hold:

```bash
git push --force-with-lease=refs/heads/fix/continuity-epoch-export-122:a40fdd3623eae4ee23712f474909d58cdbcb7bfc \
  origin HEAD:refs/heads/fix/continuity-epoch-export-122
```

PR #398 stays main-based with Refs #122, updated new-base/source/parity/validation
metadata and original adverse verdict. Published exact head is discoverable from
this tracking commit/PR, not fabricated into a self-referential receipt. Coordinator
full review and required checks follow publication; no merge/AC/board change.

## Residual Gates

Both source corrections remain exhausted. Independent full review is scheduled
after integration, not performed here. Genuine OQ-017 authority, witnessed drill,
immutable external Azure head, Azure SQL drill and unsupported-old-image exclusion
remain unmet. No live inference, Azure/Graph/IAM, private input or notices.
