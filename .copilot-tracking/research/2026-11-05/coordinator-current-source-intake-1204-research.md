<!-- markdownlint-disable-file -->
# Research: coordinator current-source intake (issue 1204, pass 5)

Written 2026-11-05T22:49Z in the original RPI session 6e276cf2-92a2-4158-a0be-70a8e778bbd6 before any new implementation edit. Research disposition: executed (bounded, inline). The activity-handoff session 74980a69 produced 6465ac16d; it was not this session and its records are preserved unchanged.

## Sources and base

* Start HEAD 6465ac16d330129ae0314d7a5ad2df79464406f1, tree 5ffa7280eb6144ffa4759534141aee5f9ff5ae27, clean.
* Freshly fetched origin/main bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f; old merge base ead177ef90d24666557708ea344848a1be43bdf8; main was six commits ahead.
* Issue 1204 (OPEN) has six criteria; the schedule criterion is already ticked. Five remain: fresh-classification stop decision, per-tick real action with closure-review progress and approval reconciliation, one-at-a-time questions with routed approved actions, launch handoffs that forbid premature publication with finite verified cleanup, and dated RPI evidence with independent static review, behavior scenarios and focused checks.

## Delta: 6465 instruction versus latest main

* The agent file is unchanged on main (578 lines on main, 792 on the branch). No conflict is possible.
* Main changed tools/backlog-sync.py (pass --active and --inactive, positives-only activity, unknown stays In Progress and unverified), tools/test_backlog_sync.py, tools/rpi-checks.py, tools/test_rpi_checks.py, src-ci.yml and the rubric score.
* Consequence: the instruction sentence "Until the activity-handoff tool change (#1207) is accepted and published ... do not run it" describes a state that main now contains. The existing rule already gates use on `--help` listing the flags, so it stays safe; the stale premise needs a short update. The legacy `--apply` rule stays negative evidence.

## Live schedules

* Operator-supplied: live delivery schedule 15 (10 minutes) and cleanup schedule 8 (hourly). These supersede the delivery #9 named in the Provenance bullet of the agent file. No live prompt text for 15 was supplied in the session evidence; only older v2 snapshots exist (delivery-schedule-v2.txt, cleanup-schedule-v2.txt, schedule-recovery-review.md). This pass does not create, stop or edit schedules and does not overwrite their provenance.
* Gap G2: the Provenance bullet names #9, so a reader would treat a superseded id as final. Fix scope: record that ids are as of a dated read-back and that the live list (currently 15 delivery, 8 cleanup) is authoritative, without restating prompts.

## Instruction gaps found (current source)

* G1 capacity: line 98 defines eight as TOTAL live issue sessions. The owner's current rule counts retained assignments, including frozen unpublished candidates awaiting coordinator validation, within eight. The text does not count them, so a candidate with no live tmux session could free a slot wrongly.
* G2 schedule provenance as above.
* G3 stale activity-handoff premise as above.
* No gap found for the 20-PR drain, original qualified RPI workers with explicit Sonnet 5.5 (step 5), no-push workers, one-at-a-time questions, or finite cleanup; these are covered by the earlier passes and are retested (not assumed).

## Automatic-profile mechanism (owner approved the intended profile; this resolves only the profile question)

Installed CLI facts, read-only:

* `copilot --model auto` selects Auto; `--auto-tier` and `COPILOT_AUTO_TIER` set routing; persisted `autoTier` and `model` config are unset (exit 1). The coordinator agent frontmatter sets no model.
* Containment flags exist: `--available-tools`, `--no-ask-user`, `--disable-builtin-mcps`, `--max-ai-credits` (minimum 30), `--log-dir`, `--share`, `-p`.
* Probe on 2026-11-05T22:48Z: `copilot --agent hve-core-all:hve-artifact-tester --model auto --available-tools view grep glob --no-ask-user --disable-builtin-mcps --max-ai-credits 30 --log-dir /tmp/h1204/logs --share /tmp/h1204/probe-share.md -s -p <probe>` exited 0. The share transcript records "Auto selected GPT-6 Luna since the task has low complexity." and the child reported only view, rg, glob tools. So Auto routing and read-only containment are observable; the resolved model can vary per task.
* Limits: the tier is unresolved (autoTier unset); Auto may pick different models per case; the executor has read tools only, so shell and write actions are emulated as text decisions, not executed; each child needs a credit budget; `--share` is the evidence. Omitting `--model` is not treated as proof of Auto.

## Rebase decision

Named reason: current-source intake, so focused checks (backlog-sync and rpi-checks unit tests) run against main's current tools and the delivered candidate is based on current main. The branch was clean and unpublished. Backup ref backup/issue-1204-pre-rebase-6465 preserves 6465ac16d. Local rebase onto bb3a3b03cb completed without conflict; new head 680d92edb8e86f1095c98fa1fdb9cd93989c34c6, tree 92473c5d9ca54cac96ee918a5c7508f01fd888bf. Pre-rebase SHAs (ef585f5, 04ed9a82e, f38162533, 6465ac16d) are historical; all earlier validation is invalid for this head. The agent file content is identical to 6465.

## Test coverage required (synthetic fixtures only)

Unsupported idle and unknown closure work; one blocked lane with ready independent work; capacity counting a retained unpublished candidate (G1); approved actions and one-at-a-time questions; child target and publication gates; retention-safe cleanup with active receipt and unknown upstream; negative controls (a weakened-rule fixture must fail).

## Focused checks selected

Unit tests for tools/test_backlog_sync.py and tools/test_rpi_checks.py (stdlib unittest, no heavy lock, PYTHONDONTWRITEBYTECODE=1), git diff --check, frontmatter diff, ASCII and local-link checks. Excluded by owner: rpi-checks --all, --changed, SQL, browser, images, scanners, pruning, lock queueing.

## Planning Readiness

Ready. Gaps G1 to G3 are small and bounded to the agent file.
