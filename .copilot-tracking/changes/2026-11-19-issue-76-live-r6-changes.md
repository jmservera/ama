# Issue 76 r6 changes (2026-11-19)

Tier: FOCUSED. No src change; mypy, ruff and rpi-checks not applicable. Docs only.

Files: docs/reference/research/issue-76-live-r6-2026-11-19.md, docs/reference/README.md, docs/reference/log.md.

Validation: `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_taskqueues test_hazard_safeguarding_clock_owner -q` gave 33 tests OK. Link and diff review done.

| Criterion | Status |
| --- | --- |
| Default view single list, status, next action | Ticked; not re-run |
| No perspective picker | Ticked; not re-run |
| Queue categories with definitions | Ticked; not re-run |
| Blocked steps reason, owner, action | Ticked; not re-run |
| Hazard and safeguarding clock and named owner | Safeguarding proven; hazard owner proven, times Unknown (owner data decision); UNPROVEN in full |
| Views agree (FR-034) | Ticked; not re-run |
| Single reset (FR-032) | Ticked; not re-run |
