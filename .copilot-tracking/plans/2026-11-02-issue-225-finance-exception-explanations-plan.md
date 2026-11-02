# Plan: issue 225 finance exception explanations (2026-11-02)

Research: .copilot-tracking/research/2026-11-02-issue-225-finance-exception-explanations-research.md

## Phases

1. Add `financeExplain` table and `financeExceptionPanel` to `role-screens.js`; render inside each invoice block.
2. Extend `test_finance_grants_screens.py`: grouped explanations, unknown code, unchecked invoice, structural keyboard checks.
3. Update atlas trace row and knowledge-base log (no src/api README note: behaviour is within the existing screens).
4. Validate with `tools/rpi-checks.py --changed --base origin/main --lock-timeout 3300`; commit, push, PR with Refs #225.

## Critique (inline, one pass, executed once)

* Risk: explanations read as decisions. Mitigation: every row names the human decider and says the match is not a payment decision. Accepted.
* Risk: invoice-level exceptions duplicated per line. Mitigation: group by code and message, list lines. Accepted.
* Risk: unknown future codes. Mitigation: Unknown fallback text. Accepted.
* Risk: over-claiming WCAG. Mitigation: structural check only; criterion 4 stays Refs. Accepted.
