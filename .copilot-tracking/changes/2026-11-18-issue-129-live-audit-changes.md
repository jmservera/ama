<!-- markdownlint-disable-file -->
# Changes: Issue 129 live audit (2026-11-18)

* Status: complete; docs-only, tier FOCUSED; no src change; Refs #129
* Plan: ../plans/2026-11-18-issue-129-live-audit-plan.md

## Files

* docs/reference/research/issue-129-live-r2-2026-11-18.md (new note)
* docs/reference/research/issue-129-live-r2-2026-11-18/ (raw test output, live_probe.py, live_probe.json, screenshot)
* docs/reference/README.md (pointer), docs/reference/log.md (entry)

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| Five bundles | Proven (constructed cases, not measured) | 26 core + 6 api tests OK |
| O10, O18-O20 out of scope | Proven in code; no bundle route on the demo | tests; live_probe.json |
| Atlas owner confirms mapping | UNPROVEN: human owner decision, no confirmation exists | note, per-criterion table |

Production-only or out of demo: real-participant runs, DPO retention decision, Finance validation of minutes.

## Validation

| Check | Result |
| --- | --- |
| core suite 26 tests | OK |
| api scenario suite 6 tests | OK |
| Playwright signed-in probe | signed_in true, no bundle navigation or route |
| credential literal scan of evidence | no match |
| Azure resources created | none |
| mypy / ruff / rpi-checks --all | not applicable: no source change; --all not run |
