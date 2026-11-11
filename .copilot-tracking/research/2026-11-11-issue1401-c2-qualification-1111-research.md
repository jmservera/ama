---
title: Issue 1401 cycle 2 requalification research
ms.date: 2026-11-11
task_id: 1401-c2-qualification-1111
---

## Scope and boundary

Cycle 2 of the owner's three scoped diagnostic/correction cycles for existing issue #1401, admitted by the root on 2026-11-11. Cycle 1 is used, cycle 3 is NOT admitted, and the inherited #133, #89 and D5 history is not reset. This cycle is a prospective RPI loop (research, plan and details committed before any new verification) that requalifies the frozen cycle 1 candidate and records its process deviation. It makes no source, test, schema or validator edit, does not implement #1402, and does not claim whole #133/#89 or production acceptance. Research disposition: executed.

## Candidate and target identity (read-only, verified 2026-11-11)

* Branch `fix/aftercare-numeric-order-1401-1111`, clean worktree, head `678c45805e029a1437318972dcca36bf4eeefbbf`, tree `9951f839e6f5cc7a8bb2440fe20ee3d8ff6f5d65`, tested historical base `e691255ff7aae111ef32d585900cf82c3789a78c`.
* Current `origin/main` is `ea811c2e015ab3dd45f1f38af12b136d04cffa38`. The base is an ancestor of it. The only non-tracking path added between the base and main is `src/api/tests/test_permit_sql.py`; no aftercare, core, agents or API source changed. A non-mutating `git merge-tree --write-tree HEAD origin/main` exited 0 with result tree `1e7b0fc2ada17ac4969130ba0d6829832d1dafd5`. No rebase or cherry-pick is performed; the original tested base stays historical.

## Independent report consumed

The complete independent report for head 678c458 (verdict approve_with_comments, one Medium process finding, no functional blocker) was read in full. Findings carried into this cycle:

* Cycle 1 research happened before editing, but the research, plan and details files were created after the source and tests were edited and tested. The original critique and Review were genuinely later and ran once each. The original plan checklist is therefore not a prospective record and must not be described as one.
* The original wrapper's native exit was missing, possibly a shared-launcher capture artifact; it is neither 0 nor a failure and is not recreated.
* Raw final core and MSSQL numeric results exist. API, lint and type exits and outputs were piped or collapsed and are not independently proven.
* The SQL cleanup count and flock exit were only handoff claims; the original manifest was removed and is not recreated. The original script's outer status can hide a test failure; the direct `mssql_exit=0` line in the saved output is real.

## Original evidence preserved in place, unmodified (sha256 at 2026-11-11T17:1x)

* `/tmp/before1401.txt` b189353aafd8901d51c4778695a7464e1aa94becea4fa5a13aeb711d3f5617f4 (genuine RED, 7 errors, 4 `StateInvalid`).
* `/tmp/after1401.txt` ffd2ebf6fffd2d17355dc2993f780de0ac6d24c87af0ef20fd35ced97fa1c340 (adverse earlier run, 4 errors from a wrong response key, later corrected).
* `/tmp/after1401b.txt` b60f100f1c796f1624e64e0b21da3bf43b982b435836e9413f44f2e5fe4bf8d9, `/tmp/final1401.txt` e7b2f219d46eb89a9969430ebcd6cdaa49825e99ae746fe6b7788fd766f24345, `/tmp/mssql1401.txt` 7f5bc553333bb5a5bb07cc04d0571e054c097c7e73beb5a065356796e50637b3, `/tmp/run_mssql_1401.sh` d9df6edaab3dd5f42c495e8bcdb497a6779fc1c7f0ba52a9c3ebe696b703a9e1, `/tmp/repro1401.py` de5935ab3d0aa71286fab8038fefafb5f818280b62888f693e10913d332a6ed3.
* The seven original cycle 1 records under `.copilot-tracking/` are not edited, moved or backfilled.

## Environment facts affecting provenance

* The installed editable `zava_forward` namespace resolves to the primary checkout `/home/azureuser/source/ama/src/*`, not this worktree. Every verification command must set an explicit candidate-local `PYTHONPATH` and record imported module `__file__` values and SHA256 in the same invocation environment, so the primary source is never executed silently.
* `ruff` and `mypy` exist in `/home/azureuser/.local/bin`. No install or global mutation is needed or allowed.
* The 15 SQL Server tests are opt-in skips unless `ZF_RESIDENT_MSSQL=1`; this cycle does not start SQL.

## Planning Readiness

Ready. No unresolved blocker. A genuine source or static failure stops the cycle with the raw failure; no edit and no cycle 3.
