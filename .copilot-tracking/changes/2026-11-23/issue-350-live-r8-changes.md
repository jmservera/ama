# Issue 350 r8 changes (2026-11-23)

Files: `infra/tests/test_bicep_policy.py` (new `test_easy_auth_never_exempts_api_paths`; passes, fails under an `/api/me` exclusion mutation; 3 pre-existing ruff findings unchanged, format clean), `docs/reference/research/issue-350-live-r8-2026-11-23.md` plus `edge-probe.json`, index and log. No `src/` change; tier FOCUSED. No divergences.

| # | Criterion | Result |
| --- | --- | --- |
| 1 | Anonymous protected API 401 with browser UA, page redirect kept | Unproven live: edge 302 (probe exit 1); guard test added |
| 2 | All dated rows and 16 assets with authorised roles | Unproven (second role, write journeys) |
| 3 | Continuing synthetic baseline | Partly proven (r6); authorisation not visible |
| 4 | Model deployment, release authority | Partly proven (r6); human decision outstanding |
| 5 | Licensed map provider | Partly proven (r6); licence unproven |
| 6 | Delegated photo tokens | Unproven (consent) |
| 7 | Law store seeded | Partly proven; human-owned |
| 8 | Ledger, document, digest durability | Partly proven (r6) |
| 9 | Time capture gated | Proven for the demo (r6) |
| 10 | Per-role results | Unproven (one role) |
