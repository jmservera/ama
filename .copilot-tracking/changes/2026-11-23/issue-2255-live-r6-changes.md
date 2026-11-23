---
title: Changes, issue 2255 run 6
ms.date: 2026-11-23
---

## Changes

* `infra/scripts/seed_demo_hazard_clock.py`: `revert` restores a re-dated `noticed` even when the original was absent (removes the invented date).
* `infra/tests/test_seed_demo_hazard_clock.py`: added `test_revert_removes_a_noticed_date_the_seeder_invented`.
* Research note [issue-2255-live-r6-2026-11-23.md](../../../docs/reference/research/issue-2255-live-r6-2026-11-23.md) with probe script, JSON, page text and screenshot; indexed in `docs/reference/README.md` and `docs/reference/log.md`.

## Validation

* New test fails without the fix (1 failure) and passes with it: `python3 -m unittest discover -s infra/tests -p test_seed_demo_hazard_clock.py -q`, 5 tests OK.
* `ruff check` and `ruff format --isolated --line-length 100 --check` on both infra files: clean.
* Tier: focused. Only private infra tooling changed (no src, workflow, permission, image, secret or gate change); `rpi-checks.py --all` not run. Hosted CI and independent review remain outstanding.
* Divergence: the implement-start witness reported the source dirty (edits predate it); the test and fix were in fact made after the witness, the dirt was the untracked research evidence and state file. Disclosed.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Elapsed time shown against a target, not "unknown" | Proven on revision 0000058 | 22 of 22 rows, 0 unknown (probe-rev58.json) |
| Some clocks running with a target window | Proven | 5 open with due time, 17 overdue |
| Named accountable owner still shown | Proven | 44 owner text matches |
| Hazard service stays timing authority | Partly proven | page text names the service; resident update stays Unknown; times synthetic |
| Seeder revert undoes its own writes | Proven at unit level (new test) | test_seed_demo_hazard_clock |
| Live re-seed survives | Unproven, owner-gated | destructive re-seed not authorised; generator outside repository |
| Generator emits the fields | Unproven | generator outside repository |
| Independent review, hosted CI, full local gate | Unproven here | coordinator runs gates |
