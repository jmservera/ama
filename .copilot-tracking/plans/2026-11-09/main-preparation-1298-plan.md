<!-- markdownlint-disable-file -->
# RPI Plan: source-preserving current-main preparation (#1298)

## Task Metadata

* Task ID: issue-1298-main-preparation
* Task slug: main-preparation-1298
* Parent: chat-schema-sql-selector-1298
* Plan date: 2026-11-09
* Research: .copilot-tracking/research/2026-11-09/main-preparation-1298-research.md
* Details: .copilot-tracking/details/2026-11-09/main-preparation-1298-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-11-09/main-preparation-1298-plan-critique.md
* Planning status: ready

## Summary

Merge `origin/main` `ef28d4da42d83b111d48f14df9b70e3c4932a477` into the frozen candidate with an ordinary merge commit after this planning record is committed. Prove the merge is source-neutral for the candidate's two tool files, then run the existing tool unit suite, the targeted regression and the pinned Ruff and mypy commands. No source change is authorized.

## Decisions

* Owner demo-targeted tier applies; no `rpi-checks --all`, no SQL run, no receipt claim.
* Literal full-gate criterion stays unmet; `Refs #1298` only.
* Old adverse findings, fresh critique and Review records are not edited.

## Phases

1. Phase 1 Plan commit: commit research, plan, details, critique and state before any merge.
2. Phase 2 Merge: `git merge --no-ff origin/main` (ordinary merge, no rebase, no squash, no conflict resolution expected). Stop and record a blocker if any conflict arises.
3. Phase 3 Source-equivalence proof: after merge, `tools/rpi-checks.py` and `tools/test_rpi_checks.py` blobs equal approved `dadcd6da8`; the candidate's source diff against `origin/main` equals the approved diff against base; ancestry of `dadcd6da8` and `ef28d4da4` in the merge.
4. Phase 4 Validation: tool unit suite (expect 103, 0 skipped), targeted regression (3 tests), Ruff check and format with gate args, mypy strict, `git diff --check`, using `~/.venvs/zf123-pinned` after a version check.
5. Phase 5 Records and handoff: changes record, review record (implementing-agent pass, not independent), state, commit, handoff-1298-main-preparation.md in the coordinator files directory.

## Success Criteria

* Clean worktree, merge commit with parents `dadcd6da8` and `ef28d4da4`.
* Both tool blobs identical to `dadcd6da8`; no non-tracking source path differs from the approved set.
* All selected checks exit 0 with recorded counts; unmet items stated.

## Critique Disposition

One critique recorded in the critique artifact; findings applied directly.
