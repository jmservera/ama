---
title: Proper Warm PRD v0.7.0 Challenge Disposition
description: Independent draft-stage challenge, author amendments and bounded follow-up provenance
ms.date: 2026-10-06
ms.topic: reference
---

## Scope and provenance

The owner requested incorporation of the nine-company-role/eleven-profile UX
review into the existing PRD, followed by an independent challenge. The PRD
Quality Reviewer challenged draft v0.7.0. This is Build-phase design research,
not approval, user validation or a new prototype review.

The initial challenge returned prose without paired quality payloads after
failing to locate its schemas. A narrower follow-up was supplied the installed
schema paths and returned payloads inline. Agent
`d31602c2-42eb-42e3-990e-ab0b62de1acd` assessed the amendments at
`2026-10-06T09:38:50Z`, then confirmed the two residual corrections at
`2026-10-06T09:42:49Z`. The final payloads are preserved verbatim in
[standard-findings.yaml](./standard-findings.yaml) and
[quality-report.yaml](./quality-report.yaml).

## Challenge and author disposition

The initial findings below are paraphrased, not a fabricated machine report.

| Challenged gap | Amendment and disposition |
| --- | --- |
| Slice acceptance applied connected checks to a correctness-only iteration | AC-043 and its subchecks now distinguish Slice A orientation, Slice B exception/shared-building and Slice C same-home events; deferred labels never pass full MVP coverage. Follow-up covered. |
| Conflict example could hide the actual conflicting inputs | AC-040 requires two distinct constructed values with source/date/version; authority/resolution/eligibility may remain unknown. Follow-up covered. |
| Reset/selection checks lacked a complete expected-result oracle | Explicit scope precedence, search retention, reset, selection and focus rules added. First follow-up still found non-exhaustive per-profile defaults; the eleven-row baseline fixture manifest v1 now defines IDs, counts, order and reset selection. Final follow-up covered. |
| Compressed traceability obscured exact FR-to-AC correspondence | Exact 35-row matrix added and reciprocal links reconciled, including AC-010/FR-008 and FR-009/AC-008. Follow-up covered. |
| Only unknown receipt/acceptance states were represented | Slice B requires distinct received-but-unaccepted and explicitly accepted snapshots with independent evidence and retained/explicitly transferred chase ownership. Follow-up covered. |
| Composite acceptance criteria could hide partial failure | Separately reportable AC-040, AC-042 and AC-043 checks added, including stock conflict, case rationale, quality, invoice inputs and applicable connected paths. Follow-up covered. |
| Constraints mixed imposing boundaries and design choices | Constraint categories/imposing sources added; proposed hybrid remains DD-001, not a production mandate. Follow-up covered. |
| Reflow wording lacked test widths and a pass condition | Proposed NFR-001 checks now specify 320/390/1280 CSS pixels and 200% text zoom, no lost/clipped content or page-level horizontal overflow, with a labelled/focusable 2D table-scroll exception. Final follow-up covered. |

An initial observation about missing FR-022 narrative-history coverage was
stale: the existing FR-022 already covered historical flow; new criteria deepen
the explicit same-home event fixture contract rather than inventing a new gap.

## Limits and unresolved gates

The first follow-up reported RISK/FAIL with one HIGH defaults finding and one
MEDIUM reflow caution. Its NIST presence rollup incorrectly marked several
existing NFR categories absent; the reviewer corrected these in the final
payload, distinguishing category presence from TBD thresholds.

The final report's PASS applies only to the two amended paragraphs. The six
other amendment dispositions come from the earlier bounded follow-up.
The final empty SMART partition and its 100% rate do not mean the four goals
passed SMART assessment. No fresh full-PRD approval is inferred. Scalability
and elasticity, quantitative thresholds, SMART timing and company validation
remain discovery/build matters; no unsupported production targets were added.

Formal Validate remains BLOCKED pending signed/current upstream BRD handoff
and quality evidence, named product/control owners and required human review.
Finalize is NOT_EVALUATED. The PRD remains draft v0.7.0 in Build.

The existing HTML prototype is unchanged. This PRD defines a subsequent
constructed-data prototype generation contract, not implemented behavior,
operational authority, accessibility conformance or company policy.
