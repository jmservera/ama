# Issue 151 live changes (2026-11-18)

Tier: FOCUSED (documentation and evidence only; no `src/`, workflow or infrastructure change; rpi-checks --all not run).

## Files

* docs/reference/research/issue-151-live-wcag-axe-evidence-2026-11-18.md (new)
* docs/reference/README.md (index row), docs/reference/log.md (appended entry)
* .copilot-tracking/evidence/2026-11-18/issue-151-live/ (scripts, JSON results, screenshots, axe SHA-256)

## Per-criterion status

| # | Criterion | State | Status |
| --- | --- | --- | --- |
| 1 | Target conformance level and scope decided | ticked | Not re-tested |
| 2 | Audit covers keyboard, focus, name/role/value, status, contrast, reflow, target size, errors | ticked | Not re-tested |
| 3 | Automated checks run in CI against key screens | ticked | Corroborated live: axe 4.10.3, 13 screens, 0 violations |
| 4 | Manual screen-reader and keyboard checks per role workflow | unticked | Unproven: keyboard and axe proven for one role (Programme Manager) only; screen reader is production-only (#1907); other roles lack accounts |
| 5 | Map, charts and tables have accessible equivalents | ticked | Not re-tested |
| 6 | Accessibility statement draft lists known gaps | ticked | Not re-tested |

## Validation

* Credential literal scan of the evidence directory: no match.
* axe SHA-256 matched the repository pin.
* Link and diff review of the Markdown changes.
* Azure: read-only; no resource created, nothing to delete.
