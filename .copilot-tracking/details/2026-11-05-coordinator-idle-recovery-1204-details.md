<!-- markdownlint-disable-file -->
# Plan details: coordinator idle recovery (issue 1204)

* Plan: .copilot-tracking/plans/2026-11-05-coordinator-idle-recovery-1204-plan.md

## Phase 1: Baseline and authoring

Edit only `.github/agents/ama-backlog-delivery-coordinator.agent.md`:

1. Replace "Never stop while work remains" with "Liveness and stop decision" (classification, tick next action, closure-review batch, recovery, tick versus run end, approvals and questions).
2. Add "Recurring schedules" (delivery 10 minutes, cleanup hourly, replacement procedure, version and ID persistence, coordinator-managed live tools).
3. Add "Cleanup contract" and tighten step 10 and the Owner delegation removal bullet.
4. Step 5: fresh per-launch brief from canonical policy, explicit target and parent, local-only no-publication, replace `5m` check text and stop condition.
5. Step 7 and step 8: missing selected-tier evidence despite green CI; rebase only for conflict or invalidated base.
6. Reconcile Human blockers, Inputs, step 9, Boundaries and the nothing-changed wording.

Frontmatter and tool/model settings are untouched.

## Phase 2: Static review

Fresh-context generic Medium-profile reviewer using the rubric and catalog; one correction batch; targeted closure on original finding IDs only.

## Phase 3: Behavior simulation

`hve-builder-tester`, simulation fidelity, no native deployment, paid inference or network mutation. Scenarios:

* S1 blocked PR plus ready independent issue
* S2 99 pending closure reviews with no tmux
* S3 21 open PRs drain versus 15 or fewer and eight-session admission
* S4 granted approval versus unavailable owner
* S5 full gate missing despite green CI
* S6 stale main-target brief versus parent stack
* S7 cleanup with active receipt or unknown upstream

## Phase 4: Validation

`git diff --check`; Markdown and relative-link review of the changed file; frontmatter diff shows no change; applicable existing artifact checks only (for example `python3 tools/rpi-checks.py --changed` if it runs without new installs); `git status` clean after commit.

## Phase 5: Close

Changes record (files, amendments, divergences, validation), RPI Review artifact with verdict against each acceptance criterion, local commit with privacy email and Copilot trailer. No push, PR or merge.
