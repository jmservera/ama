# Changes 2026-11-23 (issue 2186)

Planned: tools/rpi-checks.py (receipt_inert_path, ordering), tools/test_rpi_checks.py (new tests). Tier: tooling, focused; no src change; `--all` not run.

Per-criterion table: appended at implement-done.

## Implemented

* tools/rpi-checks.py: `RECEIPT_INERT_PREFIXES` and `receipt_inert_path` (only `.copilot-tracking/`, `support/`); full-receipt relaxation uses it; `moved_path_blocker` checks "also changed by the candidate" before the inert shortcut. `changed_groups` selection unchanged.
* tools/test_rpi_checks.py: full-receipt cases now reject `docs/*.md`, root `README.md`, `infra/README.md`, docs data files; allow `support/` and `.copilot-tracking/`; blocker test for a docs path changed by both sides. Without the fix 5 subtests fail; with it `python3 -m unittest tools.test_rpi_checks` runs 129 tests OK. `ruff format --check` clean.

Tier: tooling-only, focused. No src change; `rpi-checks.py --all` not run. Hosted CI for the exact head is not observed (nothing pushed).

## Per-criterion table (issue 2186)

| Criterion | Status | Evidence |
| --- | --- | --- |
| Relaxation recorded in receipt verify output | Proven | `test_verify_reports_docs_only_relaxation_for_full_receipt` (now with a support/ move) prints BASE RELAXED |
| Code, tool and image changes still invalidate | Proven | cases in `test_full_receipt_survives_only_inert_main_moves` |
| Test added | Proven | new rejected-path cases fail without the fix |
| Soundness of inert set (review finding) | Proven | docs, root and infra markdown now invalidate; candidate-changed check first |
| Real end-to-end full receipt on a docs-moved main | Unproven | needs `--all`, forbidden here; live Azure and browser proof do not apply to a local gate tool |

Consequence: docs-only main moves no longer preserve a full receipt; the speed goal for docs moves is traded for soundness.
