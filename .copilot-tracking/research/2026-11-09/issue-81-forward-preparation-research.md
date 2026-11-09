# Issue 81 forward preparation research, 2026-11-09

Task `issue-81-forward-preparation`, Refs #81 only. Parent record: `issue-81-demo-recovery` (preserved unchanged). Research disposition: executed (read-only git and `gh` inspection). Planning Readiness: Ready for the non-#1292 part; the #1292 source integration is Blocked pending merged #1292 on main.

## Fetched identities (2026-11-09 ~15:15 UTC)

| Item | Identity |
| --- | --- |
| Local HEAD (frozen) | `05ec1a7ee9a644da808e1585d183c0ea42511513`, branch `fix/demo-recovery-81-1109` |
| PR #1240 remote head (`feat/controlled-lifecycle-integration-81`) | `6ef6dc368ae3f8739095f740aa1e68634bd52922`, OPEN, base `main`, no checks |
| `origin/main` | `9f9aacc8be6a1b0e9a10efd367d1ea8bd7520939` (#1309 checkpoint squash) |
| Merge base HEAD/main | `b46a9ad9a9619db535368d1b2cbbddec8110e122` (#1299) |
| PR #1308 (#1292) head | `31464e65c92f13e523f03011e9917f4556a3a5c9`, OPEN, not merged; fetched as a ref only, not merged or imported |
| Remote `fix/demo-recovery-81-1109` | does not exist (local branch only) |

## Ancestry

* `6ef6dc36` is an ancestor of HEAD, so PR #1240's published head is preserved and any push of this branch to the PR branch would be a normal fast-forward (publication is coordinator-only; not done here).
* HEAD is 8 commits ahead of and 12 behind main (`git rev-list --left-right --count HEAD...origin/main` = 8 / 12).

## Main delta since b46a9ad9 (12 commits)

Sensor, IoT live-receiver, queue adapter, capstone tooling, infra Bicep and docs. Source files changed: `paired_equity.py`, `sensor_analysis_store.py`, `sensor_consumer.py`, `sensor_sql.py`, `synthetic/{device_provision,live_readings,sensor_consistency}.py` plus api live files. None is among this branch's seven changed core source files.

Overlap with this branch (both sides changed): `docs/architecture/cutover-evidence-pack.md` (non-mutating `git merge-tree` reports one content conflict; append-only evidence document, both intents reconcilable by keeping both sides) and `src/core/README.md` (auto-merges).

## #1292 (PR #1308) coupling

#1308 source files: api `server.py`, `web/app.js`, core `continuity.py`, `mssqlstore.py`, `sqlstore.py`, `store.py`, `pyproject.toml`, tests `sqlguard.py`, `test_priority_order.py`, `test_resident_decisions.py`, `test_case_journey.py`, `src/core/README.md`.

Overlap with this branch's changes: `src/core/src/zava_forward/core/store.py`, `src/core/tests/test_resident_decisions.py`, `src/core/README.md`. These are coupled source and test decisions that must not be guessed before actual #1292 main exists.

## Conclusions

* Current-main merge can proceed normally now (no #1292 dependency guessed).
* Final SQL integration, resident-decision SQL tests and ranking/quality SQL selectors stay deferred, not green.
* Adverse and original evidence in the parent recovery records is unchanged: no owned SQL run, #440 checkpoint unmet, original criteria unproven.
