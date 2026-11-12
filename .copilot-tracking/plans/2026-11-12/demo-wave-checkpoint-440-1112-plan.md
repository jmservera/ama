---
title: Plan, demo wave checkpoint 440 (2026-11-12)
description: Original plan for the bounded recurring checkpoint record after the 1465/1466/1467/1468/1469/1473 wave
ms.date: 2026-11-12
---

Task `demo-wave-checkpoint-440-1112`. Research: [research](../../research/2026-11-12/demo-wave-checkpoint-440-1112-research.md). Details: [details](../../details/2026-11-12/demo-wave-checkpoint-440-1112-details.md). Critique: [critique](./demo-wave-checkpoint-440-1112-critique.md).

## Objective

Append one dated, bounded, local-only checkpoint section to `docs/architecture/cutover-evidence-pack.md` for the merged wave, with a log entry and an index pointer. No source, test, tool, workflow, requirement or ADR change. No push, issue, board or acceptance-criterion write.

## Phases

* [x] P1 Research (done, `executed`, Ready).
* [ ] P2 Plan, details and one independent pre-implementation critique of the final candidate; apply compatible findings directly.
* [ ] P3 Run the selected focused tests once each from this worktree's own venv, capture raw output outside the repository (`/home/azureuser/.copilot/session-state/676885f4-85ba-42d8-929c-40f438e5190f/files/checkpoint-440-1112/`), preserve any failure.
* [ ] P4 Write the pack section, log entry and index pointer from observed output only.
* [ ] P5 Changes record, one author Review (recorded as not independent), state, commit locally with the privacy-safe email, return the handoff.

## Selectors (one run each, no ceremonial reruns)

| Id | Component | Selector | Purpose |
| --- | --- | --- | --- |
| T1 | core | `test_ai_provider_payload_spy` | 1466 offline provider payload and manual (AI-unavailable) paths |
| T2 | core | `test_exposure_limits` | 1467 finite observations, Unknown pause |
| T3 | api | `test_finance_exposure_api` | cross-component consumer of the 1467 source (`finance.py`) |
| T4 | core | `test_ai_consumption` | neighbour of the 1468 `ai.py` change |
| T5 | api | `test_ai_consumption_api` | 1468 legacy usage settlement journey |
| T6 | api | `test_exception_register`, `test_exception_register_screen`, `test_role_screens_conformance`, `test_data_operator_ai_state` | 1469 CSV contract, escaping, fail-closed, roles |
| T7 | api | `test_live_control`, `test_live_simulator` | 1473 permit, cohort, stop, retry handoff |
| T8 | core | `test_live_readings` | simulator-side reading generator the permit gate feeds (provider-independent) |
| S0 | preflight | `__file__` of imported modules, SHA-256 of each tested file against its blob, `git status --porcelain -- src` before and after | provenance |

If a selector fails: preserve the output, classify as product, test, environment or invocation, and re-run only a failing selector once if the cause is an invocation error. A product failure is recorded as a candidate defect with reproduction, not fixed here. Skips are reported as skips. Not run: full suites, SQL Server, Docker, browser harness (`data_operator_browser_check.py`), scanners, hosted CI, any Azure or model call. Weather and finance-CSV paths named in the task statement are not present in any merged diff and are recorded as not applicable.

## Record structure

Identities, scope and exclusions; label discrepancy table; commands and results; document-qualified traceability (BRD, PRD, ADR) with local observed, Azure observed, implemented-unverified, deferred, blocked and unknown classes; boundaries (persistence, auth and roles, resident, human, manual and AI-unavailable); findings (state "none confirmed" only if the evidence supports it); recommendation with gates, independent lanes, resume conditions and human decisions; process limits. Closure of #440 is not claimed; its last two acceptance criteria stay open and original HVE behavior testing is not retroactively completed.

## Decisions and constraints

* The 1465 PROPOSED design stays candidate policy (draft/proposed) and is not acceptance evidence.
* Fresh main `5ee8ac14` differs from the pin only in `.github/rubric/scores/latest.json`; `src` is identical, so the tested source equals current main. No rebase or merge is done to refresh.
* Publication waits for #134's append and rebase; both append-only entries are preserved when integrated.
* No fix is allowed under #440; any confirmed defect is only described with the smallest proposed fix and test.
