# Details: issue 114 live re-verification (2026-11-23)

* Phase 2 test: seed a Store with 40 current-year entries by actor `alice-private-actor`, call `verify_ledger_before_reliance(current_year=2026, seal_past_years=False)`; assert reliance allowed, no `year-*.json` files created, and the JSON-serialised report contains neither the actor nor the reference.
* Phase 4: note `issue-114-live-reverify-2026-11-23.md` plus the retained probe script, job log and local test output in the same-named folder.
