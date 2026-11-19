# Issue 1830 r4 research (2026-11-19)

Disposition: executed (re-verification). Planning Readiness: Ready for a no-source outcome.
Scope: synthetic demo, desktop only, FOCUSED tier. No live Azure or Playwright needed (no web UI).

Evidence: `python3 -m unittest tools.test_rpi_preflight tools.test_rpi_gate_timing -q` gives 54 tests OK.
`tools/rpi-preflight.py --test tools.test_rpi_checks --dry-run` exits 5 (REFUSED by design; no verified capability policy or isolation).
No retained full receipt matches `/tmp/rpi-*full*`. `tools/rpi-preflight.py` and `tools/rpi-checks.py` are unchanged since r3.

Result: criterion 2 needs an owner trust-boundary decision (security control, FULL tier); criterion 1 needs receipt data that is gone and queue wait that receipts do not record; criterion 3 has no optimization to benchmark; criterion 4 needs a PR and hosted CI, which are barred. Nothing buildable for the demo.
