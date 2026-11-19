---
title: Issue 2008 changes record
ms.date: 2026-11-18
---

Status: complete. Tier: focused (no `src/` change; the generator lives in `tools/`). Refs #2008, #80.

## Files

* `tools/make-demo-case-list.py`, `tools/test_make_demo_case_list.py`
* `docs/reference/research/demo-workbook/` (xlsx, csv, evidence folder with raw output, two screenshots, script)
* `docs/reference/research/issue-2008-demo-workbook-import-evidence-2026-11-18.md`, `docs/reference/README.md`, `docs/reference/log.md`

## Validation

* `python3 -m unittest tools.test_make_demo_case_list -q`: 3 tests OK.
* `ruff format --isolated --line-length 100 --check` and `ruff check` on both tool files: pass.
* mypy per project: not applicable, no `src/<project>` change. `rpi-checks.py --all`: not run by owner direction.
* Live run on `ca-cutover-test-demo-api` with Playwright (three attempts: two failed sign-in scripting attempts, then success); credentials read at runtime.
* Hosted CI: not observed (no push).

## Per-criterion table

| Criterion | Status |
| --- | --- |
| 1 Synthetic xlsx, declared structure, generator committed | Proven |
| 2 Clean, mapping and conflict rows shown in preview | Proven locally; deployed screen shows mapping and two row problems only |
| 3 Run on deployed demo with staff sign-in: mapping, conflicts, preview, source unchanged, evidence retained | Partly proven: mapping, rows to fix, source hashes unchanged, screenshots and raw output retained; conflicts and row-level xlsx preview not available on the deployed demo (no xlsx upload or conflict check; needs a full-tier src change) |
| 4 Walkthrough note | Proven |

## Incident

An earlier diagnostic `sed` displayed the demo test password in tool output; no file holds it. Reported for owner rotation decision.
