---
title: Case journey 526 open threads research
description: Focused evidence for the five further PR 529 corrections
ms.date: 2026-10-28
---

## Research Brief

Investigate the five open Copilot threads on PR #529 for issue #526 in the
existing topic worktree. Output mode: convergence for implementation planning.
Posture: focused, selected for named defects and bounded source files.
Resolved evidence root: `.copilot-tracking/`. Research source edits: prohibited.
Audience: implementation and independent review. Non-goals: redesign, Azure,
real data, changes to approval authority or workflow pins.

## Parameters and Direction Controls

Preserve retained tabs, non-tab query parameters, unsaved edits and record
identity. Run API units, gate-tool units and journey Chromium/axe. Heavy checks
require nonblocking flock with a maximum 40-minute retry. Never read secrets or
`.env`. Keep PR text `Refs #526`. Normal push only, subject to publication gates.

## Extension Registry and Participation

Repository instructions and RPI research selected. Web-design-guidelines selected
for web corrections; public-page design and visual redesign skills skipped:
this is an existing-app behavior correction, not a visual redesign.
No research delegation: the defects form a tightly coupled trace.
User supplied full-loop direction and sufficient acceptance criteria; no intake
question is needed in this non-interactive execution.

## Prior Knowledge Gate

Read original specification, addendum, knowledge-base index and owner memory.
Existing PR evidence is historical and does not establish this candidate's gate.
Clean worktree, existing open PR and matching remote branch verified at intake;
fetch showed no remote-only bot commit, so no pull was needed.

## Questions and Initial Evidence

* Q1: How do pending snapshots participate in navigation and unload protection?
* Q2: Which globals does the isolated route harness require?
* Q3: How can later document text/reason remain recoverable after review?
* Q4: Which exact journey output contract and receipt fixture must change?
* Q5: How can step destinations follow retained challenge pagination?

## Cycle 1

### Wider

GraphQL `reviewThreads(first:100)` returned exactly five unresolved threads:

| Thread | File and original line | Concern |
| --- | --- | --- |
| PRRT_kwDOUU8JX86xV4Z0 | app.js:225 | pending-only drafts bypass leave and unload guards |
| PRRT_kwDOUU8JX86xV4aP | app.js:232 | route harness lacks case state |
| PRRT_kwDOUU8JX86xV4at | app.js:334 | document review drops later edits |
| PRRT_kwDOUU8JX86xV4a- | tools/rpi-checks.py:959 | 37 versus 38 scans |
| PRRT_kwDOUU8JX86xV4bZ | case-workspace.js:93 | journey href loses challenge query |

Reflection: all five map to existing code and targeted test surfaces; no
broader redesign is warranted.

### Deeper

`rememberCaseFields` reconciles clean live keys and unresolved cached drafts;
reuse it rather than add a second cache. aiNotes is shared by document,
resident and funding review: completed review controls must not remain actionable.
Document output nodes are retained in the session across ordinary case refresh.
Challenge pagination uses in-place `history.replaceState`, with no hashchange.
Step hrefs therefore need an explicit controller synchronization hook there,
as well as at selection/render.

Reflection: shared dirty reconciliation and immutable review comparison fit
existing helpers. Native anchors must remain usable for modified/new-tab clicks.

### Contrarian

Disabling editing during dispatch would avoid the race but does not satisfy
the requested later-edit recovery. Retain later text/reason as labelled,
read-only, dirty recovery bound to the reviewed record; disable completed
review actions and display only dispatch-time text as submitted.
Preserving the query once is insufficient because pagination changes in place.
Exactly 38 scans remains the contract: new behavior assertions can extend the
existing browser check without introducing extra scans. Negative fixture
checks should reject 37/39 and serious violations.

Reflection: no new material uncertainty. One focused cycle is sufficient.
Accepted C1-C4 and C5-C7 below; rejected input-lock-only and static-href-only
alternatives because they miss explicit user behavior.

## Findings and Evidence Log

* C1 `src/api/src/zava_forward/api/web/app.js:225`: route dirty guard is DOM-only.
* C2 `src/api/tests/test_workspace_scripts.py:20`: VM slice starts at
  `workspaceScriptLoads`, after the caseSession declaration.
* C3 `src/api/src/zava_forward/api/web/app.js:327`: review captures submitted
  values but unconditionally clears current controls and hides the fieldset.
* C4 `src/api/src/zava_forward/api/web/case-workspace.js:93`: href hardcodes tab.
* W1 https://github.com/jmservera/ama/pull/529, retrieved 2026-10-28:
  five unresolved Copilot threads verified using gh GraphQL.
* C5 `src/api/src/zava_forward/api/web/app.js:798`: rememberCaseFields already
  reconciles clean live controls and persists unresolved snapshots.
* C6 `src/api/src/zava_forward/api/web/panels.js:280`: history pagination replaces
  URL and displayedHash in place, requiring journey-link synchronization.
* C7 `tools/test_rpi_checks.py:496` and
  `src/api/checks/case_journey_browser_check.py:506`: fixture expects 37 while
  restored-quality-evidence adds the 38th scan.
* W2 https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md,
  retrieved 2026-10-28 in full: unsaved-change warnings, native anchors, accessible
  recovery controls and stateful URL synchronization apply. Repository content
  conventions override unrelated stylistic typography changes.

## Risks and Extension Disposition

The full publication gate includes az-dependent infrastructure commands.
The user prohibits all Azure and permits local-only commit handoff in this
case; implementation validation can proceed but publication cannot be claimed.
No pinned workflow needs modification; verify hashes without editing pins.
No legal, live-data, screen-reader or usability acceptance is inferred.

## Readiness

Research disposition: executed, Complete. Planning Readiness: Ready.
All five questions answered; no additional research cycle is material.
Artifact self-check: sources, constraints, alternatives, waves and risks recorded.
Parent next action: Plan, followed by one independent critique.
