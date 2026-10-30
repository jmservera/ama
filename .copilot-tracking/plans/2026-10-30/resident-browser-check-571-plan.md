---
title: Resident browser check 571 implementation plan
description: Reconcile stale check inputs without changing bounded resident authority
ms.date: 2026-10-30
---

Task ID: 571. Slug: resident-browser-check-571. Status: completed, locally committed.

## Executive Summary

The resident check, not resident product routing, is stale. Use supported
everyday document/form questions, retain all document facts and authority
expectations, and check newly appended assistant replies rather than chat
history. Keep product code unchanged. Prove the check detects a later bad
document reply even when an earlier reply contains the expected facts.

## User Decisions and Requirements

* Complete research, plan, implement, review in order with dated evidence.
* Reproduce in a real local browser using documented startup.
* Preserve plain language, AI label rules and resident acceptance meaning.
* Validate check, resident units, Ruff and mypy. Full API units only with
  `flock -w 600 /tmp/ama-rpi-heavy.lock`.
* Commit locally with `Refs #571`; no push or closing keyword.
* No Azure, deployment, live sign-in or credentials.

## Sources

`.copilot-tracking/research/2026-10-30/resident-browser-check-571-research.md`,
C1-C8, W1. Original baseline log: `/tmp/ama-571-resident-baseline.log`.

## Goals

G1: passing meaningful browser check. G2: explicit supported/refused boundary.
G3: no false positives from earlier chat messages.

## Scope and Non-Goals

Only assistant browser harness, resident chat API tests and directly related
API guide; dated RPI artifacts. No resident runtime, grammar, templates, AI
enablement, stored data, historical review or unrelated UI changes.

## Functional Requirements

FR1: replace `documents help`, `forms help` and unsupported document-warning
paraphrase with complete recognised natural questions.
FR2: every topic/document expectation checks a newly appended assistant reply.
FR3: retain missing survey, secure upload guidance, unreadable page, mismatch,
unfinished file check, request/document source IDs, not-a-decision and no-send
limits, own-case isolation and truthful rules labels.
FR4: obsolete prompts explicitly refuse, with human help and no model access.

## Non-Functional Requirements

Use actual loopback fixture app and Chromium, digest-checked existing axe.
No new dependencies, product copy or generated artifacts. Existing style,
typing and test fixture conventions apply. Synthetic engineering evidence
does not establish human content/AT/live acceptance.

## Acceptance Criteria

AC1: baseline failure and grammar history identify stale check input.
AC2: complete assistant check passes with all prior consent, session, safety,
callback and accessibility assertions retained.
AC3: each supported document reply independently contains all FR3 evidence;
a seeded later refusal cannot pass using prior reply text.
AC4: resident units, Ruff check/format and mypy pass; optional full API units
are serialized under the exact required lock.
AC5: one critique and one independent Review retained; local Refs-only commit,
no publication. Required human acceptance remains unchecked.

## Test Ownership and Coverage Lock

Owner: API resident harness/test suite. Removals: none. Maximum additions:
one small typed browser submission helper and two focused test methods in
existing `test_resident_chat_api.py`; extend existing positive document test
where sufficient rather than adding duplicate tests. Canonical targets:
`src/api/checks/resident_assistant_browser_check.py`,
`src/api/tests/test_resident_chat_api.py`, `src/api/README.md`.
Generated targets: none. Semantic coverage: document facts/sources, labels,
consent/manual boundaries. Regression coverage: exact recognised prompts,
obsolete-prompt refusals and per-new-reply assertions. Negative browser probe:
in-memory patch makes the second supported document answer refuse, after the
first document response succeeds; require assertion failure. Preserve probe log.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and protect the resident check

<!-- rpi:task id=P01-T01 -->
* [x] Replace stale harness prompts and scope positive checks to fresh replies.
<!-- rpi:task id=P01-T02 -->
* [x] Add/extend HTTP units for supported questions and stale-prompt refusals.
<!-- rpi:task id=P01-T03 -->
* [x] Document rationale and run positive/negative browser and unit/static checks.

<!-- rpi:phase id=P02 -->
### [x] P02: Independent review and local delivery

<!-- rpi:task id=P02-T01 -->
* [x] Reconcile evidence; obtain one independent Review; route residual work.
<!-- rpi:task id=P02-T02 -->
* [x] Commit implementation and original dated RPI evidence locally, Refs-only.

## Critique Disposition

Executed once, original verdict Revise, one finding PC-001. Original path:
`.copilot-tracking/reviews/2026-10-30/resident-browser-check-571-critique.md`.

PC-001 disposition: rejected as inapplicable to this parent's execution
environment. The worker reports a no-`/tmp` file-operation restriction that is
not present in the parent's host instructions/tools. Parent already executed
and read the baseline in that location. Repository retention policy explicitly
prefers external scratch; user explicitly requires `/tmp/ama-rpi-heavy.lock`
for full API units. Applying worker-local restrictions to parent execution
would contradict that evidence and needlessly suppress authorized validation.
Retain original critique outcome unchanged; no second critique. Compatible
advice accepted: clearly distinguish parent-executed baseline from independent
review and preserve compact durable outcomes plus original external logs.
No significant unresolved product decision or implementation blocker remains.

## Follow-Up Items

No new out-of-scope implementation defect. Review RV-001 retains existing
human/live acceptance, owned by relevant acceptance owners; RV-002 retains
future publication gates, owned by release owner. Neither blocks this local
correction or authorizes additional live/remote action.

## Handoff

P01 implemented and validated after explicit disposition of the single
critique. P02 single Review executed, outcome Conformant within scoped
correction, no implementation defects; local implementation/evidence commit
`b8b958ef` completed with Refs-only message and required trailer. Final tracking
closeout is a separate metadata-only commit; no reviewed source changes.
Review:
`.copilot-tracking/reviews/logs/2026-10-30/resident-browser-check-571-review.md`.
Changes record:
`.copilot-tracking/changes/2026-10-30/resident-browser-check-571-changes.md`.
Compact original command-output evidence:
`.copilot-tracking/changes/2026-10-30/resident-browser-check-571-evidence.json`.
No full publication gate or remote action is needed for local-only delivery.
Complete local gate remains required before later publication under repository
policy; no partial validation is represented as that gate.
