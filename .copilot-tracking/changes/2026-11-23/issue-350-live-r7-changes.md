# Issue 350 r7 changes (2026-11-23)

Files: `tools/check-edge-anonymous-401.py`, `tools/test_check_edge_anonymous_401.py` (3 tests pass, ruff clean), `docs/reference/research/issue-350-live-r7-2026-11-23.md` plus `edge-probe.json`, index and log entries. No `src/` change; tier FOCUSED. No divergences.

| # | Criterion | Result |
| --- | --- | --- |
| 1 | Anonymous protected API 401 with browser UA, page redirect kept | Unproven live: edge returns 302 (tool exit 1); app side proven by test_auth; tool now repeats the measurement |
| 2 | All dated rows and 16 assets with authorised roles | Unproven (needs second role and write journeys) |
| 3 | Continuing synthetic baseline | Partly proven in r6; restore authorisation not visible |
| 4 | Model deployment, release authority, assistants | Partly proven in r6; human decision outstanding |
| 5 | Licensed map provider | Partly proven in r6; licence unproven |
| 6 | Delegated photo tokens | Unproven (consent required) |
| 7 | Law store seeded | Partly proven; 0 sources, human-owned |
| 8 | Ledger, document, digest durability | Partly proven in r6 |
| 9 | Time capture gated | Proven for the demo (r6) |
| 10 | Per-role results | Unproven (one role only) |
