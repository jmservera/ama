# Plan: issue 233 stage map slice

Date: 2026-11-03. Tier: focused. Research: `.copilot-tracking/research/2026-11-03-issue-233-stage-map-research.md`. Details: `.copilot-tracking/details/2026-11-03-issue-233-stage-map-details.md`.

* [x] Phase 1: add `journeyStages` and `journeyStageMap` to `role-screens.js`; render in the `programme-queue` selected-home view.
* [x] Phase 2: add a node-driven test for role-dependent links, deferral text and no new control; update trace doc and log.
* [x] Phase 3: run focused tests, ruff, mypy; commit and open a PR with Refs 233.

Critique (single pass, self-run): compatible. Links are `a` elements, only for screens installed for the role; unavailable screens and stage 1 are stated in text; no motion, colour or role simulator; hypothesis label stated in the panel.
