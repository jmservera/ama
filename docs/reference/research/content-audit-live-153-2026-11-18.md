---
title: Content design and plain-language audit of the deployed demo screens, 2026-11-18 (issue 153, second live run)
description: Playwright audit of 43 captured staff and resident demo screens against the content standard, with redacted screenshots, a findings table and a per-criterion proven and unproven result
ms.date: 2026-11-18
ms.topic: reference
---

Refs #153. This run extends the [first live audit](plain-language-live-153-2026-11-18.md), which covered the 13 staff
navigation views and the resident page. It adds the case page and its eight tabs on three cases, four more staff
views and the full resident page text. Scope is the synthetic demo (the signed-in persona is a synthetic test user whose name is not hard-coded in the scripts), desktop only (1440 x 900). Owner decisions of
2026-11-18 apply: DPO and Legal approval, Azure billing reconciliation and person-run assistive-technology testing
are not needed for the demo.

## Method and evidence boundaries

* Targets: `ca-cutover-test-demo-api` and `ca-resident-demo` in resource group `ama`. Read-only: no case edited, no
  AI generation requested, no Azure resource created, so nothing needed deleting.
* Sign-in values were read at runtime from the owner's files and never printed. Session state was kept outside the
  repository (`~/.cache/ama153`, mode 700). The first state location in `/tmp` was removed by something else
  mid-run; the scripts now use the private directory.
* Redaction: before every screenshot and text capture, the script replaces the sign-in names and email addresses,
  any email, UK phone numbers and addresses that end in a postcode with `[redacted...]`. Check: the retained
  hit summary contains no sign-in value and no `@`. Not redacted: synthetic resident, officer and supplier names and
  the synthetic home names in tables (invented test data; some table addresses have no postcode so the pattern did
  not match them).
* Screenshots are viewport-only (not full page) and are labelled by file name: `staff-*` are staff app views,
  `staff-case-N-<tab>` are tabs of one case page, `resident-home` is the signed-in resident page. Raw page text was
  not retained (it holds synthetic personal-style data); only the banned-term hit lines are, in
  [screen-hit-summary.json](content-audit-live-153-2026-11-18/screen-hit-summary.json). Screenshots:
  [content-audit-live-153-2026-11-18/screens/](content-audit-live-153-2026-11-18/screens/). Scripts:
  [content-audit-live-153-2026-11-18/scripts/](content-audit-live-153-2026-11-18/scripts/).
* Banned-term pattern: gate, hold, provenance, trace, snapshot, envelope, human-approved, AI-drafted, pending,
  unassigned, advance, consent pending, hazard unresolved (word-boundary, case-insensitive) over the visible page
  text. Results the scan cannot show are labelled as such: it checks words, not meaning, tone or reading age.
* Retained versus not retained: screenshots, scripts and the hit summary are retained. The raw terminal output of
  the runs is not retained beyond this note.

## Coverage

43 screenshots (hit summary: 51 keys; the extra 8 keys, resident-status to resident-showcase-limits, are sections of the one resident page): 16 staff views (cases, all, overview, progress, visits, funding, finance, time, assistants, capacity,
aftercare, closed, law, handoffs waiting, import, specialist screens); for three cases (ZF-2025-0029, -0030,
-0031) the case page plus tabs Blockers and safety, Survey and assessment, Funding, Resident, Contractor and works,
Quality and handover, AI assistance and History (3 x 9 = 27 tabs, 26 retained: the case 3 Resident tab capture was byte-identical to the case 2 one, so the tab did not change and the duplicate was dropped; all tabs opened in the final run, checked on the case 1 AI tab
screenshot); and the resident page. Only case 3 (ZF-2025-0031) had AI proposals, so P2 and P3 come from it. The resident page is one scrolling document, so
its section links are anchors, not separate screens, and one capture holds all sections.

## Findings against the content standard

