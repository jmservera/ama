# Issue 1409 record reconciliation: research

Date: 2026-11-10. Task `issue-1409-record-reconciliation` (parent `issue-74-provenance-qualification`). Base `54eae28f8bc2b3c5e3786ab5169b0ed375f826ef` on branch `docs/home-audit-record-reconciliation-1409`. Research disposition: executed. Planning Readiness: Ready.

## Request and scope

Issue #1409 (Low, nonblocking, documentation only, `Refs #74`) asks for three things: a dated reconciliation of the delivered Phase C and the superseded Phase 4 instructions in the #74 planning records; preservation of earlier commits, adverse reviews, provenance limitations and human approval boundaries; and verification of the documentation diff and links without claiming fresh product execution or whole #74 acceptance. Backlog admission recommends the smallest change: one dated reconciliation plus precise cross references in the existing records.

Out of scope: runtime source, public policy, source grants, permissions, human gates, any whole #74 acceptance or criterion tick, #134 and #440 work, push, PR and issue or board writes.

## Evidence

* Independent finding (Low, number 1, file `.copilot-tracking/plans/2026-11-10-issue-74-qualified-audit-plan.md` line 29): the Phase C line is unchecked although the review, completed state, commit and handoff exist; details line 22 and critique line 13 still say the Phase 4 unchecked text was left intact, whereas the plan checks Phase 4 and explains the historical state. The same finding states these are minor internal inconsistencies, not missing human approval. Original report: the same-reviewer final additive provenance assessment at `99fd20bc11432c718d14257bc15281641c3c8cb4` (tree `b7a0650cbe7bdec0681e4d8906a75364575711c6`), `readiness/readiness-findings.json` in the external directory `independent-74-provenance-1999`. Its suggested fix: reconcile delivered Phase C and qualify the superseded Phase B and P3 instructions as changed in favour of the dated Phase 4 checkbox reconciliation, preserving historical commits and all human gates. It also notes that the handoff statement of standalone validation before every marker is stronger than the visible log between commit and commit-complete; that provenance limit is kept as is.
* Delivery of Phase C: commit `99fd20bc1` (`docs(rpi): qualify issue 74 review ordering and validator provenance claims`) added `.copilot-tracking/reviews/2026-11-10-issue-74-provenance-qualification-review.md` (self-review, not independent) and `.copilot-tracking/rpi-sessions/2026-11-10/issue-74-provenance-qualification-state.json` (completed, Follow-up, session running, blocker B1 pending independent reassessment, hosted CI and human approval). It reached main as squash `47e43ec7f` (PR #1406); the three target records are byte-identical between `99fd20bc1` and `47e43ec7f`. The handoff is external (`handoff-74-provenance-qualification-1110.md` under the session files directory) and is not a repository file.
* Phase 4 history: commit `cb400d618` held `* [ ] Phase 4` (plan line 14); commit `99fd20bc1` changed it to `* [x]` with a dated note (plan line 23) and kept the history in the commit.
* Superseded instructions, all in three files:
  * Plan `.copilot-tracking/plans/2026-11-10-issue-74-qualified-audit-plan.md` line 29: Phase C `[ ]` (stale); line 28 (Phase B) describes reconciling Phase 4 "as a dated note", which the commit did together with the checkbox change.
  * Details `.copilot-tracking/details/2026-11-10-issue-74-qualified-audit-details.md` line 22: "Phase 4 line is left as written ... The `[ ]` text is not rewritten."
  * Critique `.copilot-tracking/reviews/plans/2026-11-10-issue-74-qualified-audit-plan-critique.md` line 13: P3 "leave Phase 4 `[ ]` text intact and add a dated delivered note".
* Not in scope on inspection: `.copilot-tracking/plans/2026-11-10-issue-74-main-acceptance-audit-plan.md` Phase 4 (field and role matrix) is a different, checked phase with no superseded instruction. No human or PR-review checkbox exists in these records.

## Approach options

1. Add a dated Reconciliation addendum to the plan, one dated additive note under each of details and critique, and leave every historical line in place. Chosen: smallest change, additive, consistent with the existing style of dated notes in these records.
2. Flip the Phase C checkbox in place and rewrite lines 22 and 13. Rejected: erases the original instruction text and weakens the historical record; the owner and independent reviewer both asked for preservation.
3. Add a new standalone document. Rejected by the admission ("no new broad audit or product document").

Decision on the Phase C line: the stale `[ ]` is left as written and a dated line states it is delivered; this mirrors how Phase 4 was handled and avoids rewriting history. The addendum states the checkbox reconciliation by dated note, so a reader of the plan sees the current disposition at the first stale line.

## Constraints to carry

* Additive only: no historical line is deleted or edited; no commit, hash, review outcome or provenance qualification changes.
* The delivery of the review, state and commit is documentary delivery only. It is not human approval, independent approval, hosted CI success, a gate waiver, #74 acceptance or a criterion tick. #74 and #73 stay open; B1 and the routed follow-ups of the parent state remain unchanged.
* Validation tier: focused docs-only: changed-file allowlist, diff review, link and anchor check, ASCII check. No tests, gates, scanners, browsers, SQL, images or provider calls.
* Closure: this work may support `Closes #1409` only when review evidence proves all three criteria; it must never close #74.

## Planning Readiness

Ready. Targets, line numbers, delivery commits and boundaries are verified against local Git objects and the external independent report; no unresolved dependency.
