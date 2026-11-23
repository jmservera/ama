# Issue 2255 live re-check research (2026-11-23)

Disposition: executed. Planning Readiness: Ready.

Prior evidence: docs/reference/research/issue-2255-backfill-2026-11-22.md and issue-2255-reverify-2026-11-22.md. Issue has no tick list; criteria taken from Expected paragraph. Open criterion from earlier passes: survival of the seeded clock fields over a dataset re-seed.

Findings (code): hazard_clock in src/core/src/zava_forward/core/taskqueues.py fails closed to "elapsed time unknown" when aware_at/response_due_at are absent. SqlStore.merge_seed is insert-only (never updates a stored case). The 980-case demo dataset generator is not in this repository, so the generated hazards cannot be fixed at source here; infra/scripts/seed_demo_hazard_clock.py is the repo path (4 tests). Live: revisions api 0000054 and resident 0000026 active at 100 percent; main equals HEAD b11b8259bd.

Plan: re-run read-only probe on 0000054, confirm resident 0000026, add owner-gated statement for re-seed; no src change (focused tier).
