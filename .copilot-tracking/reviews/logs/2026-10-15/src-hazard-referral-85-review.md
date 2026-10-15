---
title: Hazard referral and retrofit hold review
description: Single post-implementation review, reproduced defect and residual acceptance routing
ms.date: 2026-10-15
---

## Execution and Outcome

Task 85, src-hazard-referral-85. Review execution: Complete.
Review outcome: Not accepted. One High concurrency defect remains open.
Exactly one post-implementation Review was performed; no correction or repeat
Review is claimed. The local suites pass but do not prove the concurrent gate.

## Compared Artifacts and Assessed Boundary

* `.copilot-tracking/research/2026-10-15/src-hazard-referral-85-research.md`
* `.copilot-tracking/plans/2026-10-15/src-hazard-referral-85-plan.md`
* `.copilot-tracking/details/2026-10-15/src-hazard-referral-85-phase-details.md`
* `.copilot-tracking/plans/2026-10-15/src-hazard-referral-85-critique.md`
* `.copilot-tracking/changes/2026-10-15/src-hazard-referral-85-changes.md`
* Issue 85 acceptance text and recorded retrieval W1 (no comments returned).
* Accepted ADR 0006, parity matrix and merged src moves 296 through 302;
  existing building and handoff delivery.
* Current changed core workflow, store/projection, procurement, sign-off,
  quality, API server/web, directly coupled tests, new semantic/HTTP tests,
  READMEs, content standard, reference index and append-only log.

Review boundary is local engineering, authority separation, persistence,
privacy and plan/evidence reconciliation, not legal advice, verified repairs
transport, real-model effectiveness, actual SQL Server/Azure or human approval.
P01-T01/P02-T01/P03-T01 are reconciled with completed local evidence.
P03-T02 delivery bookkeeping (commit/push/PR) follows this assessment and cannot
convert the verdict to acceptance. Original issue criteria remain unticked.

## Coverage and Dispositions

| Requirement or decision | Assessment |
| --- | --- |
| src-only placement and ADR 0006 dependency/image rules | Preserved; no new workload imports, SQL or agents SQL/blob extras |
| External service owns categorisation, clocks and closure | No service mutator added; report labels and hold-only restart wording distinguish authority |
| Sent, receipt and acceptance | Separate authenticated evidence snapshots and role gates; real transport remains unverified |
| Hold scope and accountable independent release | Whole-home scope and release actor/role/evidence durable locally; concurrent procurement enforcement is defective, RV-001 |
| External response/resident-update visibility | Due/actual/unknown observations, no overwrite; recording remains possible after retrofit restart |
| Consent, case owner and independent building controls | Existing decisions/ownership unchanged; sequential gate and sibling regressions pass |
| PC-001 closed-record intake | Applied in core, HTTP and reachable panel without reopening |
| PC-002 legacy forward continuation | Original record preserved; prospective binding/receipt/acceptance/repair evidence, no invented awareness |
| PC-003 inherited wording/policy | New same-day promise removed; existing ledger untouched; plain-language restart wording |
| Field minimisation and model boundaries | Protected narratives withheld from no-need roles and contractors, not added to model sources |
| Implementation-time changes | Additional progression checks are necessary coupled enforcement, not unrelated redesign; fixture/copy updates preserve test intent |
| Follow-ups and acceptance limits | Owner/live evidence remains correctly unclaimed; RV-002 and RV-003 route it separately |

## Validation Considered

* Final full core suite: 312 tests, passed.
* Final full API suite: 475 tests, passed with 99 optional/environment skips.
* Agents: 70 tests, passed; orchestrator: 17, passed; importer: 39, passed.
* Fourteen new JSON/SQLite semantic tests and three actual loopback synthetic
  HTTP application tests are included in those totals.
* All five project ruff lint/format and mypy gates passed.
* JavaScript syntax, diff whitespace and 25 migration regressions passed.
* Docker info/build both failed with daemon permission denied; no image,
  runtime or scan evidence is claimed. CI remains necessary.
* Existing sensor-file ResourceWarnings and negative auth logs are not test
  failures. Initial failed commands and their repairs are preserved in changes.
* Additional two-store synthetic review reproduction below passed its
  defect-demonstration assertion: completion committed after an active hold.

## Independent Participation

One generic read-only code-review lens assessed the specific uncertainty of
cross-surface hazard authority, persistence and progression enforcement.
It reported the High concurrency defect. It wrote no source or separate
review artifact and launched no nested agents. The parent reproduced the
finding through an executable two-store check, not another source review.

## Findings and Routing

### RV-001 High: concurrent hazard intake can bypass procurement restriction

