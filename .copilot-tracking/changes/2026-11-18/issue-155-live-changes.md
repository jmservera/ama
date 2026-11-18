---
title: Issue 155 live changes
ms.date: 2026-11-18
---

Docs only; no source changed. Tier: focused. Refs #155.

Files: research note `docs/reference/research/issue-155-live-usability-programme-evidence-2026-11-18.md`, index row in `docs/reference/README.md`, log entry in `docs/reference/log.md`, evidence under `.copilot-tracking/evidence/2026-11-18/issue-155-live/`.

## Per-criterion table

| Criterion | Proven for demo? | Basis |
| --- | --- | --- |
| Test plan names tasks, participants, accessibility support, consent, data handling | Proven (already ticked) | Plan file present; 15 core usability tests pass |
| Task scripts derive from journey contract and bundles | Proven (already ticked) | Same |
| Measures aggregate only; audit-use statement agreed with staff first (SA-010) | Unproven | Code gate refuses unagreed runs and tests pass, but staff agreement needs named human staff; production-only. Route probes uninformative (control also 403) |
| Findings logged with severity and linked to backlog | Proven (already ticked) | Code and plan present |
| Negative and inconclusive outcomes; synthetic walkthroughs labelled | Proven (already ticked) | Plan states the label |

## Validation

* `python3 -m unittest tests.test_usability_programme -q` in `src/core` (PYTHONPATH=src:tests): 15 tests OK (raw output not retained).
* Live Playwright read-only run: sign-in succeeded (`/api/me` returned the test role), but the screenshot shows the signed-out landing page; no claim is made about workbench strings.
* mypy and ruff: not applicable, no Python source under `src/` or `infra/` changed.
* Hosted CI and independent review: not run here; coordinator publishes.
