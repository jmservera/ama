# Issue 1830 r4 plan details (2026-11-19)

Phase 1: `python3 -m unittest tools.test_rpi_preflight tools.test_rpi_gate_timing -q`; `python3 tools/rpi-preflight.py --python $(which python3) --test tools.test_rpi_checks --dry-run` (expect refusal rc 5); `find /tmp -name receipt.json`.

Phase 2: copy the per-criterion table into the research note under docs/reference/research/, add a row to `docs/reference/README.md` and an append-only entry to `docs/reference/log.md`. No secrets, no Azure, no Playwright.

Phase 3: changes, review and state artifacts; commit with trailers; no push.
