# Research: issue 225 finance browser evidence (2026-11-03, r1)

Task: issue-225-finance-browser-check. Research disposition: executed (PR and repo inspection). Planning Readiness: Ready.

## Delivered already (merged)

* #657: Invoice queue and Funding route and claim pack reader screens, line comparison, conflicts, readiness view (criteria 1 to 3).
* #785: plain-language exception explanations.
* #862: AI economics section on both screens (tokenomics criterion, design only).
* #490 and #824 closed unmerged; superseded.

## Gap

The prior review (2026-11-03 ai-economics) routes the browser keyboard and axe run as follow-up 1; criterion 4 has only structural unit tests. `src/api/checks/` has browser checks for sibling role screens (#226, #228) but none for finance. Chromium and Playwright are present locally; pinned axe 4.10.3 file matched SHA-256 880970c8...

## Slice

Add `checks/finance_screens_browser_check.py` reusing the #226 shared fixture. Frontend and checks only; no security, infrastructure, SQL or deployment change, so the focused tier applies and the gate is left to the coordinator.

## Boundaries

Desk-hypothesis screens; no submission, award or payment inferred; no simulator; AI-unavailable behaviour is already covered (reports unreadable show Unknown).
