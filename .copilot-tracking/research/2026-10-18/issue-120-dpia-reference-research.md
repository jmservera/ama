<!-- markdownlint-disable-file -->
---
title: Issue 120 DPIA reference research
description: Exact-base bounded time-capture admission research
ms.date: 2026-10-18
---

# Task Research: issue-120-dpia-reference

| Field | Value |
| --- | --- |
| Date | 2026-10-18 |
| Researcher | RPI parent, rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-18/issue-120-dpia-reference-research.md |

## Research Brief

Research whether bare affirmative DPIA flags bypass the documented reference
requirement, how to reject them before writes, and which existing contracts must
remain unchanged. Audience: delivery coordinator and independent reviewer.
Output mode: convergence, preparing an implementation plan.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | Admission root cause; prior art; persistence/history; focused validation |
| Scope | timecapture.py, existing test_timecapture.py, narrow API README, task evidence |
| Initial internal candidates | API time capture, chat_privacy.py, rai_release named-reference guard, existing tests and component commands |
| External scope | Read-only GitHub issue and branch metadata only |
| Posture | Focused, inferred from caller's bounded criteria |
| Completion basis | All six bounded criteria evidenced; material alternatives challenged |
| Limits | One independent critique, one original Review; at most two later correction cycles |
| Resolved root | .copilot-tracking/ |
| Edits during research | Research and required workflow evidence only; no production edits |
| Exclusions | Server, shared fixtures/schema/web, #92/#122, private data/env/support, Azure/IAM/Graph/spend/model calls, live governance approval |

## Extension Registry and Provenance

| Kind | Candidate | Disposition and authority |
| --- | --- | --- |
| Instructions | Repository guidance, applies to all files | Selected; component installation, topic branch, evidence and human boundaries |
| Skill | rpi-research | Selected; ordered Wider, Deeper, Contrarian evidence |
| Skill | privacy-standards | Not needed for new legal claims; this is an existing string-presence contract, not legal analysis |
| Specialist | RPI Researcher / privacy planner | Skipped; one tightly coupled code trace handled inline |

## User Participation and Research Decisions

Caller explicitly requests complete ordered execution and commit/push/new PR.
This is confirmed automatic direction, not inferred consent from a handoff.
No intake questions are necessary. Stop after delivery for coordinator review.

## Scope and Success Criteria

* Verify clean branch and exact base a86282c4badebc58eabbf9e441410d930a201ac2.
* Reproduce with real TimeCapture before source changes; preserve failing output.
* Reject missing/blank and trimmed case-insensitive yes/true/on/1.
* Deny request, activation, acknowledgement and entry without new rows or a fresh local store.
* Retain seeded history and prevent invalid historical controls bypassing admission.
* Preserve valid D1 and DPIA-2026-007, trimming, changed-reference semantics,
  manager separation, notice, aggregate/own-entry/audit and shared SQL contracts.
* Document reference presence only, never authenticity or legal approval.

## Direction Controls

| Control | Source | Effect |
| --- | --- | --- |
| Narrow production writes | Caller | Only timecapture.py, existing test file and API README |
| No format invention | Caller | No prefix, URL, length rule or unrelated approval service |
| Human boundaries | Caller and issue | Issue remains open; DPIA, consultation, notice/admin ratification unfulfilled |
| Exact ancestry | Caller | Branch verified clean; HEAD and origin/main both exact requested base |

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Does real capture accept a bare affirmative, and which common gate owns refusal? | Depth | Open |
| Q2 | Which prior art and historical/reference-change cases constrain a minimal fix? | Depth | Open |
| Q3 | Which existing suites/checks demonstrate unchanged persistence and HTTP boundaries? | Straightforward | Open |

## Prior Knowledge Gate

Read original case study, addendum framing/exercise limits, KB index and owner
memory, API guide and current time-capture source/tests. Caller reports a
nonempty-string defect; verify experimentally rather than treating it as fact.
Read-only GitHub issue 120 confirms open status, no dependencies and parent 113.
No existing PR for this branch. No dirty files at intake.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Current source's module contract forbids bare yes, but status uses bool(dpia).
Read candidate contracts and existing component validation/persistence coverage.
Reflection: prioritize the shared status gate and preserve stored reference matching.

#### Wave 2: Deeper

Executed the installed-source probe before production changes. Two assertions
failed: direct request/activate/ack/record all succeeded with ` yes `, and actual
authenticated loopback HTTP returned 200 for all four routes. Both created the
unused local store. HTTP also appended the three successful governance audit
events. Preserved the original output in
`issue-120-dpia-reference-baseline-probe.log`, exit 1 (2 failures).
The existing full time-capture suite passed 16 tests, showing the coverage gap.

Reflection: `_ready_to_enable` and `_require` both consume `status`, so one
derived predicate can protect every write without SQL or server changes.
The server audits only after successful admission. First Python import failed
with missing `zava_forward`; then installed only source distributions and API
dev tools in the ignored task-local `.venv`. Verified imported API path belongs
to this worktree. No mvp path or private data was used.

#### Wave 3: Contrarian

