---
title: Issue 2186 changes 2026-11-26
description: Changes record, tier FULL (tools/ gate edit)
ms.date: 2026-11-26
---

Tier: FULL (gate tool edit); `rpi-checks.py --all` not run, the coordinator runs gates. Local commit only.

## Planned changes

* `tools/rpi-checks.py`: rubric score files become receipt-inert.
* `tools/test_rpi_checks.py`: test cases.
* `docs/reference/research/issue-2186-live-full-receipt-docs-move-2026-11-21.md` update and `docs/reference/log.md` entry.

## Completed

* `tools/rpi-checks.py`: `.github/rubric/scores/` added to `RECEIPT_INERT_PREFIXES`; `moved_path_blocker` returns "" for receipt-inert paths after the candidate-overlap check.
* `tools/test_rpi_checks.py`: two cases added.
* Docs: research note update and log entry.
* Validation: `python3 -m unittest tools.test_rpi_checks -q` 133 OK; ruff format clean; ruff check 21 findings identical to baseline (pre-existing).

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Extend BASE RELAXED to full receipts across inert main moves | Proven | `test_full_receipt_survives_only_inert_main_moves`; now also covers rubric score commits. Note: `docs/` is deliberately excluded because tests read it, so the "docs-only" wording is met for `.copilot-tracking/`, `support/` and rubric scores only |
| Relaxation recorded in receipt verify output | Proven | `test_verify_reports_docs_only_relaxation_for_full_receipt` asserts the `BASE RELAXED (disjoint-move)` line |
| Code, tool and image changes still invalidate | Proven | Same test: src code, tests, markdown, gate tool, Dockerfile, rubric scripts and mixed moves raise `Base moved on` |
| Test added | Proven | 133 tests pass |
| End-to-end verify of a real full receipt on a moved main | Unproven | Needs `rpi-checks.py --all`, forbidden for workers; coordinator gate owns it |
