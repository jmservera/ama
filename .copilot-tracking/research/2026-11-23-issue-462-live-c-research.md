# Research: issue 462 third pass (2026-11-23)

Disposition: reused plus targeted new investigation. Planning Readiness: Ready.

Reused: r6 live check and r7 hosted-history note in `docs/reference/research/` (criteria 1 to 8 per-criterion tables, owner decisions of 2026-11-18). Gaps carried forward: absent `Strict-Transport-Security` on the resident app (`src/api/src/zava_forward/api/resident_demo/app.py` `HEADERS`, line 69), and the "existing local previews remain available" clause of criterion 2, never re-tested.

New work this pass: fix the HSTS gap in source with a test (full tier, no `rpi-checks.py --all`), run the resident preview and demo unit tests locally for the preview clause, re-run the read-only live header probe (no deploy, no Azure change).
