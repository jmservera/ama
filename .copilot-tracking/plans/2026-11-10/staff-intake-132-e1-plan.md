---
title: Staff intake 132 extension E1 plan
ms.date: 2026-11-10
---

Extension E1 of five. Research: `.copilot-tracking/research/2026-11-10/staff-intake-132-e1-research.md` (Ready).

## Phases

* [ ] Phase 1: red evidence. Reproduce the two project mypy errors (done in Research, `/tmp/zf132-e1-mypy-red.log`).
* [ ] Phase 2: fix `correction` return annotation and `view` return typing in `src/api/tests/test_staff_intake_api.py` only.
* [ ] Phase 3: green. Project `mypy` from `src/api`, `ruff format --check` and `ruff check` on the file, targeted intake unit tests (SQLite and JSON stores) and the impacted role-inventory test on the merged tree.
* [ ] Phase 4: one Review, changes record, state, commit, frozen local handoff.

## Success criteria

* Project mypy exits 0 over 228 files with the pinned toolchain.
* Intake unit tests pass; skips listed with reasons.
* Diff to the C5 candidate source is limited to the merge plus the test annotation; intake source files are unchanged.

## Out of scope

Behaviour change, UI, SQL, browser, models, cloud, accounts, permissions, consent, AC5, sibling or parent work.
