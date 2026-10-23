---
title: Issue 350 feedback checker correction 5 research
description: Focused research into non-finite exponent and boolean schema-version findings
ms.date: 2026-10-23
---
<!-- markdownlint-disable-file -->

## Research Brief

Correct the two owner-supplied P2 findings in the offline checker only.
Audience: implementation/review coordinator. Output mode: convergence.
Resolved research root: `.copilot-tracking/research/2026-10-23/`.
Research posture: focused, selected from the bounded named findings.
Questions: how does decoded JSON admit exponent overflow; how does bool
equal the supported schema integer; what existing tests and plan boundaries
must be preserved?

## Research Parameters and Direction Controls

Work only in the specified worktree on `test/deployed-feedback-harness-350`.
Initial HEAD `e55bcd835c414cf55e57d2b49119cd24a30fff92`, base
`140d8f494482c78e84d15f3d46b9223d3c487af0`; clean intake verified.
PR #436 is open/draft; issue #350 is open. Supplied earlier exact-head receipt
SHA-256 `1b01ea5d797af7d12981bdf6f0122e6dfabd765940982f8d5ba579b64c85f1cc`
is historical after any correction. No reuse as a new-head gate.
Do not change acceptance criteria, deploy, push, amend, merge or close issues.
Stop after local tests, RPI review and a new local commit; coordinator owns
full gate and independent exact-head assessment before publication.

## Extension Registry and Participation

Repository instructions and RPI skills selected for evidence and lifecycle.
No web, accessibility or regulatory extension applies to this backend-only
JSON correction. No specialist research delegation: one small continuous
trace is better examined directly. No interaction needed: owner supplied
scope, branch, stop boundary and desired behavior.

## Research Cycle Log

Cycle 1 opening: Wider will inspect prior plan/details/findings and test
entry points; Deeper will trace decoding and schema comparison; Contrarian
will test finite floats and alternatives without widening evidence scope.

## Findings, Decisions and Planning Readiness

### Cycle 1 Wider

Inspected original harness plan and correction4 plan/details/Review/state.
Both named source files already contain all required test entry points.
Reflection: this remains a loader-only correction, not a new runtime contract.
Earlier plan's publication and gate sequencing markers are historical/stale
against the supplied later receipt. Report this discrepancy; do not rewrite
earlier outcomes or reopen their scope.

### Cycle 1 Deeper

* C1: `tools/check-demo-feedback.py:78-114`: parse_constant rejects literal
  NaN/Infinity, but default float parsing admits exponent overflow. Inline
  reproduction: `1e999` and `-1e999` decode to non-finite floats; rank=1e999
  yields ai_evidence pass. Reject in a typed parse_float callback before any
  evidence checks, reusing the existing ValueError-to-BLOCKED path.
* C2: `tools/check-demo-feedback.py:105-106`: equality-only schema comparison
  accepts True and 1.0 as version 1. Inline reproduction confirms both yield
  ai_evidence pass. Require exact int type before comparison.
* C3: `tools/check-demo-feedback.py:158-159`: existing is_int excludes bool;
  exact `type(value) is int` is also sufficient for JSON decoder output and
  matches the caller's exact-type requirement.
* C4: `tools/test_check_demo_feedback.py:788-834`: InputSafety already exercises
  serialized invalid inputs and literal constants; extend here with exponent
  tokens rather than json.dumps(float("inf")), which would emit Infinity.
* C5: `tools/check-demo-feedback.py:444-451`: latency accepts finite nonnegative
  floats, rejects negatives and non-finite in-memory values. Rank is outside
  component field validation. Preserve finite rank floats without implying
  rank correctness or actual inference.

Reflection: reject float overflow at the decoder boundary globally, including
nested unchecked fields, rather than adding an AI-only rank constraint.

### Cycle 1 Contrarian

Inline comparison confirmed finite 1.25 and 1e308 decode normally. Preserve
underflow to finite zero and large integer handling. A recursive decoded-tree
walk would be more code and unnecessary for json.loads' parse_float hook;
checking only latency or rank would miss unchecked fields elsewhere. Decimal
would alter accepted runtime types; do not introduce it.
False already blocks because it differs numerically from 1, but retain an
explicit regression alongside True, 1.0 and supported integer 1. No new schema,
dependencies, field content rules or full-gate attempt is needed.

## Alternatives and Current Decisions

Select typed `parse_float` conversion with math.isfinite, plus exact integer
schema guard; keep parse_constant and existing Verdict handling unchanged.
Scope all decoded floats, not numeric-looking strings; malformed numeric
strings remain subject only to existing field-specific rules.
No independent research worker ran; small continuous trace examined inline.
No material research gap remains; another cycle would repeat known sources.
Prior receipt is not current-candidate evidence after this change.

## Planning Readiness and Self-Check

Research disposition: executed. Planning Readiness: Ready.
Both P2 hypotheses reproduced, alternatives assessed, scope and relevant
prior-plan issue recorded. No implementation edits made during Research.
Next: parent transitions to Plan, obtains one independent critique, then
red-first tests before checker edits. Earlier artifacts remain untouched.
