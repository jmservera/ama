---
title: Issue 153 live content re-check, fourth run, 2026-11-18
description: Repeat Playwright and HTTP check of the deployed demo against the content standard with a proven and unproven result for each acceptance criterion
ms.date: 2026-11-18
ms.topic: reference
---

Refs #153. This run repeats the [third re-check](content-recheck-153-live-2026-11-18.md) with the same
[script](content-recheck-153-live-r4-2026-11-18/scripts/recheck.py) against the synthetic demo, desktop only
(1440 x 900). Owner decisions of 2026-11-18 apply: DPO and Legal approval, Azure billing reconciliation and
person-run assistive-technology testing are not needed for the demo. No source file changed and no Azure resource was
created, so nothing needed deleting. Staff app: `ca-cutover-test-demo-api`, revision `0000032`, image digest
`sha256:5368f4e4009cc32937377862e6d242c124005ed39081e1d9caa3b6b5dc17e5fb` (read with `az containerapp show`).

## Method

* Read-only: three page loads, one case tab, three API GETs, one empty POST. No case edited, no AI generation asked.
* Sign-in state came from the owner's files at runtime, was kept outside the repository and never printed. The script
  masks names and emails before each screenshot; `grep -c "@"` on the retained
  [results](content-recheck-153-live-r4-2026-11-18/recheck-results.json) returned 0.
* Four viewport screenshots were taken and then deleted because they showed home addresses and supplier rows. The word scan cannot judge
  meaning, tone or reading age.

## Observations

| Id | Probe | Observed | Result |
| --- | --- | --- | --- |
| R1 | Finance view | "Pause for human decision. Held. No person-approved envelope or tolerances are recorded." | `Held` and `envelope` still shown. The text is emitted by `src/core/src/zava_forward/core/exposure_limits.py:258` on main, so main has the same wording |
| R2 | Case, Quality and handover tab | "Resident update owner: Unassigned; commitment: Unknown. No message is sent automatically." | Owner shown as "Unassigned"; reason and next action not stated |
| R3 | All cases, Handoffs waiting | No banned term | Holds in this capture |
| R4 | `GET /api/cases/NO-SUCH-CASE` | 404 `Case not found.` | Reason only |
| R5 | `GET /api/no-such-route` | 403 `Your role does not include this.` | Reason only |
| R6 | Empty `POST` to a case resident route | 403, empty body | No message; cause not isolated (likely the cross-site request guard) |
| R7 | `GET /api/cases` without a session | 302 to sign-in | Redirect without text |

Result is unchanged from the third run: all seven observations match.

## Named reviewer record

A search of `docs/` and the issue thread found no record that names a person, role, date, exact text reviewed and
outcome. The [content standard](ux/content-standard.md) states the actual review of exact copy was not run and no use
is authorised. The owner's waivers do not cover a wording reviewer, and an automated run cannot supply one.

## Per-criterion result

| Criterion | Issue state | Demo result | Evidence |
| --- | --- | --- | --- |
| Content standard and glossary exist | Ticked | Proven | `ux/content-standard.md` present |
| Copy audit covers core flow and removes gate, hold, provenance, trace | Ticked | Partly proven: no banned term in All cases or Handoffs; `Held` and `envelope` remain on Finance | R1, R3 |
| Errors and blocked messages state reason, owner, next action | Ticked | Partly proven: generic API bodies give reason only; R2 shows "Unassigned" | R2, R4 to R6 |
| AI suggestion text says "AI suggestion, not approved" | Ticked | Proven in the [second audit](content-audit-live-153-2026-11-18.md) (P2, P5); no AI tab opened here | Second audit |
| Resident wording reviewed by a named human | Unticked | Unproven. Needs a named person's recorded review | Record search |

Production-only, not attempted: real-resident comprehension testing and live tenancy use of resident wording.
Fixing R1, R2 and the generic error bodies needs a source change and would take the FULL tier; it is outside this run.
Issue 153 stays open and no ticked box should be reversed on this evidence alone.
