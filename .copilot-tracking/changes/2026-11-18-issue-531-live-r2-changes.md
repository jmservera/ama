# Changes: issue #531 live verification r2 (2026-11-18)

Docs and evidence only. Added: docs/reference/research/issue-531-live-r2-2026-11-18-note.md and folder issue-531-live-r2-2026-11-18/ (scripts, delta JSON; screenshot not retained); index and log entries. No src change; Focused tier.
Per-criterion table: see the note (copied below once written).

| # | Criterion | Result |
| --- | --- | --- |
| 1 | Loading states, live region, hint, retry | Proven live (timing/retry simulated in browser) |
| 2 | Cold start without blank page | Simulation proven; real cold start unproven (no scale-to-zero in 10 min, forcing excluded) |
| 3 | AI/rules/source distinction, HAX note | Rules path proven live; AI path unproven live |
| 4 | Outcome wording, boundary unchanged | Proven live incl. one recorded reject; approve/edit submit not run |
| 5 | Sources, refresh time, unverified label | Sources and time proven; unverified label simulated only |
| 6 | axe, no AT claim | axe 0 violations (earlier run); AT not claimed |
| 7 | Live verification recorded | Proven for demo build with stated limits |

Validation (Focused): git diff review; literal secret scan of evidence folder (no match); no src change so no mypy/ruff/unit tests; rpi-checks not run. Divergence: tracked state file `issue-531-live-state.json` from an earlier session was overwritten (history in git); witness `implement-start` first refused (state lacked changes path), then passed after correction. Residue: one rejected review record on a synthetic case.
