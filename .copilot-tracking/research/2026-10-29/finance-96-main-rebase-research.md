<!-- markdownlint-disable-file -->
# RPI Research: finance-96-main-rebase

## Research Brief

Task ID / slug: finance-96-main-rebase. Date: 2026-10-29.
Bring existing draft PR #510 (Refs #96, #98, #99), branch
docs/finance-96, up to fetched origin/main without pushing or Azure activity.
Audience: coordinator preparing the next remote candidate.
Research root: .copilot-tracking/research/2026-10-29/.

## Research Parameters

Focused, caller-selected bounded integration task; convergence output.
Full RPI loop explicitly requested. No routine phase confirmation needed.
Only integration/CI fixes are in scope; preserve original adverse reviews,
human approval boundaries and historical artifacts.

## Extension Registry and Provenance

Repository instructions and src/README.md govern source ownership and checks.
rpi-research selected for evidence, then rpi-plan, rpi-implement and rpi-review.
No web edits planned; visual skills do not apply. Independent critique and
Review required; tightly coupled research remains inline, no research worker.

## User Participation and Research Decisions

No-interaction execution: the caller provided branch, base, conflict policy,
venv, validation limits, commit trailer and explicit no-push/no-Azure limits.

## Scope and Success Criteria

Rebase onto fetched main; preserve both append-only/index entries, use main's
rubric and scenario manifest, check changed pinned-source hashes, run required
lint/types and relevant tests, commit dated evidence, leave branch unpushed.
Fresh hosted CI cannot run on an unpushed candidate and must remain unclaimed.

## Task Research Requests

Identify actual conflict state, source/configuration drift and old CI failure.

## Direction Controls

Refs only, no issue-closing keywords. Source only src/, tests outside packages.
Use /tmp/mv and explicit local namespace source/test paths. No full API
discovery unless the specified nonblocking heavy-lock probe succeeds.

## Research Questions

1. Is a rebase already active, and which local commits must be preserved?
2. Which current-main contracts/checks affect the finance patch?
3. Can all hosted checks be asserted locally without a push?

## Prior Knowledge Gate

Read original/addendum, reference index/memory, original finance changes/Review,
src guide, PR metadata and current status. Prior history lookup found no
additional matching recent sessions. Original RV-001/002 remain open and are
not authorization to expand this integration into finance feature repair.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Initial worktree clean; branch docs/finance-96 tracks the open draft PR.
Two local commits above old base 09099ecd; no active conflict/rebase observed.
Fetch succeeded: origin/main 356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7.
Existing Source CI jobs pass at the old remote head, but rubric conclusion
fails and rubric/score is pending. Inspect detailed failure next.

Reflection: reproduce the real conflict with an authorized rebase rather than
assuming the caller's earlier cheap attempt is still in progress.

#### Wave 2: Deeper

Upstream changed shared server/store, component READMEs, core mypy
configuration, role inventory and scenario manifest. The finance patch adds a
specific core mypy override that must survive alongside new main overrides.
The existing failed rubric job reports daily workflow AIC guardrail exceeded,
not a source-test failure. No workflow/protection bypass is appropriate.

Reflection: use main's rubric/manifest unchanged; test the manifest against
actual combined pinned sources, preserving failure evidence if hashes drift.

#### Wave 3: Contrarian

Clean history does not mean conflict-free replay: both branches edited the
same documentation/configuration regions. Main-only resolutions would silently
drop finance documentation and its type accommodation. Conversely branch-only
resolutions would lose current main behavior. Explicit local PYTHONPATH avoids
testing the unrelated worktree currently installed in /tmp/mv; assert resolved
imports. A green local run cannot clear a remote AIC guardrail or the prior
finance Review's adverse outcome.

Parent synthesis: preserve both finance commits and additive behavior, resolve
only actual conflicts, verify merge-base ancestry and exact main rubric/
manifest equality, then use full project lint/types and focused regressions.
No additional research cycle is justified: all bounded questions have evidence;
any new conflict/test failure re-enters implementation investigation.

## Evidence Log

### Codebase Evidence

* C1: src/README.md:64, local gate and focused validation boundaries.
* C2: .copilot-tracking/reviews/logs/2026-10-27/finance-96-98-99-review.md:30,
  original Complete / Not accepted, two Medium findings retained.
* C3: .copilot-tracking/changes/2026-10-27/finance-96-98-99-changes.md:48,
  original validation and explicit whole-issue limits.
* C4: .github/workflows/src-ci.yml:75, project unittest/lint/mypy contracts.
* C5: src/core/tests/test_scenario_manifest.py:21, pinned-source validation.
* C6: src/core/pyproject.toml:120, narrow finance typing override to retain.

### External Evidence

* W1: https://github.com/jmservera/ama/pull/510, retrieved 2026-10-29,
  open draft, main base, docs/finance-96 head, original findings disclosed.
* W2: https://github.com/jmservera/ama/actions/runs/40582472769,
  retrieved 2026-10-29: conclusion reports daily workflow AIC guardrail
  exceeded; Source CI at the old head passed its project checks.

## Findings Mapped to Questions and Evidence

Q1: no active rebase; preserve e114bc45 and 373ab192 intent.
Q2: C4-C6 and upstream overlap determine conflict/test targets.
Q3: no; only the coordinator's later push can trigger fresh hosted checks,
and the rubric budget failure is externally controlled (W2).

## Alternatives and Decision State

Caller selected rebase, not merge/reset. Preserve historical findings and main
policy; do not fabricate hosted status or force-push.

## Open Questions, Risks, and Residual Uncertainty

Shared /tmp/mv editable distributions currently point at another worktree;
explicit local source paths must precede them. No dependency mutation planned.

## Current Decisions

Continue the existing topic branch, preserve both finance commits.

## Unresolved Decisions

No missing caller decision. Hosted/external acceptance remains separate.

## Potential Next Research

None needed for planning; investigate concrete rebase/check failures if found.

## Planning Readiness

Ready. Research disposition: executed; Wider, Deeper and Contrarian complete.

## Closeout Record

Selected additive rebase under caller policy; no source changes during
Research. Original adverse findings and remote budget blocker remain explicit.
Handoff to Plan: C1-C6, W1-W2 and confirmed caller limits.

## Artifact Self-Check

Identity, date, boundaries, ordered waves, evidence, recommendation and
readiness recorded. Historical findings are not rewritten as integration bugs.
