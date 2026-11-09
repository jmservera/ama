---
title: SQL feature-recovery wave checkpoint 440 C2 qualification plan
ms.date: 2026-11-09
task_id: 440-sql-wave-checkpoint-1109-c2
---

## Task metadata

* Task `440-sql-wave-checkpoint-1109-c2`, parent `440-sql-wave-checkpoint-1109`. Research: `.copilot-tracking/research/2026-11-09-sql-wave-checkpoint-440-c2-research.md` (executed, Ready). Details: `.copilot-tracking/details/2026-11-09-sql-wave-checkpoint-440-c2-details.md`.
* Branch `docs/demo-sql-checkpoint-440-1109`, prior head `06f408dd7`, target `main`.

## Executive summary

Apply two dated qualifications for the Readiness findings in the pack and cross-reference a new #1292 diagnosis, without changing any original authored record, source or policy.

## User decisions and requirements

* Fix ONLY the two Readiness findings plus the dated cross-reference to the #1292 diagnosis. No product, source, test, workflow or policy change.
* Preserve the original authored Review, critique and pack text; the table row at 5388 is qualified by an appended dated note, not silently rewritten (the original text stays visible).
* Pure documentation: link and diff review only; no local gate, no test repeat, no SQL, browser, cloud or model use.
* Local merge of the pinned main `ef28d4da42d83b111d48f14df9b70e3c4932a477` is planned after this planning commit; it differs from the checkpoint base only by the generated rubric score (verified `git diff --stat 8d6f029ca ef28d4da4`: one file). The later `origin/main` `1464b4d850a89aaaf835ba8a9ad98d38aeb1fdd6` (#1312, adds `tools/` and tracking changes) is NOT merged here: it is beyond the rubric-only condition. It is reported and left to the coordinator. The PR-level "no merge" below refers only to pull requests and `main`.
* Do not claim independent clearance, hosted verification, closure, whole 440/1292/81, live SQL, Azure or AI acceptance. `Refs #440` only. No push, PR, board, issue write or merge.
* Keep exact source `8d6f029ca` and the checkpoint observations distinct from the new candidate ancestry.

## Implementation phases

1. P1 Commit this research, plan, details, critique and state BEFORE any documentation edit.
2. P2 Pack: add a dated "C2 qualification" subsection after the existing findings section, covering Q1 (committed versus uncertain, with `server.py:1242-1246`, `sqlstore.py:156-159`, `app.js:38-40,724-730`, stating the 5388 row is qualified), Q2 (one failure across five executions, then four passes, cause UNKNOWN, no waiver, errors-list assertion at 734), and Q3 (cross-reference to the #1292 diagnosis: frozen `59accfa1`, 0 of 6, H1 not confirmed, no fix or closure inferred).
3. P3 Append a note under the row at 5388 pointing to the Q1 qualification. Do not delete or rephrase the original row.
4. P4 Index paragraph and log entry, concise and append-only. Pack `ms.date` stays `2026-11-09`.
5. P5 Recheck `git diff --stat 8d6f029ca ef28d4da4` is only the rubric file, then merge `ef28d4da4` locally; stop and report if not. Check the worktree and staged diff for the uncommitted edits, then the final committed diff against `ef28d4da4`.
6. P6 Documentation validation (diff scope, ASCII, anchors, log prefix unchanged), changes record, one Review, state, commit, handoff.

## Acceptance criteria

* AC1 Q1 distinguishes the two paths and cites the exact anchors; Q2 states 1 of 5 then 4 passes with UNKNOWN cause and no waiver; Q3 states 0 of 6, H1 unconfirmed, no fix or closure.
* AC2 The original Review, critique, research, plan and original pack text are byte-unchanged except the appended note and subsection.
* AC3 Diff against `origin/main` touches only pack, index, log and `.copilot-tracking` records.
* AC4 No approval, closure, acceptance, hosted or live claim is added.

## Risks

* R1 Independent reader needs whole-file context; the coordinator supplies it.
* R2 The #1292 facts are coordinator-reported from a handoff, not re-read from raw logs; the record labels them so.
