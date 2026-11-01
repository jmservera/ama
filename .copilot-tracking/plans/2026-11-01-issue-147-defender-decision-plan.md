# Issue 147 plan (2026-11-01)

1. Add infra/defender-decision.json (owner, plans, billable inventory, cost status, activation state).
2. Add tests in infra/tests/test_governance.py tying the record to governance.bicep defaults.
3. Link record from infra/README.md governance section.
4. Focused validation: infra governance tests, ruff check and format on the test file.

Critique (single pass): do not fabricate prices; keep activation false; do not claim criterion 1. Applied directly.
