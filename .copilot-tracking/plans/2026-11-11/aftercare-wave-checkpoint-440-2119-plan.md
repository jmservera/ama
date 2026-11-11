---
title: Aftercare numeric-order integrated-main checkpoint plan (Refs #440 #1401 #1402 #134)
description: Plan for one bounded documentation checkpoint record in the existing cut-over evidence pack, with focused local checks of the merged numeric-order aftercare delta
ms.date: 2026-11-11
---

## Scope and decisions

* Task: `aftercare-wave-checkpoint-440-2119`, existing issue #440, branch `docs/aftercare-wave-checkpoint-2119`, target `main`, pin `077ad5ad20293a1d79932ea14e9f639dd11e5a22`. Research: [research](../../research/2026-11-11/aftercare-wave-checkpoint-440-2119-research.md). Details: [details](../../details/2026-11-11/aftercare-wave-checkpoint-440-2119-details.md).
* Deliverable: one appended section in `docs/architecture/cutover-evidence-pack.md`, a knowledge-base index entry in `docs/reference/README.md` and an append-only entry in `docs/reference/log.md`. Owner memory is not touched.
* Confirmed decisions from the task: no application, test, tool or workflow change; no source correction; no new issue, PR, push, board edit, merge or cleanup; no requirement relaxation or deferral; no reset of finite correction allowances; no live Azure, model, SQL service, private dataset or spend; no `uv` and no `PYTHONPATH=mvp`.
* The record separates current-main observation (PR 1456 merged, pin source) from pending candidate evidence (PR 1458 and PR 1455, OPEN, unmerged). PR 1458 candidate results are cited only as candidate policy and never counted as main evidence.

## Phases

1. Preflight (read-only). Prove the interpreter would import this worktree: set `PYTHONPATH` to the worktree `src/core/src`, `src/api/src`, `src/agents/src` plus test directories, under `env -i` with an owned temporary `HOME`, `ZF_DATA` unset, and print module origins and blob hashes. If any origin lies outside the worktree, stop that check and record a blocker; do not install.
2. Run once each, in the worktree, with raw output outside the repository (session `files/` folder), exit code recorded per command:
   * A1 `python3 -m unittest test_aftercare -q` from `src/core`.
   * A2 `python3 -m unittest test_aftercare_store -q` from `src/core` (MSSQL variants skip).
   * A3 `python3 -m unittest test_aftercare_intake -q` from `src/core`.
   * A4 `python3 -m unittest tests.test_aftercare_served tests.test_aftercare_screen -q` from `src/api` (node vm, no served browser).
   * S1 Ruff check and format check and mypy on `aftercare.py`, `test_aftercare.py` and `test_aftercare_store.py`; `git diff --check` on the documentation change.
3. Failure handling: a first failure is recorded as adverse evidence with its cause. A missing-dependency failure permits one pinned pip install of the named package into a user location only; no other retry. A concrete product defect is recorded against the closest existing owner (#1401 closed, so #1402 or #134 or #133 as fits), the affected acceptance stops, and nothing is fixed or opened.
4. Skips are counted separately and never as passes. The pending blank-state gap is recorded from static source only (no probe), marked as owned by #1402 and PR 1458.
5. Write the record, index entry and log entry; run `git diff --check`; check links.
6. One independent plan critique before implementation (rubber-duck agent), dispositions recorded; one Review after implementation. No second critique or Review.
7. Commit with the repository-local noreply identity for author and committer, Conventional Commit `docs(checkpoint): ...` and the Copilot co-author trailer. No push.

## Validation tier and gates

* Classification: focused tier (documentation-only plus planned local unit and static checks). The complete local gate is not run and no receipt is claimed. Basis: no source, dependency, workflow, Dockerfile, infrastructure, SQL, deployment or security-control change; the record is not a release, deployment or security acceptance.
* Affected gates the record states: closure of whole #133, #134, #89 and #440 stays held; #1402 (blank state) closure and any dependent aftercare expansion beyond constructed synthetic registers under 999 concerns relying on `FileStateStore` stay gated on PR 1458 merging and an exact-head check; independent exact-head review of this record and hosted checks of the exact head remain required.

## Critique amendments

[Critique](./aftercare-wave-checkpoint-440-2119-critique.md), one pass, applied before implementation: (C-02) the `FileStateStore` limitation, not relying on it for damaged-state refusal, applies at any register size and independently of numeric ordering; replace the "under 999 concerns" gate wording above accordingly. (C-03) The blank-state gap is static-only and A3 passing is not blank-state verification. (C-04) Record the exact HEAD and an empty `git status --porcelain -- src` before and after the checks, and the blobs of the tested files. C-01 and C-05 rejected with reasons in the critique.

## Exclusions

PR 1458 and PR 1455 as main content, MSSQL and Azure, browser and accessibility tooling, the 75-test personal-handoff campaign, #132, #109 and #111, deployment, resident or professional acceptance, and any change to requirements, ADRs or memory.
