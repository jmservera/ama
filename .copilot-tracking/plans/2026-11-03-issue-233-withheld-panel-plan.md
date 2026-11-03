# Plan: issue 233 withheld panel slice

Date: 2026-11-03. Tier: focused (web-only, no security, infrastructure, SQL or
deployment change). Research: `.copilot-tracking/research/2026-11-03-issue-233-withheld-panel-research.md`.
Details: `.copilot-tracking/details/2026-11-03-issue-233-withheld-panel-details.md`.

* [x] Phase 1: add `screenWithheld` helper and call it from `programme-queue` and `resident-choice`.
* [x] Phase 2: replace the "absent text" guard with a presence guard; update the trace wording and log.
* [x] Phase 3: run focused tests, ruff, mypy; commit and open a PR with Refs 233.

Critique (single pass, self-run): compatible. Panel states withholding is not
authorisation, adds no control, no motion, no inline colour, no role simulator.
No human approval or consent boundary is touched.
