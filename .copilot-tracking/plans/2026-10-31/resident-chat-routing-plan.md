---
title: Resident chat routing implementation plan
description: Bounded natural own-record routing with unchanged authority
ms.date: 2026-10-31
---

Task ID and slug: resident-chat-routing. Status: Ready for implementation.

## Executive Summary

Keep legacy exact matches and every specialist/exclusion check. Add a bounded
keyword/intent fallback for natural own-record questions and four plain-language
refusal examples. Fixed answers and optional AI configuration remain unchanged.
Focused validation covers the actual HTTP boundary and adversarial complete-message
regressions; no deployment or live acceptance is claimed.

## User Decisions and Requirements

* Recognize reported "How's my case going" and "Is my case blocked?" with AI off.
* Cover status/waiting/blocking/update/retrofit, documents/paperwork receipt or
  missing items, forms and home/address.
* Retain injection, cross-resident and action refusals, safety precedence,
  consent/appointments/regulations/repair routes and unknown refusal.
* Add three or four everyday example questions to unsupported-answer copy.
* Tests belong in existing `src/api/tests`; do not enable AI, deploy or use secrets.
* Use focused resident chat/app tests, Ruff lint/format and mypy, not heavy validation.
* Commit with requested co-author trailer, push without force and open a main PR
  using Refs #520 and Refs #563, never an issue-closing keyword.

## Goals

Residents can reach existing grounded rules answers through natural own-case
questions. Unsupported text still abstains with a housing-officer help route.

## Scope and Non-Goals

Canonical targets: `src/api/src/zava_forward/api/resident_demo/chat.py`,
`src/api/tests/test_resident_chat_api.py`, directly related API README and dated
RPI artifacts. Generated targets: none. No frontend files, activation configuration,
core answer changes, infrastructure, deployed services or dataset access.

## Functional Requirements

* Preserve legacy matches; fallback requires a complete allowed character envelope,
  bounded per-topic vocabulary, an own-record/receipt anchor and a question intent.
* Match one complete ordered intent grammar, not just token-set membership.
  Reject unknown words, markup, identifiers, mixed intents, repeated subjects,
  repeated question clauses and unrelated suffixes. No text may remain unconsumed.
  Do not rely exclusively on a forbidden-word blacklist.
* Existing safety/exclusion/specialist code continues before record classification.
* Refusal keeps task-limit source, no-action response and four supported examples.

## Non-Functional Requirements

Reuse `words`, `Topic` and existing `advise` answers. No dependency additions,
network/model calls or durable conversation storage. Keep typed interfaces.
Finite recognition is explicit, not universal natural-language understanding.

## Acceptance Criteria

* Both reported questions return exactly the same grounded answer/sources as
  explicit status, with rules labels, own-case isolation and no callback action.
* Natural questions in all four categories map to existing answers with AI off.
* Positive questions with adversarial suffixes, cross-resident/action/injection
  requests, markup and mixed topics refuse without provider or advisor work.
* Hazard and specialist routes retain existing response contracts.
* Unsupported response includes four actionable examples and a person-owned help path.
* Focused resident tests, Ruff lint/format, mypy and diff checks pass.

## Test Ownership and Validation Lock

Owner: API maintainer. Exact removals: none. Maximum additions: three HTTP/route
test methods in existing `test_resident_chat_api.py`, plus shared data matrices.
Semantic coverage: routing categories, fallback copy, no-AI own-case grounding.
Regression coverage: all legacy complete-message/refusal/specialist tests and
new natural-phrase suffix attacks.

From `src/api`:
`PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest test_resident_chat_api test_resident_demo_api test_resident_chat_agenda test_resident_assistant_api -q`.
Then `python3 -m ruff check .`, `python3 -m ruff format --check .`,
`python3 -m mypy`. Capture versions and all exits. Current installed versions:
Ruff 0.17.3, mypy 2.4.1; manifest pins 0.17.1 / 2.4.0. No dependencies missing.
Focused tier follows dated `src/README.md:63,309` policy; CI remains required.

## Phase Checklist

<!-- phase:P01 -->
### P01: Routing and copy

* [x] P01-T01: Implement bounded fallback after current exact matches.
* [x] P01-T02: Add useful refusal examples without weakening limits.

<!-- phase:P02 -->
### P02: Regression evidence and documentation

* [x] P02-T01: Add positive and adversarial HTTP tests; preserve existing matrix.
* [x] P02-T02: Document finite routing and execute focused validation.

<!-- phase:P03 -->
### P03: Independent Review and publication

* [x] P03-T01: Execute one independent post-implementation Review.
* [ ] P03-T02: Commit original evidence, recheck committed candidate, push and open PR.

## Dependencies and Evidence

P02 depends on P01. P03 depends on P02 and critique disposition.
Research: `.copilot-tracking/research/2026-10-31/resident-chat-routing-research.md`,
C1-C7. Baseline: 69 resident chat/demo tests passed before changes.
Reviewed base: `87bf629c630314f5be086697e322e1b0ec22277d`.

## Critique Disposition

Execution: Complete. Original verdict: Revise; retained unchanged in
`.copilot-tracking/plans/2026-10-31/resident-chat-routing-critique.md`.

* PC-001 applied directly: use ordered complete-message intent grammar and add
  allowed-vocabulary repeated-clause/anchor negatives for all four categories.
  Token sets alone are insufficient. This is within the confirmed safety scope.
* PC-002 applied directly: publication requires acceptable independent Review
  and no unresolved material acceptance findings. Nonblocking residuals may
  remain explicitly qualified. If independent reassessment is required, record
  a publication blocker rather than rerun Review or bypass its finding.

No significant/divergent owner decision and no second critique are required.

## Follow-Up Items

Named human review and live acceptance remain separate; #563 activation stays
owner-gated. They are not acceptance claims for this source-only fix.

## Handoff

P01/P02 complete; independent Review executed once, outcome Conformant, no
material blockers. Original critique Revise remains preserved. RV-001 is a
nonblocking human-copy/live-acceptance follow-up. Parent prepares the clean
committed candidate and performs P03-T02 publication with focused checks.
