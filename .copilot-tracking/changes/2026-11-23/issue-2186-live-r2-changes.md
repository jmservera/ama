# Changes 2026-11-23 r2 (issue 2186)

Planned: tools/test_rpi_checks.py (one regression case). Tier: tooling, focused; no src change; `--all` not run.
Per-criterion table: appended at implement-done.

## Implemented

* tools/test_rpi_checks.py: one case in `test_full_receipt_survives_only_inert_main_moves` pinning that `docs/presentations/x.pptx` invalidates a full receipt (repo-wide secrets, legacy-reference and preflight scans read every tracked file). `python3 -m unittest tools.test_rpi_checks`: 129 tests OK; `ruff format --check` clean; `ruff check` reports 8 pre-existing SIM117 findings, identical without this change. No src change; `rpi-checks.py --all` not run; hosted CI not observed (nothing pushed).
* Witness note: the edit landed in the same step as the implement-start witness call, so the witness recorded a dirty source qualification.

## Per-criterion table (issue 2186)

| Criterion | Status | Evidence |
| --- | --- | --- |
| Relaxation recorded in receipt verify output | Proven | `test_verify_reports_docs_only_relaxation_for_full_receipt` passes (129 OK) |
| Code, tool and image changes still invalidate | Proven | cases in `test_full_receipt_survives_only_inert_main_moves` incl. the new binary-docs case |
| Test added | Proven | merged tests plus the new case |
| Docs subtree inert for full receipt (speed goal) | Unproven, unsafe | repo-wide scans read all tracked files; see research |
| End-to-end full receipt on docs-moved main | Unproven | needs `--all`, forbidden; Azure, browser, billing proof not applicable |