Read prior art and challenged stricter formats using real TimeCapture.
`D1`, padded `DPIA-2026-007`, and `yes-reference` all enable, record and survive
restart; a different valid reference disables their old controls. Preserved
successful experiment in `issue-120-dpia-reference-contrarian.log`.
`chat_privacy.py` repeats the bare-yes prose but checks only nonemptiness,
therefore it is not a correct reusable validator. `rai_release.named` uses
trimmed casefold sentinel exclusion but has unrelated length/sentinel rules.

Reflection: adopt the local pattern, not either service dependency. Reject only
the explicitly bounded affirmative tokens plus blanks. Historical invalid
rows need not be removed or hidden: derived `dpia_recorded=false` must dominate
matching request/activation and acknowledgement history. Add regression coverage
with literal SQL-seeded controls so the test does not rely on the new writer
being able to generate invalid history.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Central status predicate | C1-C4 | Accepted | Protects both admission paths, including seeded controls |
| Existing portable SQL and runtime | C5-C6 | Retain | No query, DDL, connection or audit changes needed |
| Import shared approval service | C7-C8 | Rejected | Unrelated semantics and dependency would broaden policy |
| Prefix/URL/length enforcement | C9 | Rejected | Short valid references are explicitly supported |
| Human sign-off | Issue and caller | Deferred to humans | Reference presence cannot establish authenticity or approval |

#### Cycle Re-entry Evaluation

No further cycle required: all material code questions are answered, direct and
HTTP reproductions agree, and contrarian tests support the minimal bounded
approach. Historical-invalid regression is planned, not falsely reported as
already passed. Focused stop basis: scope coverage, no unresolved design choice.

## Evidence Log

| ID | Claim | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Module requires an actual reference, not bare yes | src/api/src/zava_forward/api/timecapture.py:6 | High |
| C2 | status currently treats every nonempty trimmed string as recorded | src/api/src/zava_forward/api/timecapture.py:137-166 | High |
| C3 | Both enabling and recording use status-derived admission | src/api/src/zava_forward/api/timecapture.py:199-253 | High |
| C4 | Real direct and authenticated HTTP accept bare yes | .copilot-tracking/research/2026-10-18/issue-120-dpia-reference-baseline-probe.log:1 | High, observed exact base |
| C5 | Shared SQLite test covers entries, acknowledgements, restart and table counts | src/api/tests/test_timecapture.py:270-298 | High |
| C6 | Server role checks and audits surround existing service admission | src/api/src/zava_forward/api/server.py:815-836 | High |
| C7 | Chat privacy prose is not an implemented sentinel validator | src/core/src/zava_forward/core/chat_privacy.py:119-127 | High |
| C8 | named uses stripped casefold sentinel matching with unrelated constraints | src/core/src/zava_forward/core/rai_release.py:33-38 | High |
| C9 | Short/padded/non-prefix references retain semantics after restart | .copilot-tracking/research/2026-10-18/issue-120-dpia-reference-contrarian.log:1 | High, observed |
| C10 | API Ruff/format and mypy configured with legacy exclusions | src/api/pyproject.toml:25-65 | High |
| C11 | Prior engine review claims SQL Server suite passed, without exact count/log | .copilot-tracking/reviews/2026-10-15-issue-120-time-capture-shared-store-review.md:10 | Historical claim only, not rerun |
| C12 | Installed-source baseline full suite passes 16 tests | src/api/tests/test_timecapture.py:1-302 | Observed command, 7.132 seconds |

## External Evidence

Read-only issue/branch metadata is workflow evidence, not a regulatory source.
No external legal sources or currentness claims are required.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence | Implication |
| --- | --- | --- | --- |
| Q1 | Nonempty DPIA predicate admits bare flags through all four writers | C1-C4, C6 | Fix shared status predicate |
| Q2 | Retain exact stored reference matching and trimmed valid strings | C5, C7-C9 | No generalized validator, history cleanup or new format |
| Q3 | Full existing time suite plus added local/shared history and HTTP cases | C5-C6, C10-C12 | Run focused suite and configured API checks locally |

## Alternatives and Decision State

Selected: derive `dpia_recorded` once from the stripped value, rejecting empty
and case-insensitive `yes`, `true`, `on`, `1`; use it both for the DPIA reason
and returned status. Preserve `_refs` and every persistence statement.
Update plain reason to explain an actual DPIA reference, not a boolean flag.
The existing source module contract already requires this; no new policy.

## Open Questions, Risks, and Residual Uncertainty

No implementation blocker. Docker is available, so attempt existing hardened
source image with synthetic loopback HTTP after implementation. No MSSQL run is
required if source diff and AST prove every SQL/schema/runtime boundary unchanged;
report historical engine claims as historical, not a current pass. No browser
changes, checks or fresh WCAG assertion. Human DPIA/consultation/notice/admin
ratification and independent coordinator acceptance remain unmet.

## Planning Readiness

Ready. Research disposition: executed. Q1-Q3 answered by C1-C12.
Self-check: all three ordered waves executed inline, no research worker implied,
claims linked to actual code or preserved experiments; no legal-currentness
claims, no source edits, task boundary and human blockers retained.
