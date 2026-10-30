<!-- markdownlint-disable-file -->
# RPI Plan: Issue 440 current-main integration and final gate

## Task Metadata

* Task ID: 440; parent: #123 (hierarchy only). Slug: issue-440-current-main-integration.
* Plan date: 2026-10-25, written before any merge or edit.
* Research: .copilot-tracking/research/2026-10-25/issue-440-current-main-integration-research.md.
* Phase details: .copilot-tracking/details/2026-10-25/issue-440-current-main-integration-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-25/issue-440-current-main-integration-plan-critique.md (one execution, Revise; PC-001 to PC-004 applied directly).
* Prior review (immutable): .copilot-tracking/reviews/logs/2026-10-24/issue-440-stabilization-review.md.

## Objective

Integrate origin/main ea5577b2 into the existing branch with a non-rewriting merge, resolve only the two append-only documentation conflicts, then run one genuine full local gate on the frozen clean exact head and verify its receipt. No new coordinator feature, no threshold waiver, no second Review.

## Phases

* [x] P01 Pre-merge checks and state: re-fetch main, confirm clean tree and free lock, persist state with intended next action.
  * [x] P01-T01 Record main SHA, HEAD and tree and the conflict prediction.
* [x] P02 Integrate main by merge.
  * [x] P02-T01 Merge origin/main without fast-forward; resolve docs/reference/README.md and docs/reference/log.md keeping both sides.
  * [x] P02-T02 Verify no loss: main's log bytes preserved, branch entries preserved, no other file differs from main outside the five branch files and own tracking.
  * [x] P02-T03 Check that the coordinator and src/README.md still match their pre-merge blobs and that frontmatter is unchanged.
* [x] P03 Lightweight validation before the heavy gate.
  * [x] P03-T01 Run only cheap checks: git diff --check, relative-link check of the changed docs, runner --help flag inspection to confirm local-only.
  * [x] P03-T02 If cheap checks expose a defect, apply the bounded fix procedure below.
* [x] P04 Update dated evidence and freeze the candidate.
  * [x] P04-T01 Append to the cutover evidence pack a dated reconciliation note: main moved, the pinned first checkpoint is historical for 140d8f49, attested-discovery caveat, failed receipt kept as repository record only, gate pending.
  * [x] P04-T02 Append one new dated entry to docs/reference/log.md. Do not edit earlier entries.
  * [x] P04-T03 Reconcile changes record and state. Stage and commit once, with privacy-safe author and committer and the Copilot trailer: this plan, details, research and critique, the evidence pack, log, changes record and state (critique PC-002). Require an empty git status --porcelain --untracked-files=all before launch. This is the legitimate evidence commit, not a receipt-only one.
* [ ] P05 Final full gate.
  * [ ] P05-T01 Fetch origin/main and record the fresh SHA. If it moved, repeat P02 to P04 for the new head (still before any gate), then continue. Use the fresh SHA for both --all and --verify-receipt (critique PC-001).
  * [ ] P05-T02 Launch python3 tools/rpi-checks.py --all --base <fresh origin/main SHA> --out /tmp/ama-440-final-ea557-gate1 --lock-timeout 14400 asynchronously; record PID and log path; freeze the worktree; do not poll in a loop.
  * [ ] P05-T03 On completion run --verify-receipt against fresh origin/main; record receipt path, SHA256, head, tree, base and the actual benchmark result against the unchanged 1500 ms threshold.
* [ ] P06 Disposition and publication decision.
  * [ ] P06-T01 Publication rule (critique PC-003): a verified receipt plus no technical blocker makes a draft PR eligible. RV-003 (attested, unreproduced discovery), simulated-only behavior evidence and unmet acceptance criteria are carried as stated residual work; claim no Conformant outcome or acceptance, leave human checkboxes unchecked, no discovery redo. Then push the branch normally and open a DRAFT PR, Refs #440 with no closing keyword, honest Residual work and unmet criteria, simulated and attested evidence labelled, no merge. No receipt-only commit.
  * [ ] P06-T02 If the gate fails or is stale, record the exact evidence and resume point and do not publish.

## Correction Procedure (any P03 or gate failure; critique PC-004)

* Keep the failed output and receipt; never overwrite or delete.
* Reproduce the exact failing check in isolation with the smallest focused test.
* Classify: this branch's defect, a main defect, environmental or unknown. Only a defect in this branch's scope may be fixed here. A main defect gets a separate scoped issue and a blocker, not an unrelated fix. The benchmark threshold and the gate are never changed.
* Each cycle is a bounded plan addendum with a focused test, then a new head and a new gate with a new unique output path. At most two cycles, then report the blocker.
* A change to the coordinator artifact invalidates static, behavior and host evidence and requires hve-builder contained simulation. Actual coordinator rollout and model tasks are not authorised.

## Success Criteria

* Merge preserves all of main and all of the branch intent, append-only logs intact, with no rewritten history.
* Final receipt from a complete run on the exact clean head and current main, verified officially.
* Honest report of each original finding disposition, the benchmark result, and evidence classes.

## Constraints

* Local only. No Azure, Microsoft 365, Graph, live SQL, providers, spending, resource deletion or discovery redo. Protect the ama-350-feedback-sql container and other sessions' worktrees and outputs.
* Leave human-review checkboxes unchecked. No acceptance ticks. No memory.md change.

## Follow-Up Items

* Later stabilization checkpoint on new main (BRD 0.21.0, PRD 0.20.0, #360 Entra access) scheduled by the coordinator.
* Benchmark repeatability diagnosis if it recurs.
