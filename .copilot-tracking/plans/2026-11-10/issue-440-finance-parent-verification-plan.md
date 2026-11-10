---
title: Issue 440 finance-parent verification plan
description: Finite local verification of finance head 4642b55f with no product edits
ms.date: 2026-11-10
---

Details: [issue-440-finance-parent-verification-details.md](../../details/2026-11-10/issue-440-finance-parent-verification-details.md). Research: [research](../../research/2026-11-10/issue-440-finance-parent-verification-research.md).

## Phases

* [ ] Phase 1: identity guard. Confirm HEAD, tree, clean status; record main pin.
* [ ] Phase 2: external venv at `/tmp/440fv-1110/venv` from `src/build-requirements.txt` (hashed), `--no-deps --no-build-isolation` editable installs of `src/core`, `src/agents`, `src/api`; prove owned distributions and import paths.
* [ ] Phase 3: observation A, the two ordered-history and legacy-copy tests, then observation B, the five Core modules.
* [ ] Phase 4: observation C, `tests.test_form_staging_api` from `src/api`, only if A and B pass and imports resolve.
* [ ] Phase 5: post-run identity guard (clean tree, HEAD and tree unchanged, source bytes equal), then changes record, one Review and handoff.

## Stop rules

* Stop at the first failing step; preserve its full output; no repair, rerun loop or new issue.
* No product, test, config or shared-document edit; no push, PR, issue, board, amend, reset or rebase.
* Raw logs, exit codes and counts stay under `/tmp/440fv-1110/`; tracking records cite summaries and SHA-256 of logs.
* No approval, whole #440, #93 or #96 criterion ticks. No type check selected (unchanged tree; exact project config only if ever chosen).
