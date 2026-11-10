# Profile-main checkpoint changes (issue 440, 2026-11-10)

Status: implementation complete (documentation only). The skeleton was written before `implement-start`; this file records the actual results. Raw outputs: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/profile-main-440-observation-1110/` (`01-identity.txt` to `08-post-run.txt`).

Plan: [plan](../plans/2026-11-10-profile-main-440-1110-plan.md). Details: [details](../details/2026-11-10-profile-main-440-1110-details.md).

## Planned changes

* `docs/architecture/cutover-evidence-pack.md`: one new appended dated section. No earlier section altered.
* Own RPI files under `.copilot-tracking/` (research, plan, details, critique, changes, review, state).
* No other path. Shared knowledge base files, source, tests, probe, manifest, infra, tools, workflows and rubric are not changed.

## Observations (actual)

| Step | Exit and result |
| --- | --- |
| Identity | HEAD `b23c08e33e4ebdb0aaa1dfd8fa586999448d8ca6`, tree `0bdc704b78b9a3ed95926b5915ae93ae9148032d`, four blobs equal C2; fetch at 2026-11-10T18:07:12Z shows origin/main `88a17f8b6d3da6dcfcb8b0db19f481f9e257f61e` (rubric score file only) |
| A1, A2 system Python selectors | Exit 0 (6 and 16 tests) but Core resolved to the separate primary checkout `/home/azureuser/source/ama/src/core`; classified not current-main proof, preserved |
| Private venv `/tmp/ama-440-profile-venv-1110` and editable install of this worktree's `src/core`, `src/agents`, `src/api` plus `playwright==1.64.0` | Exit 0; restore after the wrong-source finding, no global or browser install |
| B1 API helper tests, B2 Core journey, scenario and perspective tests | Exit 0; 6 and 16 tests OK; modules inside this worktree |
| Admission | No lock holder, MemAvailable about 2.75 GiB, cached Chromium present |
| C1 one existing browser walk | Exit 0, 714 PASS, 0 FAIL, 38 role-screen walks, 15 negatives, 15 declared no-table walks, case `ZF-4` only, about 29 seconds |
| Cleanup | No leftover process; empty scratch `/tmp/z440p` removed; venv and ignored editable metadata retained; `__pycache__` removed |
| Documentation checks | `git diff --check` exit 0; no non-ASCII added; all section links resolve (the review link after the review file exists) |

## Divergences and amendments

* Divergence from the details plan: A1 and A2 were not missing-dependency failures. They passed but imported another checkout, so the wrong-path restore condition added by the critique applied. No other divergence.
* The pre-existing primary-checkout editable install was not used as source proof and was not modified.
* No failure, retry or repair occurred. Nothing was waived.
