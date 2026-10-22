---
title: Issue 349 preflight correction2 research
description: Focused investigation of malformed collection response fields
ms.date: 2026-10-22
---

## Research Brief

Status: Complete. Research disposition: executed. Planning Readiness: Ready.
Task: issue349-tenant-readiness-preflight-correction2; issue #349.
Output mode: convergence. Audience: implementer and coordinator.
Resolved evidence root: `.copilot-tracking/research/2026-10-22/`.
Posture: focused, selected for the caller's bounded failure evidence.

Investigate the audience, identifier URI and web redirect URI readers, existing
absent-field behavior, offline tests and publication requirements. No live tenant,
Graph, Entra, credential, Azure or resource calls or changes are permitted.
Issue acceptance and sign-in remain unestablished. Exactly one full local gate
is authorized after implementation against
`b4d467cad84535ed106cffa1ae9aa303db7bfed2`.

## Extensions and Participation

Repository guidance and rpi-research selected for code and evidence scope.
Web/design/security assessment skills skipped: this is a bounded Python
functional correction, not a web change or vulnerability assessment.
Research specialist skipped: this is one tightly coupled trace, handled inline.
Caller supplied sufficient scope; no intake questions are necessary or possible.
Caller explicitly requests all four phases in order and publication after gating.

## Prior Knowledge and Questions

Candidate is `4753af1edf74db7f5cf0ec1025b69d22f72f18f5`; worktree is clean,
topic branch `feat/tenant-readiness-preflight-349` has no existing PR.
Supplied independent functional review is NEEDS CHANGES; prior gate is stale.
Issue #349 is open with all six criteria unticked.

* Q1: Which malformed shapes can crash or accidentally pass each reader?
* Q2: How must absent/null fields retain existing behavior?
* Q3: Which tests, lint/type checks and exact-head gate prove the correction?

## Cycle 1

### Wider

Read the three readers and surrounding fail-closed reporting path. All three
use `value or []` before iteration, which does not enforce a JSON list.
Reflection: successful JSON decoding is insufficient; shape validation is needed.
Prioritize existing tests, safe reason codes and absent-field semantics next.

### Deeper

The 29 baseline offline tests pass. Existing canned `Fake` transport allows
each field to be varied without any service access. The CLI returns exit 1
when any check is unknown. Missing/null collections currently become empty;
audiences/identifier URIs report mismatch and callbacks report absent.
Reflection: preserve these outcomes explicitly, but do not use truthiness for
other malformed values. System Python lacks Ruff; installed pinned Ruff 0.17.1
and mypy 2.4.0 in a task-owned external venv after that observed failure.

### Contrarian

An offline shape matrix reproduced TypeError for integer 7 at every reader.
It also disproved the assumption that non-crashing iterables are safe: dictionary
keys containing the expected audience/identifier URI incorrectly produce ready.
False, empty string and empty object silently become missing rather than malformed.
Reflection: validate every non-null non-list shape before iteration, including
falsey values. Keep existing string-member filtering for actual lists in scope;
do not expand into unrelated response schema rewrites.

### Parent Synthesis and Re-entry

Accept strict list guards at all three readers (C1-C3, C5), preserving null and
absent semantics (C6). Reject broad exception handling: it hides the malformed
check and can conceal other bugs. Reject coercion to iterable/list: dictionaries
can incorrectly pass (C5). No additional cycle is needed: Q1-Q3 are covered and
the remaining controls are implementation and publication gates, not unknown design.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Audiences iterate an unchecked response field | infra/scripts/tenant-readiness-preflight.py:377 | High |
| C2 | Identifier URIs iterate an unchecked response field | infra/scripts/tenant-readiness-preflight.py:497 | High |
| C3 | Redirect URIs iterate an unchecked response field | infra/scripts/tenant-readiness-preflight.py:515 | High |
| C4 | Unknown blocks overall status; rendering exposes only fixed checks/facts | infra/scripts/tenant-readiness-preflight.py:568 | High |
| C5 | Integer crashes and dictionary false-ready reproduced using canned transport | infra/tests/test_tenant_readiness_preflight.py:41 | High |
| C6 | Fake transport, CLI output and exit tests support offline compatibility/regression checks | infra/tests/test_tenant_readiness_preflight.py:434 | High |
| C7 | Gate validates committed clean head/current base and takes shared lock | tools/rpi-checks.py:1676 | High |
| C8 | Current fetched main is requested b4d467cad84535ed106cffa1ae9aa303db7bfed2 | src/README.md:100 | High |

## Findings and Decision State

Q1: Non-null non-list JSON values must emit unknown/malformed-response and block
without value/count facts (C1-C5). Q2: Null/absent continue empty-list outcomes;
valid lists preserve filtering and counts (C6). Q3: Add focused CLI tests for
each field, all non-list JSON types and both output formats; run focused suite,
isolated Ruff/format and strict script mypy, then one full committed-head gate
and exact-head receipt verification (C6-C8). Callback-target dependency remains
higher priority when the target itself is unavailable.

## Risks, Readiness and Self-check

No unresolved correction design decision. No external sources or live tenant
operations used. All three waves were actually executed inline in order.
One narrow code/test correction is ready to plan. The prior adverse review and
old-head receipt remain historical, never acceptance or new-head validation.
Independent final PR assessment remains the coordinator's responsibility.

## Sources and Remaining Work

No external sources used. No source files changed during Research.
