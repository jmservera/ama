---
title: Issue 132 delivery-channel and identity decision record details
ms.date: 2026-11-11
task_id: issue-132-channel-decision-1111
---

## Phase 1: ADR 0007 in-place amendment

Target: `docs/adrs/0007-contractor-intake-staff-mediated-proposal.md`. Keep the file name and title.

1. Frontmatter: `description` becomes "Proposed decision to deliver contractor job packs and field evidence as a staff-mediated intake rather than a provider portal; owner-directed for the synthetic demonstrator only, production identity and provider portal remain unresolved (Refs #132)". `ms.date` is the edit date.
2. `## Status`: keep "Proposed on 2026-11-04". Replace "Not accepted. This record does not close criterion 6 of issue #132: the owner has not decided, and the provider identity model in #116 is open." with: "Proposed for production use. Owner-directed for the synthetic demonstrator only on 2026-11-09 (see Owner Direction below). This does not accept the ADR as a whole, a provider portal or any production identity arrangement, does not resolve #116 and does not tick any criterion of issue #132." Preserve the original sentence in an "Earlier status (2026-11-04)" line so the change is visible.
3. `## Context`: leave bullets; append to the last bullet "Answered for the synthetic demonstrator on 2026-11-09; see Owner Direction." Mark the "Not delivered" bullet as the 2026-11-04 snapshot
4. New section after `## Proposed decision`, headed `## Owner Direction for the Synthetic Demonstrator (2026-11-09, Refs #132)`. Required content, in this order:
   * Status label: "Owner-directed for the synthetic demonstrator only."
   * The complete verbatim text of comment 6753054374 (code block in the research artifact; quote it whole, with no omission or ellipsis), id, URL, 2026-11-09T22:22:47Z, and the provenance sentence. Compare it byte for byte with a fresh read-only `gh api` read.
   * Decision: the staff-mediated route (ADR option A in substance) is owner-directed for the synthetic demonstrator; the comment does not adopt the ADR text verbatim, so do not call it formal acceptance of option A. Identity: existing authenticated staff only; staff identity authority is the ADR 0002 owner decision (2026-10-24), bounded, with its external release gates still open; a contractor is a named person in the record and not a signed-in actor.
   * Current implementation (evidence, not approval): `src/api/src/zava_forward/api/auth.py` modes `password` (development, refused in production) and `trusted-proxy`; `src/core/src/zava_forward/core/staff_intake.py` refuses the Contractor role and records the worker as a named person; link the core README staff intake section. State that the `ZavaForward.Contractor` role label and fixture logins are not a contractor identity model and do not authenticate actual workers.
   * Not authorized or decided: provider portal, contractor identity or B2B guest, new accounts or permissions, public access, provider send, contract instruction, resident consent, live or production acceptance, any real-company Legal, Compliance, DPO or identity-owner approval.
5. `## Owner decisions needed`: two lists, "Owner-directed for the synthetic demonstrator" (the staff-mediated route and the authorised staff-only slice; cite the comment; no claim of formal option acceptance) and "Still open" (option B deferral for production and owner of #116; real worker identity and its approvals; named variation and escalation owner under the separate criterion).
6. `## Next stacked slices once accepted`: mark as the 2026-11-04 snapshot and add the single dated clause described in the plan, only after confirming PR numbers and scope with `git log`; separate the delivered intake from the still-undelivered escalation write path; no claim of accessibility or live acceptance.

## Phase 2: Index and log

* `docs/reference/README.md`: add the one task-table row described in the plan, matching the surrounding three-column format and using a relative link with the anchor `#owner-direction-for-the-synthetic-demonstrator-2026-11-09-refs-132`.
* `docs/reference/log.md`: append `## [YYYY-MM-DD] update | Staff-mediated contractor intake decision recorded for the synthetic demonstrator (Refs #132)` with bullets: what changed, source (comment 6753054374, ADR 0002 and 0005 precedent), evidence class documentation only, non-claims (no tick, no closure, no portal, no identity or production approval, ADR stays Proposed), tracking pointers.

## Phase 3: Validation

Read-only review: anchors resolve (heading text slugs), links relative and valid, quote is byte-identical to the comment text, ASCII punctuation, no em dashes, `git diff --stat` shows exactly three files. Docs-only tier; no runtime gate.

## Stop conditions

* Stop and return the focused question if the owner or Root requires a named #116 owner or a production-scope decision to treat the record as sufficient.
* Stop if any wording would imply ADR-wide acceptance, a tick, portal approval or real-worker authentication; revise instead.
* Stop if a selected identity architecture or new ADR becomes necessary; name the decision, do not broaden scope.
