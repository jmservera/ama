# Issue 116 review fixes: plan

1. Gate contact outcome in `cites_for` on `reason_ok` (channel otherwise).
2. Gate appointment outcome in `capture` on every capability role having a recorded need; otherwise status values only.
3. Make `hold_notes` recursive over note keys, contact outcomes and non-status appointment outcomes; apply status-only to contractor detail.
4. Canary tests for list, export, search, case, briefing and visits views, plus citations and assistant source.

Critique: executed once; compatible findings applied (appointment status enum retained so proactive eligibility still works).
