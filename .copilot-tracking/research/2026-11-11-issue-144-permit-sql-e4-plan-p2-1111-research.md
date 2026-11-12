---
title: Issue 144 permit SQL E4 plan correction P2 research
description: Research for the second review-driven plan correction (1 High, 3 Medium) before any real-MSSQL execution
ms.date: 2026-11-11
task_id: issue-144-permit-sql-e4-plan-p2-1111
---

## Scope and disposition

* Research disposition: executed, read-only source and metadata only. Planning Readiness: Ready for a P2 plan; execution is not admitted.
* Frozen P1: HEAD `523ea4977e58befcc6c2a2ea86da225c6bb5f473`, tree `0a75c016937f3bb2dac0484467f8d770ed80c594`, base `e691255ff7aae111ef32d585900cf82c3789a78c`. The ten original and P1 tracking blobs are unchanged.
* Inputs incorporated by reference, not copied or regraded: `independent-144-permit-sql-plan-1111.json` (7 findings) and `independent-144-permit-sql-plan-p1-1111.json` (REQUEST_CHANGES, 1 High, 3 Medium, 0 Critical, 0 Low). Both reports and both authored critiques (parent proceed, P1 ready-for-review) stay unchanged adverse history. The findings concern the validation recipe, not a demonstrated application defect.
* Authority: Root admitted one E4 under the Nov 10 five-cycle extension, counted separately from E3 although the reviewer called these same-E3 corrections. Reviewer recommendations cannot grant or reset authority. E1/E2/E3 counted, E4 counted from this correction even if implementation never starts, one unadmitted cycle remains, no automatic E5, no new five, no reset. A later implementation, if admitted, belongs to this same E4.

## Facts verified for the four findings (tree e691255ff, read-only)

* Pre-E2 contamination (finding 1). With the E2 hunk reversed, a conflicting `meter_root` is no longer refused: `complete_result` settles the marker meter and calls `complete`, which writes an `output` under the caller's syntactically valid root (`ai_consumption.py` 821-866 accepts it) and moves the leased task to `ready`. A shared-task sequence that runs the root conflict before the id conflict therefore leaves the id branch and the matching-success step looking at a mutated task. The existing SQLite case 6 order is `for key in ("meter_root", "meter_id")` on one task, which is exactly that hazard under N2.
* The conflicting `meter_id` branch is unchanged by E2 (pre-E2 already rejected `envelope.meter_id not in (None, marker.meter_id)`), so on N2 it still returns False and writes `result-rejected` without settling.
* Case 5 in the existing SQLite test indexes `outputs` through a list comprehension compared with `assertEqual` on a tuple list, so a missing output fails an equality assertion, not an `IndexError`; the new SQL version must keep the collection-count assertion before any indexing and label it `E2-STORED-ROOT`. `reference(task["id"])` is the expected output reference and `eligible` is True. The allowance row exposes `used_calls` and `reserved_tokens` (`assistants.py` 477, 487), both usable as baselines.
* Build backend (finding 2): `src/core`, `src/agents`, `src/api` (and importer, orchestrator) each declare `build-system.requires = ["setuptools>=77"]`; none declares `wheel`. `pip install -e` without `--no-build-isolation` builds in an isolated environment and may fetch the backend from the index regardless of `--no-deps`. The legacy `144-main-port-extension1-1110/venv` has no setuptools (Root probe exit 1), so no existing environment is a usable build base and it is not reused.
* Strict typing (finding 3): strict mypy enables `disallow_subclassing_any`. `test_assistants` is `ignore_errors` with `follow_imports = skip`, so `ta.MssqlFixture` and `ta.Base` are `Any`; a `class X(ta.MssqlFixture, ta.Base)` statement is a separate diagnostic site. A runtime `type(name, (a, b), {})` call is not a subclassing-any site and its result is a plain object when annotated `Any`.
* Cleanup (finding 4): the P1 plan created holder and observer before `try` and described a sequential `finally`; a raising rollback or observer failure could then skip later closes or the join.
* No tracking-path, source, test, helper, workflow, gate, requirement or pyproject file is touched by this correction. No nested agent and no runtime command is used.

## Unknowns carried forward

Pip index availability of the pinned backend wheels; actual strict mypy output; DMV lock granularity; the N1 and N2 outcomes; the reconstructed pre-E2 hunk (future receipt evidence only); all X1 to X10 execution.
