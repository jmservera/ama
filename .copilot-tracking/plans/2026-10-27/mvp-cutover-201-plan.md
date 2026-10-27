<!-- markdownlint-disable-file -->
# RPI Plan: Retire legacy MVP directories

## Task Metadata

* Task ID: issue-201
* Task slug: mvp-cutover-201
* Date: 2026-10-27
* Planning status: Ready; original Revise critique disposed without repetition
* Details: .copilot-tracking/details/2026-10-27/mvp-cutover-201-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/mvp-cutover-201-plan-critique.md

## Executive Summary

Remove the remaining pointer directory after preserving its last main commit
under a local BRD-version archive tag. Repair active guidance/navigation to
the already migrated source projects and append the owner-authorized cut-over
record without changing dated evidence or CI identities.

### What You May Not Know

All executable paths are already migrated. Legacy data guards and historical
test strings must remain to prevent reintroduction and preserve evidence.
All five issues have broader unmet acceptance; this PR will use Refs only.
The owner, not the agent, publishes the archive tag. No full gate is authorized.

## User Decisions and Requirements

* Execute Research, Plan, Implement and Review in order with dated artifacts.
* Owner SIGNED OFF #201 on 2026-10-27; record in PR.
* Work from origin/main on chore/mvp-cutover-201; delete residual mvp/prototype.
* Create archive tag only if locally absent; describe exact owner push command.
* Preserve workflow/check names and all historical records; no secrets or uv.
* Update KB index and append-only log; do not edit memory.
* Run requested API and rename regressions; no full gate, optional scoped only.
* Commit Conventional Commits with required Copilot trailer; push topic and PR.
* User permits Closes only with every criterion proven; research establishes
  that this PR must use Refs for all five issues, unconditionally in this task.

## Goals

* Complete the bounded legacy-directory retirement with recoverable Git history.
* Make current source location and owner sign-off discoverable without
  misrepresenting historical blocked gates as new successful evidence.

## Scope and Non-Goals

In scope: mvp/README.md deletion; live repository/src/capstone/PRD/rubric prose;
parity navigation, cut-over evidence pack, ADR dated addendum, KB index/log.
Non-goals: runtime changes, regeneration of old audits, source package rewrites,
deployment, private data/backup reads, release/tag push, workflow renames,
branch protections, full SQL/browser/image gate or issue closure.

## Functional Requirements

* No tracked or filesystem residual legacy directories after deletion.
* Current instructions and mutable links point to src projects.
* Historical paths are explicitly classified, not globally replaced.
* Archive tag v0.21.0 refers to last commit before deletion; never move a tag.

## Non-Functional Requirements

* Preserve previous log bytes exactly; memory and original case study unchanged.
* Workflow and check definitions unchanged.
* Tests use installed distributions, never PYTHONPATH=mvp.
* No false deployment/rubric/whole-issue completion claims.

## Acceptance Criteria

* git ls-files under mvp/prototype empty and neither directory exists.
* Absent tag is created locally at verified pre-deletion baseline; existing tag
  is verified and any conflicting existing target blocks rather than moves it.
* Active instructions/link repairs reviewed; unchanged historical log has an
  additive repair map; changed document local links resolve.
* Requested API discovery and rename regressions pass with skips explained;
  focused parity regression/namespace check demonstrates mapped destinations.
* Dated full RPI evidence includes one critique and one independent Review.
* PR records sign-off, archive target/push command, exact validation, and Refs.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-27/mvp-cutover-201-research.md
Changes: .copilot-tracking/changes/2026-10-27/mvp-cutover-201-changes.md
Review: .copilot-tracking/reviews/logs/2026-10-27/mvp-cutover-201-review.md
Automatic parent continues after critique disposition. No research gaps.

## Sources

* Research C1-C11 / W1-W5, fetched main 65a514ed20e97816dbf47e9fb981ab4cfe40597d.
* Current caller authority overrides old unsigned cut-over status prospectively.
* src/README.md local gate policy permits focused testing for small maintenance.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve and retire

Dependencies: completed research and critique disposition.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Create verified local archive tag and delete pointer

Verify tag absence, BRD version and last pre-deletion main commit. Configure
privacy-safe author identity before annotated tag/commit. Delete mvp/README.md
with apply_patch; remove its empty directory only. Prototype already absent.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Reconcile live guidance and preserve history

Update README archive notice, src index and instructions, coordinator's
source-layout status note, capstone current
registry table, active PRD build baseline, rubric current summary and parity
link. Add dated owner cut-over section in existing evidence pack, qualify its
older unsigned baseline without rewriting it, and add dated ADR note.
Update architecture/KB navigation and append log with old-anchor repair map.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate bounded retirement

Dependency: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run existing tests and exact reference/link checks

Requested API and rename commands, plus existing cutover-audit and eval-registry
unit selectors. Compare workflow bytes to main, verify log prefix, inspect
only tracked eligible text (never data/private paths) and local changed links.
No full gate; do not call --changed unless actually needed.

<!-- rpi:phase id=P03 -->
### [ ] P03: Review and publish

Dependency: P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Obtain one independent Review and persist original outcome

Run rpi-review once after implementation, with independent worker for bounded
source/evidence assessment. Do not repair/rerun Review in this task; route any
findings separately, blocking ready publication if material.

<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: Commit and publish authorized maintenance PR

Resolve gh account and repo-local noreply identity, commit source plus original
RPI evidence with Conventional Commit/trailer, push only explicit branch ref
with --no-follow-tags, create PR with Refs #199-#203 and no closure claims.
Fetch main before publication; do not silently rewrite/rebase if it moves.
Hosted checks/merge remain separate.

## Test Ownership and Locked Change Budget

* Test owner: parent implementation; independent Review assesses evidence.
* Exact production removal: mvp/README.md only, plus empty mvp directory.
* Other removals: none. Prototype absent on base.
* Test removals/additions: none; zero new test files needed for prose/pointer work.
* Canonical targets: existing source/docs/instructions listed in P01.
* Generated targets: none; preserve dated TSV/score/evidence snapshots.
* Semantic proof: no legacy directories/live links, valid archive target,
  append-only log, unchanged workflow identities.
* Regression proof: existing API, rename and parity/eval-registry tests.

## Dependencies

Owner sign-off supplied, migration verified, local Git/gh available.
Package dependencies may need isolated pip installation if required tests
report missing modules; preserve existing pins.

## Critique Disposition

Exactly one independent critique executed, original verdict Revise preserved.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 High | Applied sanitized execution boundary; rejected unsupported claim that system scratch is prohibited | P02-T01 details now require allowlisted environment and exact task-owned external scratch under session files; caller/repository permit external scratch |
| PC-002 Medium | Applied | P01-T01/P03-T02 derive identity before both tag and commit, no literal account email |
| PC-003 Medium | Applied Refs-only publication conclusion; corrected critique's provenance | User conditionally permits closure, but W1-W5 justify unconditional Refs for this PR; P03-T02 details now match |

No unresolved significant/divergent finding; no user decision or second
critique needed. Original finding wording and verdict remain unchanged.

## Follow-Up Items

* Hosted CI/deployed health, all-suite baseline comparison and post-merge rubric
  acceptance remain with the owner/coordinator under #199-#203.
* Owner tag publication/release are explicitly outside agent execution.

## Handoff

P01/P02 and P03-T01 complete. Independent Review executed Complete / Conformant
for source and scoped validation; no substantive findings. P03-T02 publication
remains. Changes record includes original
prerequisite failures, repaired environment, final passing scoped tests and
semantic assertions. No routine approval is needed for the explicit
owner-requested loop/publication. No full gate ran or is required for this task.
