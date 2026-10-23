<!-- markdownlint-disable-file -->
# RPI Phase Details: issue126-cost-refresh-base-maintenance

## Metadata

* Task: 126 / issue126-cost-refresh-base-maintenance
* Date: 2026-10-23
* Plan: .copilot-tracking/plans/2026-10-23/issue126-cost-refresh-base-maintenance-plan.md
* Research: .copilot-tracking/research/2026-10-23/issue126-cost-refresh-base-maintenance-research.md
* Write boundary: only new maintenance artifacts; inherit rubric from main
  through the authorized rebase, never edit it manually.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Ready candidate after critique | P01-T01/P01-T02 |
| P02 | Dependent on P01 | P02-T01/P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Checkpoint and authorized local rebase

Original branch is clean at630603d69e3f2d4ef9b9f1b580da2f4ff6b82952.
Research has added only separate uncommitted maintenance artifacts, so seal
them before rebase. No existing work is stashed/discarded/carried elsewhere.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Seal maintenance readiness evidence

Use gh api user and derive {id}+{login}@users.noreply.github.com; set only
repository-local user.email, explicit author/committer values for new evidence
commits. Preserve original author attribution and Copilot trailer during replay.
Only named maintenance artifacts may be staged. Conventional Commit subject,
Refs #126 and Copilot trailer, no tracking paths in commit message.
Expected evidence: clean pre-rebase checkpoint and exact checkpoint SHA in
later changes record. Do not record rebase success in advance.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Rebase onto verified fresh main

Read-only fetch only origin main/topic and compare exact refs again. If main
has moved beyondf1e2d830 or topic beyond630603d6, stop this affected task with
new evidence; do not silently widen scope. No additional remote commits may
be dropped. Original unique630603d6 plus maintenance checkpoint must be replayed.
Use explicit no-autostash, no-update-refs, no-auto-squash rebase onto
f1e2d830f17558efd868919de1973ea7244a8841; no external hook/tool fallback.
Original old commit remains reachable by supplied SHA; no backup branch,
other worktree, ref deletion, reset, amend or force push is needed.

Conflict policy: stop on any conflict, even a potentially reconcilable one.
Record paths/status and unresolved decision, with no resolve, continue, skip,
silent abort or reset. This is a conservative subset of caller permission.
No canonical edits anticipated; record no-conflict result if actual.

<!-- rpi:phase id=P02 -->
## P02: Continuity and continuation Review

<!-- rpi:task id=P02-T01 -->
### P02-T01: Focused byte and consistency checks

Parse git ls-tree -r -z at old head and new replay head: compare all old paths'
mode/type/blob tuples, except .github/rubric/artifacts.json must exactly equal
new main. Assert no original missing paths, new additions exclusively belong
to the plan's Exact New-Artifact Allowlist. Checkpoint additions must be a
subset; final additions exactly all seven paths, including the separate
.copilot-tracking/rpi-sessions/2026-10-23/issue126-cost-refresh-base-maintenance-state.json.
Compare original ten paths with research SHA256 pins
and current working-tree bytes. Original log must be exactly equal, not merely
prefix. Original research/critique/Review/state all unchanged; entire product
tree also unchanged except inherited rubric.

Compare old-base/new-base rubric parsed JSON structurally: exactly one added
max_file_bytes20000000 in final capstone entry; all other values identical.
Check current rubric equals new base and original update git patch-id unchanged.
Inspect original current-cost subsection relative links/anchors using existing
local headings; inspect new artifact pointers/marker alignment, JSON/fences and
git diff --check. No new remote links or billing queries required.

Record actual checks and new ten-file SHA256 column in changes evidence.
Parent can read/hash only the existing named receipt/sidecar as inert evidence
to confirm retention, never invoke its environment/verifier or alter contents.
No full gate, queue, lock acquisition, tests that create worktrees or browser/
Docker/SQL/application/cloud runs.

<!-- rpi:task id=P02-T02 -->
### P02-T02: One actual continuation Review and final evidence commit

The original Residual work Review is immutable. New maintenance Review compares
this plan/details/critique/research/changes and focused results only. No
independent coordinator verdict or original residual closure inferred.
Disposition any material candidate finding by stopping and routing to later
coordinator work; do not repeat Review in the maintenance task.

Parent seals new Review and factual state/markers with an issue-only commit.
Pre-seal: staged paths must be an exact subset of the seven allowlisted paths;
all seven must exist. Validate new Review, state JSON, artifact pointers,
plan/detail task and phase markers, fences and whitespace. Post-seal: repeat
read-only full old-tree path/mode/blob and ten-SHA256 continuity, current rubric
equality, exact seven additions, clean status and fixed-base ancestry on final
HEAD. Report actual results with terminal SHA externally; no full gate,
official verifier or second Review. Any failure stops handoff as blocked.
Before/after any transition persist intended/resulting state in the separate
new state, never shared/original state. Final commit digest is external to
itself. Recheck clean status, current main and topic remote lease by read-only
git refs; report exact head/base/lease and ancestor relation. If refs move,
report new blocker, do not rebase repeatedly. Stop before gate/publication.

Known residuals: original costs/headroom Unknown; current prices/operator/
tenant/task readiness not proved; USD700 replacement ceiling and unchanged
expiry remain; prior receipt tied to old base is historical. No KB/source
rewrite needed. Coordinator owns any gate/independent/publication sequence.
