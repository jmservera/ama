---
title: Changes for #154 live resident and representative UX proof
ms.date: 2026-11-18
---

## Changes

* Added `docs/reference/research/issue-154-live-resident-ux-evidence-2026-11-18.md`.
* Added evidence under `.copilot-tracking/evidence/2026-11-18/issue-154-live/` (two scripts, two JSON files, three PNGs, including `03-workbench-landing-signed-out.png`, which shows the signed-out landing page and not a signed-in workbench view).
* Updated `docs/reference/README.md` (index row) and `docs/reference/log.md` (entry).
* No `src/`, `infra/` or workflow change; no Azure resource created or changed. Tier: FOCUSED.

## Per-criterion table

| Criterion | Result |
|-----------|--------|
| Journey designs cover choice, pause, appointments, commitments, handover, complaint (ticked) | Not re-proven live; showcase is a read-only subset |
| Non-digital alternative, language and adjustment support (ticked) | Non-digital routes observed live; language and adjustment support not exposed |
| Representative views task-limited and expiring (ticked) | Not provable live (no case has a representative); local expiry tests pass (raw output not retained) |
| Offers distinct from commitments (ticked) | Not re-proven live (showcase makes no offers) |
| No live resident contact (unticked, part 1) | Proven for the demo |
| Designs validated through the usability programme before use (unticked, part 2) | Unproven; needs participants and SA-010 staff agreement; criterion stays unticked |

## Validation (FOCUSED; docs and evidence only)

* `git diff --check`: clean. Relative links in the new note resolve. Credential values searched in all #154 artifacts and evidence files: no hits (values not printed).
* From `src/api`: `python3 -m unittest tests.test_representative_expiry_api tests.test_resident_demo_api -q` with the documented PYTHONPATH: 53 tests, OK (raw output not retained). The `src/` and `infra/` outbound-library search output is also not retained.
* mypy, ruff and `rpi-checks.py` not applicable: no Python source under `src/` or `infra/` changed; `rpi-checks.py --all` not run, by instruction.
* Witness note: the first `implement-start` call was refused (state lacked the changes path); after recording it the retry succeeded with the qualification that the worktree was already dirty (research note and evidence predate it). Both outcomes are kept in the witness log.
