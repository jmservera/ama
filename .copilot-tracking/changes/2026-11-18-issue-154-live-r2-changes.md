---
title: Changes for #154 live resident and representative UX proof, round 2
ms.date: 2026-11-18
---

## Changes

* Added `docs/reference/research/issue-154-live-resident-ux-audit-r2-2026-11-18.md`.
* Added evidence under `.copilot-tracking/evidence/2026-11-18/issue-154-live-r2/`.
* Updated `docs/reference/README.md` (index row) and `docs/reference/log.md` (entry).
* Round 1 files and state are untouched. No `src/`, `infra/` or workflow change; no Azure resource created or changed. Tier: FOCUSED.

## Per-criterion table

| Criterion | Result |
| --- | --- |
| 1. Journey designs cover choice, pause or withdrawal, appointments, commitments, handover, complaint (ticked) | Partly proven live: choice, pause or withdrawal and update commitment on the workbench Resident choice screen; appointments, handover and complaint status not seen in a resident-facing view |
| 2. Non-digital alternative, language, literacy, adjustment (ticked) | Partly proven: non-digital routes (round 1); language and adjustment content absent from the showcase |
| 3. Representative views task-limited and expiring (ticked) | Unproven live (no case has a representative); local 53-test run retained |
| 4. Offers distinct from commitments (ticked) | Partly proven: "not recorded" wording on Resident choice screen; no offer displayed on the resident showcase |
| 5a. No live resident contact (unticked) | Proven for the demo; no network trace |
| 5b. Usability programme validation (unticked) | Unproven; cannot be for the demo; stays unticked |

## Validation (FOCUSED; docs and evidence only)

* `git diff --check`: clean. Relative links in the new note resolve. Credential values searched in the note, r2 evidence and r2 artifacts: no hits (values not printed). Ids, emails and names redacted in retained JSON; the retained resident screenshots mask ids and addresses; workbench screenshots were removed.
* From `src/api`: the two unittest modules, 53 tests OK; raw output retained in `local-tests-raw.txt`.
* mypy, ruff and `rpi-checks.py` not applicable (no Python source under `src/` or `infra/` changed); `rpi-checks.py --all` not run, by instruction.
* Disclosed: the first two screenshot runs captured only the welcome page because the workbench is at `/app`; the first audit also hit the same page. Evidence scripts were rerun and only the final outputs are retained. Address masking is regex-based and best effort.
