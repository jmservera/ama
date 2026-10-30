<!-- markdownlint-disable-file -->
# RPI Plan: Resident generated answers

## Task Metadata

Task ID: issue-563. Slug: resident-chat-ai-563. Date: 2026-10-30.
Status: P01/P02 executed; original independent Review Complete / Not accepted.
Details: .copilot-tracking/details/2026-10-30/resident-chat-ai-563-phase-details.md
Critique: .copilot-tracking/reviews/plans/2026-10-30/resident-chat-ai-563-plan-critique.md

## Executive Summary

Repair the source routing that prevents consented housing questions from using
AI, and add generated grounded prose rather than merely choosing template IDs.
Preserve the fixed-topic API, deterministic protected routes and human authority.
Use the existing compact widget label and collapsed sources, not a redesign.
Local behavior and validation are delivered, but Review found overbroad repair
admission (RV-001). That defect is routed to later implementation; this is not
accepted whole-issue delivery.

### What You May Not Know

AI activation alone cannot fix this defect. The default remains off, the
deployment template supplies no activation, and the tariff expires November 1.
Local scripted-model evidence is not actual-model or authenticated live proof.
No live setting, approval or deployment will be changed.

## User Decisions and Requirements

* Full dated Research, Plan, Implement and independent Review.
* Read #563 and #562/sibling live evidence; find and fix the source cause.
* Relevant grounded AI answers, thin AI-generated label, collapsed sources.
* Consent first; honest inability, human contact and explicit fallback retained.
* Use src/, no new mvp/ feature code, tests outside packages.
* Relevant API units with caller PYTHONPATH, ruff, mypy and actual local Playwright.
* Local commit with Copilot trailer, Refs #563 only, no push or Azure operations.

## Goals

* Make an enabled consented repair question reach generated inference.
* Make generation, rules and unavailable states distinguishable and recoverable.

## Scope and Non-Goals

API advisor, core protocol, host routing, resident consent/copy/label and tests.
No new service, model memory, raw question logging, authority extension, default
activation, deployment, paid inference, real data or whole-issue acceptance.

## Functional Requirements

* In-scope typed case/document/form/home/repair questions use a generated-answer
  method; fixed-topic API retains its bounded sentence-selection behavior.
* Host-owned safety, legal, consent, appointments, action/injection and unrelated
  refusals remain deterministic, ahead of repair routing.
* Model gets only the current question and minimum own-case answer/progress plus
  approved repair-reporting guidance, never email, case selector or other records.
* Require bounded nonempty prose and a valid nonempty subset of supplied source
  IDs. Render plain text only; append host-owned inability/advisory/human limits.
* Disabled/unavailable/budget/expiry/invalid output uses explicit rules fallback.

## Non-Functional Requirements

* Existing <=4096-byte prompt/reply, <=256 output tokens, five-second transport,
  precommitted SQL reservation, lifetime/hourly caps and no retries remain.
* Exact boolean consent before data/model lookup; bind session and reauthorize
  after inference; no browser storage or model conversation memory.
* Native details, polite log, keyboard focus, reduced motion and wrap retained.
* Thin AI-generated label uses existing meta typography; unapproved/incorrect
  advisory detail stays visible, no hover-only critical disclosure.

## Acceptance Criteria

* HTTP repair question reaches scripted Azure transport with own-case grounding;
  its generated text (not a canned summary) renders with valid sources.
* Missing/false/string consent performs no read/reservation/token/model call.
* Safety/injection/out-of-scope do not call generated inference.
* Unavailable, cap, expired, malformed/truncated/unknown-source replies visibly
  fall back with housing-officer help; revocation discards a late response.
* Local browser proves consent ordering, label geometry, collapsed/open sources,
  escaping, narrow reflow and unavailable state. This is not live-model proof.

## Sources

Research: .copilot-tracking/research/2026-10-30/resident-chat-ai-563-research.md
(C2-C9, W1-W2), plus caller #563/#562 evidence.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement grounded resident generation
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Routing, model contract, UI copy and regression coverage

Dependencies: completed research and one critique. Details own exact boundaries.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and preserve evidence
<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Unit, lint, types and local browser

Depends on P01-T01. Save sanitized results externally and summarize in changes.

<!-- rpi:phase id=P03 -->
### [ ] P03: Review and local persistence
<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: One independent Review and local commit

Depends on P02-T01. Preserve original critique and Review; route findings to
later work, do not repeat Review. Local-only commit; full gate attempt after
commit as required by repository guidance, no publication.

## Test Ownership and Change Budget

Canonical code: src/core/src/zava_forward/core/resident_assistant.py and
src/api/src/zava_forward/api/resident_demo/{app,chat,aoai}.py.
UI canonical target: resident_demo/web/assistant.js; shared widget stays unless
browser evidence demonstrates a tightly coupled need. Generated targets: none.
Tests: src/api/tests/test_resident_{chat_api,aoai}.py; at most one new browser
check under src/api/checks and at most 18 new unit test methods. Removals: none;
update old "never AI for rat" regression to reflect the intentional feature.
Semantic checks: grounded free-text schema/request/output and refusal routing.
Regression checks: existing fixed topics, consent/isolation/expiry/budget and
shared widget behavior. Never substitute canned local output for live proof.

## Dependencies

Task-owned installed source distributions/dev tooling, local Chromium.
Live activation needs existing managed identity, SQL procedures and renewed
review if the existing tariff expires. Those are owner gates, not local blockers.

## Critique Disposition

Executed once, Pass, no findings.
Original: .copilot-tracking/reviews/plans/2026-10-30/resident-chat-ai-563-plan-critique.md.

## Follow-Up Items

* RV-001 Medium: later rpi-implement must constrain housing admission and retain
  host-owned refusal for unrelated repair words and report/contact actions.
  Original Review reproduces five negative examples; no current-task repair
  or repeat Review is authorized by the one-pass lifecycle.
* Owner: separately enable/review deployment settings and prove actual-model
  relevance with authenticated live Playwright. Outside local-only scope.
* Human resident/content and assistive-technology approval remain separate.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-30/resident-chat-ai-563-changes.md.
P01/P02 complete and reconciled; original Review Complete / Not accepted.
P03 local persistence/full-gate attempt remains. No product decision gap;
RV-001 is a later implementation defect, not completed acceptance.
