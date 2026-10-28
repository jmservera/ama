<!-- markdownlint-disable-file -->
---
title: Case journey unsaved-edit correction research
description: Focused evidence for seven unresolved review threads on PR 529
ms.date: 2026-10-28
---

## Research Brief

Correct all seven unsaved-edit defects on PR #529, Refs #526, on the existing
clean topic branch. Audience: implementer and independent reviewer. Output:
convergence preparing Plan. Preserve journey ordering, permissions and human
approval. No Azure, secrets, private data, framework or visual redesign.
Trusted evidence root: `.copilot-tracking/`.

## Research Parameters and Direction Controls

Focused posture, selected from the named files and supplied failure reports.
User explicitly requests the whole RPI loop and normal commit/push/thread
resolution. Execute automatically without routine phase prompts. Heavy checks
require nonblocking flock with short retries bounded to 40 minutes.

## Extension Registry and Participation

Repository instructions, RPI research and web-design-guidelines selected.
Current guidelines fetched 2026-10-28 from the upstream raw command.md.
No design skill needed: this is behaviour repair, not app redesign. Independent
critique and Review will use bounded agents; research stays inline because the
failure chain is tightly coupled. No questions required by the complete brief.
Owner memory is context only; case study and addendum read, unchanged.

## Research Cycle 1

### Wider

GraphQL `reviewThreads(first:100)` returned exactly seven unresolved threads:

| Thread | File:line | Defect |
| --- | --- | --- |
| PRRT_kwDOUU8JX86xUr6L | app.js:316 | Document review model disappears on refresh |
| PRRT_kwDOUU8JX86xUr6p | app.js:331 | Edited document displays old wording |
| PRRT_kwDOUU8JX86xUr7A | app.js:572 | Pending proposal snapshots lost on overlapping refresh |
| PRRT_kwDOUU8JX86xUr7q | app.js:577 | Mutation snapshots taken after dispatch |
| PRRT_kwDOUU8JX86xUr8F | app.js:717 | Checklist controls restored before async creation |
| PRRT_kwDOUU8JX86xUr8k | app.js:727 | Funding text key lacks AI record identity |
| PRRT_kwDOUU8JX86xUr9C | assistants.js:32 | Verification marks unsubmitted JSON clean |

Reflection: shared field capture alone cannot recover dynamic models. Inspect
session ownership, asynchronous construction and immutable dispatch boundaries.

### Deeper

* C1 `src/api/src/zava_forward/api/web/app.js:562`: case session retains only
  resident draft nodes; fresh document output has no review controls.
* C2 `src/api/src/zava_forward/api/web/app.js:577`: refresh correctly snapshots
  direct callers before `fn`, but upload and recorded forms invoke it too late.
* C3 `src/api/src/zava_forward/api/web/app.js:724`: keys bind proposals to
  revisions but not funding text to its record. Snapshots are local variables,
  not session-owned, so an unrendered assistant panel loses them.
* C4 `src/api/src/zava_forward/api/web/ops.js:100`: `/api/checklists` creates
  evidence inputs after synchronous restoration, with unversioned IDs.
* C5 `src/api/src/zava_forward/api/web/assistants.js:32`: every successful
  action clears editor dirtiness although verify never sends output.
* C6 `src/api/checks/case_journey_browser_check.py:61` and
  `src/api/checks/assistants_browser_check.py:98`: existing isolated real-server
  Chromium checks cover ordinary refresh, revision recovery and axe.

Reflection: repair ownership and identities, not timing delays. Extend those
checks with explicitly delayed responses to reproduce each race.

### Contrarian

Retaining every whole panel would preserve stale case-state handlers and
permissions; reject. Blind restoration on any future control would mix records
or checklist versions; reject. Disabling all inputs during requests hides the
race rather than meeting preservation requirements; reject. Retain the document
review output node only, session-own pending proposal snapshots, restore
checklist fields after versioned construction, and isolate funding recovery.

## Parent Synthesis and Decision State

Accepted C1-C6. Existing refresh dispatch comparison is useful and should be
reused. No API/domain/stepper changes needed. Earlier RPI artifacts and adverse
outcomes remain immutable; this correction is a new child loop of #526.

## Planning Readiness

Ready. Research disposition: executed. One complete wider/deeper/contrarian
cycle covers the named defects; another cycle would repeat the same sources.
Residuals: human screen-reader/real deployment acceptance remain outside local
synthetic evidence; complete publication gate must not invoke prohibited az.
