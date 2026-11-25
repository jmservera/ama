# Details: issue 107 r13

Phase 1 reuses heldout_batch.authorization_problems, worst_case_usd, _usage, _cost, dry_run_call. Five assistant IDs from the live listing. One synthetic case-free prompt each. Outcomes: refused, blocked, completed, stopped-at-cap, stopped-bad-usage.
Phase 2 tests cover each outcome with a counting provider double; the double must stay at zero calls when refused.
