# Changes: issue 2255 live re-check (2026-11-23)

No source change. Tier: focused. Added docs/reference/research/issue-2255-live-2026-11-23.md, its probe folder, README index entry and log entry.

Evidence: probe on API revision 0000054 (resident 0000026 active, no safety queue); seeder tests 4 pass; ruff pass.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Elapsed time shown against a target | Proven | 22 of 22, 0 unknown |
| Some clocks running | Proven | 5 open, 17 overdue |
| Named owner shown | Proven | owner text on every row |
| Hazard service stays timing authority | Partly | synthetic seeded due times, marked; no responded_at written |
| Survives a dataset re-seed | Unproven, owner-gated | needs data-changing re-seed; generator outside repo; re-run seeder after any re-seed |
| Independent review, hosted CI, full local gate | Unproven here | not run; no src change |
