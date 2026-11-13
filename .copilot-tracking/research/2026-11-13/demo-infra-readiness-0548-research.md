<!-- markdownlint-disable-file -->
# Research: demo infrastructure readiness, #137 #144 #146 #148 #189

Date 2026-11-13. Pin: main `15bfee2d7f6ae9b73d24c51d3dbbea7c7b78f626`. Branch `research/demo-infra-readiness-0548`. Research disposition: executed (bounded, read-only; issue bodies and latest comments, selected infra blobs, prior ledger findings at the same pin reused). Planning Readiness: Ready (for a documentary disposition plan).

## Boundaries

* Read: the five issue bodies/latest comments; `infra/main*.bicepparam`, `infra/live-simulator-job.bicep`, `infra/README.md` region/quota section (lines 1000-1140), `infra/monitoring-runbooks.md` header, `infra/tests/` listing; ledger `demo-run-ledger.md` lines matching these issues.
* Not read or run: test bodies, SQL, private data, `.env`; no Azure/cloud/model/Docker/deployment; no source edits. Prior same-pin findings reused, not repeated.
* Spend: nothing consumed. Source-correction budgets are not reset by this work: #148 C1 1 of 5 spent; #144 E1-E5 exhausted; #189 C5 exhausted; #184 format permission ungranted. Unknown balances stay UNKNOWN.

## Literal AC dispositions

| Issue / AC | Current-main evidence | Class |
| --- | --- | --- |
| #137 AC1-3, AC5 (ticked) | `infra/main.bicepparam` 4f5ec4c2, `main.test.bicepparam` 750b2bd6, `main.pilot.example.bicepparam` 04a8d59b; README difference table and naming | Delivered, unchanged |
| #137 AC4 region/quota choices are parameters with recorded checks | Parameters `location`, `sqlLocation`, `regionCheckReference`, `quotaCheckReference` exist; empty reference fails a named guard (README 1024); README 1030-1084 records dated uksouth listings (R1/R12 pass, SQL/IoT/model quota Unknown or Blocked) | Source half implemented. Owner selection of pilot region `uksouth` and subscription owner is recorded (issue 137 comment 6192754703, README 965-975); not decided: SQL region, zone redundancy, sizing, subscription binding. Dated selected-subscription region/quota check records remain human/cloud-only. The stale comment at `main.pilot.example.bicepparam:6` is a comment-only inconsistency that README 965-975 already calls stale; correcting it would satisfy no literal AC, so it is not admitted as a ready task |
| #144 five open criteria (workers, scaling, rollout/rollback, load test) | Probes/scaling pass two focused checks (comment 2026-11-13); standalone agents image is a placeholder; E1-E5 allowance exhausted; PRs #1428, #1452 merged | Owner decision (API-hosted AI vs new bounded worker slice); live load/rollout human/cloud-only; no reset |
| #146 AC1-4 | Source alerts, workbook (blob 614bdfd9), runbooks (83640bcc), PRs #512/#1011/#1140 merged; routing candidate 9c2a59f6 paused because it would disable two severity-1 ledger alerts. Runbook lines 273-295 list the two poison queues (`agent-tasks-poison`, `import-jobs-poison`) as missing signals: no queue-specific depth/age producer, and service-wide queue depth is expressly not a substitute, so a Bicep metric alert cannot close it; a producer is runtime code, outside this Bicep/run-control slice and unadmitted. Diagnostic sanitiser (runbooks ~350-353) is not wired into platform log collection; wiring is the paused routing candidate | Implemented-unverified for AC1/AC2/AC3; AC1 poison-queue part and AC4 are true source gaps but each is blocked: poison producer has no admitted source scope or Bicep-only form, sanitiser wiring waits on the owner tradeoff decision. Installed coverage and named owners human/cloud-only |
| #146 RAI harm and tokenomics unticked criteria | Issue body: depend on #110, #115 and #432; application/report/UI surfaces, not Bicep | Dependency-held; outside the initial local Bicep/run-control slice; not assessed further here |
| #148 AC1-3 (ticked) | PRs #1348, #1410 merged (dry runs, image checks) | Delivered |
| #148 AC4 dry-run and disposable-environment test | Dry-run mode delivered; actual disposable Azure rebuild/teardown not observed | Human/cloud-only (spend authority) |
| #189 AC1-2 (ticked) | Estimate and quota headroom recorded | Delivered |
| #189 AC3 run owner, time limit, budget alert | `live-simulator-job.bicep` requires an owner approval reference and `replicaTimeout`; control.json carries cohort, owner, expiry, stop; admin tests exist (C5 exhausted) | Source controls delivered; live owned run and budget-alert observation human/cloud-only; depends on #140 and #146 |

## Gap search result

No source-backed missing INITIAL local Bicep or run-control slice found. Each candidate local change either repeats delivered work (#148 adapter, #146 workbook, #189 controls) or needs a spent allowance (#144, #189 C5) or an owner decision (#146 routing, #144 worker scope, #137 region). Recording that fact does not claim global blockage; #184, #74 and other independent work are unaffected.

## Evidence qualifications

* #148 dated local evidence is at source 64c3f919, not fresh main. #184 frozen e904ba4c0 now has Ruff format FAIL and SQL unrun; no format permission inferred. Quarantined c71 SQL helper pass remains unapproved. No stale five-minute wording repair is made here.
* README region/quota rows are historical dated observations, not a fresh check of current main.
