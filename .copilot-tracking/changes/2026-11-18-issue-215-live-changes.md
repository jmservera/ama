# Changes: issue 215 live re-verification (2026-11-18)

Tier: FOCUSED (docs and evidence scripts only; no src code, no Azure resource created or modified). Refs #215.

## Files

* docs/reference/research/regulatory-ux-live-215-2026-11-18.md and its folder (login.py, probe-alerts.py, probe-alerts.out.json, screenshots not retained because they show a staff name)
* docs/reference/README.md, docs/reference/log.md
* .copilot-tracking research, critique, plan, details, changes, review, and the session state (replaces the earlier committed state of the same name)

## Per-criterion result

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 Patterns per role | Ticked, not reopened | n/a |
| 2 Alert fields | Ticked, not reopened; not re-proven live | Law store unloaded live, zero alerts shown |
| 3 WCAG 2.2 AA, no colour-only, keyboard, plain mode | Partly proven, not proven as written | Keyboard path, plain toggle, axe 0 violations on two panels, target sizes, text status proven live; non-unknown states unobservable live; AT testing excluded by owner |
| 4 Doubt route and no-source states | Ticked, not reopened; no-source state observed live | Unknown/law-store-not-loaded text shown |
| 5 Staff comprehension | Unproven | Needs staff participants; none exist and automation cannot substitute |

## Validation

* Live Playwright and axe probe run three times during development; final output retained.
* Local unit tests, mypy, ruff: not applicable, no source changed.
* git diff and link review of the note, README row and log entry.
* Scratch session file removed; no secrets printed or stored.
