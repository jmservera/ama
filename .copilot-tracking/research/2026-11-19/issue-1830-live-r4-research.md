# Issue 1830 r4 research (2026-11-19)

Research disposition: reused (r3 note `docs/reference/research/issue-1830-live-r3-2026-11-19.md` plus fresh re-check). Planning Readiness: Ready for a no-code outcome.

Question: does any unticked criterion of #1830 remain buildable or provable for the synthetic desktop demo?

Findings:

* Criterion 1 needs retained receipts from comparable host, head and base. `/tmp` holds no `receipt.json` and no `rpi-*` directory now, so even the r3 analyzer inputs are gone. The analyzer `tools/rpi-gate-timing.py` and its tests exist.
* Criterion 2 needs preflight to execute selected repository tests, browser wrappers and SQL. `tools/rpi-preflight.py` refuses all of that by design after five correction cycles (issue comment, candidate a2c27fda). Enabling it changes a security control: FULL tier and an owner trust or isolation choice. No such decision is recorded.
* Criterion 3 depends on criterion 2 and on an implemented optimization; none exists.
* Criterion 4 needs a pull request, exact-head review and hosted CI, which this lane may not open.

Verdict: no demo-buildable criterion. Azure, Playwright and src changes are not applicable.
