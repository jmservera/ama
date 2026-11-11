<!-- markdownlint-disable-file -->
# Bounded live demo plan revision 2: plan (2026-11-11, Refs #184 #1288 #108 #440)

Task `issue-184-bounded-live-plan-rev2-1111`. Native session `053b0ad3-0c8d-46d8-b30c-e3b1f3fcdb3f`. **NO EXECUTION.** Documentation-only revision under the same planning scope. Research: [rev2 research](../../research/2026-11-11/issue-184-bounded-live-plan-rev2-1111-research.md). Revised content: [rev2 details](../../details/2026-11-11/issue-184-bounded-live-plan-rev2-1111-details.md). Critique: [rev2 critique](./issue-184-bounded-live-plan-rev2-1111-critique.md).

## Objective

Correct the six findings of the independent adverse report against `76e21e9a` in new records, without editing the original five artifacts, and replace the combined approval with the single next design question. No source change, guard bypass, runtime gate, install or live action. No further automatic revision.

## Supersession and disposition map

The original artifacts remain immutable and keep their adverse history. Where a rev2 statement differs, rev2 supersedes it for planning purposes only.

| # | Severity | Original statement now superseded | Rev2 disposition | Where |
| --- | --- | --- | --- | --- |
| 1 | High | Receiver "reads from the latest position"; four short windows; stop at first failure | Corrected: `starting_position='-1'` is retained-stream beginning; success needs `max_events` receipts else `RUN_DEADLINE` exit 2; default 1000. Finite-window receive design is a prerequisite, no code change approved; run-specific ID linkage required | details sections 1 |
| 2 | High | "Hard maxima", "no send after expiry" | Corrected: expiry gates only new slot admission; logical slots, attempts, acknowledged sends and unique rows distinguished; no absolute stop claimed; stronger control is a separately scoped owner design prerequisite | details section 2 |
| 3 | Medium | 12,000 characters as conservative token bound; USD0.00576 as worst case | Corrected: serialized-byte reservation; 50,400 may admit fewer than four calls; four total physical attempts including retries; illustration only | details section 3 |
| 4 | Medium | Price rows without records; receiver 1,440 s | New dated retrieval with compact records, labelled new; replica 480 s, 1,920 s total; cost classes separated; no cap or affordability claim | research, price records, details section 4 |
| 5 | Medium | Critique "on the final candidate", d7c3b05b as run UUID | Qualified: single pre-revision invocation; d7c3b05b is an artifact identifier; native UUID recorded separately; wrapper exit missing, not inferred or recreated | research, critique, details section 5 |
| 6 | Medium | Combined spend, liability and execution approval question | Replaced by one design question; execution request deferred; unknown liability is a hold | details section 6 |

## Fixed decisions

* Protected and unchanged: captured-reading guards in `assistants.py` and `ai.py` (no seal, mock, renamed carrier or financial approval bypass), the non-case-scoped proactive scanner, missing receive path, expiry, currency, headroom, OD-51, #440, and human, resident, consent and professional approvals.
* The independent report is preserved byte for byte as a review copy; its approval is not claimed.

## Phases

* [x] Research (executed) then Plan (this file) then author critique (one pass, mine, not independent) then documentation revision then Review (scoped, mine, not independent).
* [ ] Independent review of this exact revision, owned by Root, before any publication or owner execution question.

## Follow-ups (not selected)

1. Owner chooses: retain the non-executable plan with the live-model criterion unproved, or have a separate narrow source and design proposal prepared for review.
2. Only later: a separate exact execution request.
