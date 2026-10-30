<!-- markdownlint-disable-file -->
# RPI Phase Details: Resident generated answers

Task ID: issue-563. Slug: resident-chat-ai-563. Date: 2026-10-30.
Plan: .copilot-tracking/plans/2026-10-30/resident-chat-ai-563-plan.md
Evidence: .copilot-tracking/research/2026-10-30/resident-chat-ai-563-research.md

## Phase Index

| Phase | Name | Status |
| --- | --- | --- |
| P01 | Implement generation | Complete |
| P02 | Local validation | Complete |
| P03 | Review/local persistence | Review Complete / Not accepted; persistence pending |

<!-- rpi:phase id=P01 -->
## P01: Implement grounded resident generation
<!-- rpi:task id=P01-T01 -->
### P01-T01: Routing, model contract, UI copy and regression coverage

Research C2-C4 proves both routing and provider capability need changes.
Add a repair category after protected routes, before unrelated refusal; unknown
non-housing text stays refused. Extend the existing Advisor protocol with a
generated-question method. Build a minimal source map from the host-owned answer
and own progress/next step, plus generic reporting guidance for repairs.
Keep facts labelled as recorded, not an assessment of the reported smell.
The model must not diagnose, assert safety, promise attendance or invent history.
Use a strict answer/source-ID object, validate shape, limits, usage and citations,
and return host-approved source descriptions, not model URLs.

Reuse accounting/transport for both model paths. Preserve mandatory fixed-topic
facts and tests. Log only outcome codes/counts. Fallback must include a reason
and human help; host-owned inability/advisory notice remains visible.
No source activation, expiry/tariff or SQL changes.

Resident checkbox must disclose that the question and limited own-case data may
reach AI when enabled; remove contradictory "typed text never reaches AI".
Thin label says AI-generated, with "not approved"/may-be-incorrect detail.
Use existing escaped-text/shared-native-details mechanism and tokens.

Completion: code plus provider/HTTP regressions and API guide updated together.
Test ownership/removals/budget are locked in the parent plan.
Completion evidence: generated-question protocol, shared accounted request,
repair routing, resident disclosure/label and eight new unit methods authored;
one new local browser check. Existing shared-widget rat-refusal assertion now
expects explicit disabled-AI repair fallback, an immediately relevant regression
update rather than unrelated UI change. No test removed.

<!-- rpi:phase id=P02 -->
## P02: Local validation
<!-- rpi:task id=P02-T01 -->
### P02-T01: Unit, lint, types and local browser

Run API units from src/api with
PYTHONPATH=../core/src:../agents/src:../core/tests:../agents/tests and installed
editable API. Use discovery patterns for relevant resident suites and tests
path when invoking named suites/check modules. Run API ruff check/format and
mypy, plus affected core checks and node syntax.

Browser check starts real ResidentDemo on an ephemeral loopback port using only
constructed test rows/password and scripted Azure transport. Block external
requests. Prove no request/model before consent, then actual HTTP generated
reply; inspect prompt for question/own sources and exclusion of other cases.
Assert no raw HTML execution, source details initially closed and keyboard
operable, thin metadata typography, 1280/390/320 reflow, unavailable fallback
and consent withdrawal. Store screenshots/results outside checkout.
Do not call the model or use credentials. Record unperformed AT/live proof.
Completed: 147 resident API tests (140 passed, seven existing opt-in SQL skips);
six core advisor tests; API Ruff/format and full mypy (113 files); focused core
Ruff/format/mypy; JS syntax. Three actual-loopback Chromium checks passed:
generated-answer, shared widget with pinned axe, resident assistant/callback
with pinned axe. AT, actual model and authenticated live acceptance not run.

<!-- rpi:phase id=P03 -->
## P03: Review and local persistence
<!-- rpi:task id=P03-T01 -->
### P03-T01: One independent Review and local commit

Fresh review worker assesses exact diff/evidence using rpi-review, writes original
review only, and reports material findings. Refresh Web Interface Guidelines
before changed-UI assessment. No repeat Review or same-task repair loop.
Resolve authenticated GitHub ID/login noreply identity, use repo-local config,
commit source and dated evidence with Copilot trailer and Refs #563 only.
Attempt the repository full local gate externally after commit; do not queue
behind another user's heavy gate or change shared infrastructure. Missing
prerequisites remain publication blockers. Never push or deploy.
