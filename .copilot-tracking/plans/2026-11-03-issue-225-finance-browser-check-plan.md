# Plan: issue 225 finance browser check (2026-11-03, r1)

Research: .copilot-tracking/research/2026-11-03-issue-225-finance-browser-check-research.md

## Phases

1. Add `src/api/checks/finance_screens_browser_check.py` from the #228 pattern: three role/screen stories (Programme Manager and Programme Support Officer on Invoice queue; Grants and Evidence Officer on Funding route and claim pack), exact phrases, AI economics Unknown rows, no controls or simulator text, labelled focusable table regions, Tab reach, reflow at 320 and 1280, no write requests, optional pinned axe.
2. Document in `src/api/README.md`; append `docs/reference/log.md` entry.
3. Focused validation: run the check with axe, ruff, mypy, finance unit tests.

## Details

* Fixture: shared `role_screens_fixtures.synthetic_data` plus one grant stage so the funding screen has a table.
* Keep read-only; no new server behaviour.

## Critique (inline, executed once)

* Risk: phrase assertions pass vacuously with content-visibility. Mitigation: scroll each panel into view before reading. Accepted.
* Risk: overclaiming accessibility. Mitigation: wording says engineering check, not WCAG/AT acceptance. Accepted.
* Verdict: proceed; no conflict with confirmed decisions.
