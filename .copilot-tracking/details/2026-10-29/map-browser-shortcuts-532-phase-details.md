---
title: Map browser shortcuts correction phase details
description: Task-level implementation and validation expectations
ms.date: 2026-10-29
---

Task: 532-map-browser-shortcuts-2026-10-29.
Evidence: .copilot-tracking/research/2026-10-29/map-browser-shortcuts-532-research.md.

<!-- rpi:phase id=P01 -->
## P01: Correct handler and regression coverage

<!-- rpi:task id=P01-T01 -->
### P01-T01

First extend the browser assertions and run them against the unmodified handler
under the nonblocking heavy lock to retain red regression evidence. Then add a
single early-return modifier guard before offsets or zoom. Preserve current
defaultPrevented/control exclusions. Existing check helper focuses map/marker,
dispatches bubbling cancelable keydown events across protected modifier/key
matrix and asserts uncancelled dispatch, stable pane content/transform, no map
API reads and unchanged route/focus. Invoke in embedded/expanded modes.
Use real Playwright keyboard press for Shift plus, equals and minus; inspect
actual map API request zoom levels for exact deltas. Existing pan assertion
continues testing real 80px movement. No test removals or fixture edits.

<!-- rpi:task id=P01-T02 -->
### P01-T02

Update expanded-map README section only: document unmodified map commands,
Shift plus and browser modifier ownership; describe added check coverage.

<!-- rpi:phase id=P02 -->
## P02: Validate and preserve local correction

<!-- rpi:task id=P02-T01 -->
### P02-T01

Depends on P01. Run extended browser check after source fix. Pre-fix proof belongs
to P01-T01, before its guard edit (PC-001). Commands run from src/api with
PYTHONPATH including this worktree's core/agents/api src and test directories.
Requested venv absent: use existing /tmp/ama-532-venv, record actual provenance.
Acquire nonblocking shared lock for heavy checks; if busy, targeted unit tests
only and explicitly mark browser/full suites not run. Otherwise run API unittest
discovery and full existing map check with pinned /tmp/ama-532-axe-4.10.3.min.js
and a new external output path. Never invoke az or full publication gate.
Inspect axe JSON for violations and incompletes. Use existing Ruff/Node checks.

<!-- rpi:task id=P02-T02 -->
### P02-T02

Depends on P02-T01. Reconcile plan markers and changes before Review. Independent
reviewer runs rpi-review exactly once; writes dated original outcome without
claiming human approval. Later findings are routed, not a second Review.
Configure repository-local privacy-safe identity from gh api user (id 8036360,
login jmservera), Conventional Commit and exact requested Copilot trailer.
Commit implementation/evidence locally; no push or PR edit. Publication gate
and human approval remain outside this correction.
