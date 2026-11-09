---
title: Issue 1214 320px case-summary layout research
description: Root cause of the 320x800 case-summary bound failure on main c6d5a8f3
ms.date: 2026-11-05
ms.topic: reference
---

## Research Brief

* Topic: why `.case-summary` bottom is 1676.40625 at 320x800 on unchanged main c6d5a8f3c3a35892322300be27b9747f7b11362d, against the unchanged bound of 1600 (`src/api/checks/case_journey_browser_check.py:1526`).
* Purpose: provide evidence for the smallest Fluent 2-preserving CSS/layout correction under issue #1214. Output mode: convergence. Posture: focused (bounded internal task, named sources, supplied failure evidence; provenance: caller brief).
* Non-goals: relax the bound, hide, clip, remove or reorder content, change viewport thresholds, redesign, full gate, tooling/bytecode fix.
* origin/main refreshed at session start: c6d5a8f3c3a35892322300be27b9747f7b11362d. No movement. HEAD equals it, worktree clean.
* Extensions: applied repository instructions (AMA, web guidance); skills `redesign-existing-projects` and `web-design-guidelines` (guidelines source fetched 2026-11-05 from raw.githubusercontent.com vercel-labs command.md, full retrieval); design-taste skills skipped (public pages only). Subagents not used: single continuous trace.
* Research disposition: executed. Interaction: none needed; inputs sufficient.

## Method

Existing check run unmodified on the candidate checkout under the heavy lock (nonblocking flock), reusing the gate venv and Chromium read-only with candidate module paths asserted, plus an external Locator.evaluate hook that dumps element geometry at the failing assertion. Wrapper and dump script are session artifacts. Outputs: /tmp/g1214-research-1105a and /tmp/g1214-research-1105b (dump.json, logs). Both runs: process exit 1, same assertion, bottom 1676.40625.

## Findings

* C1 `src/api/checks/case_journey_browser_check.py:1517-1526`: the bound measures the absolute document-bottom of `.case-summary` after `scrollTo(0,0)`, so it includes everything above the summary (shell header, status line, case heading rows), not only the summary box.
* C2 Measured geometry at 320 (dump.json): `header.top` 0 to 526.8 (527px), `#workspace-status` 538.8 to 586.8, case heading block 606.8 to 921.8, summary 921.8 to 1676.5 (754.7px, six items: 116, 65, 156, 86, 131, 142 high).
* C3 The shell header is the largest single contributor. Its nav is `flex-basis:100%` (`src/api/src/zava_forward/api/web/style.css:82`) with 9 links, each `min-height:2.5rem` plus `.2rem` padding (`style.css:310`, 42px tall), wrapped into 7 rows. Row pitch is 58px because `nav{gap:1rem}` (`style.css:43`) applies to the row axis as well: 6 gaps of 16px = 96px of pure vertical gap in a 7-row wrap.
* C4 Why it regressed after #529: nav, header and workspace shell were added or grown afterwards (#317 shared role workbench IA `style.css:310`, nav link min-height, #554 thinner journey). The summary itself (`style.css:134-140,183`) already has 320 compaction (8px padding, 8px gap, one column) from #529/#554. Cause is cumulative growth of the shell above, not new summary content.
* C5 The summary's own contents are safety and approval content (status line with stop reason, next action with jump button, blockers disclosure, AI state). They must not be hidden or reordered, so the summary has little legitimate room; its dd stack already uses 8px gaps.
* C6 Excess is 76.4px (1676.41 - 1600). Nav row gap reduction from 16px to 2px (a 2px value, see C7) saves 6 x 14 = 84px, giving about 1592.4, 7.6px margin. A 4px gap (`--sp-1`) saves only 72px (1604.4, still failing).
* C7 `style.css:9` defines spacingHorizontalXS .25rem, S .5rem, M .75rem, L 1rem, XXL 1.5rem. The local token block has no XXS token, so a 2px value needs a literal `.125rem` or a new token (decision recorded in the plan).
* C8 Touch/target: links stay 42px tall (>= 24px, WCAG 2.5.8) and keep full width labels; vertical spacing is the only change. Focus outline behaviour unchanged.

## Alternatives (contrarian wave)

| Option | Effect at 320 | Verdict |
|---|---|---|
| Relax the 1600 bound | n/a | Rejected: explicit prohibition |
| Hide or collapse nav / summary items | large | Rejected: no hiding or removing content, manual paths must stay visible |
| Reduce nav row gap at max-width 600px (existing breakpoint) to 2px | about -84px | Selected candidate; smallest, header only |
| Reduce `#nav a` min-height / padding | -2px or less per row, harms target size | Rejected: weakens touch targets |
| Tighten summary dl gap/padding further | about -16 to -24px | Insufficient alone, more cramped around safety text |
| Put account control on brand row | about -58px | Needs logo resizing; larger visual change; deferred |
| New threshold below 600px (for example 360px) | same | Rejected: viewport-threshold change prohibited; 600px breakpoint already exists |

* Contrarian check: a 600px rule also tightens nav rows at 390px (still 42px targets, no overflow). The existing 390 reflow assertions and screenshots must be rechecked. This is a disclosed small visual change at 390, not a behaviour change.
* Evidence gap: the 390 and 1280 geometry before and after is to be recorded by the implementation.

## Decision

* Selected: add a `max-width:600px` rule setting the header nav row gap to 2px (row-gap only; column gap unchanged), no other CSS, no JS, no check change. Rationale: C1 to C3, C6, C8.
* Existing browser check is the regression coverage; no new test planned (a CSS constant test would be trivial).

## Planning Readiness

Ready. Validation tier: FOCUSED (small CSS-only fix outside SQL, security, finance, infrastructure and deployment). Open risk: 7.6px margin to the bound is deterministic in pinned Chromium but small; plan must record before and after geometry.

## Evidence Pointers

* C1 `src/api/checks/case_journey_browser_check.py:1517-1526`
* C3 `src/api/src/zava_forward/api/web/style.css:43,82,310`
* C5 `src/api/src/zava_forward/api/web/case-workspace.js:83-113`, `style.css:134-140,183`
* Baseline traces: /tmp/g96-diag-out/run2.log, /tmp/g1214-research-1105a.log, /tmp/g1214-research-1105b.log (external, not durable)
