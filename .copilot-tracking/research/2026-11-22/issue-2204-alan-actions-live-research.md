---
title: Issue 2204 Alan Steiner rule actions live, research
description: Research record for proving approve, activate, hold, release and retire with a second RuleOwner identity
ms.date: 2026-11-22
---

## Task

Issue #2204 acceptance criteria are unticked: (1) each role signs in and sees only permitted views, admin sees all; (2) one wrong-role denial, no credentials printed or stored; (3) evidence recorded. The prior note
`docs/reference/research/issue-2204-rule-actions-law-store-live-2026-11-22.md` left a successful RuleOwner action unproven because no second MFA-registered identity existed. Alan Steiner now holds `ZavaForward.RuleOwner`.

## Disposition

Research disposition: executed (live). Planning Readiness: Ready. Findings are appended as the run proceeds.

## Findings

* Alan Steiner (Entra user, object id known to Graph) holds only `ZavaForward.RuleOwner`. A first Playwright sign-in with the stored credentials passed Entra (no MFA prompt, "Stay signed in" only), Easy Auth returned 302 from the callback, then `/api/me` answered 401 "Please sign in." (`alan_probe.py`).
* Cause from source: `auth.py` `authenticate` (about lines 142 to 145) removes capability roles from the staff set and denies a principal with no mapped staff role and no `ApplicationAdmin`. A RuleOwner-only identity can never sign in. MFA is not the blocker.
* Domain rules in `rulecards.py`: approve, activate, hold, release and retire need role RuleOwner and the actor must equal the card `approver` field; approve also needs an actor distinct from the author; activation needs the card within its effective dates and `activation_guard` clear; release needs state `held`.
* Plan without source change: give Alan Programme Manager next to RuleOwner for the run, author a new exercise card with the account that holds RuleAuthor and PM, naming Alan as approver, then run the five actions as Alan. Restore both identities afterwards.

Planning Readiness: Ready.
