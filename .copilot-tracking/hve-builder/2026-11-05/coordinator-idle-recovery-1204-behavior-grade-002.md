<!-- markdownlint-disable-file -->
# Independent grade: behavior test 002 (correction run), issue 1204

Grader: independent read-only pass over the scenarios and test log, with grep spot-checks against `.github/agents/ama-backlog-delivery-coordinator.agent.md`. No scenario was re-executed.

## Spot-check of quoted phrases

* "when the tool supports it" found at line 692 (step 8). Confirmed, and no fallback is stated.
* `BASE RELAXED` (lines 451, 695), `--required-scope partial` (438, 698), `--resume` limited to a failed gate run (460, 698): confirmed.
* "not an owner gate unless its actual cause needs owner authority" (709): confirmed. The R1 report quote "exact-head review stays valid" is a paraphrase of lines 703-704 ("does not by itself invalidate"), not a verbatim target phrase.
* Cleanup: finite manifest and delegation (198-206), unknown upstream defers (206, 215), receipt holder deferral (213): confirmed. The literal text "no upstream" does not appear, only "missing upstream".
* Sessions and PRs: auto-merge stays open until merge is confirmed (102), counted once and checked separately (103-106): confirmed.
* Idle tick, `task_complete` and dependency on a running predecessor (130-138): confirmed.
* Schedules: provenance with #9, #8, #6, #2, #7 and "not byte-identical" (183-187): confirmed.
* "two active deliveries": there is no literal match. Repair of a zero or two read-back is at about line 176 (confirmed by context).

## Grades

| Scenario | Grade | Basis |
| --- | --- | --- |
| R1 | Pass | Matches expected: refresh at the existing head, no rebase, not an owner gate, no merge this tick. Lock deferral cited. |
| R2 | Pass | BASE RELAXED valid with no rebase. #2503 treated as ready repair, failed output kept, new `--changed` receipt at the same head, verified with `--required-scope partial`, no `--resume`. |
| R3 | Pass | 1801 removed through the manifest without `--force`. 1802 and 1803 deferred, with the holder and unknown upstream named. Both /tmp paths preserved with a scoped owner question. Disk pressure is not treated as authority. |
| R4 | Pass | 14 open PRs (queued one included), 8 sessions counted once, no launch, ready issues stay `ready`, closure and PR work continue. |
| R5 | Pass (with caveat) | Tick ended only, no `task_complete`, schedule kept. The executor read pre-N1 text, so the final wording was not exercised. |
| R6 | Pass | Exactly #9 and #8 active, #6, #2 and #7 stopped, evidence supplied and not run by the worker, condensed prompts, repair of a duplicate with readback. |

No forbidden behavior (rebase, merge, force removal, self-approved broad deletion, schedule stop, extra launch, byte-identical claim) appeared in any trace.

## Gaps

| # | Severity | Gap |
| --- | --- | --- |
| 1 | Medium | R1/step 8: "when the tool supports it" has no stated fallback. If the tool cannot refresh a full receipt at the existing head, the action (new full run versus rebase versus wait) is unresolved and could prompt a wrong rebase. |
| 2 | Medium | R5: the executor saw pre-N1 text, so the post-edit wording is not evidenced by this run. The test only supports the correction if the N1 edit is wording-only, which is asserted by the lead and not independently verified. A one-scenario re-run on the final head is needed. |
| 3 | Medium | R5: the class of PRs waiting on a not-yet-existing exact-head review is not defined. If an independent review is launchable, those PRs are executable work and exclude an idle tick. The executor flagged this and the target does not resolve it. |
| 4 | Medium | R6: no rule picks which of two active deliveries to keep or stop. A wrong stop could leave zero active deliveries (step 4 of the replacement rule only says repair). |
| 5 | Low | R3: where the manifest is recorded, and whether the coordinator's record is itself the approval, is only implied. |
| 6 | Low | R3: the owner question bundles two paths. A one-question-per-path rule is not stated. |
| 7 | Low | R2: order of #2502 and #2503 and base drift after the first merge are unspecified. Step 8 rechecks after each merge, which likely covers it. |
| 8 | Low | R2: behavior if the replacement receipt also fails is unspecified. It would presumably repeat as ready repair, with no escalation bound. |
| 9 | Low | R4: ordering of the 3 ready issues when a slot frees is unspecified. |
| 10 | Low | R5: whether an allowed idle tick counts against the no-progress rule, and one-line versus summary report, is unspecified. |
| 11 | Low | R6: executors read the whole target, so the R6 pass is not an isolation test of the provenance section. |

## Limits of this evidence

* Executors ran on an inherited proxy model of unknown profile. Passes may not transfer to the production model.
* The scenarios were designed by the same lead that wrote the corrections (disclosed). They mirror the new wording, so they confirm the text is readable and consistent, not that it resists adversarial prompts.
* All commands were emulated, with no live tools, and each scenario ran one time with no variance estimate.
* The run covers only the behaviors changed by the correction. Original S1-S8 coverage is historical for commit ef585f5.
* Four scenario answers (R1, R2, R3, R6) depend on the executor inferring flags or procedures that the text leaves open, so passes there are partly inference.

## Overall verdict

Revise. All six scenarios pass on expected and forbidden behavior, but under the strict rule four unresolved ambiguities (gaps 1 to 4) could cause a wrong action (an unnecessary rebase, an idle tick with executable review work, a wrong schedule stopped), and the R5 evidence predates the final wording. Close gaps 1 to 4 with small text edits, then re-run R1, R5 and R6 on the final head.
