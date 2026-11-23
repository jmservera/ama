---
title: Issue 2243 live changes
---

Tier: focused (no `src` change). Basis: documentation, probe evidence and index/log entries only; no workflow, dependency, infrastructure or deployment edit. Hosted CI for the exact head is not observed here (no push).

## Changes

* Added `docs/reference/research/issue-2243-live-2026-11-23.md` with the probe script, result JSON and three screenshots under `issue-2243-live-2026-11-23/`.
* Added an index entry in `docs/reference/README.md` and a log entry in `docs/reference/log.md`.
* No source edit: main already derives the expiry from `ZF_DEMO_EXPIRES_AT` (#2249).

## Validation run

* `test_resident_aoai` and `test_resident_demo_api` from `src/api`: 70 tests, OK.
* Live desktop probe of `ca-resident-demo--0000026` (sign-in 200, two questions 200, both `usage_limit`); API `--0000054` Healthy. Read-only; no Azure resource created.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Derive EXPIRES from `ZF_DEMO_EXPIRES_AT` | Proven | `expires_at()` on main; env value live; "exercise has ended" label gone |
| Add a test | Proven | expiry and guard tests pass (70 tests) |
| Rebuild and roll the resident image | Proven for a roll, unproven for commit | Revision 0000026 Healthy; registry firewalled |
| Resident chat answers with the model within caps | Unproven, owner-gated | Live `usage_limit`; needs the private SQL ledger procedure and `resident_ai.budget.expires_at` set by the owner |
