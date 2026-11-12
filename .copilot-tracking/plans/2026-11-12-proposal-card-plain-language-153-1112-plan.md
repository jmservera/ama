---
title: Issue 153 proposal card plain-language default plan
ms.date: 2026-11-12
task_id: 153-proposal-card-1112
---

## Objective

Make the default assistant proposal card task-focused and plain, keep all technical evidence intact under one labelled native disclosure, and keep edit, verify, accept and reject behaviour unchanged. Details: [details](../details/2026-11-12-proposal-card-plain-language-153-1112-details.md).

## Phases

* [x] Phase 1: Restructure the technical evidence in `assistants.js` (one `details` with explanatory note, two labelled headings, focusable named `pre` blocks) and relabel the edit field.
* [x] Phase 2: Update directly coupled label expectations; add one static guard test and one served-browser regression (desktop 1280 px and 360 px).
* [x] Phase 3: Update the content-standard card note and the knowledge-base log.
* [x] Phase 4: Run focused checks, fetch guidelines and review changed web file, commit.

## Critique (author, prospective, one pass)

No independent critique agent was used; this is the author's own pre-implementation check and is recorded as such.

* Risk: hiding warnings in the disclosure. Disposition: only the two existing JSON records move; every warning, reason, unknown and review control stays outside (asserted by test).
* Risk: relabelling breaks recovery ("Earlier ..." labels). Disposition: updated all locators; browser check covers recovery.
* Risk: invented explanatory prose. Disposition: the disclosure note states only what is true of the card (technical record kept unchanged), with no inferred meanings.
* Risk: guard exemptions silently widened. Disposition: `ALLOWED` is not changed.

## Out of scope

Server and API changes, permission or approval changes, audit removal, resident wording acceptance, restyling, dependency changes, full gates.
