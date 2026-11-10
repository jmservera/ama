<!-- markdownlint-disable-file -->
# Plan: Issue 134 eleven-perspective walkthrough acceptance (C1, C2, C5)

* Task `134-walkthrough-plan-1110`; base `64c3f9191a2ffa97ef2dc07245422333ad4d6585`; branch `test/demo-profile-walkthrough-134-1110`
* Research: [research](../research/2026-11-10-walkthrough-plan-134-1110-research.md); details: [details](../details/2026-11-10-walkthrough-plan-134-1110-details.md); critique: [critique](./critiques/2026-11-10-walkthrough-plan-134-1110-plan-critique.md)
* Status of this plan: planned, not started. Implementation needs Root admission after the native 440 aftercare checkpoint (exact 64c3/main/b7source equivalence) is independently consumed. No source, test or fixture change is authorised now.

## Objective

Produce honest, source-pinned, screen-level evidence for the unmet issue #134 criteria without relaxing them: for each of the eleven perspectives, a served entry, evidence inspection, safe endpoint, recovery route and accountable handoff; the AC-034 to AC-043 disposition (pass only if the full Given/When/Then is shown, otherwise Partial or Deferred with reason); and textual state meaning, keyboard operation and status announcements. Results are constructed-fixture evidence, not user validation, authentication assurance or approval.

## Non-goals and guards

* No rerun of the ticked same-home, sibling and building trace; no re-execution of the #74 home-field audit or #80 export inventory.
* No backend or API test as a substitute for a screen walkthrough; no fabricated approval, sign-off, receipt or human acceptance.
* No invented screens or login roles. Missing coverage (Asset, Procurement, Auditor have no login role) stays Deferred or Unknown with the reason.
* Do not ratify the Atlas oracle, fix or waive #1401/#1402, include #109/#111 sensor drafts or #132 intake, or adopt main in this plan.
* C2 reads "pass or deferred with reason". Partial is an interim register state only: before any C2 tick each AC must be pass (full Given/When/Then shown) or Deferred with reason, otherwise C2 stays unticked. The current validator (`journey_acceptance.py` lines 99 to 101) accepts only partial or deferred, so a pass needs a separately Root-admitted validator change; none is planned.
* No issue tick, no pass claim, no change to `REGISTER`/`EVIDENCE` statuses to met or passing without recorded evidence and independent review.
* Preserve Fluent 2, plain language and the WCAG baseline (proposed, pending O-1); no redesign; no conformance claim.

## Phases

Dependency chain: P0 -> P1 -> P2 -> P3 -> P4 (P5 review). Slices are independently revertible commits.

| Phase | Slice | Content | Needs |
| --- | --- | --- | --- |
| P0 | Admission and preflight | Root consumes the 440 checkpoint and independent exact-head review; Root states main/rebase decision and admits P1. Record `git status`, HEAD and tree; build venv from this worktree and prove imports resolve inside it; verify heavy lock free | Root admission (blocker for everything) |
| P1 | S1 existing-check execution (no code) | Run the existing maintained checks listed in details (workbench, role_screens selectors, safety, finance, procurement, data operator, home case) under non-queued heavy lock with owned scratch; capture raw logs externally; fill the per-row evidence table | P0 |
| P2 | S2 owned synthetic probe (proposed, needs separate Root scope admission) | One local probe under `src/api/checks/` that walks each declared perspective by keyboard only (entry -> evidence -> endpoint -> recovery -> handoff) and asserts the status text; plus negative controls; no new screens | P1 results define the gap list |
| P3 | S3 register and docs update | Only where P1/P2 evidence supports: update `perspective_walkthroughs.py`/`journey_acceptance.py` reasons and evidence lists (statuses stay partial/unmet/deferred; the existing model allows no pass), the workbench manifest notes, profile review, KB log and index | P1 (and P2 if admitted) |
| P4 | Validation | Focused tier: targeted unit tests (`test_perspective_walkthroughs.py`, `test_journey_acceptance.py`, `test_scenario_manifest.py`), documentation link and diff review, and the P1/P2 local browser checks read as local-only; classify the full tier question (see below) | P3 |
| P5 | Review and routing | One independent Review; findings become later work. Issue ticks and "Closes/Refs" decided by owner from reviewed evidence | P4 |

Tier classification (to be recorded at implementation): P1 is no change; P2/P3 touch checks, registers and docs only, no workflow, dependency, Dockerfile, permission, secret, deployment or gate semantics, so the focused tier fits if confirmed at start. Doubt, a gate-tool edit or a hosted-check change escalates to the full tier. Hosted CI does not reference these browser checks (grep on this head), so they stay direct local checks and must be reported as such.

## Planned commands (future, not run now)

From `src/api` in the exact worktree venv, one at a time, each wrapped `flock -n /tmp/ama-rpi-heavy.lock` (refuse if held), with `ZF_BROWSER_SCRATCH=/tmp/z134-<n>` and no credentials or default data:

* `python -m checks.workbench_browser_check`
* `python -m checks.role_screens_browser_check <selector>` for `230`, `231`, `231q`, `231p`, `231qp`, `226`, `232`, `232s`
* `python -m checks.safety_screens_browser_check`, `finance_screens_browser_check`, `procurement_screens_browser_check`, `data_operator_browser_check`, `home_case_browser_check`, `progress_browser_check`
* `ZF_AXE_JS` only when the pinned axe file is present; otherwise report "axe not run"
* Unit: `python3 -m unittest` for the three core tests named above from `src/core`, and `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q` from `src/api` only if an API test changes

## Roles and slices

* Coordinator (Root): admission, scope, lock, receipt handling.
* Worker A: P1 execution and per-row evidence table (read-only).
* Worker B: P2 probe and P3 edits, only after separate scope admission.
* Independent reviewer: P5, not the implementer; human and hosted approvals remain required and are not replaced by local checks.

## Success criteria

* Every one of the eleven rows has recorded evidence or an explicit Partial/Deferred/Unknown reason for each of the five elements plus keyboard, text and status.
* AC-034 to AC-043 each carry a recorded disposition with reason; none relaxed; none marked pass unless the full criterion is shown.
* All results labelled constructed-fixture evidence; role fixtures distinguished from authentication, actual human or resident acceptance.
* Raw logs retained outside the checkout; PRD, register and manifest agree.

## Stop conditions

Any Root admission missing; heavy lock held; import path outside the worktree; a check needs default or private data; a failure revealing a defect outside this scope (record as follow-up, do not repair); need to touch an oracle or #1401/#1402 findings.
