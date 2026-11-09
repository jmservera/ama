---
title: Issue 1259 frozen parent C6 integration plan
description: Prospective integration-only plan to merge exact parent 99814198 and re-verify the child
ms.date: 2026-11-09
---

## Objective and boundary

Ordinary local merge of exact `99814198079c7c8fcd641497826986c706627b0f` into `fix/ranking-archive-path-health` (`--no-ff`; no rebase, amend, reset, force, push, PR, issue, board or parent mutation). Reconcile only the clear mechanical conflict; stop on ambiguous intent. Preserve the child's C2-typed helpers and all current-main runtime, 1308 SQL, 1313 controls, 1315 photo and 1320 receipt behaviour. Declared target stays the parent topic. Refs #1259 and #1258 only. Integration and evidence only: no new source cycle, no source edit planned.

## Ordering

Research, this plan, details and one independent critique are committed before any merge. A source edit is made only if a child-owned defect is found; it would be recorded as C3 after its own plan and critique.

## Phases

* [x] 1. Research (`...-parent-c6-research.md`).
* [x] 2. Plan, details and one independent critique; compatible findings applied.
* [ ] 3. Merge exact parent; resolve `test_ranking_archive_blob.py` by keeping the child's typed test before the parent's annotated method; no other hand edit. Verify second parent, no conflict markers, and that `ranking_archive_blob.py`, `documents.py`, `ranking_publication.py` and `ranking_publication_runner.py` blobs equal the qualified hashes (source and protocol unchanged proof).
* [ ] 4. Maintained-profile checks (CI profile in `.github/workflows/src-ci.yml`: Python 3.12, `pip install -e ../core -e ../agents -e ".[dev]"`, `ruff check . && ruff format --check .`, `mypy`, from each project root), ruff 0.17.1 and mypy 2.4.0, plus the `blob` extra profile where the Blob adapter is imported. Compare diagnostics with the parent's own; classify child-owned versus inherited by running the same checks on a clean export of the parent commit.
* [ ] 5. Targeted tests from the worktree: core `test_ranking_archive_blob test_ranking_publication test_ranking_publication_runner test_documents` and ranking discover; API wiring, policy and scale; agents cohort eval if a ranking module is touched (it is not). Record counts, exits, skips.
* [ ] 6. Evidence binding: hash manifest of logs; decide Azurite reuse by the hash rule only.
* [ ] 7. Changes record, one authored Review, state, commit, handoff.

## Critique dispositions (one pass, rubber-duck, verdict Revise, applied directly)

* Significant, evidence reuse: the reuse rule now covers the adapter, `documents.py`, `ranking_publication.py`, `ranking_publication_runner.py` and `ranking.py` (parent change is annotation-only: two imports and a typed `snapshot` signature, no behaviour), plus the `blob` extra pin. The earlier Azurite run used the Node SDK for setup only and the urllib adapter for the test, so reuse claims are limited to adapter protocol behaviour on those inputs and never cover the merged tree as a whole. If any hash differs, no reuse.
* Significant, environments: separate CI-minimal core and API environments (core: `-e ../core`-equivalent, no Blob or SQL extras; API: core, agents and API), each compared with the same environment type on a parent export; Blob SDK profile checked in its own environment.
* Minor, ownership: diagnostics are normalised for path, then mapped to changed hunks; the API wiring test mypy exclusion is stated as a coverage limitation.

## Stop rules

Stop and record a blocker on an ambiguous conflict, a failing selected test (not waivable), a child-owned diagnostic needing a source edit (then C3 needs a prospective plan and critique), a moved parent (revalidation needed), or a busy shared admission lock (pending, not queued). A new emulator run is not planned; it would need one finite non-queued heavy admission.

## Unperformed and remaining

Independent exact-head review, hosted checks, parent qualification, human approval, real Azure, WORM, deployment, folder-record migration, FULL stack receipt and the PC-1 duplicate `NextMarker` decision stay open. Original acceptance criteria stay literal and unticked.
