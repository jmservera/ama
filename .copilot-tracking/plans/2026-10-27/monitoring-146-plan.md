---
title: Monitoring 146 implementation plan
ms.date: 2026-10-27
---

Task ID: 146. Slug: monitoring-146. Status: source-only authoring complete;
independent Review Complete / Residual work; operational acceptance blocked.

## Executive Summary

Author an additive, disabled-by-default job/IoT alert module, an aggregate-only
operations workbook and complete operator runbook catalogue. Correct the existing
ledger 26-hour search boundary. Preserve all original issue criteria as unproven
where runtime/human evidence is missing. Publish one draft PR with Refs #146,
not an activated monitoring solution.

## Sources

Research: .copilot-tracking/research/2026-10-27/monitoring-146-research.md.
Details: .copilot-tracking/details/2026-10-27/monitoring-146-phase-details.md.
Review base: f183ba391de10fb7bcfc6157cbcbb2290b9cf4fc.

## User Decisions and Requirements

* Full ordered RPI loop with dated artifacts, existing branch, one draft PR.
* Bicep and documentation authoring only; no deployment or application edits.
* No secret/.env/private-data reads, uv, --all gate or workflow/check renames.
* At most one --changed gate, only for large changes, under timeout-zero heavy
  lock. This bounded source-only task does not justify the heavy gate.
* Actual operators, live thresholds and privacy approval are human decisions.
  Implement independent work and stop at that boundary, documenting it in PR.
* Preserve resident consent, independent hazard/manual routes and human approval.

## Goals

Make source monitoring gaps and response ownership explicit without falsely
claiming operational completeness, availability, financial reconciliation or RAI
acceptance.

## Scope and Non-Goals

In scope: infra/main.bicep, new infra/modules/operationalMonitoring.bicep,
new infra/monitoring-workbook.json, infra/monitoring-runbooks.md, infra/README.md,
knowledge-base index/log and dated tracking artifacts.
No application code, deployments, new telemetry producer/platform, price
selection, named operator appointment, unapproved threshold or retention change.

## Functional Requirements

* FR1: disabled candidate alerts for failed executions of each authored background
  job, IoT ingestion throttling and routing drops/invalid/orphaned messages.
  Wire both normal and demo names and optional token-renewal job.
* FR2: workbook scoped to the existing workspace/Application Insights, aggregate
  request/error/p95 samples and availability-test results. Missing telemetry shows
  Insufficient; proposed SLOs are not attained values. Budget configured value is
  distinct from Unknown Azure actual/forecast cost and missing AI usage.
* FR3: runbooks cover every existing and new alert plus poison-queue, AI-limit
  and RAI incident gaps; proposed accountable roles are not actual appointments.
* FR4: ledger missing-success search truly covers 26 hours, preserving names and
  existing behavior otherwise.

## Non-Functional Requirements

* No new log categories, identities, public endpoints or raw-content outputs.
* New alert enablement false by default; enabling requires a nonempty reference
  to separately reviewed named-human owner/threshold/activation evidence.
* Workbook must never coalesce missing usage, cost, approvals or thresholds into
  zero/green. Protected audit evidence stays separate.
* Existing allLogs/audit privacy gaps are exposed, not claimed fixed by queries.

## Acceptance Criteria

These are authoring acceptance criteria, not checkmarks on issue #146.

* AC1: Bicep compiles under the existing strict analyzer; compiled resources show
  correct action group, scopes, names, flags and optional workload conditions.
* AC2: workbook JSON parses after Bicep parameter substitution; queries use actual
  schema columns and count/weight samples; missing rows have explicit statuses.
* AC3: each existing/new alert has a unique runbook anchor, proposed owner,
  triage, safe response, recovery evidence and human boundary.
* AC4: original, RAI and tokenomics criteria have explicit evidence/gap mappings;
  no operational criterion falsely checked.
* AC5: targeted existing infrastructure regression suites pass with their
  skips/failures honestly recorded; no deployment/heavy gate.

## Test Ownership and Coverage Lock

Author owns local compiled-template assertions and existing infra regression
execution. New committed test code: none (caller Bicep/docs-only restriction).
Removals: none. Maximum added production artifacts: two Bicep/JSON source files
and one runbook Markdown, plus required dated RPI records. Canonical files are
the Bicep/JSON/docs; compiled ARM and validation output stay external in a new
temporary directory. Semantic checks cover optional flags, exact metric names,
26h boundary, JSON structure and no raw-content query projections. Regression
coverage uses existing Bicep policy/container/IoT/governance/secret tests.

## Phase Checklist

<!-- phase: P01 -->
### P01: Author monitoring definitions and operator guidance

* [x] P01-T01: Add disabled metric candidates and workbook; wire flags/names.
* [x] P01-T02: Fix ledger query lookback, author all alert runbooks and gap matrix.
* [x] P01-T03: Update infra guide, knowledge-base index and append-only log.

<!-- phase: P02 -->
### P02: Validate and reconcile evidence

* [x] P02-T01: Compile, parse workbook, inspect compiled conditions and run existing
  bounded infrastructure tests.
* [x] P02-T02: Reconcile changes/details and stop at human activation boundary.

<!-- phase: P03 -->
### P03: Independent Review and draft publication

* [x] P03-T01: One fresh independent exact-source Review; preserve its outcome.
* [x] P03-T02: Commit with privacy-safe identity and required trailer, push topic
  branch, open one draft PR to main with Refs #146 and exact evidence/gaps.

## Critique Disposition

Critique executed once: Complete / Revise, preserved at
.copilot-tracking/reviews/2026-10-27/monitoring-146-plan-critique.md.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Applied | Details P01-T01/P02-T01 now define tables, missing/error behavior and weighted-sample source checks |
| PC-002 | Applied | Details P02-T01 includes explicit deployment/name/activation matrix and independent IoT rules |
| PC-003 | Applied | Details P01-T02 adopts 12 existing notifications/rules, eight candidate anchors and B1-B4/R1-R8/T1-T3 |
| PC-004 | Rejected | Claimed prohibition on /tmp/external scratch is not in this parent execution's instructions. Caller explicitly requires external output for a heavy gate, if used; no such gate runs. Use a uniquely named external scratch directory and retain original evidence. No invented constraint accepted |

No significant/divergent authoring decision remains. Human activation stays
blocked; this is readiness only for independent source authoring. No re-critique.

## Follow-Up Items

* Owner: appoint named operations/incident owners and approve windows/thresholds,
  response limits, recipients and activation evidence.
* Runtime follow-up: safe per-poison-queue depth/age and AI-limit/harm aggregate
  producers through existing SQL audit/report/incident surfaces.
* DPO/Compliance: establish source-side diagnostic exclusion and restricted
  evidence retention; no privacy approval is supplied here.
* Finance: OD-51 budgets/price source/period reconciliation; cost remains Unknown.

## Handoff

P01/P02 source authoring and local validation complete. P03 independent Review
is Complete / Residual work at source 64148474e6c6e8cbedfeb09b1f4e9a3775b15318,
preserved at .copilot-tracking/reviews/logs/2026-10-27/monitoring-146-review.md.
Draft PR: https://github.com/jmservera/ama/pull/512, Refs #146, no closure claim.
Final publication records do not change assessed implementation. No
return-to-implementation or second Review. Stop at human decisions; RV-001
through RV-004 require separate owner-selected follow-ups. No whole-issue,
full-gate, final-publication-head independent assessment or live acceptance.
