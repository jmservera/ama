---
title: Regulatory audit snapshot research
description: Focused research for issue 208 and PR 506 concurrent append regression
ms.date: 2026-10-29
---

## Research Brief

Resolve the audit-read race in regulatory_chat.py for /usage and /status.
Output mode: convergence. Posture: focused, selected from the named source,
specific review finding and explicit requested correction. Audience: implementer
and independent reviewers. Scope: bounded snapshot read and deterministic core
regression; no broader concurrency, infrastructure or regulatory-policy changes.

## Research Parameters and Direction Controls

Use the existing clean feat/regulatory-assistant-208 branch, open PR #506.
Run all RPI phases and commit locally; no push, az or rubric-score edits.
Primary evidence root: .copilot-tracking/research/2026-10-29/.
Questions: where is the snapshot boundary lost, what existing test seam can
simulate an append, and does the correction preserve large-file tail behavior?

## Extension Registry and Participation

Repository instructions and component guidance apply. rpi-research selected.
Web/design/regulatory evidence extensions do not apply to a backend file-read
correction. Research specialist delegation skipped: this is one coupled trace.
No interaction required: the user specified outcome, fix, tests and boundaries.

## Research Cycle Log

Cycle 1 opening: verify the supplied finding against source and existing tests.
Wider: inspect component contracts, audit consumers and test organization.
Deeper: trace size, seek, read and JSON parsing with the existing mocking seam.
Contrarian: inspect large-file boundary handling and alternatives before
recommending the captured-length read. Results and stable evidence follow.

## Findings, Evidence, Decisions and Readiness

| Evidence | Source | Finding |
| --- | --- | --- |
| C1 | src/core/src/zava_forward/core/regulatory_chat.py:144-185 | JSON captures EOF and start but reads MAX_BYTES, admitting later appends when the captured file was smaller. SQL already captures a sequence window. |
| C2 | src/core/tests/test_regulatory_chat.py:203-244 | Existing service fixture tests role/day, restart, position and byte truncation across JSON and SQL. |
| C3 | src/core/src/zava_forward/core/regulatory_usage.py:11-12,69-116 | Bound is exactly 262144 bytes; summary rejects malformed JSON and returns coverage plus recorded counts. |
| C4 | src/core/README.md:3499-3506 | Public component contract promises bounded audit reads and explicit partial coverage. |
| C5 | src/core/tests/regulatory_fixture.py:28-80 | Constructed temporary JSON/SQLite fixtures need no private data or Azure. |

Wider reflection: C1-C5 identify one JSON-only boundary defect; no API/schema
or SQL change is needed. The installed editable package resolves to this worktree.

Deeper reflection: C1 computes start=max(0,size-MAX_BYTES), so size-start
is nonnegative and never exceeds MAX_BYTES. Read exactly that length. Inject
an append during read with a wrapped real binary file; preserve EOF seek and
real bytes. Assert exact requested byte length and snapshot summary.

Contrarian reflection: for captured sizes above the bound, size-start already
equals MAX_BYTES, so tail and first-fragment dropping remain unchanged. For
empty files the corrected read is zero. JSON decoding error suppression would
hide corruption and is rejected. Locks/retries widen scope unnecessarily.
Truncate/replace races and incomplete writes already present at capture are
not solved by this append-only snapshot correction.

Parent disposition: accept the captured-length read (C1,C3); reuse existing
large-file tests (C2) and add a deterministic below-limit capture/above-limit
append regression (C5). No second cycle is needed: all scoped questions are
answered and further sources are redundant.

Research disposition: executed. Planning Readiness: Ready.
Self-check: scoped evidence, alternatives, constraints, participation, ordered
wave reflections and residual uncertainty recorded. No research source edits.
Parent next action: Plan and one independent critique.