| Id | Surface | Observation | Standard section | Disposition |
| --- | --- | --- | --- | --- |
| N1 | Staff My cases list, Quality and handover tab | "Resident update: Unassigned, Unknown" and "Resident update owner: Unassigned; commitment: Unknown" (`app.js` lines 827, 1581). The standard says an owner is never shown as "unassigned" | Blocked and error messages (owner) | Open. Plain wording: "No owner named yet. Next action: ask the case lead to name one" |
| N2 | Staff All cases and Handoff lists | "Unassigned" in chase owner and receiver table cells (`app.js` lines 935 to 936) | Same | Open |
| N3 | Staff Finance | "Pause for human decision. Held. No person-approved envelope or tolerances are recorded." Contains "Held" and "envelope" (`exposure_limits.py` line 258) | Content standard (internal terms) and glossary (Envelope, hold) | Open. Suggest: "Payment paused for a person to decide. No approved limits are recorded yet." |
| N4 | Staff Resident tab, challenge text | "It never pauses, holds or extends the clock" (`challenges.py` line 165). Verb use of "holds", not the finance term | Glossary | Low; judgement call, a lexical match only |
| N5 | Staff AI assistance tab | "Release admission denied: no approved release matches (approved, unexpired release record). Owner: RAI task owner not appointed (OQ-017; ...)" names reason and owner but uses "Release admission", "RAI" and an open-question code with no explanation (`assistant_release.py` line 50). The first audit flagged the same class as F2 | Content standard (jargon abbreviations) | Open |
| N6 | Staff case pages | Many "Unknown" values in one line ("evidence: Unknown; version: Unknown; destination: Unknown") | Content standard (short, everyday words) | Open, low. Echoes first audit F1 |
| P1 | All 43 screenshots | No occurrence of provenance, trace, snapshot, human-approved, AI-drafted, pending, advance or consent pending | Core-flow audit | Holds for the scanned screens |
| P2 | Staff AI assistance tab | "AI suggestion, not approved. Not an instruction." and "Accepting or editing this proposal records a draft review. This is not an approval, consent or safety decision." | AI suggestion wording (SA-004) | Holds |
| P3 | Staff AI assistance tab | Refusal reads "Accept unavailable: request fresh evidence ... Owner: the reviewer. Next action: request fresh evidence, record your own source verification, then accept." Reason, owner and next action present | Blocked and error messages | Holds for this message |
| P4 | Staff case Overview | "Waiting on ... to agree access", "Next action: Ask the proposed receiver to accept or decline" and "Blockers: Resident decision or authority needs confirmation" use glossary wording | Glossary | Holds |
| P5 | Resident page | Plain status ("Contact is paused ... We will not contact you until the pause is lifted"), "Summary by rules. Not an instruction.", "Neither rules nor AI can make decisions, approve documents, book works, or give consent." and unknown file checks say "Ask staff to check it". Banner states review is outstanding | AI wording and Human review | Holds; the AI summary button was not pressed |

## Per-criterion result for issue 153

| Criterion | State on issue | Result for the demo |
| --- | --- | --- |
| Content standard and glossary exist | Ticked | Proven: [content standard](ux/content-standard.md) read; its glossary was the audit reference |
| Copy audit removes gate, hold, provenance and trace from the core flow | Ticked | Partly proven: none of gate, provenance, trace or snapshot on all captured screens; "Held", "envelope" and verb "holds" remain (N3, N4) |
| Error and blocked messages state reason, owner and next action | Ticked | Partly proven: P3 holds; N1, N2 and N5 show owner or next action missing or opaque in some messages; error bodies were covered by the first audit (its F3, F4) |
| AI suggestion text says "AI suggestion, not approved" | Ticked | Proven on the staff AI tab and the resident page (P2, P5) |
| Resident-facing wording is reviewed by a named human before any use | Unticked | Unproven and not provable by an automated run: a review record needs a named person, role, date, exact text and outcome. The resident page itself states that review is outstanding. The owner's demo decisions waive DPO and Legal approval, not this reviewer step; no review record exists in the repository |

The unticked criterion stays unticked.

## Evidence limits

* One role (Retrofit Programme Manager) and one resident were available. Other roles, the chat widget, error states
  needing a state change and the AI-generated summary were not exercised.
* Findings are wording defects in application text; no source was changed in this run.
