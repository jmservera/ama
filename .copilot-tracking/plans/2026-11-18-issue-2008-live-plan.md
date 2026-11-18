---
title: Issue 2008 plan, synthetic demo workbook and live import proof
ms.date: 2026-11-18
---

## Scope

Focused tier, no `src/` change. Refs #2008, #80.

## Phases

* [x] Phase 1: generator `tools/make-demo-case-list.py` using `zava_forward.importer.xlsx.write_workbook`; committed workbook and CSV export under `docs/reference/research/demo-workbook/`; test `tools/test_make_demo_case_list.py` (deterministic, sha stable, preview shows clean, mapping, problem and duplicate-conflict rows, source unchanged).
* [x] Phase 2: local raw preview output via `python -m zava_forward.importer preview`.
* [x] Phase 3: live run on `ca-cutover-test-demo-api` with Playwright and the staff test sign-in (credentials read at runtime, never printed); retain raw API output and distinct labelled screenshots; ids redacted; file hash before and after.
* [ ] Phase 4: research note `docs/reference/research/issue-2008-demo-workbook-import-evidence-2026-11-18.md` (walkthrough, per-criterion table), index and log entries.
* [ ] Phase 5: review, commit.

Details: [details](../details/2026-11-18-issue-2008-live-details.md).
