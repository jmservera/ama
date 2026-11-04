<!-- markdownlint-disable-file -->
# Plan: Resident demo UX redesign (Refs #462)

Research: [research](../../research/2026-11-04/resident-demo-ux-462-research.md). Details: [details](../../details/2026-11-04/resident-demo-ux-462-details.md).

## Phases

* [ ] Phase 1 (PR 1, branch `feat/resident-demo-ux-redesign`): sign-in loading, icon-only Account, view contract (`stage`, `documents`, `summary`), section hierarchy, sticky nav, timeline, documents, funding, rules summary, optional consented AI summary.
* [ ] Phase 2 (PR 2, branch `feat/resident-demo-sensors-forecast`, based on PR 1, target `main`): sensors below help, deterministic 24h synthetic forecast, stale/fault/empty states, SQL stock link fix.

## Validation (focused tier)

`python3 tools/rpi-checks.py --changed`; from `src/api`: unit tests, `ruff check`, `ruff format --check`, `mypy --cache-dir=/tmp/mypy-462ux`; local Playwright checks for the resident app where Chromium runs.

## Single-pass critique (recorded once, applied directly)

| Finding | Disposition |
| --- | --- |
| Spec proposes `summary` in `GET /demo/view`; rules summary must come only from allowlisted fields. | Accepted. Built in `showcase_view` from already allowlisted values; test asserts no `case_id`/`provenance`. |
| Spec slice 3 calls assistant with topic `status`; the AI path reuses the existing endpoint and label strings. | Accepted. No new route, so `test_role_endpoint_inventory.py` unchanged. |
| Spec lists `Funding` and `What is needed` copy that could imply decisions. | Accepted with spec wording only; no payment or consent controls. |
| Spec puts AI summary and rules summary labels as exact phrases. | Accepted. Labels `Summary by rules. Not an instruction.` and `AI suggestion, not approved. Not an instruction.` |
| Forecast formula uses diurnal harmonic from backfill. | Phase 2 uses the simpler trailing mean plus clamped drift with the same eligibility rules; the formula is deterministic and labelled an estimate. |
| SQL fix cannot be compiled locally. | Accepted risk; text-level source tests only, stated plainly. No live apply. |

No critique advice conflicts with a confirmed owner decision. Critique executed once; verdict: proceed.
