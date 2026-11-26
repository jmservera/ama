---
title: Issue 2186 Live, Full Receipt Across Docs-only Main Moves
description: Per-criterion evidence and the defect fixed so a full gate receipt survives inert origin/main moves
ms.date: 2026-11-21
---

Source head: `dd8df9631a` (origin/main). Evidence: local unit tests, no Azure or browser surface (the change is a gate tool).

## Finding

`validate_receipt` in `tools/rpi-checks.py` refused any moved base unless the receipt scope was `partial`, so a full receipt died on every docs commit. That defect is fixed: a full receipt now relaxes when origin/main moved as a fast-forward and every moved path is inert (`docs/`, `.copilot-tracking/`, `support/`, markdown outside `src/`). Any other moved path, including code, tests, workflows, `tools/` and Dockerfiles, still raises `Base moved on <path>`.

## Residual risk

Tests read `docs/` (for example `src/core/tests/test_live_doc_links.py` scans every live markdown file), so a docs move can break the merged result even though the gated head passes. The receipt never tested the merge with the moved base; the existing partial relaxation carries the same exposure. Hosted CI on the merged head remains the check for it.

## Criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Extend BASE RELAXED to full receipts when main moved only inert paths | Proven | `test_full_receipt_survives_only_inert_main_moves`: docs and tracking moves reach tool identity (accepted past the base check) |
| Relaxation recorded in receipt verify output | Proven | Existing `test_verify_requires_stack_member_and_reports_relaxation` asserts the `BASE RELAXED` line; the same `base_relaxation` result feeds it for full receipts |
| Code, tool and image changes still invalidate | Proven | Same test rejects src code, src tests, src markdown, `tools/rpi-checks.py`, `src/api/Dockerfile` and a mixed move with `Base moved on`; identity digests of matrix and helper are unchanged |
| Test added | Proven | `python3 -m unittest tools.test_rpi_checks -q`: 119 tests pass |
| End-to-end verify of a real full receipt on a docs-moved main | Unproven | No full receipt was produced; `rpi-checks.py --all` is not run in this task |

## Update 2026-11-22

Added `test_verify_reports_docs_only_relaxation_for_full_receipt`, which drives `verify()` for a full-scope receipt after a docs-only move and asserts the `BASE RELAXED (disjoint-move)` line with the moved-path count. `python3 -m unittest tools.test_rpi_checks -q`: 124 tests pass. The verify test stubs `validate_receipt`, so the end-to-end verify of a real full receipt stays unproven (`rpi-checks.py --all` is not run).

## Update 2026-11-22, second run

No source edit was needed. `python3 -m unittest tools.test_rpi_checks -q` ran 127 tests, all OK, and `ruff format --isolated --line-length 100 --check` is clean for `tools/rpi-checks.py` and its test file. The four criteria keep the statuses above; the end-to-end verify of a real full receipt stays unproven because `rpi-checks.py --all` is not run. Record: `.copilot-tracking/changes/2026-11-22/issue-2186-live-r2-changes.md`.

## Update 2026-11-26

Probe of `origin/main` (79937c1cc8): the newest move, cc7caafefb to 79937c1cc8, touches only `.github/rubric/scores/latest.json`, and 29 of the first-parent commits since 2026-11-23 are `chore(rubric): record score` commits. That path was neither inert nor mapped, so a full receipt died on each of them. No gated test or check reads the score files (the rubric scripts sit outside the `rpi-checks.py` matrix; `tools/rename-zava-tests.py` only matches the path string), so `.github/rubric/scores/` is now receipt-inert in `RECEIPT_INERT_PREFIXES`, and `moved_path_blocker` returns early for receipt-inert paths after the candidate-overlap check. `docs/` stays excluded because tests read it. The test `test_full_receipt_survives_only_inert_main_moves` gained a score-file case (accepted) and a `.github/rubric/scripts/prepare.py` case (rejected). `python3 -m unittest tools.test_rpi_checks -q`: 133 tests OK; `ruff format --isolated --line-length 100 --check` clean; `ruff check` reports the same 21 pre-existing lines before and after. The end-to-end verify of a real full receipt stays unproven (`rpi-checks.py --all` is not run, tier FULL receipt belongs to the coordinator).
