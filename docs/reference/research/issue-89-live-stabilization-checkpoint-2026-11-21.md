---
title: Issue 89 scoped stabilization checkpoint for the provider capacity epic (2026-11-21)
description: Requirement reconciliation, local regression results and a live read-only probe for the Epic 89 stabilization criterion, with a per-criterion verdict
ms.date: 2026-11-21
ms.topic: reference
---

Scope: synthetic demo, desktop only, head `9c3fe9dcb0376cc396bd18f0c6d05076b11ba06b`. Refs #89. No source change, no GitHub issue created, no Azure resource created or changed. The live probe is read-only. The method is the scoped checkpoint defined in #440 and recorded in [the #440 triage](./stabilization-checkpoint-triage-440-live-2026-11-18.md).

## Issue state

Epic #89 has two criteria. "All child features closed or deferred" is ticked: #90, #91, #92, #132, #133, #1384 and #1402 are all closed (REST read, 2026-11-21). The open criterion requires the scoped #440 checkpoint, with BRD/PRD and ADR reconciliation, relevant local regression, bug disposition, Azure-only residuals and any owner-approved pivot or defer decision.

## Requirement reconciliation

| Item | Observation | Class |
| --- | --- | --- |
| Issue source references | The issue cites BRD `FR-016` and `FR-017`. In the BRD those IDs are the automated-progression stop rule and the handoff content rule. The provider package and quality requirements the issue describes are PRD `FR-016` (versioned provider-package record) and PRD `FR-017` (independent per-measure quality disposition), which the PRD traceability table maps to BRD `FR-019` to `FR-022`, `FR-028` to `FR-030`, `RULE-008` and `RULE-013`. | Contradiction in the issue text, not in the code; flagged, no requirement changed |
| RULE-007 (no confirmed work without committed capacity) | BRD traceability: `FR-019`, `FR-020`, `AC-026`. Covered by `test_committed_capacity_needs_evidence_and_limits_work_orders`, `test_imported_numeric_capacity_is_not_evidenced` and `test_advance_without_evidenced_booked_order_is_refused`. | Local observed |
| RULE-008 (named authorised issuer; drafts are not instructions) | `AC-030`. Covered by `test_named_authority_is_not_a_role_or_caller_claim` and `test_work_order_lifecycle_versions_and_audit`. | Local observed |
| RULE-004 (contractor cannot approve quality) and RULE-013 (independent re-verification) | `AC-013`, `AC-044`. Covered by `test_never_auto_accepts_and_accepter_must_be_independent`, `test_installer_name_blocks_acceptance` and `test_quality_remediation_and_reinspection`. | Local observed |
| RULE-023 (leaseholder consultation before let or renewal) | `AC-073`. `tests.test_consultation_controls` passes. | Local observed |
| ADR intent | [ADR 0007](../../adrs/0007-contractor-intake-staff-mediated-proposal.md) keeps contractor intake staff-mediated; [ADR 0008](../../adrs/0008-single-external-demo-environment.md) sets the single external demo environment used for the live probe. Neither decision contradicts the delivered behaviour (text reading only). | Local observed |
| Provider channels, terms and real contracts | PRD open questions OQ-004, OQ-005 and OQ-007 remain open; the demo package contract reference is `SYNTHETIC-SOURCE-ONLY`. | Unknown (owner and supplier facts) |

## Local regression results

All runs used this worktree's `src` trees on `PYTHONPATH`; the editable installs resolve to the primary checkout.

| Suite | Result |
| --- | --- |
| `src/core`: `tests.test_quality_procurement` | 136 tests, OK |
| `src/core`: `test_consultation_controls`, `test_aftercare*`, `test_job_pack` | 205 tests, OK, 32 skipped |
| `src/api`: `test_procurement_api`, `test_procurement_screens`, `test_quality_decisions_ui`, `test_technical_quality_screens`, `test_capacity_browser_check`, `test_procurement_screen_wcag` | 91 tests, OK |

