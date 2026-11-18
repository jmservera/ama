<!-- markdownlint-disable-file -->
# Plan: issue #126 restart follow-up (six-module batch and three evidence-quality gaps)

* Task: `issue-126-restart-followup` (parent `issue-126-residual-source-assessment`); date 2026-11-17; mode automatic
* Research: `.copilot-tracking/research/2026-11-17/issue-126-restart-followup-research.md` (Planning Readiness Ready)
* Phase details: `.copilot-tracking/details/2026-11-17/issue-126-restart-followup-phase-details.md`
* Critique: `.copilot-tracking/reviews/plans/2026-11-17/issue-126-restart-followup-plan-critique.md`
* Validation tier: focused. Basis: the only repository changes are `.copilot-tracking` Markdown/JSON evidence plus one additive update to an existing tracking table; no application, test, SQL, config, workflow, gate-tool, dependency, Dockerfile, policy, requirement, agent or skill file changes, so no permission, package, secret, deployment, security control or gate semantics change. HVE not applicable.

## Objective

Run the deferred six-module core test batch with proven own-source installs, record exact counts and skips with external logs, refresh the seven affected rows of the existing 22-row table additively, and close the three low evidence-quality gaps (MAP-01 test linkage, MN-3.2 tier rationale, unretained verifier) without implying acceptance or closure.

## Boundary

* Writes: `.copilot-tracking/**` (new dated follow-up artifacts, one small additive section in the existing table) and the external evidence directory only. Original Review, parent state, research, plan, details, critique and changes unchanged. No `log.md`, `memory.md`, application, test, SQL or config edit; no push, PR, remote, deletion, stash, amend or rebase.
* No SQL opt-ins, browser, container, Azure, live or paid model, private data or full gate. Skipped SQL or real-AI tests stay unproven, not pass.
* Vocabulary and tier rule are the parent table's (`RAI_TIERS`); a tier changes only where a directly relevant passed test covers the baseline engineering gap. No row is closed; no issue tick.

## Phases

* [x] P01 Research and lineage (Research artifact; witness `research-open` seq 2)
* [x] P02 Plan, details and one independent critique (verdict Revise; PC-001..PC-004 applied directly)
* [x] P03 Implement (witness `implement-start` after the changes record exists, before any table edit)
  * [x] P03-T01 Stage `git archive HEAD src/core` outside the candidate, create an external venv, run the chosen command, record the missing-module report, then pip install the staged own-source and hash-prove installed modules equal worktree files
  * [x] P03-T02 Run the six modules once from `src/core` in a clean `env -i` environment, single process, external logs and SHA-256, exact counts and skips
  * [x] P03-T03 Add the additive "Restart Follow-Up Update" section to the existing table (qualified dispositions for affected rows, MAP-01 context label, MN-3.2 rationale as missing retirement-detection test evidence plus absent human review, external verifier reference by path and script hash)
  * [x] P03-T04 Retain and run the reconstructed external verification helper on the table section and logs (hashes recorded externally and in the changes record only)
  * [x] P03-T05 Write the changes record and reconcile plan markers (witness `implement-done`)
* [x] P04 (outcome Partial; MAP-01 wording corrected after Review) One original read-only Review scoped to the follow-up (witness `review-done`)
* [x] P05 Commit locally with verified identity and trailers, freeze, rerun lightweight checks at final HEAD with external outputs (witness `commit-complete` with the real SHA)

## Gates

* Critique executed once; compatible findings applied directly; not repeated.
* Review executed once; findings route to later work.
* Final: `git status` shows only intended tracking paths; source blobs unchanged against start `23eca3a5`; no caches, egg-info or raw bundles staged.
