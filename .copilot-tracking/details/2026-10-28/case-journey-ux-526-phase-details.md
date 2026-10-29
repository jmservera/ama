---
title: Case journey UX 526 phase details
description: Completion expectations, dependencies and implementation boundaries
ms.date: 2026-10-28
---

Task 526; plan: .copilot-tracking/plans/2026-10-28/case-journey-ux-526-plan.md.
Readiness: supplied design and completed focused research; no new API fields.

<!-- rpi:phase id=P01 -->
## P01: Workspace structure and state

<!-- rpi:task id=P01-T01 -->
### P01-T01: Derive journey and render summary/stepper

Add a native case-workspace module, loaded before app.js. One mapping is the
source for stepper and stage-to-tab navigation. Test against Python STAGE_ORDER.
Blocker names map to the specified steps with unknown fallback to current.
Closed overrides all, and funding/decision completion requires explicit
status. Unknown stage stays unknown. Summary reads existing payload, counts
all blockers/overdue and names unconfirmed handoff. No new colours.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Retain and route tab panels and drafts

Depends on P01-T01. Refactor caseView composition only, preserve handler
closures. Split contractor/appointment text from Overview. Safety lives once
above journey when open; otherwise in Blockers. Summary jumps activate tab
and focus heading. Same-case tab-only hash changes switch retained nodes
without route abort or dirty guard. Other queries still use existing route.
Capture dirty fields/details on same-case refresh alongside challenge
node preservation. Do not retain completed action inputs after success.
Retain the complete generated resident draft container (plain/AI text,
record_id, review metadata and live handlers) for this case only. Capture
dirty call, funding, assistant reason/edit and other controls by stable
id/name/accessible-label identity plus occurrence; keep challenge live forms
with their existing helper. A successful action clears only its initiating
section's dirty controls. Reuse resident draft nodes on unrelated refresh.
Case/identity departure disposes this session after the existing leave guard.
Never turn a failed/stale review into success locally.
Default first active blocker tab, else Overview. Unknown tab uses default.
Use role tab/tabpanel, controls/labelledby, manual keys and roving tabindex.
Construct headed sections before enhancement. If case-workspace.js is absent,
leave every section stacked and report that tab navigation is unavailable;
do not call a missing global or hide content before initialization.

<!-- rpi:phase id=P02 -->
## P02: AI presentation and review

<!-- rpi:task id=P02-T01 -->
### P02-T01: Harmonize cards and accessible review controls

Depends on P01-T02. Existing aiNotes and assistantProposal use .ai-suggestion.
Visible Reason label/fieldset, linked errors and focus invalid control,
required edit/reject reasons, native disabled stale/unverified accept.
Existing draft /api/ai/review and assistant revision/verification flow remain.
Missing confidence displays "not provided"; sources and mode/date retained.
Reviewed/stale proposals are grouped in Reviewed details. Resident draft
output is listed in AI tab by a live pointer, not duplicated form IDs.
Asynchronous assistant load updates summary/tab count and compares case path
rather than full hash. Chat metadata matches; no fake recorded turn review.
Count state table: assistant ready + output + not stale = waiting for review
(including not yet source-verified); queued/running/failed/accepted/rejected/
edited/stale = not waiting. Local draft approval Not reviewed = waiting;
accepted/edited/rejected = not waiting. Missing output is never a suggestion.
Follow all existing case-filtered next_after cursors and update summary and
AI tab together. Generated resident and funding draft records count once per
record_id, updated after review; no duplicate DOM or count from cross-links.

<!-- rpi:phase id=P03 -->
## P03: Evidence and validation

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add semantic/browser checks and update documentation

Depends on P01/P02. One new Python unit file can run Node with a minimal
document stub to test pure derivation; fail if Node absent. One focused
Playwright check owns synthetic local case/axe/tab/keyboard/zoom states.
Existing browser checks receive only tab navigation changes.
Exception PC-003: assistants_browser_check may update old note/button names
to visible Reason and Accept, and replace stale button absence with disabled
non-actionability. Preserve all scenarios, person-specific verification and
unchanged-domain assertions.
Register supplied design in docs/reference/README.md; append log entry
without rewriting history. Clarify implementation evidence and API gaps in
the design. Update src/api README reproduction command.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Run local checks, independent Review and publication gate

Depends on all implementation tasks. Lock heavy commands with nonblocking
flock in 60-second retries for at most 2400 seconds. Baseline environment
lacked distributions, so use installed declared extras in .venv.
Run exact requested unit command with venv Python, focused browser and
existing design-system/workbench, employee workspace, assistant, challenge,
regulatory axe checks on constructed data. No default-data browser_check.
Record actual browser version/results, 200% mechanism and human gaps.
Run one independent post-implementation Review, route findings without
re-review. Commit source plus dated original evidence; run full --all gate
external on clean candidate. Fetch main and verify exact receipt immediately
before non-force push; no later source or evidence commit after final gate.
If base advances, rerun gate at current base. Never weaken a failed gate.

### Exact browser assertion matrix (PC-005)

| Fixture/state | Action | Pass condition |
| --- | --- | --- |
| Open, blocked, no blockers, closed, assistance unavailable | Visit all nine tabs; axe pinned 4.10.3 | Zero serious/critical violations by state/tab; one h1; six ordered steps |
| Loading | Hold case API | Visible busy/loading message; no premature tabs |
| Normal at 1280x800 | Measure summary | All six values bottom <=800 without scroll |
| Normal at 320x800 | Measure summary | All six values bottom <=1600, one viewport scroll bound |
| All tabs at 320px and browser zoom 200% | Inspect overflow/focus | No body overflow; active focus visible; named tab/table scrolling permitted |
| Reduced motion / forced colours | Emulate preferences | No step/tab transition; text states and distinct borders remain |
| Unsaved generated AI/plain text and call | Switch/back/unrelated refresh | Same text/review record; action-local clear; no cross-case leakage |
| Delayed assistance and >50 proposals | Tab-only navigation then finish load | No abort/rebuild; correct full count and matching summary/tab |
| Tab keyboard / summary links | Arrows/Home/End/Enter/Space | Manual activation, one tab stop; jump focuses panel heading |
| Optional module unavailable | Block script | Stacked headed controls/safety usable; no pageerror |

Use Chromium browser zoom via browser keyboard or DevTools window zoom
where available; document mechanism and explicitly disclose if unavailable.
Do not substitute device_scale_factor alone for browser zoom.
