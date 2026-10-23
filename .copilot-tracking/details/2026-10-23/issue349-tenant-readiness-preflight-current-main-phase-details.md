---
title: Issue 349 current-main continuation phase details
description: Evidence-led local rebase, validation, Review and seal
ms.date: 2026-10-23
---

## Metadata

Task ID: 349-current-main-20261023.
Slug: issue349-tenant-readiness-preflight-current-main.
Plan: .copilot-tracking/plans/2026-10-23/issue349-tenant-readiness-preflight-current-main-plan.md.
Research: .copilot-tracking/research/2026-10-23/issue349-tenant-readiness-preflight-current-main-research.md.
Initial direction: preserve checker and main intent without changing behavior.
No unresolved product decision. One critique Complete/Revise; PC-001/PC-002
accepted and directly applied in the plan. P01/P02/P03-T01 complete;
P03-T02 final commit next, P04 pending at this pre-seal snapshot.

## Progression Rule

Any failed required command, preservation invariant or unresolved blocking
Review finding stops dependent work; preserve actual evidence and report the
blocker without automatic remediation, repeat Review or gate retry.
Seal/gate requires all prior required checks passed and one Review with no
unresolved blocker. Coordinator/hosted/live limitations remain distinct.
Let an already running gate finish if main moves, then report stale.

<!-- rpi:phase id=P01 -->
## P01: Reconcile local history

<!-- rpi:task id=P01-T01 -->
### P01-T01: Preserve phase evidence and both source histories

C1/C2: local is ancestor of remote, with one generated remote-only score.
Use git format-patch for exact 3b881a65 and 6c284d45 commits into
.copilot-tracking/research/2026-10-23/issue349-current-main-evidence/.
Exactly two patch outputs; no generation of active scores or new claims.
Record commit/parent/run/hash evidence, derive local privacy-safe email with
gh api user and commit this genuine pre-rebase evidence checkpoint.
No existing uncommitted user work was present at intake.
Actual: two format-patch outputs generated and committed with phase evidence
as 4fd7a32f5b418d53fa22069ae980740cdde94c3d before history change.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Rebase preserving known intents

Depends P01-T01. Re-fetch main/topic, inspect any movement. Rebase checkpoint
onto remote topic, which retains the only remote-only commit; no merge.
Then replay old-base topic onto exact main with an explicit todo dropping
only 3b881a65 and 6c284d45, now archived and superseded for active latest.json.
All five human commits and phase checkpoint remain. No automated ours/theirs.
Capture real conflict decisions or conflict-free result; stop unfamiliar
conflict rather than altering intent. Do not edit main KB or append-only log.
Actual: refreshed refs unchanged; remote integration and exact-main replay
both conflict-free. Result fab84fa4a0e82b920808fd06c64d7856e68183e9.
Explicit todo dropped only both archived score commits; five human commits
and phase checkpoint remain. No merge, source edit or blanket resolution.

<!-- rpi:phase id=P02 -->
## P02: Validate reconciled checker

<!-- rpi:task id=P02-T01 -->
### P02-T01: Ownership and distribution prerequisites

Depends P01-T02. Inspect process lineage and lslocks immediately before
validation. Current tmux rpi-349-current-main is this resumed task, not a
competing gate by label alone. Respect any actual held lock/other gate.
Create a fresh isolated non-receipt environment for this continuation.
Check its missing installed distribution metadata before application/infra
execution, then install existing core/agents/api/orchestrator/importer
distributions with pip -e per source commands. Bind all focused tests/tools
to that interpreter; record its path, checkout and five distribution sources.
Use no old receipt environment for installs or cache changes.
Actual: no gate process or held ama-rpi lock before validation. Fresh context
/tmp/ama-349-current-main-20261023-focused-7R5VgG/venv was created; metadata
confirmed all five project distributions missing. Pip installed existing
dev manifests, all project versions 0.1.0, direct_url editable sources bound
to this worktree's five src projects. Pip check passed. No prior environment
was touched; install log retained in the fresh context's parent directory.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Focused validation and reconciliation invariants

Depends P02-T01. No test additions/removals and no production edits planned.
Run all 35 focused tests with -B, isolated no-cache Ruff 0.17.1 lint/format,
strict checker mypy with external cache and whitespace check.
Compare Git blobs for checker/tests and every original topic RPI artifact
to 3eebcc39; compare all main-only changed files, full docs/reference/log.md,
latest.json and badge.svg to exact main. Record range-diff for all original
topic commits, explaining only two bot-score omissions. No private datasets.
Actual: 35 tests passed with -B; isolated no-cache Ruff lint/format passed;
strict checker mypy and diff check passed. All 28 original source/test/RPI
blobs identical to initial HEAD; all 10 main-changed files identical to exact
base, including entire KB log and active rubric files; both Git patches exact.
Five human patches range-diff identical, two expected bot omissions only.
Pip generated five ignored .egg-info directories in this worktree; inspected
and removed only those named generated directories, not any receipt environment.
Focused environment and logs retained externally; no ignored candidate inputs.

<!-- rpi:phase id=P03 -->
## P03: Original Review and committed candidate

<!-- rpi:task id=P03-T01 -->
### P03-T01: One independent Review

Depends P02-T02. Fresh worker activates rpi-review. Read the original history,
reconciliation evidence and new artifact set. Write only
.copilot-tracking/reviews/logs/2026-10-23/issue349-tenant-readiness-preflight-current-main-review.md.
No source fix, second Review, gate or remote action. Execution/outcome distinct;
preserve original dispositions and route residual coordinator/live limitations.
Actual: one Review Complete/Conformant with no blocking source/history finding.
Independent read-only reproduction confirms all 28 original blobs, all 10 main
files, both patches, ordered reflog and human commit mapping. No reviewer
test/install/gate/live execution; parent focused evidence attributed accurately.
RV-001 parent seal/gate, RV-002 coordinator and RV-003 hosted/live residuals.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Seal complete RPI evidence

Depends P03-T01. Reconcile plan/detail/changes/state and commit all continuation
artifacts with required privacy-safe identity/trailer. Gate is pending, not
predicted passed in committed evidence. Re-fetch/confirm exact main, inspect
ownership and clean inputs, then seal without later repository mutations.
Pre-seal actual: fetched main/topic unchanged, no other gate process or held
heavy lock, intended four artifact updates plus new Review only; no ignored
inputs. Privacy-safe authenticated identity resolved again. Positive eligibility
satisfied; final commit/gate are future actions, not retrospective claims.

<!-- rpi:phase id=P04 -->
## P04: Single exact-head full gate

<!-- rpi:task id=P04-T01 -->
### P04-T01: Gate once and verify currentness

Depends P03-T02. Use one new unique external /tmp/ama-349-current-main-20261023-*
output, not an existing directory or prior receipt environment. Exactly one
tools/rpi-checks.py --all; no --extra-test change or disabled group required.
Retain SQL parity, browser, Docker/non-root, scanners, logs and environment.
Do not interrupt another lock owner, duplicate/restart gate or clean receipts.
Let gate finish even if main moves. Fetch main, officially verify against
current origin/main, hash receipt and report current vs stale honestly.
Keep post-commit completion state external. STOP BEFORE PUSH.
