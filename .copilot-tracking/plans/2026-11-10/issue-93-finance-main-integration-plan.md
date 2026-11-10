---
title: Issue 93 finance main integration plan
description: Bounded local integration of the finance parent, its verification records and pinned main, with targeted validation
ms.date: 2026-11-10
---

Research: [research](../../research/2026-11-10/issue-93-finance-main-integration-research.md). Details: [details](../../details/2026-11-10/issue-93-finance-main-integration-details.md). Critique: [critique](../../reviews/plans/2026-11-10/issue-93-finance-main-integration-critique.md).

Tier: owner DEMO TARGETED. No full local gate, no push, PR, issue or board write. Refs #93 only.

## Phases

* [ ] Phase 1: prospective records. Commit research, plan, details, critique and state before any merge or test.
* [ ] Phase 2: ordinary merge of `test/demo-finance-parent-440-1110` (`ef63d180`), preserving its seven records; then ordinary merge of main `5318f738`. Resolve only append-style conflicts in `src/core/README.md` and `docs/reference/log.md`, preserving both histories.
* [ ] Phase 3: byte guards on the merged tree. Seven product blobs equal the finance `4642b55f` blobs; `server.py`, `test_form_staging_api.py` and every other non-documentation path equal the main pin; the seven verification records are byte-identical to `ef63d180`.
* [ ] Phase 4: isolated environment `/tmp/issue93-finance-main-1110/venv` with hashed pinned build tools and `--no-deps` editable installs of this worktree's `core`, `agents`, `api`; prove `direct_url.json`, module `__file__` and test blob identities.
* [ ] Phase 5: observations in order. A: two history tests. B: five Core modules. C: complete main `tests.test_form_staging_api`. D: strict mypy for Core and API with the project configuration. E: Ruff check and format check on the seven product paths.
* [ ] Phase 6: SQL evidence determination. Re-run the contract search on the merged tree; report absent MSSQL form or history contracts; no admission unless critique or a new finding shows material SQL impact.
* [ ] Phase 7: changes record with commands, exits, counts, skips and identities; one Review; final state; handoff to the coordinator path.

## Critique amendments applied (C1 to C8)

* README and log guard is `git diff 5318f738 HEAD -- <file>` showing additions only, no removed main line.
* Record sorted unique test ids and the union count; do not assume the brief's counts.
* `PYTHONDONTWRITEBYTECODE=1`, external `MYPY_CACHE_DIR`, Ruff `--no-cache`; confirm clean tree including ignored files before the final commit.
* Phase 6 also checks that the parent delta touches no `sqlstore`, `mssqlstore`, schema or persisted key names.
* Classify every failure as parent, main or pre-existing; repair only parent-caused defects in the seven files.
* Parent-only verification observations are history, not evidence for the merged tree.

## Stop rules

* First failure stops the affected step; raw output preserved; reproduce and scope before any repair. At most five total review-correction cycles. A significant unexpected defect or any semantic conflict outside the seven product files pauses for the coordinator.
* Edits only to tracking records and append-only resolution of the two documentation files. No edit to reserved API, store, schema or navigation hooks, finance rules, eligibility, calculation, approval or submission.
* No approval, whole #93, #96 or #440 criterion ticks. BRD 0.21 draft and PRD 0.21 in-review remain unapproved.
* Raw logs under `/tmp/issue93-finance-main-1110/logs/`; tracking cites summaries and SHA-256 of logs. Do not count a repeated test as unique.
