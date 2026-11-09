<!-- markdownlint-disable-file -->
# Plan: issue #81 parent alignment (2026-11-06)

Task `81-alignment`. Source research:
[research](../../research/2026-11-06/issue-81-alignment-research.md). Details:
[details](../../details/2026-11-06/issue-81-alignment-details.md). Prospective:
written before any alignment, rebase or test run.

## Objective

Local alignment of branch `feat/controlled-lifecycle-integration-81` (starting
HEAD `af891a5cc`) onto freshly pinned `origin/main`
(`56eec736906774ef56d8c9a66ed7f3f9c1e520c6`), proof that the three merged child
contributions (#1226, #1228, #1229) are preserved, no-service regressions,
and one bounded dated checkpoint. No new feature. Not FULL, not acceptance.

## Phases

* [ ] P1 Commit prospective research, plan, details and critique with dispositions (pre-alignment, on `af891a5cc`).
* [ ] P2 Local rebase onto the pinned main; stop on any unclear conflict.
* [ ] P3 Preservation proof (ancestry, blobs, range-diff, evidence files).
* [ ] P4 Isolated no-service regressions and static checks.
* [ ] P5 Checkpoint in `docs/architecture/cutover-evidence-pack.md`, changes record, author Review, log entry if a knowledge-base file changes.
* [ ] P6 Final commits, clean ignored-inclusive freeze, report.

## Success criteria

* `origin/main` pin is an ancestor of the new HEAD; three child commits are the only source commits above it (plus RPI/evidence commits).
* Each of the eight child source/test blobs is identical to its pre-alignment identity, or each difference is explained and caused only by conflict resolution (none expected: main touched no `src/`).
* Original issue-82 RPI evidence files are byte-identical to their pre-alignment blobs.
* Listed local checks run with actual exits recorded; skips recorded, not hidden.
* Four issue #81 criteria and issue #440 acceptance stay unticked; no approval inferred.

## Conflict handling

Rebase with `git rebase origin/main`. Dry-run merge-tree predicted clean. If a
conflict appears: keep both intents, never drop either side, never use
`-X ours/theirs` blindly. Disjoint paths (agent file vs `src/core`) mean any
conflict is unexpected and is escalated: abort with `git rebase --abort`,
record precise evidence, do not guess. The starting identity is kept as local
ref `refs/ama/issue81-start` plus recorded SHA.

## Focused regression selection (no service)

Isolated venv in scratch; install only `src/core` (and `src/agents` only if an
import fails) with pip after a real missing-dependency failure, non-editable or
editable from this worktree; prove installed origin by `zava_forward.core.__file__`
under this worktree. Env: `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR`,
`MYPY_CACHE_DIR`, `RUFF_CACHE_DIR` in scratch, `ZF_DATA` in scratch, `HOME` untouched.

| Check | Covers |
| --- | --- |
| `python -m unittest test_gates test_quality_procurement test_hazard_referral -q` (`PYTHONPATH=src:tests`) | quality fail-closed, malformed metadata, rule provenance, capacity Pass/Fail/Unknown, hazard refusals |
| `test_resident_decisions test_resident_documents test_resident_choice_queue -q` | existing resident consent/authority refusals; run subject to no private data and no sending |
| authority/consent tests discovered by `grep` in `src/core/tests` (selected by name, not guessed) | authority refusals |
| `ruff check` and `ruff format --check` on the five changed source files and three tests | static |
| `mypy` on `src/core` | static, cache in scratch |
| `python3 tools/rpi-checks.py --changed --list` or equivalent dry list only if it needs no service | focused-tier selection, not a gate |

Not run (declared): FULL gate, API/agents suites, SQL, browser, Docker, scanner,
Azure, performance, manual acceptance.

## Critique routing

One independent critique of this plan and details before P2. Compatible
findings applied directly; conflicting advice with explicit coordinator
decisions rejected and recorded; significant divergence unresolved by current
direction becomes a blocker. No second critique, no repeat Review.

## Amendment 1 (post-critique, still before alignment)

Source: [critique](./issue-81-alignment-critique.md). Applied dispositions:

* Test runs use `env -i` with an explicit allowlist (`PATH`, `PYTHONDONTWRITEBYTECODE=1`, scratch `TMPDIR`, `ZF_DATA`, cache dirs); no `ZF_RESIDENT_AZURE_TEST`, `AZURE_*`, `MSSQL*` or provider keys.
* Preservation proof inventories the child evidence paths at the starting SHA and compares blob and mode per path at the new HEAD.
* Any failed preservation check or required regression, or unavailable check, blocks an "aligned" claim and is reported as failed or blocked.
* If `origin/main` moved past the pin, inspect the delta and stop for replanning when it touches child source, tests, evidence or this scope.
* Isolated local SQLite file tests (`SqlFlows`, `SqlResidentDecisions`) are permitted and classified `local observed (SQLite file)`; SQL Server and Azure stay excluded.
* Research wording amendment: the quality and capacity rule records cite PRD FR-008 with FR-017 and FR-016 and fixtures; booking rules cite BRD RULE-001/002. BRD is related traceability only for quality and capacity.
