---
title: Issue 153 live content re-check and per-criterion audit, 2026-11-18 (third run)
description: Fresh Playwright and HTTP re-check of the deployed demo against the content standard, a search for a named-reviewer record, and a proven and unproven result per acceptance criterion
ms.date: 2026-11-18
ms.topic: reference
---

Refs #153. This run follows the [second live audit](content-audit-live-153-2026-11-18.md) and the
[content standard](ux/content-standard.md). Scope is the synthetic demo, desktop only (1440 x 900). Owner decisions of
2026-11-18 apply: DPO and Legal approval, Azure billing reconciliation and person-run assistive-technology testing
are not needed for the demo. No source file was changed and no Azure resource was created, so nothing needed deleting.

## Method and evidence boundaries

* Targets: `ca-cutover-test-demo-api` in resource group `ama` (staff app and API). Read-only: three GET probes, one
  empty POST and one unauthenticated GET; no case edited, no AI generation requested.
* Sign-in state came from the owner's files at runtime, was stored outside the repository (`~/.cache/ama153`, mode 700)
  and was never printed. The script masks sign-in names and any email before each screenshot and capture. Check: the
  retained [results](content-recheck-153-live-2026-11-18/recheck-results.json) contains no `@`.
* Retained: [script](content-recheck-153-live-2026-11-18/scripts/recheck.py), the results file and four viewport
  [screenshots](content-recheck-153-live-2026-11-18/screens/) (All cases, Finance, Handoffs waiting, one case
  Quality and handover tab). Raw page text is not retained; only banned-term lines are.
* The scan matches words (gate, hold, held, provenance, trace, snapshot, envelope, human-approved, AI-drafted,
  pending, unassigned, consent pending, hazard unresolved). It cannot judge meaning, tone or reading age.

## Results

| Id | Probe | Observed | Standard check | Result |
| --- | --- | --- | --- | --- |
| R1 | Staff Finance view | "Pause for human decision. Held. No person-approved envelope or tolerances are recorded." | Internal terms (hold, envelope) | Still live; matches earlier N3 |
| R2 | Staff case, Quality and handover tab | "Resident update owner: Unassigned; commitment: Unknown." | Owner never shown as unassigned | Still live; matches earlier N1 |
| R3 | Staff All cases and Handoffs waiting | No banned term in either view | Core-flow audit | Holds in this capture. Earlier N2 ("Unassigned" table cells) appears only for rows with no receiver, so absence here is not proof it is fixed |
| R4 | API `GET /api/cases/NO-SUCH-CASE` (signed in) | 404, body `Case not found.` | Reason, owner, next action | Reason only; no owner or next action |
| R5 | API `GET /api/no-such-route` (signed in) | 403, body `Your role does not include this.` | Reason, owner, next action | Reason only; no owner or next action |
| R6 | API empty `POST /api/cases/{id}/resident` | 403, empty body | Reason, owner, next action | No message at all; likely the cross-site request guard, which the probe did not isolate |
| R7 | API `GET /api/cases` without a session | 302 redirect to sign-in | Blocked message | Redirect, no text; acceptable for a browser, unproven for API clients |

## Named human review record search

A search of `docs/` for a resident wording review record found only the
[content standard](ux/content-standard.md) line "Reviewer appointed below; actual review of exact copy Not run. No use
authorized" and mentions in the knowledge-base log. No record names a person, role, date, exact text reviewed and
outcome. The owner's demo decisions waive DPO and Legal approval and assistive-technology testing; none of them waives
or satisfies a named wording reviewer. An automated run cannot create that record, so the criterion stays unproven.

## Per-criterion result for issue 153

| Criterion | State on issue | Result for the demo | Evidence |
| --- | --- | --- | --- |
| Content standard and glossary of status and next-action wording exists | Ticked | Proven | Standard read at `ux/content-standard.md`; its glossary was the check reference |
| Copy audit covers the core flow and removes gate, hold, provenance and trace | Ticked | Partly proven. Gate, provenance, trace: none on the captured views. Hold and envelope: still shown on Finance (R1) | R1, R3 |
| Error and blocked messages state reason, owner and next action | Ticked | Partly proven. Typed refusals in the second audit (P3) do; generic 404 and 403 bodies give a reason only (R4, R5); R2 shows an owner "Unassigned" | R2, R4 to R6 |
| AI suggestion text says "AI suggestion, not approved"; drafts do not imply approval, consent or safety decisions | Ticked | Proven in the second audit (staff AI tab P2, resident page P5); not re-captured here because this run did not open an AI tab | Second audit |
| Resident-facing wording is reviewed by a named human before any use | Unticked | Unproven. Needs a named person's recorded review; none exists | Record search above |

Production-only or waived items, kept separate: DPO and Legal approval, person-run assistive-technology testing and
Azure billing reconciliation (waived for the demo by the owner); real-resident comprehension testing and use of
resident wording in a live tenancy programme (production only, not attempted).

Unmet for the demo: the unticked criterion, plus the partial results above on the three ticked criteria. Fixing R1,
R2 and the generic error bodies needs a source change, which is outside this audit run and would take the FULL tier.
The issue should stay open and the ticked boxes should not be reversed on this evidence alone.
