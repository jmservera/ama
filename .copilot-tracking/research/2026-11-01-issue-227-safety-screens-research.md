# Research: issue 227 building safety lead and repairs hazard screens (2026-11-01)

Task: issue-227-safety-screens. Disposition: executed (focused). Planning Readiness: Ready.

## Evidence

* Host `src/api/src/zava_forward/api/web/role-screens.js` (merged for #226) renders `#/screens` with a bounded permitted-case queue (flagging "Safety issue open"), explicit home selection, no writes, and `registerRoleScreen({id,title,roles,load,render})`. Helpers `screenPanel`, `screenFields`, `screenTable`, `screenUnknown` give design-system card, dl and table-scroll patterns.
* Case detail (`store.py` ~390) projects `hazards` through `workflows.hazard_view`: `category`, `priority`, `aware_at`, `source`, `sent_at`, `received_at`, `accepted_at`, `destination`, `sender`, `follow_up`, `state` (Raised, Sent, Received, Accepted, Repair evidenced hold active, Retrofit hold released, Legacy referral), `response_due_at`, `responded_at`, `hold` (scope, status, accountable_role, decision {at, actor, reason, evidence}), `classification` ("Unverified report; service categorisation not recorded here").
* Authority: `release_hazard` requires an authorised human, receipt, acceptance and external repair evidence; the screen must only display this evidence. Clocks are set by the external service; awareness time is a recorded report time.
* Roles: `SAFETY_ROLES` = Building Safety Liaison plus the two manager roles. Triage staff are `Retrofit Coordinator`, `Resident Liaison Officer`, `Quality Inspector` (staff roles that can raise and refer).
* Journeys (`customer-journeys/safety.md`): sender chases until acceptance (EXA-008 fictional 24/48/72h fixtures, not statutory); receipt is not acceptance; no AI classification; SA-007 never hide hazard items.
* Evidence is desk-based hypothesis, not observed behaviour; validation is #155.

## Decisions

* Register two read-only screens: `safety-lead` ("Building safety referral queue", safety roles) and `hazard-triage` ("Repairs and hazard triage", triage staff), sharing one referral table renderer.
* Per selected home show every hazard (never filtered), with awareness time and source, destination, separate sent, received and accepted columns, textual state, named follow-up owner when receipt or acceptance is pending, and scoped hold with release decision evidence.
* No controls; boundary text states the screen does not classify, set clocks, close hazards or authorise work.

## Not in scope

Cross-home referral queue (needs portfolio endpoint), server changes, browser/axe run locally, observed validation (#155).
