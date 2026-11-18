---
title: Issue 151 live WCAG baseline research (round 2)
ms.date: 2026-11-18
---

## Task

Refs #151. Demo scope, desktop only, live Azure authorised (rg ama, cap USD 700, read-only checks). Only unticked criterion: manual screen-reader and keyboard checks recorded for each role workflow.

## Research disposition

Executed (new live evidence). The first round (`docs/reference/research/issue-151-live-wcag-axe-evidence-2026-11-18.md`, commit 2704bec2b, tracked `issue-151-live-*` artifacts) kept slim axe output only, left three `color-contrast` incompletes, saw Time capture in an error state, covered one employee role and no resident app, and exercised no case view. Those artifacts and the original state JSON are preserved unchanged; this round uses `-r2` names.

## Process note (adverse)

The first action of this round overwrote the tracked `issue-151-live-research.md` and `issue-151-live-state.json` with new content before the worktree's tracked history was checked. Both were restored with `git checkout` before any commit; the witness `research-open` event (seq 2) was recorded while the overwritten state existed. Later boundaries use the `-r2` state file.

## Measurement plan

* Re-scan all 13 employee screens plus one case view with axe 4.10.3, retaining raw axe JSON per screen.
* Resolve contrast incompletes by computed-style sampling.
* Scan the resident demo app (sign-in and signed-in home).
* Record per-route document title; redact identifiers; label unretained results.

## Findings

See `docs/reference/research/issue-151-live-wcag-axe-evidence-r2-2026-11-18.md`. Summary: 0 axe violations on 16 screens, 0 contrast failures in 706 sampled nodes (lowest 4.66), no trap after correcting a datetime-local false positive, one document title for all employee routes (2.4.2 not proven).

Planning Readiness: Ready.
