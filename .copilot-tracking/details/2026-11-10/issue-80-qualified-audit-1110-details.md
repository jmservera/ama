<!-- markdownlint-disable-file -->
# Details: issue #80 qualified audit correction

Plan: `.copilot-tracking/plans/2026-11-10/issue-80-qualified-audit-1110-plan.md`.

## Phase 1: supplement content

* Section "Corrections": quote each incorrect claim (matrix line 8 "12 CSV routes plus the progress report variant"; handoff "13 routes", "10 of 13 controls"; matrix lines 8, 31, 33-34, 67, research Finding 1/5 and review line 12 "controlless ... claim holds") with the corrected statement.
* Section "Twelve-entry table": eleven distinct paths plus progress variant, with control location or "not located" per row.
* Section "Control construction trace": per research artifact, source lines only, limitations stated.
* Section "Mapping to planning minimum M1-M4", later-only candidates, exclusions; synthetic-only; no narrowing of "every list".
* Section "Historical observations": API 11/24/14, schema 21, progress 58 are original-session observations, not rerun.
* Section "Remaining scope and Root decisions": no implementation; human gates; C2, C4, #73 open.

## Phase 2: verification

`git diff 5d94c710 -- ` over original files must be empty; `git diff c66370042 HEAD -- src` empty; status shows only new `.copilot-tracking` files.

## Phase 3

One Review artifact; commit tracking only with noreply identity and Copilot trailer; `verify` exit code recorded.
