# Issues 225 and 226: local mandatory-action source gap research

Scope: #225 (Finance and grants screens) and #226 (Asset executive and board views) only. Tracking-only, documentation-only. Child of frozen parent b9d7db29b (feat/demo-home-parent-0555, PR1504); main baseline 15bfee2d7 is distinct from the qualified parent read-only display.

## Read manifest

* Demo run ledger (exact path given by the caller): lines 350-359, 6548, 6609, 7323, 7856, 7889 read; the rest of the file not read (budget).
* Live readback 2026-11-13 of both issue bodies and the latest comment on each.
* Source file existence check only (no test execution): `src/api/checks/finance_screens_browser_check.py`, `src/api/checks/role_screens_browser_check.py`, `src/api/tests/test_asset_board_screen.py`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/core/src/zava_forward/core/stock.py`.
* Specs, index, memory and component guides were not reread in the five-minute budget; this is a stated partial reading, not a pass.

## Per-AC disposition

| Issue | AC | Disposition | Evidence |
| --- | --- | --- | --- |
| 225 | 1 invoice queue | Delivered, checked | Issue comment 2026-11-04 cites #657, #785, #862, #937, #978; source `finance_screens_browser_check.py`, `role-screens.js` |
| 225 | 2, 3 funding route, safe endpoint | Delivered, checked | Same comment |
| 225 | 4 WCAG 2.2 baseline | Unmet; human AT and review only | Comment 2026-11-04: keyboard, reflow and axe checks merged (#937), conformance needs #151/#155 |
| 225 | 5 design system | Delivered, checked | Same comment |
| 225 | tokenomics design | Delivered, checked; draft proposal, no price or budget | Issue body |
| 226 | 1-3 asset queue, unknowns, no approval | Delivered, checked | `test_asset_board_screen.py`, `role-screens.js`; body |
| 226 | 4 WCAG 2.2 baseline | Unmet; human AT and review only | Comment 2026-11-05 (closure audit batch 015) |
| 226 | 5 design system | Delivered; the older unmet comment is stale | Comment 2026-11-05: #960, #1129 |
| 226 | tokenomics design | Delivered; evidence class preserved (#870) | Comment 2026-11-05 |

Unknown: per-criterion merged blob hashes were not retrieved in the budget; PR numbers are cited from issue comments, not re-verified.

## Increment decision

No independent initial local engineering increment is required by these ACs. The ledger already records the same finding (finance and asset-role source delivered, only human AT/WCAG remains); this lane is stopped and not repeated. The held and known items in the caller brief (184, c71, B1/1473/1288/1331, 74b9, 891, 531, 144/189, 146, 96, AI bdec, 440) were not examined or rediscovered. Scope 440 does not apply to this assignment.

## Resume condition

Resume only if #151/#155 AT and WCAG evidence exists, or a new source-proven gap appears in the finance or asset screens. Any future implementation needs actual authority, ready inputs, overlap and ordering checks, and an exact-head assessment against the frozen parent or a merged main.

## Phase boundaries

Research reused; Plan, critique, implementation and Review not executed because no slice exists. No gates, tests, Azure, spend, issue edits, AC ticks, push or PR.
