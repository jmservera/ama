# Changes: #134 extension E2

Start head b2d27335403db184fa686125d307c997de228c75 (unchanged ancestry). Files: connected_home_browser_check.py, test_connected_home_check.py, these tracking files.

## Renderer to inventory mapping (role-screens.js)

| Screen | Record (scanned) | Audited other |
| --- | --- | --- |
| asset-board | Stock conflict comparison, Eligibility | Evidence boundary, queue across homes, Missing investment inputs, Benefits and phase check, Portfolio scope, two Ledger-wide panels |
| programme-queue | Connected view for (dynamic) | Evidence boundary, Shared queue, Lifecycle and funnel |
| technical-queue | Source facts, Design version, Separate sign-offs, Returns and routing, Missing references | Evidence boundary, Technical readiness |
| resident-choice | Choice for each measure, Paused or withdrawn, Linked update commitment, Service requests | Evidence boundary, portfolio commitments, Choice comes before offered capacity |
| quality-queue | Handover readiness, Quality evidence, "Measure: State" (dynamic) | Evidence boundary |
| finance-invoices | Invoice line comparison | Evidence boundary, Invoices waiting, AI economics |

## Regression and failing-before

New pure tests: Source facts with the real ZF-1 query id (read from the snapshot, literal title) is rejected while legitimate ZF-2 expectations pass; a renderer audit fails if a screenPanel literal is in neither list. With Source facts removed from the inventory in memory, the full class gave failures=2 (before.err), the two new tests. Browser: Technical control now injects into Source facts.

## Commands, full raw output under /tmp/z134/e2 (name.out, name.err, name.exit)

| Name | Exit |
| --- | --- |
| unit (python -m unittest -v tests.test_connected_home_check, 10 tests) | 0 |
| ruffcheck / ruffformat / mypy | 0 / 0 / 0 |
| before (failing-before demonstration) | 0 (script), 2 test failures recorded |
| browser (flock -n -E99 timeout 900 python -m checks.connected_home_browser_check, once) | 0; 139 PASS; empty stderr |

Adverse attempts retained: unit-attempt1 (exit 1: my audit test wrongly included the hazard screen block) and ruffcheck-attempt1 (exit 1: one over-long comment); both fixed before the browser run, not browser reruns. E1 log browser-e1.log untouched.

Browser identity: Chromium 156.0.8078.4 as reported by browser.version. Playwright 1.64.0. Axe not run.

## Limits

Unchanged: six screens, five logins, Asset proxy, no rows 6/7/8/11, intake, aftercare, event order, AT, approvals. R1 (A4 reading of ZF-2) unresolved. No criterion ticked; no #134, #233 or #149 closure.
