---
title: "Plan: #79 tie-break, policy-version and read-only archive regression"
ms.date: 2026-11-14
task_id: 79-tiebreak-version-audit-0016
---

## Objective

Add focused regression tests only. No production change.

## Phases

* [x] Phase 1: core tests `src/core/tests/test_ranking_tiebreak_audit.py`: tie-break order independent of input order, version stamping, read-only `verify` over a retained record.
* [x] Phase 2: API tests `src/api/tests/test_ranking_tiebreak_read.py`: snapshot and publication status read endpoints stamp the version and leave the archive and cases unchanged.
* [x] Phase 3: validate in `/tmp/venv-79-0016` (ruff check, ruff format --check, mypy, targeted tests, `test_scenario_manifest.py`).
* [x] Phase 4: commit with trailer, clean status, no push.

Details: [details](../../details/2026-11-14/79-tiebreak-version-audit-0016-details.md).

## Critique (single pass, direct dispositions)

* Risk: a UPRN assertion on a field that does not exist. Disposition: applied; test case-id tie-break on a shared address and document the UPRN gap.
* Risk: file overlap with PR #1585. Disposition: applied; new files only, no infra or orchestrator paths.
* Risk: mypy strict on tests. Disposition: applied; fully annotate the core test file; the API test follows the untyped sibling pattern only if `src/api` mypy config permits.
