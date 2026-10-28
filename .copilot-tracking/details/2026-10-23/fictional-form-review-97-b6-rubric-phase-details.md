<!-- markdownlint-disable-file -->

# Phase Details: fictional-form-review-97-b6-rubric

Plan: .copilot-tracking/plans/2026-10-23/fictional-form-review-97-b6-rubric-plan.md
Research: .copilot-tracking/research/2026-10-23/fictional-form-review-97-b6-rubric-research.md (C1-C7)

Test ownership: no test added or removed. Validation: git lineage and diff checks, JSON parse and total check, rubric script pytest run recorded as is.

## P01 Rebase onto fresh main and verify lineage

* P01-T01: Confirm clean status, remote head a74652aa and no unique remote commits, then rebase onto origin/main f1e2d830 (C6). Done before this plan was drafted; recorded in changes as a ordering deviation only if the critique so requires.
* P01-T02: Verify ancestry, diff against main limited to issue files, log append-only (one ms.date line removed).

## P02 Record findings, validate and commit

* P02-T01: Changes record: B6 evidence (C1-C4), options (b) and (d), no hand edit, 21 unrelated rubric-script test failures (C7), the rebase-before-plan ordering deviation, and the publication-method decision.
* P02-T02: Complete-gate plan: after PR 441 releases the heavy lock, one run of `python3 tools/rpi-checks.py --all --base <fresh origin/main> --out <new external dir> --lock-timeout 0`, then `--verify-receipt` against fresh main; any later commit or base move invalidates it. Same independent reviewer assesses the exact head afterwards.
* P02-T03: Resolve gh api user, set repository-local noreply email, commit only tracking files with Conventional Commit and trailer, no push.
