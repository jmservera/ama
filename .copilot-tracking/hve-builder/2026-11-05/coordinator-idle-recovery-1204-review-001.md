# Static review 001: ama-backlog-delivery-coordinator (issue #1204)

Target: .github/agents/ama-backlog-delivery-coordinator.agent.md (702 lines, read in full)
Baseline: HEAD diff (180 insertions, 56 deletions). Frontmatter unchanged (name, description). `tools:` ignored by instruction.
Criteria: hve-builder requirements-catalog.md and review-rubric.md.

## Verdict: Pass

No Critical or High findings. The eight stated requirements are present and findable. Five Medium and three Low findings remain; none blocks the purpose. Fix the Medium items before merge if cheap.

## Requirement coverage

* R1 liveness and classification: met (Liveness and stop decision, classes and unknown rule).
* R2 real next action, rotating batch of five, session SQL, no-op ban: met.
* R3 two no-progress ticks, bounded recovery, tick is not the run, task_complete ban, owner pause and real gates: met.
* R4 one question at a time, approvals persisted, reclassification, no re-request or expansion: met.
* R5 caps, stacks, batching, tiers, no gratuitous rebase: met; PR admission rule consistent (see below).
* R6 schedule replacement and read-back, versions and ids persisted, live tool: met.
* R7 fresh briefs, no worker publication, no stale /tmp template: met (step 5).
* R8 cleanup contract: met.

Stale-term sweep: no "5m", "every push" (only the accurate CI sentence, line 283), "stop that schedule" or old `/tmp/brief-{number}.md` remain. The PR-count rule is consistent in lines 95-100, 294-297 (more than 20 drain to 10-15; admit only at 15 or fewer; 16-20 launch nothing).

## Findings

F1. Workflow contract, Medium. Lines 119-126 (stop rule) vs lines 10-13, step 9 (lines 664-668), Inputs lines 192-195.
The stop rule allows stopping the schedule only when scope is delivered or the owner pauses. The opening paragraph and step 9 also end the run when every remaining issue is merged or human-blocked with fresh classification, and Inputs says a limit pauses the run. The three terminal outcomes are not stated together, so a reader can keep polling forever when everything is human-blocked, or stop on a limit without a rule to cite.
Fix: add to line 125 "or every remaining item is merged or human-blocked/dependent on a human with a fresh classification, or a stated limit is reached".

F2. Workflow contract, Medium. Line 192 vs lines 94-96, 307-308, 466.
Inputs still says "maximum parallel loops (default 3)"; the eight-session limit overrides it only by a parenthetical in Liveness. Step 3 and Stabilization still refer to "the parallel limit". Contradictory layers resolved by a cross-reference.
Fix: change Inputs default to 8 and drop "overriding the Inputs default of three" from line 95.

F3. Workflow contract, Medium. Step 5 lines 520-521 (retry once then "becomes a human blocker with its log path") vs Human blockers and Liveness rules.
A launch that fails twice is declared human-blocked without a real human gate, which conflicts with "human-blocked needs a real gate" and with the bounded-recovery rule (repair the failing launch route). The Human blockers list covers "a check the loop cannot fix", so the wording needs to be aligned.
Fix: "retried once in the same worktree, then diagnosed under the bounded recovery rule; ledger it as a blocker only when the cause needs a human (missing tool, credential, decision)".

F4. Emphasis calibration, Medium. Duplicated rules.
* Eight active sessions: lines 95-96, 307, 466.
* PR cap and admission: lines 96-100 and 294-297 (the second points to the first but restates thresholds).
* "Green checks and MERGEABLE never replace missing selected-tier evidence": lines 107-108 and step 7 (lines 625-628).
* "Nothing changed" handling: lines 121-123 and step 5 (lines 593-594).
Fix: keep one canonical statement (Liveness for admission and session limit; step 7 for merge evidence) and point to it elsewhere; for CI economy replace the restated thresholds with "see admission rule".

F5. Workflow contract, Medium. Line 98-99 and line 294-295 use "rebase" for PR repair.
"Repair, rebase and merge existing PRs" in the cap rule can be read as licence to rebase valid green heads, against line 289-290 and step 8.
Fix: write "repair (rebase only under step 8), review and merge".

F6. Convention/structure, Low. Lines 59-61.
The new sentence "A missing local gate... are work for the run" is fused into the paragraph about commenting on blockers, mixing two rules in one block.
Fix: split into its own bullet or paragraph.

F7. Load-timing, Low. Lines 68-70.
The incident narrative (5 November ticks, 99 reviews) is history in an always-loaded rule section; the rule stands without it. The heading also carries dates and an issue number.
Fix: shorten to one clause or move the narrative to the issue/log.

F8. Convention, Low. Lines 486 and 488.
Brief path is written `{UTC timestamp}` in one place and `{timestamp}` in the command; the log path `/tmp/rpi-{number}.log` is reused across retries and is not versioned.
Fix: use one placeholder name; optionally note that the retry overwrites or appends to the same log.

## Not findings

* Section order (purpose, delegation, blockers, liveness, schedules, cleanup, inputs, workflow, boundaries, report) places outcome and stop rules before steps, as the rubric prefers.
* Line 3 description still says "stopping only on human blockers"; frontmatter is out of scope and must stay unchanged.
