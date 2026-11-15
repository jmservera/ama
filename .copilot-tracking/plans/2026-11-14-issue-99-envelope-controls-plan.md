# Issue #99 plan

1. Accept canonical `approved_by` and `approved_at` (date or ISO timestamp), keep legacy aliases, require both, no defaults.
2. Add `pause_signal` (paused, decision_required, decision_owner, automatic_cut=False, reason) to every assess result and every Held result (`held()` helper reused by finance.py).
3. Add focused unit tests; run targeted tests, ruff, mypy only.
Critique: single pass, compatible change kept additive; legacy fields preserved for API tests.
