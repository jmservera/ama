<!-- markdownlint-disable-file -->
# Critique: #74 building separation plan (issue-74-building-separation-0400)

Date 2026-11-13. One independent rubber-duck execution, read-only, before any implementation. Verdict: Revise. Plan: [plan](issue-74-building-separation-0400-plan.md).

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| CR-001 | High | Home-case building panel hides item applicability; a ZF-2-only work item also shows in ZF-3's building panel with no scope (`app.js` 1331, `building_fixture.py` 94) | Applied directly: G5 reclassed as an established display limitation, still decision-gated; research gap map updated |
| CR-002 | Med | Missing or null funding renders as "no" (`home_case.py` 156, `app.js` 1344) | Applied directly: recorded as adverse evidence and open representation decision; not changed here |
| CR-003 | Med | `buildingView` coverage overstated; heading assertion counts headings, not levels | Applied directly: `buildingView` marked source-inspected, unobserved; heading wording corrected |
| CR-004 | Low | "No dataset, real app" and Chromium version wording conflicts with the harness | Applied directly: synthetic dataset on a local loopback server; version read separately |
| CR-005 | Low | 24 includes the server PASS; browser portion 23 with axe; still author-reported | Applied directly in details V1 |

No conflict with a confirmed user decision; no user decision required. Critique is not repeated for this task.
