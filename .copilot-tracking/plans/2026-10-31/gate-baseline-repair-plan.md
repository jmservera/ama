<!-- markdownlint-disable-file -->
# RPI Plan: Complete local gate baseline repair

## Task Metadata

* Task ID: a81da11b-4af4-4c2c-bd8a-ca8a765c6fd4
* Task slug: gate-baseline-repair
* Planning status: Ready; original Revise critique disposed directly
* Plan date: 2026-10-31
* Phase details: .copilot-tracking/details/2026-10-31/gate-baseline-repair-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-31/gate-baseline-repair-plan-critique.md

## Executive Summary

Bind the nine iteration-specific closure references in the strict case-journey
browser check and isolate intentional synthetic skip output in a gate regression
test. No application behavior, selector wiring, skip policy or workflow changes.
Preserve original failures, validate the failing groups and API suite, obtain
one independent Review, then commit and pass a fresh complete exact-head gate
before publishing a PR to main.

### What You May Not Know

The unchanged exact chat-panel Chromium selector passes locally. The full
baseline instead fails before reaching it, plus its tooling regression leaks
two artificial skip transcripts into the outer static-suite parser.
The gate owns its heavy-resource lock; a valid outer flock would deadlock.

### Unresolved Decisions or Blockers

No design blocker. Main advanced to e64c6e6c9da407682de59b926944424f94f50671
with #600's stronger exact-chat execution contract; incorporate it by ordinary
fast-forward, not rebase or force push. Complete execution can expose additional latent baseline
defects, which must be diagnosed without relaxing contracts.

## User Decisions and Requirements

* Run Research, Plan, Implement and Review in order with dated artifacts.
* Reproduce main's full gate first; wait for heavy lock and use jobs 3.
* Bind loop closures without behavior changes or Ruff suppressions.
* Diagnose the chat-panel browser failure, fixing only a small defect; do not duplicate #572 wiring.
* Validate failing groups, API unit tests and Ruff.
* Pip only, synthetic data, no secrets or workflow changes unless necessary.
* Commit with the supplied Copilot trailer, push HEAD without force and open a main PR using Refs #572.

## Goals

Remove inherited strict-browser lint and artificial-static-skip blockers while
retaining exact execution and fail-closed publication controls.

## Scope and Non-Goals

In scope: src/api/checks/case_journey_browser_check.py;
tools/test_rpi_checks.py; directly related API documentation; dated RPI evidence.
Non-goals: production JS/API changes, unrelated exempt browser harnesses,
new skip reasons, duplicate Chromium wiring, workflow/protection modifications,
real accounts/data/cloud/models, automatic merge or history rewrite.

## Functional Requirements

* Route callbacks retain their iteration's list/scalar/snapshot by reference/value as appropriate.
* Intentional adversarial fixture transcripts are asserted internally, not emitted as parent-suite evidence.
* The exact chat-panel selector remains unchanged and executes with ZF_BROWSER_TESTS=1.

## Non-Functional Requirements

* Strict isolated E,F,I,B,UP browser lint and isolated formatter pass from the
  exact gate working directory src/api, not root-based import inference.
* No changes to WORKFLOW_HASHES, workflow commands, skip parser or allowances.
* Complete final receipt remains external, is bound to a clean committed candidate and current origin/main, and is verified before push.

## Acceptance Criteria

* Original complete baseline failure retained with exact HEAD/base and commands.
* Nine B023 references corrected; no suppression added.
* Static gate regression suite emits no synthetic chat skip lines and still asserts unexpected/integration skip rejection.
* Exact Chromium test executes with zero skips; complete browser checks and API unit/lint/type suites pass.
* One independent critique and one independent original Review preserved.
* Final complete exact-head gate and receipt verification pass; branch pushed and main PR published, Refs #572 only.

## Implementation Context Record

