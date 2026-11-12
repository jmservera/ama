---
title: Research, demo wave checkpoint 440 (2026-11-12)
description: Original dated research for one bounded recurring checkpoint record after the merged 1465/1466/1467/1468/1469/1473 wave
ms.date: 2026-11-12
---

## Task and disposition

* Task id `demo-wave-checkpoint-440-1112`, Refs #440 only. One bounded recurring checkpoint record appended to `docs/architecture/cutover-evidence-pack.md`. Not a new issue, feature, approval or correction pool. No source fix.
* Research disposition: `executed` (fresh git, gh and source reading). Planning Readiness: `Ready`.
* Mode: automatic (the owner's instruction is to run the full loop in order and return a frozen local candidate).

## Documents read

* `docs/case_study_48_original.md` and `docs/case_study_48_addendum.md` start-of-task read: scoped reading only, the addendum (158 KB) was searched by section rather than read end to end; stated as a limit.
* `docs/reference/README.md` (index) used for placement, `docs/reference/memory.md` read for context (not evidence).
* Latest comparable checkpoint in the pack used as the format template: "Aftercare numeric-order integrated-main checkpoint (2026-11-11 ...)" and its dated follow-up.

## Identities resolved (2026-11-12)

| Item | Finding |
| --- | --- |
| Branch and HEAD | `docs/demo-wave-checkpoint-440-1112` at `bbb1d20cc984d7c4107459485712d4b618a17afe`, clean before work |
| Fresh `origin/main` | `5ee8ac14c70f457925f3333321094e46b93373b9`, one child of the expected pin; the only path changed is `.github/rubric/scores/latest.json` |
| Trees (pin vs fresh main) | root `f0cc063601...` vs `f5348aa9b4...`; `src` `60d841010c4a` equal at both, `infra` `a022907662e2`, `tools` `432a4e8f7d74`, `.github` differs (rubric score only), `docs` `629b84683280` |
| Docs | BRD 0.21.0 `draft` `34d88395de86`; PRD 0.21.0 `in-review` `c788b917bafa`; ADR 0003 `d60645397b20`, ADR 0006 `956da1a3b804` (Accepted per earlier records); ADR 0007 `541e0f72dd2c` Proposed. None of the six PRs changes any BRD, PRD or ADR |

## Merged wave: the owner's labels do not match the actual PRs

Actual `gh pr view` data (state, merge commit, title) and `git show` diffs were read. Several labels in the task statement are wrong and are recorded as an adverse qualification, not silently corrected.

| PR | Merge commit | Actual content (read from the diff) | Task label | Match |
| --- | --- | --- | --- | --- |
| 1465 | `5df20e63982165048b3496f7b2792238aaf79128` | Documentation only: PROPOSED narrow #184 engineering design (bounded run and cost controls) in `iot-sensor-analytics-research-plan.md`, index, log and RPI evidence. No source | "#116 weather/provider-spy" | No |
| 1466 | `04e2620556b09c2f2ad61bdc2bbc281d1b0f1828` | Tests only: `src/core/tests/test_ai_provider_payload_spy.py` (596 lines), offline AI provider payload boundaries, #116 | not listed (1465 label) | Label swap |
| 1467 | `e3339de62b19a2c70a2b239b42ea3c8d51f3ee37` | Source fix: `exposure_limits.py` non-finite committed or tolerance observation becomes Unknown (pause), #99 | "target-mode proposal" and "#99 finite household finance CSV" | No: it is a core fix, not a proposal and not a CSV |
| 1468 | `f0896869d4374721d25f483c12caae9f733b6977` | Source fix `ai.py` (settle ledger, then report usage), API tests, tokenomics correction, #432 | "#432 legacy usage settlement" | Yes |
| 1469 | `71fabf00957a5e69edae7bfc9fe3ef26b101297f` | `role-screens.js` browser-built four-column exception summary CSV with formula neutralisation and fail-closed export, tests, README, browser check, #80 | "#80 exception CSV" | Yes |
| 1473 | `bbb1d20cc984d7c4107459485712d4b618a17afe` | `live_simulator.py` and `live_control.py`: recheck run control before every send attempt, `RUN_CONTROL_FENCED`, #184 stage B1 | "#184 simulator stop/retry B1" | Yes |

Consequences for the record: there is no "finite household finance CSV" PR in the wave; #99 is the exposure-limit finite check (Finance screen input, no CSV). The only candidate policy in the wave is the 1465 PROPOSED design, which stays Draft/proposed and is not executable acceptance. No 1467 target-mode proposal exists. Excluded and unmerged: 1470, 1475, local #184 minute/cohort commit `6819456`, all siblings, and any real-model, consent or cloud function.

## Source delta (src paths only)

* `core/ai.py` (1468): `self.consumption.complete(...)` now runs before the receipt carries `usage`.
* `core/exposure_limits.py` (1467): `_finite_observation` (`type is int` or finite `float`) replaces `type in (int,float) and != self`.
* `api/web/role-screens.js` (1469): `exceptionSummaryRows`, `exceptionSummaryCell`, `exceptionSummaryCsv`, `exceptionSummaryControl`; export offered only for `state == ok`, no unreadable entries, non-empty list, all ids `EX-\d{3,}`; kind and role allowlists else `Unknown`; leading `=+-@\t\r` neutralised with an apostrophe; quoting for `",\r\n`.
* `api/live_simulator.py`, `api/live_control.py` (1473): `attempt_permitted`, `_permitted`, `attempt_gate` in `send_slot` and `run`; any gate failure or exception fails closed to `FENCED`; defaults without control file unchanged; B2 cross-process fence deferred.
* Tests added or changed: `test_ai_provider_payload_spy.py`, `test_exposure_limits.py`, `test_ai_consumption_api.py`, `test_exception_register.py`, `test_exception_register_screen.py`, `test_role_screens_conformance.py`, `test_data_operator_ai_state.py`, `test_live_control.py`, `test_live_simulator.py`.
* `src/orchestrator` and `src/importer`: no change in any merged PR; no orchestrator test is impacted and none is run.

## Environment findings

* Installed `zava-forward-{agents,api,core}` are editable installs of the owner's primary checkout `/home/azureuser/source/ama/src/*`; a preflight import of `zava_forward.core.ai` resolved there. They are not used.
* An owned venv outside the repository (`--system-site-packages`, then `pip install --no-deps -e src/core -e src/api` from this worktree) imports every tested module from this worktree. No `uv`, no `PYTHONPATH=mvp`, no network dependency download.
* `/tmp/ama-rpi-heavy.lock` exists; no heavy resource (Docker, SQL Server, browser, scanner, services) is required by the selected tests, so the lock is not taken and none is used.

## Hosted state

* Hosted checks for the pin (read before writing the record, amending the earlier vague line): the only workflow run listed for `bbb1d20` is `Capstone Rubric Scorer` (success); none is listed for `5ee8ac14`. No Source CI success is claimed; an absent workflow is not a successful check.

## Open questions (carry to plan)

* Weather and "finance CSV" paths named in the task are not in the merged diffs; record as not applicable, not as passed.
* #134 may append to the log and the pack concurrently; publication waits for it.