The 32 skips are the suites' own conditional skips; they are not counted as passes. Their cause was not investigated.

## Live read-only probe

Signed in to `ca-cutover-test-demo-api` as the employee test account (role Retrofit Programme Manager) with Playwright. Probe [live_probe.py](../../../.copilot-tracking/evidence/2026-11-21/issue-89-live-20261121T075609Z/live_probe.py), output [live_probe_output.json](../../../.copilot-tracking/evidence/2026-11-21/issue-89-live-20261121T075609Z/live_probe_output.json), desktop screenshot [capacity-screen.png](../../../.copilot-tracking/evidence/2026-11-21/issue-89-live-20261121T075609Z/capacity-screen.png).

| Observation | Class |
| --- | --- |
| `/api/packages` 200 with one package `PKG-SYN-001`, with period, contract reference `SYNTHETIC-SOURCE-ONLY`, scope version 1 and per-contractor `offered`, `committed`, `headroom`, `unevidenced` and `usable_committed` fields. | Azure observed |
| The first contractor shows 86 committed, 5 unevidenced and `usable_committed: 0` with the evidence status "Unknown - not confirmed: Legacy capacity is unverified". Unverified capacity therefore does not count as usable, which is the RULE-007 behaviour. | Azure observed |
| `/api/workorders` 200 with 601 synthetic work orders carrying `version`, `versions`, `issued_by`, `scope_version` and `state`. | Azure observed |
| `/api/checklists` 200; `/api/handoffs` 200. The `#/capacity` screen renders "Capacity and work orders", "Packages", "Record capacity", "Issue a work order" and "Work orders", with the text "A package is a draft, not an instruction. Creating it grants no contract authority." and "nothing is issued beyond a contractor's evidenced commitment" (screenshot). | Azure observed |

The probe did not issue a work order, record capacity or submit a quality decision on the demo: those writes would change shared demo data and the same paths are exercised by the local tests above.

## Bug disposition

* `gh issue list --label bug` could not be re-read because the GraphQL quota is exhausted for the account. The last recorded read, the [#440 third pass](./issue-440-live-criteria-verdict-2026-11-21-r3.md), shows no open bug label and #1837 as the only gating finding. That is an earlier observation, not a fresh one.
* No defect was found in the #89 delivery surface (packages, capacity, work orders, quality, consultation, aftercare), so no regression test or source change was added.
* Adjacent, not #89: the [#123 pass](./issue-123-live-criteria-verdict-2026-11-21.md) recorded that `/api/handoffs/unaccepted` returns 500 on the demo because four seeded handoffs have a timezone-less `offered_at`. `/api/handoffs` itself returned 200 here. It belongs to the handoff queue and stays with #123.

## Azure-only residuals

* Real contract, call-off and capacity commitment evidence from suppliers, which needs actual provider facts (OQ-004, OQ-005, OQ-007).
* A write-path run on the demo (issue a work order against committed capacity) is deferred; it is covered locally and would mutate shared demo data.
* Billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are excluded for the demo by the owner decisions of 2026-11-18, so they are not residuals here.

## Criterion verdicts

| Criterion | Verdict | Reason |
| --- | --- | --- |
| All child features closed or deferred | Already ticked | Re-read: all seven children closed. |
| Scoped #440 stabilization checkpoint | Evidenced for the demo; tick left to the owner | Reconciliation, local regression, live probe, bug disposition and residuals are recorded above. The criterion names an owner-approved pivot or defer decision and none is proposed. An earlier checkpoint record (2026-11-15) was restored to unticked on 2026-11-16 because merged children alone do not satisfy it, so this worker does not tick it. |

## Limits

* One worker and one in-loop review; no PR and no independent reviewer exist.
* The BRD and PRD were read at this head; their versions were not re-audited line by line.
* Credentials were read at runtime and never printed; email addresses were redacted in the page before the screenshot.
