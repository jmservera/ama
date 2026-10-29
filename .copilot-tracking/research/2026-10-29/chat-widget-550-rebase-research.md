---
title: Chat widget 550 rebase research
description: Focused integration research for the existing chat widget branch
ms.date: 2026-10-29
---

## Brief

Task 550-rebase, slug chat-widget-550-rebase. Bring existing
feat/chat-widget-550 onto origin/main, preserving both product intents.
Audience: local coordinator. Output: integration evidence and planning handoff.
Explicit full-loop request authorizes phase progression; no push, PR, Azure
changes, issue closure, unrelated redesign or private data access.
Focused posture follows the bounded caller scope. Interaction is unavailable
and unnecessary: the caller specifies branch, conflict policy and validation.

## Extensions and prior knowledge

Selected repository guidance, rpi-research, existing chat implementation and
focus-followup evidence. No research worker is needed for this continuous
integration trace. Web guidelines apply if web code needs edits; no visual
redesign skill is needed for documentation-only conflict resolution.
Existing research is context, not proof after rebase.

## Cycle 1

### Wider

* C1: `src/api/README.md:1` is changed on both branches. Main has two
  additional UX commits, #553 and #554; local branch has shared chat and
  focus corrections. Initial worktree is clean; no PR exists for this head.
* C2: `.copilot-tracking/changes/2026-10-29/chat-widget-550-focus-fixes-changes.md:65`
  records targeted unittest, Ruff, mypy and three real-application browser
  commands using /tmp/mv.

### Deeper

* C3: `.github/workflows/src-ci.yml:65` runs project unit discovery, Ruff
  and configured mypy. API additionally runs case journey/design/regulatory
  browsers; all hosted/image/SQL gates remain distinct from focused local checks.
* C4: `src/core/tests/test_scenario_manifest.py:21` validates all manifest
  source hashes. Neither branch changes the protected manifest in its
  topic diff; rerunning the module is cheap and protects against hidden drift.
* C5: `src/README.md:119` identifies the shared heavy lock. The caller
  forbids full API discovery unless the nonblocking lock probe succeeds.
* C6: `src/api/checks/chat_widget_browser_check.py:1` exercises actual
  synthetic employee/resident applications; pinned axe is required.
  /tmp/mv already imports Playwright, Ruff and mypy.

### Contrarian

The branch has no protected-file delta, so gratuitous regeneration would
violate the instruction to retain main's copy. README additions are independent
sections, not competing behavior; retain both instead of choosing one side.
Prior browser success does not prove integration success. Run fresh checks,
including the CI case-journey browser affected by both histories, and explicitly
avoid claiming hosted CI or the complete publication gate.
No further research cycle is needed: the remaining uncertainty is execution
of the specified rebase and checks, not a missing implementation decision.

## Decisions and readiness

Preserve both README sections; use origin/main for rubric and manifest.
Research disposition: executed. Planning Readiness: Ready.
Accepted C1-C6. Rejected broad visual overhaul and manifest regeneration.
Deferred hosted/full publication evidence to coordinator; no push is authorized.
