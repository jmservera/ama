# Issue 444 rebase and readiness changes

Date: 2026-10-25. Plan: ../../plans/2026-10-25/issue444-rebase-readiness-plan.md. Earlier records (2026-10-24 and lineage 2026-10-25, including their Conformant outcomes and the merge-based lineage) are retained unchanged; the rebase linearised the merge commit 2049b3b2 (content preserved, original tip kept as local branch backup/444-pre-rebase-6878d6ec).

## Rebase

* Branch rebased onto origin/main 0245944a04d44444de9c9f1af765121e961a075c (adds #457 seed merge, #456 and #448 docs) under coordinator authority; push uses `--force-with-lease` only.
* Conflicts: docs/reference/README.md (`ms.date`: kept main's 2026-10-25) and docs/reference/log.md (kept every main entry, then the #444 entry). No source conflict.
* Superseded bot commit e1bb33efe186d7c454053d7d4c9b591eba529081 `chore(rubric): record score 64/100` (only .github/rubric/scores/latest.json, rubric/score SUCCESS, scored old head 6878d6ec). Not carried: it scores a superseded head and conflicts with main's newer baseline. The rubric workflow re-scores on synchronize; any new bot commit is inspected and the gate refreshed.
* Equivalence checks: resident source and tests identical to 6878d6ec (empty diff); log.md adds exactly 6 lines vs main, none removed; no rubric file differs from main; no staff file changed.

## Validation (rebased tree, before the evidence commit)

* ruff and mypy clean: core 71 files, api 69 files.
* Full core 1295 tests OK (167 skipped); full api 1029 tests OK (308 skipped).
* Browser check and the complete gate run on the final head (see PR and final report).

## Limits retained

* No human screen-reader audit; accessibility harness not run; Fluent 2 partial; no conformance claim.
* Not live Azure/SQL/real-AI acceptance; #444 stays open (Refs only). #441 backlog acceptance paused; nothing from it implemented.
* Services 8350/8444/8445 untouched and pre-change snapshots. Old receipt /tmp/rpi-444-gate-main36996d70 (SHA 9ecb9317...) is historical.

## Review disposition

One independent review of the PR boundary: Conformant with one Low follow-up (dataset copy not re-read per request; restart needed for authority edits). Recorded as a limitation; no correction cycle was needed (0 cycles).
