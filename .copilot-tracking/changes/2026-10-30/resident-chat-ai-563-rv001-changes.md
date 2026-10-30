---
title: Resident chat RV-001 changes
description: Implementation evidence for the issue 563 bounded follow-up
ms.date: 2026-10-30
---

## Execution State

Implement complete, P01/P02 reconciled; P03 Review/persistence next. Baseline 66924f3a; initially clean topic branch
feat/resident-chat-ai-563, no upstream branch or open PR. Parent original Review
is Complete / Not accepted and is not being edited or rerun.

## Approved Scope

User-selected RV-001: household repair admission, deterministic action/off-topic
and protected routes, external regression tests, resident suite and API tooling,
one independent follow-up Review, local commit only. No Azure or UI edits.
Plan/details are the corresponding resident-chat-ai-563-rv001 artifacts.

## Validation Intent

Reproduce the original five false positives, add protected and household-context
instruction/action negatives, retain dead-rat generated output and disabled
fallback. Assert no advisor method/reservation/token/transport for host routes.
Run resident discovery, ruff check/format and mypy per the API README.
Raw evidence stays outside the repository. Full publication gate follows commit.

## P01-T01: Host Admission and External Regressions

chat.py now requires household-linked repair observations or bounded
informational questions, rather than a repair keyword alone. Expanded host
instruction/action refusals run before ordinary topics; safety remains first.
Reporting/contact actions are refused, while questions about how residents can
report a repair or whom they should contact remain informational. Ambiguous
multi-clause/combined requests stay deterministic. README documents this
conservative lexical scope, not general language understanding.

Added two unit methods outside the package in test_resident_chat_api.py:
30 exact negative/protected route examples exercised over actual loopback HTTP,
with both advisor methods, reservation/completion, token and transport asserted
unused; ten generated repair positives exercise scripted transport and
accounting. Existing dead-rat own-case/disabled-fallback tests remain unchanged.

External evidence root:
/home/azureuser/.copilot/session-state/1f24faca-4dc1-4e9a-9431-c81211ada179/files/

* rv001-before.log reproduces 17 false-positive assertions before the fix.
* rv001-chat.log records an intermediate missing modifier in household matching:
  "my broken boiler" was conservatively refused. The local grammar was corrected
  without a scope/product decision.
* rv001-chat-final-bounded.log: all 22 chat tests pass after final source changes.
* Reused installed runtime from the parent session, with source/test paths
  pointing at this checkout. No install or shared runtime change was needed.

No model/consent/accounting/authority/UI changes, no Azure or actual inference.
Full resident discovery and API tooling are next; browser is not rerun for this
backend-only change. Original Review/critique are preserved.

## P02-T01: Final Validation and Review Readiness

* rv001-resident-suite.log: 149 tests run in 66.767s, 142 passed and seven
  existing opt-in skips (six local SQL accounting tests, one local browser
  integration test). These are not new skips or full SQL/browser acceptance.
* rv001-api-tooling.log: complete API ruff check passes; ruff format --check
  passes for 59 files; configured strict mypy passes for 113 source files.
* git diff --check passes. No UI/source browser rerun: backend-only correction.
* Plan P01/P02 and phase details reconciled. Exactly two new external unit
  methods, no removals, no product decision gap or expanded implementation.

Fresh read-only main fetch: f7482602ee8dd8e7eb36dc05426732a56aa982f7 is now an
ancestor of current HEAD. The parent recorded a historical ancestry failure;
do not carry it forward as a current blocker. Complete local gate still needs
a post-commit attempt. Authenticated GitHub account resolved to id 8036360,
login jmservera for subsequent repository-local noreply identity.

Follow-ups remain parent RV-002 actual-model/live owner activation, RV-003
human/content/AT approval and the complete publication gate. No push or Azure.
P03 independent follow-up Review and local persistence remain.

## P03-T01: Independent Review Outcome

Review executed once: Complete / Not accepted, recorded at
.copilot-tracking/reviews/logs/2026-10-30/resident-chat-ai-563-rv001-review.md.
It reproduced four comma/then continuations that escaped prefix matching,
including recognised email/call actions after informational prefixes.
The single-clause claim is not yet established. Preserve this complete adverse
record; do not overwrite it or run this Review again.

Route its RV-001 to a later implementation invocation for complete-request
matching within the user's original requested deterministic boundary. No
product decision or scope expansion is needed. This task's Review is finished;
local persistence remains shared with the routed implementation. Final code
after that later implementation must not be described as accepted by this
earlier Review.
