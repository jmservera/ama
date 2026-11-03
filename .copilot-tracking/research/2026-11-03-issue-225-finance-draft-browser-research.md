# Research: issue 225 constructed field draft in browser (2026-11-03, r2)

Task: issue-225-finance-draft-browser. Research disposition: reused (PR list and prior review). Planning Readiness: Ready.

## Delivered already (merged)

* #657 reader screens; #785 exception explanations; #862 AI economics; #937 browser keyboard and axe check (3 stories).

## Gap

#937 review nit and follow-up 1: the funding story has no constructed draft with conflicts, so criterion 2 (draft, conflicting candidates, reviewed evidence) is only unit-tested. The form-review view needs a server-built draft with bound documents; a routed constructed response in the view shape is the smallest honest browser fixture.

## Slice

Add one story to `src/api/checks/finance_screens_browser_check.py`. Checks and README only; no screen, server, security, infrastructure, SQL or deployment change, so the focused tier applies; the gate is left to the coordinator.
