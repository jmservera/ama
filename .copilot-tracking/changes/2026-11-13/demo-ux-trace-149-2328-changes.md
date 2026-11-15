<!-- markdownlint-disable-file -->
# Changes: UX design traceability matrix (issue 149)

Date: 2026-11-13. Plan: [plan](../../plans/2026-11-13/demo-ux-trace-149-2328-plan.md).

## Files

* `docs/reference/research/ux/design-system.md`: new "Journey to requirement to design to test traceability" section (13 journey rows, every human column `pending human test`); `ms.date` 2026-11-13.
* `src/api/tests/test_ux_design_traceability.py`: 7 checks that resolve every file, screen, panel, route, test class and method, requirement ID, all 13 registered role screens, and the pending-human marker.
* `.copilot-tracking/{research,plans,details,changes,reviews}/2026-11-13/`: RPI evidence.

## Divergences

* `information-architecture-navigation.md` does not exist, so only `design-system.md` was updated.
* The knowledge-base `log.md` entry and `index` note are deferred: `log.md` is reserved by open PRs #1575 and #1576.
* No edits to `wcag-conformance-baseline.md`, `log.md` or `panels.js` (`git diff --stat` shows neither).
