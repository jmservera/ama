---
title: Rule Owner Actions Proven Live With a Second Identity (Issue 2204)
description: Approve, activate, hold, release and retire exercised live on the demo API by Alan Steiner as RuleOwner, why a RuleOwner-only identity cannot sign in, and the per-criterion result
author: AMA programme
ms.date: 2026-11-22
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: synthetic demo, desktop only, live Azure authorised (resource group `ama`,
cap USD 700, no drills, no Key Vault rotation, no production change). This note closes the gap left by the
[law store note](./issue-2204-rule-actions-law-store-live-2026-11-22.md), where a successful RuleOwner action was
unproven for want of a second identity. Evidence is in `.copilot-tracking/evidence/2026-11-22/issue-2204-alan-actions-live/`
(scripts `alan_probe.py` and `live_alan_actions.py`, machine record `live-alan-actions.json`, two screenshots with
emails masked). Credentials were read at run time and never printed or written.

## Blocker found and its cause

Alan Steiner held only `ZavaForward.RuleOwner`. Sign-in passed Entra with no MFA prompt (only the "Stay signed in"
page), Easy Auth redirected back, and `/api/me` then answered 401 "Please sign in." The cause is in
`src/api/src/zava_forward/api/auth.py`: capability roles are removed from the staff set and a principal with no mapped
staff role and no `ApplicationAdmin` is denied. A RuleOwner-only identity can never use the API. MFA is not the
blocker. Without a source change, the run gave Alan Programme Manager next to RuleOwner through Graph, and restored him
to RuleOwner only afterwards (verified through Graph).

## Run

The account that holds RuleAuthor (the main test account, Programme Manager plus RuleAuthor for the run) proposed the
exercise card `exercise-rules-alan-2204` naming Alan as approver. Alan then acted from the signed-in page with the CSRF
header. Both accounts were restored (test account Programme Manager only, Alan RuleOwner only) and verified.

| Actor and step | Result |
| --- | --- |
| Alan (RuleOwner and PM): GET cards | 200 |
| Alan: propose a card (wrong role) | 403 "A provisioned rule author or named owner capability is required." |
| Author account: propose naming Alan | 201, version 2, state `draft` |
| Author: approve own card, activate (wrong role) | 403 each |
| Alan: approve | 200, state `approved`, recorded role `rule_owner` |
| Alan: approve again | 409 "only a draft can be approved" |
| Alan: activate | 200, state `active` |
| Alan: hold | 200, state `held` |
| Alan: release | 200, state `active` |
| Alan: hold again, then retire | 200 each, final state `retired` |
| Alan: release after retire | 409 "only a held card can be released" |

The recorded event roles are `rule_author` for the draft and `rule_owner` for every later event. The distinct-owner rule
held: the author and the owner are different identities, and Alan matched the named approver.

## Observations

* Version 1 of the same card id also exists as an untouched `draft`. It was not created by the successful run; an earlier aborted attempt of this task (sign-in loop defect in the script, since fixed) is the only candidate, and its origin is not otherwise established.
* The card table is append-only, so both synthetic labelled exercise versions persist in the demo SQL database. No other throwaway resource was created.
* The email claim the API shows for Alan is a pseudonymous code, not a real address; screenshots mask it anyway.
* Approval is simulated and exercise only; it is not legal or operational approval (ADR 0005).

## Acceptance criteria

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Each role signs in and sees only its permitted views; admin sees all | Proven | [All-roles note](./issue-2204-all-roles-live-2026-11-22.md) covers the eight roles and the administrator, and the refused ones; this note adds RuleAuthor and RuleOwner actions live with a distinct owner |
| 2 | One wrong-role denial shown; no credentials printed or stored | Proven | 403 for RuleOwner propose and for the author approving and activating; literal scan of the evidence folder for both credentials found no match |
| 3 | Evidence recorded | Proven | This note, the evidence folder, the index, the log and the changes record |

The GitHub issue boxes are left for the owner to tick after merge, as repository practice requires.

## Follow-ups

* Decide whether a capability role alone should reach a minimal view; today a RuleOwner-only user is refused, which a sign-in review might not expect.
* Reconcile the stray draft version 1 only if the owner wants a clean card history (append-only table, so it would need a note, not deletion).
