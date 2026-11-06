<!-- markdownlint-disable-file -->
# Changes: coordinator idle recovery (issue 1204)

* Date: 2026-11-05
* Plan: .copilot-tracking/plans/2026-11-05-coordinator-idle-recovery-1204-plan.md
* Details: .copilot-tracking/details/2026-11-05-coordinator-idle-recovery-1204-details.md
* Research: .copilot-tracking/research/2026-11-05-coordinator-idle-recovery-1204-research.md

## Files changed

* .github/agents/ama-backlog-delivery-coordinator.agent.md (modified, about 184 insertions and 58 deletions; frontmatter untouched)
* Dated evidence under .copilot-tracking/research, plans, details, changes, reviews, hve-builder/2026-11-05 and rpi-sessions/2026-11-05 (added)

## Amendments to the agent

* Replaced "Never stop while work remains" with a Liveness and stop decision (fresh classification, unknown is work, tick end differs from run end, two no-progress ticks trigger same-tick recovery) and an Approvals and owner questions section.
* Added Recurring schedules (replace by create, verify, stop old, read back one delivery and one cleanup; prompt versions and ids in approved evidence) and Cleanup contract sections.
* Reconciled owner delegation, human blockers, CI economy, backlog-sync paragraph, steps 5, 7, 8, 9, 10 and Boundaries: fresh per-launch briefs with explicit target, workers never publish, rebase only on conflict or invalidated base, closure batches of five with SQL cursor.

## Critique and dispositions

* Single final-candidate critique: independent static review, Pass, F1 to F8 (review-001). F1 to F5 and F8 applied in one correction batch; F6, F7 low, accepted without change. A targeted closure was done by the lead by re-reading the edited text and `git diff --check`; it was not a separate independent rerun.

## Divergences

* Authoring by the parent lead rather than a generic authoring subagent (disclosed).
* The correction batch was applied with a Python script rather than the edit tool.
* Behavior simulation ran on a proxy model (see behavior report).
* Focused local tier: `tools/rpi-checks.py --changed` requires a clean committed candidate, so it was run after the commit; its external receipt is not committed.

## Validation

* `git diff --check`: clean.
* Frontmatter: first diff hunk begins in the body at line 11, so frontmatter is unchanged.
* Relative links in the agent file (cutover-evidence-pack, tracking-retention-policy, src/README) all resolve.
* Behavior: Pass, 8 of 8 (behavior report).