* Kind: introduced functional enforcement defect.
* Evidence: `src/core/src/zava_forward/core/procurement.py`, guarded
  work-order transitions, especially `complete_work_order`; existing
  `src/core/src/zava_forward/core/sqlstore.py` save logic persists procurement
  but does not validate an unchanged dependent case row.
* Reproduction: store A passes the safety check; store B commits an emergency
  hazard for the same home; A commits work-order completion. Persisted result:
  `{"work_order_state":"Completed","active_home_safety_holds":1,
  "last_actions":["safety_emergency","safety_raised","workorder_completed"]}`.
* Why suites miss it: they validate sequential refusal and restart, not a
  second instance changing the dependent case after validation.
* Impact: the new safety restriction is not a reliable concurrent boundary
  for work-order progression. This prevents acceptance/merge despite passing
  local suites.
* Destination: distinct later `rpi-implement` task, highest priority. Validate
  dependent case version/safety state inside the transaction that commits each
  affected procurement transition, with portable SQL Server behavior and an
  interleaved two-store regression. Merely touching `_case()` is insufficient
  because unchanged case bodies are skipped by save.
* Status: Open. No fix or closure verification executed in this lifecycle.

### RV-002 Medium: operational responsibility and timing policy unratified

* Kind: declared owner decision gap, not a hidden implementation claim.
* Evidence: research/plan/changes defer approved hazard destination/release
  authority, operational timing/escalation thresholds and human acceptance.
* Destination: later `rpi-plan` with Repairs/Safety/Housing owners; preserve
  original issue checkboxes until role and service-process acceptance exists.
* Status: Open; no policy, legal deadline or human approval invented.

### RV-003 Medium: actual service and mandatory platform evidence unavailable

* Kind: declared evidence gap and residual application acceptance work.
* Evidence: local human-recorded references are not transport proof.
  Tests use fictional JSON/SQLite and loopback HTTP, not a permitted real
  model task, actual SQL Server durability or an Azure workflow. Local Docker
  cannot access its daemon.
* Destination: later `rpi-research`/distinct validation work to obtain approved
  access and verify service contract, then actual AI/SQL Server/Azure workflow
  and human evidence; CI handles image/runtime/scan gates.
* Status: Open. Existing AI release/human gates are preserved, not forcibly
  enabled or treated as a waiver of mandatory real-platform acceptance.

## Parent Reproduction Command

Executed from the worktree, exit 0; temporary fictional files automatically
removed by TemporaryDirectory. This reproduces a defect, not passing safety:

```bash
PYTHONPATH=src/core/tests .venv/bin/python - <<'PY'
import json
import tempfile
from pathlib import Path
from dataset import DATA
from zava_forward.core.sqlstore import SqlStore

with tempfile.TemporaryDirectory() as folder:
    seed = Path(folder) / 'synthetic.json'
    seed.write_text(json.dumps(DATA))
    db = str(Path(folder) / 'state.sqlite')
    a = SqlStore(str(seed), db)
    manager = a.staff['pam@example.test']
    pid = a.create_package(manager, 'Synthetic race', '2026-01-01', '2099-12-31', 'Loft', 'SYN-CONTRACT')
    a.set_capacity(manager, pid, 'Test Ltd', 2, 2, 'SYN-CAPACITY')
    wid = a.issue_work_order(manager, pid, 'ZF-3')
    a.record_wo_appointment(manager, wid, 'Booked', '2099-01-01')
    b = SqlStore(str(seed), db)
    check = a.require_safety_clear
    def interleaved_check(case):
        check(case)
        b.raise_hazard(manager, 'ZF-3', 'Electrical', 'Emergency', metadata={
            'source': 'SYN-CONCURRENT-REPORT', 'aware_at': '2026-01-01T10:00:00Z'})
    a.require_safety_clear = interleaved_check
    a.complete_work_order(manager, wid, 'SYN-COMPLETION')
    with b.lock:
        order = b._work_order(wid)
        active = sum(not h['released'] for h in b._case('ZF-3')['hazards'])
        print(json.dumps({'work_order_state': order['state'], 'active_home_safety_holds': active,
                          'last_actions': [e['action'] for e in b.audit_entries()][-3:]}))
        assert order['state'] == 'Completed' and active == 1
    a.db.close()
    b.db.close()
PY
```

## Outcome and Handoff

Execution Complete, outcome Not accepted, severity summary one High defect
and two Medium decision/evidence gaps. Complete this RPI task with routed
follow-ups; do not transition back to Implement or repeat Review.
Authorized delivery should be a draft PR using Refs #85, prominently stating
RV-001 is open and not merge-ready. Do not mark issue criteria complete.
No child work is selected or started automatically.
