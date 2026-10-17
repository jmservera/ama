<!-- markdownlint-disable-file -->
# Correction ONE: sensor-privacy-boundary-112

Task 112, 2026-10-17. Same worktree/branch/session resumed after authorized
VM upgrade. Base 74617981b71bc3f10bd21d0b78691bc3cf36c473; no remote branch/
PR existed at resume. No rebase, main write, other-worktree edit or discard.

## Retained Original Verdict

Original Review execution Complete, outcome Not accepted, two High findings.
Review SHA-256:
`dfd93ade80a484ac0551ec228d4ec974471cad98d98d806a98dbdb4583bf5476`.
Original critique retained too. This is implementation evidence, not another
Review or independent Pass. One correction cycle used of maximum two.

## RV-001: Raw Status Contributors

`export_fields.status_inputs` validates actual raw contributors, not the
already-stringified manual status. Closed/completed status needs no waiting
fields; open hazard validates its owner's scalar shape; ordinary status checks
waiting_on/reason. Chat validates the raw current record under the same Store
lock as authorized detail collection. Legacy prompt validation includes this
guard, and briefing validates before constructing its facts.

Manual `status_line`, detail, source history and hazard authority are unchanged.
No sensor-looking-key filter, blanket case hold or new AI task introduced.

## RV-002: Metadata Before Dispatch

`Store.read_document` validates selected name/mime before scan/audit
interpolation. `ai_tasks.run_document` validates metadata and captures checked
case sources before `look_at`. `Ai.look_at` validates at its direct adapter
boundary before rendering. Invalid selected structured metadata cannot call
provider/transport or emit the read-route AI-start audit.

No new semantic document-content classifier, legal approval, permission grant
or change to the ordinary valid document/manual path.

## Failing-First and Corrected Evidence

Two new test methods within the eighteen-method budget (sixteen total).
After fixture-only harness corrections, original uncorrected source produced
six assertion/subcase failures with no harness errors. Sentinels exercised
ordinary waiting/hazard owner chat+briefing and direct task/adapter/Store
document reading, including no-provider/no-transport/no-audit assertions.
Corrected fixtures persist raw data via existing SQL writer discipline before
chat refresh; no disabled checks or weakened assertions.

From repository root, commands executed sequentially to bound resources:

```bash
PYTHONPATH=src/core/tests .venv/bin/python -m unittest \
  test_sensor_privacy.SensorPrivacyTests.test_raw_status_inputs_refuse_before_chat_and_briefing_dispatch \
  test_sensor_privacy.SensorPrivacyTests.test_document_metadata_refuses_before_transport_and_audit -q

cd src/core
../../.venv/bin/ruff check .
../../.venv/bin/ruff format --check .
../../.venv/bin/mypy
PYTHONPATH=tests ../../.venv/bin/python -m unittest \
  test_sensor_privacy test_sensor_backfill test_sensor_stock test_sensor_faults \
  test_chat_panel test_chat_memory test_chat_privacy test_chatthreads \
  test_sqlreads test_documents test_dependency_rule -q

cd ../agents
../../.venv/bin/ruff check .
../../.venv/bin/ruff format --check .
../../.venv/bin/mypy
PYTHONPATH=tests:../core/tests ../../.venv/bin/python -m unittest discover -s tests -q

cd ../api
../../.venv/bin/ruff check .
../../.venv/bin/ruff format --check .
../../.venv/bin/mypy
PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest \
  test_ai_tasks test_chat_isolation test_chat_panel -q
```

Corrected results: new boundary file16 run/15pass/one opt-in actual SQL skip;
broader core145 run/144pass/one skip in58.395s; agents94pass in52.530s;
API86pass in27.276s. Ruff/format/mypy pass for all three. Expected existing
unavailable-law-store logs and CSV ResourceWarnings remain visible.

Earlier actual owned-loopback MSSQL pass remains applicable: correction
does not change persistence/admission. Own SQL container/database/credential
were already cleaned; no idle SQL server restarted. Earlier complete-core
discovery exit137 remains incomplete, not retroactively passed after upgrade.
No browser (no web edit), live Azure/IoT/Graph, private dataset, paid inference,
deployment or human/legal acceptance performed.

## Disposition

RV-001 and RV-002 implementation corrections verified by the scoped oracles
above. Original adverse Review remains unchanged and final-head independent
acceptance is coordinator-owned. OD-43 approvals and #175 unverified origins
remain open; no real-data activation. Ready for clean normal push and main PR
with Refs #112, no merge/issue closure.

Publication receipt: https://github.com/jmservera/ama/pull/393 targeting main,
normal-pushed implementation commit 6225442c496653cab3b63b611f9632c642859bf5.
Delivery-state commit persists this link; final remote topic head is returned
in the CLI handoff. No second Review, merge or issue closure.
