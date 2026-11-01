---
title: Issue 215 regulatory alerts UX changes
ms.date: 2026-11-01
---

## Changes

* `src/api/src/zava_forward/api/web/style.css`: `.regulatory textarea{overflow-x:hidden}`.
* `src/api/checks/regulatory_ux_check.py`: assert no unresolved `color-contrast` incomplete per scanned state.
* `src/api/README.md`: 2026-11-01 update and criterion audit row.
* `docs/reference/log.md`: appended entry.

## Validation

* Browser harness with axe 4.10.3 (SHA verified): 21 states, 0 violations, 0 incompletes (before: 10 states incomplete).
* 120 unit tests OK (1 skipped) across test_regulatory_chat_api, test_rule_alerts, test_chat_panel, test_chat_isolation, test_accessibility_baseline, test_design_system, test_role_matrix, test_regulatory_ux_check.
* `ruff check .`, `ruff format --check` on the harness, `mypy` (127 files): pass.
* Local dev venv `/tmp/v215`; pip only. No complete local RPI gate run, by direction; CI is the evidence.

## Divergence

An initial scroll-into-view change was tried and removed; it did not address the cause.

## Review feedback (PR 640 Copilot threads)

* `scan()` in `src/api/checks/regulatory_ux_check.py` gained an opt-in `strict_contrast` parameter (default off) so other harnesses importing it, such as the resident assistant check with recorded `color-contrast` incompletes, are not aborted. All regulatory scans pass `strict_contrast=True`.
* Added mocked scan tests in `test_regulatory_ux_check.py`: contrast incomplete raises when strict, other incompletes and clean results pass, and contrast incompletes are only reported when not strict. 8 tests OK; ruff check and format pass.
