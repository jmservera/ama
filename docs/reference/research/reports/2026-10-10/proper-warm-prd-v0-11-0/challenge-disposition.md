---
title: Proper Warm PRD v0.11.0 Amendment Challenge Disposition
description: Draft-stage System One and form-assistance corrections, verification scope and retained approval blockers
ms.date: 2026-10-10
ms.topic: reference
---

## Scope and Evidence

One independent PRD Quality Reviewer challenged the draft amendment and
returned [standard findings](./standard-findings.json) and a
[quality report](./quality-report.json). These original payloads are retained
unchanged: full-document outcome FAIL, Validate BLOCKED, Finalize
NOT_EVALUATED. They describe the pre-correction text, not a final regrade.
The reviewer could read the complete PRD and references but could not obtain
the Git diff. The author verified amendment scope against `origin/main`.

The user requested updating the PRD, not resolving every pre-existing
requirements-maturity gap or authorizing implementation. The following
dispositions are author corrections checked in the final document; they are
not independent re-approval or operational acceptance.

## Dispositions

| Finding | Scope | Disposition and check |
| --- | --- | --- |
| req-qual-002 | Amendment | FR-038/AC-046 now require a versioned schema for every form but an evidenced scheme/route only for funding forms. Non-funding technical/invoice fixtures explicitly use a not-applicable funding association and can open without a funding route. |
| req-qual-003 | Amendment | FR-019/042 and AC-022/050 now distinguish application submission/disposition from claim submission/disposition. External events bind scheme/route, pack version and authorized evidence; separate subchecks compare unrelated application, claim, award, cash and invoice states exactly. Both FR/AC tables and the reciprocal matrix were updated. |
| req-qual-004 | Amendment | AC-047 has separately reported parser/OCR lineage, candidate/no-match, conflict and manual-recovery checks. AC-051 requires a fixture-owned expected direct/transitive affected-ID set, unaffected reviews and blocked-export expectation, with exact actual-set comparison. |
| req-qual-001 | Existing readiness plus stale source label | Reconciled active BRD source labels to its current draft v0.15.0. Signed current upstream handoff/quality evidence, named owners and required human reviews remain blockers; no approval was fabricated. |
| req-qual-005 | Existing full-document maturity | Four product-goal time horizons, achievable targets and approved protocols remain unresolved. No company targets invented or SMART pass claimed. |
| req-qual-006 | Existing full-document maturity | Quantitative performance/load and canonical scaling targets remain owner decisions. No deployment, SLO or whole-stock performance result claimed. |
| req-qual-007 | Existing proposal taxonomy | TR/DH/PR/SA remain proposed baselines. The 44-FR metric is canonical link coverage, not coverage of every proposed obligation or behavioral acceptance. Canonicalization beyond this amendment remains future Build work. |

## Document Verification

* Verified 44 canonical FRs, 54 ACs, 13 NFRs, 8 constraints and 16 open
  questions, including exact reciprocal FR/AC/matrix and goal-table links.
  Corrected two existing missing goal-table references while extending that
  table; requirement IDs and intended goals were unchanged.
* The PRD, System One synthesis and idea register pass pinned
  `markdownlint-cli2` 0.18.1 with the existing MD013 long-table convention.
  The index/log retain exactly three baseline lint findings: two existing
  incomplete index rows and a historical bare URL. The same findings were
  reproduced from `origin/main`; no lint gate was weakened or historical
  log entry rewritten to hide them.
* Reviewed generated Markdown table/heading output, new local links and
  anchors, state JSON/version consistency and the Git diff. No application
  behavior test, form export, model call or Foundry deployment was run.

## Remaining Gates

The PRD remains draft/Build. Approved scheme templates and critical-field
criteria (OQ-015), task-specific datasets/thresholds and serving/privacy
evidence (OQ-016), current signed upstream evidence and human reviews are
still required. Parent amendment dispositions do not supersede the original
quality report or authorize Validate/Finalize exit.