| Context item | Current artifact or record |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-31/gate-baseline-repair-research.md; executed, Ready |
| Plan | .copilot-tracking/plans/2026-10-31/gate-baseline-repair-plan.md |
| Phase details | .copilot-tracking/details/2026-10-31/gate-baseline-repair-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-31/gate-baseline-repair-plan-critique.md; executed Revise, both findings disposed |
| Changes | .copilot-tracking/changes/2026-10-31/gate-baseline-repair-changes.md; implementation-owned |
| Continuation | caller-confirmed automatic full loop |

## Sources

* Research C1-C7: original full gate, exact Chromium execution, scoped skip regression and closure lifetimes.
* src/README.md: full clean exact-head publication gate.
* docs/reference/method/tracking-retention-policy.md: preserve original evidence externally.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Repair and validate the inherited blockers

Dependencies: completed research and one final-candidate critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Bind strict case-journey closures

Bind pending/loads/reads/held lists, change and snapshot; typed function defaults
where applicable. Run pinned isolated lint and formatter, preserving semantics.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Isolate synthetic skip fixture stdout

Capture only the two adversarial Runner.command calls in the existing test.
Assert captured transcript presence and unchanged receipt skip evidence.
Preserve production skip rejection. Run the full tooling regression suite.

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Validate browser and API and document scope

Run actual unchanged chat selector, design-system, case-journey and regulatory
browser checks under the heavy lock, then API unit/lint/type checks. Record
precise counts and limitations in changes and directly related API README.

<!-- rpi:phase id=P02 -->
### [ ] P02: Original Review and publication

Dependencies: P01 completion and reconciled artifacts.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Preserve original independent Review

One fresh reviewer assesses the actual source diff and evidence against this
plan. No repeated Review; findings route to later work. Any unresolved material
finding blocks publication. Do not correct or repeat Review inside this task;
if such a finding occurs, preserve it as a blocker for later work.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Commit, full exact-head gate, push and PR

Resolve gh account and privacy-safe local email, commit with trailer, run
complete full gate in new external output with current main base, fetch main
and verify immediately before exact-head assessment and push. Adverse exact-head
assessment also blocks publication. Publish with
git push -u origin HEAD and gh pr create --base main. No merge.

## Dependencies

Existing pinned Python/dev packages, Chromium, Docker, owned SQL, offline
infra tools and scanner. Missing prerequisites block publication, not a reason
to skip or change workflow protection.

## Test Ownership and Change Budget

Canonical source targets: the two named Python files and API README.
Generated targets: none in checkout; heavy logs/receipts stay external.
Exact removals: none. Maximum added test methods: zero; strengthen the existing
skip regression. Semantic coverage: real browser journey and exact chat selector.
Regression coverage: existing fail-closed parser test with captured transcript
assertions. Validation: strict Ruff, API unit/mypy, tooling suite, real browser
groups and final complete gate.

## Critique Disposition

| Finding | Disposition | Evidence / correction |
| --- | --- | --- |
| PC-001 High | Resolved directly | P02 explicitly blocks publication on unresolved material Review findings or adverse exact-head assessment. Advice to return to Implement within this task is rejected as conflicting with the one-pass RPI contract. |
| PC-002 Medium | Resolved directly | P02 details require no-deletion default and finite archive/readback/restore-backed authorization before any necessary pruning. Own fresh pip metadata is not historical tracking evidence. |

Original critique verdict remains Revise. Execution count one; no repeat.

## Follow-Up Items

* #572 remains open: broader integration acceptance belongs to its owner; this PR references it without a closing keyword.
* Other exempt browser harness B023 findings are outside this strict-gate repair.

## Handoff

Implementation artifact: .copilot-tracking/changes/2026-10-31/gate-baseline-repair-changes.md.
P01 and the original Review complete. Review execution Complete, outcome
Conformant for P01; RV-001/RV-002 are non-blocking residual follow-ups.
P02 publication remains pending clean committed full gate and exact-head
assessment. Final receipt/publication closeout stay external to preserve the
exact candidate binding; this committed checklist is pre-publication evidence.
