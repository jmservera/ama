---
title: Legacy-Reference Checker Exemption and Live Health, Issue 203, 2026-11-18
description: Checker exemption for regression-test files and dated live-evidence notes, with per-criterion proven and unproven results for the two unticked issue 203 criteria.
ms.date: 2026-11-18
---

Refs #203. Demo scope (desktop, synthetic data); live Azure authorised under resource group `ama`. No secrets were read and no resource was created.

## Change

`tools/check-legacy-references.py` now treats three regression-test files (`test_epic_legacy_path_retirement.py`, `test_epic_parity_matrix_old_paths.py`, `test_private_mvp_data_exclusion.py`) as guard files, and dated live-evidence research notes (`issue-N-...` or `src-repoint-...` with a date, file or evidence folder) as records. A unit test shows undated research notes and dated notes outside that prefix are still flagged.

## Results

| Command | Before | After |
| --- | --- | --- |
| `python3 tools/check-legacy-references.py` | exit 1, 47 reference violations | exit 0, 0 reference and 0 link violations |
| `python3 -m unittest tools.test_check_legacy_references` | 7 tests, 1 failure | 8 tests, OK |
| `ruff check` and `ruff format --isolated --line-length 100 --check` | n/a | pass |

## Per-criterion table

| Criterion | Status | Why |
| --- | --- | --- |
| 1. Search returns only intentional historical references naming the archive tag; old package name only in dated records | Unproven (literal) | The checker now passes, but only through documented exemptions for guards, generated records and dated notes. The owner comment of 2026-11-17 says the literal criterion needs owner agreement; guards are not removed. |
| 5. Deployed app and CI green from `src/` | Partly proven, not ticked | Live: `ca-cutover-test-demo-api` revision `0000032` Running, `/healthz` 200 on it and on `ca-resident-demo`; `Source projects CI` success on the latest five pull-request runs. Unproven: the running image digest `sha256:5368f4e4...` is in a private registry with no build-provenance link to `src/`, and the workflow is pull-request only, so no push run on `main` exists. |

Criteria 2, 3 and 4 were already ticked and are untouched.
