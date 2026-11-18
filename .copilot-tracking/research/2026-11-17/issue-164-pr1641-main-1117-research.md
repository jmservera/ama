# Research: #164 / PR #1641 repair against main f1df574bb (2026-11-17)

Task: issue-164-pr1641. Worktree pr-1641-main-1117, branch fix/rebase-1641-main-1117, created at PR head 4b759cb68514686ee2d484993337681df57f85a9.

## Opening facts

* PR head is DIRTY against main f1df574bba2b94cd83bb2a783079ec94cd584c90; merge base 61e1917dd.
* Overlap between PR and main since the base: about 60 files (core store, taskqueues, chat web assets, infra, log.md, README index).
* Prior worktree pr-1641-rebase (HEAD 3ec8444c0) merged older main; it is not current and is not reused.

## Research disposition

executed. Planning Readiness: Ready.

## Findings so far

* Prior local commits beyond PR head: 69367b4f1 (merge-alignment of chat widget, safeguarding redaction, AC-071 traceability; conflict-resolution specific to the old main, to be re-derived), e2d4691b1 (ruff format join of one literal in test_alert_chat_end_to_end_stabilization_215.py; formatter-only, to be reapplied only if the format check still fails), plus tracking records and old-main merges (not carried).
* Scope: chat, consent and SQL-adjacent store code. Tier FULL expected; rpi-checks.py --all is NOT run here (coordinator schedules under the heavy lock).
* Consent-regrant defects in #1641 are separate and out of scope; settled review findings are not reopened.
