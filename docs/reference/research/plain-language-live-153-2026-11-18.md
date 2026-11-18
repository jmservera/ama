---
title: Plain-language copy audit on the live demo, 2026-11-18 (issue 153)
description: Playwright audit of status names, errors and AI labels on the synthetic Azure demo against the content standard, with a per-criterion proven and unproven table
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and method

Docs and evidence only; no source or UI change. Desktop viewport 1440 x 900. Synthetic demo only (owner decisions
2026-11-18: no Azure billing reconciliation, no DPO/Legal approval and no person-run assistive-technology testing
are needed for the demo).

* Staff app: `ca-cutover-test-demo-api`, revision `ca-cutover-test-demo-api--0000031` (resource group `ama`).
* Resident app: `ca-resident-demo`, revision `ca-resident-demo--0000012`.
* Sign-in values were read at runtime by the scripts in
  [plain-language-live-153-2026-11-18/scripts/](plain-language-live-153-2026-11-18/scripts/) and are not stored.
* The staff SPA was driven by clicking all 13 navigation entries; visible text was scanned for the banned terms
  in [the content standard](ux/content-standard.md) (gate, hold, provenance, trace and similar), snake_case
  identifiers and AI wording. Read-only GET probes covered error bodies. No data was changed, no AI generation was
  triggered and no Azure resource was created, so nothing needed deleting.
* Raw output: `staff-audit.json`, `staff-spa-audit.json`, `staff-errors.json`, `resident-signed-in.json`,
  `resident-signed-in-text.txt` and 20 screenshots in `plain-language-live-153-2026-11-18/`.

Process incident: while checking the shape of the credential files, one command printed the file contents to the
session log by mistake. The values are not recorded in any repository file. The owner should treat the two demo
test-account passwords as exposed to that session log and rotate them if that matters for the demo.

## Findings against the content standard

| Id | Surface | Observation | Standard section | Disposition |
| --- | --- | --- | --- | --- |
| F1 | Staff My cases and All cases, queue item "Source" line | Shows `Source: case:ZF-2026-0742/measure_decisions; evidence: Unknown; version: Unknown` (snake_case record path, "Unknown" twice). Built at `app.js` line 841 from `work.source`, so the 2026-11-17 lexical guard could not see it | Core-flow audit, identifier leak audit | Open. New finding; needs a display mapping, not done here |
| F2 | Staff Aftercare concerns | AI pack line begins "Optional AI concern pack (FR-036): not active (unapproved)". A requirement code is person-visible | Glossary (internal terms) | Open. Source of text is dynamic data, not in the web files |
| F3 | Staff API errors | `Case not found.` (404) and `Your role does not include this.` (403) state the reason only. Neither names an owner or next action. An unknown `/api/...` path also answers with the role message, which misstates the cause | Blocked and error messages | Open; partial for criterion 3 |
| F4 | Staff unknown page | `/no-such-page-153` returns a 9-character plain body with no navigation or next step | Blocked and error messages | Open |
| F5 | Resident Documents and Case plan | "dMEV ventilation" and "EPC (D1)" are unexplained abbreviations | Glossary | Open, low |
| P1 | Staff scan, all 13 navigation views | No occurrence of gate, hold, provenance, trace, payload, stub, null, undefined or NaN | Core-flow audit | Holds on the live revision for these views |
| P2 | Staff Assistant proposals | "AI suggestion, not approved. Not an instruction." shown three times | AI suggestion wording (SA-004) | Holds |
| P3 | Staff Progress dashboard | "Accepted, Changed and Rejected describe draft review, not approval, consent or a safety decision" | AI suggestion wording | Holds |
| P4 | Staff home | AI choice reads "Allow AI suggestions" or "Use rules and templates, without AI"; rules text reads "Written by rules and templates. No AI was used." | AI suggestion wording | Holds |
| P5 | Resident signed-in page | No banned term or snake_case. Statuses are plain ("Contact is paused. We will not contact you until the pause is lifted"). Unknown file checks say "Ask staff to check it". Reviewed drafts say neither rules nor AI can approve or give consent | Core-flow audit, AI wording | Holds |
| P6 | Resident chrome | Synthetic banner states that Legal and Data Protection Officer review is outstanding, which is accurate for the demo | Human review | Holds |

Not covered: the AI-generated resident summary (button not pressed, to avoid an AI call), case detail pages, the
chat widget and error states that need a state change.

## Per-criterion result for issue 153

| Criterion | State on issue | Result |
| --- | --- | --- |
| Content standard and glossary exist | Ticked | Proven earlier; unchanged |
| Copy audit removes gate, hold, provenance, trace from the core flow | Ticked | Live scan of 13 staff views and the resident page found none (P1, P5). F1 and F2 show internal identifiers still reach dynamic text |
| Errors and blocked messages state reason, owner and next action | Ticked | Not proven universally: F3 and F4 give the reason only |
| AI suggestion text says "AI suggestion, not approved" | Ticked | Proven live on Assistant proposals (P2) |
| Resident-facing wording is reviewed by a named human before any use | Unticked | Unproven. The reviewer was appointed on 2026-10-15 (Juan Manuel Servera), but a review record (name, role, date, exact text, outcome) cannot be produced by an automated run, and ticking it would be an approval this run cannot give. Under the owner decisions, DPO/Legal approval is not needed for the demo, but the named wording review is a person action. The exact resident wording to review is in `resident-signed-in-text.txt` |

The unticked criterion stays unticked. Four ticked criteria were re-observed and two carry live caveats (F1 to F4).
