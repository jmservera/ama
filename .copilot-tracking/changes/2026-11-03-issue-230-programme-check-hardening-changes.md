# Changes: issue 230 programme check hardening

* `src/api/checks/role_screens_browser_check.py`: coordinator queue must not contain the withheld reason or sender; case record compared before and after the connected view; `scan_main` fails when there is no single main landmark (no document fallback); status text asserted with `expect()`; reflow label now says horizontal overflow, not a full WCAG 1.4.10 test.
* `src/api/README.md`: story 230 paragraph updated; Reset check labelled as corroboration of #662.
* Supersedes the stale "Original text above is preserved" note in the 2026-11-02 programme-browser-proof changes file; that file is left unedited.

## Validation

Run: `ZF_BROWSER_TESTS=1 python -m checks.role_screens_browser_check 230` (all PASS; axe skipped, PARTIAL, `ZF_AXE_JS` unset); unittest `test_programme_screen` and `test_role_screens_conformance` (21 OK); ruff check and format check; mypy with `--cache-dir=/tmp/mypy-230`.
Not run: focused gate `rpi-checks --changed`, complete gate, full suites, benchmarks, axe scan, assistive technology.
