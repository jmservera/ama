---
title: Issue 349 current-main continuation plan
description: Preserve local and remote checker intent while reconciling current main
ms.date: 2026-10-23
---

## Task Metadata

Task ID: 349-current-main-20261023.
Slug: issue349-tenant-readiness-preflight-current-main.
Parent: 349-correction3, within the same issue349 RPI history.
Status: Ready after one critique and direct dispositions.
Details: .copilot-tracking/details/2026-10-23/issue349-tenant-readiness-preflight-current-main-phase-details.md.

## Executive Summary

Keep the complete checker/correction history and current main's requirements,
log and generated latest evidence. Integrate remote ancestry locally before
rebasing onto main. Preserve the two historical topic score patches as inert
evidence, but omit their obsolete latest.json replacements from replay.
No checker behavior change is needed. Focused validation and one original
Review precede final evidence commit and exactly one complete local gate.

### What You May Not Know

Remote differs from local only by a generated score. Its later timestamp
does not make it applicable to main's changed BRD/PRD and pitch. Old receipts
do not survive a rebase. Publication remains entirely coordinator-owned.
No unresolved design choice; unfamiliar conflicts are blockers, not guessed.
Focused validation uses a new isolated pip environment. Any failed prerequisite
or unresolved blocking Review finding stops sealing and gate progression.

## User Decisions and Requirements

* Continue the SAME issue349 history with genuine ordered phases and dated
  committed Research, Plan/details/critique, Implement/changes and Review.
* Use only this worktree and branch; inspect local/remote lineage first.
  Initial local 3eebcc3922188f5ddd614bfa5d4583b082f4e1c5,
  fetched remote 6c284d4547de7c52a360b2ec2406ea2078a98f16.
* Rebase run-owned branch onto fresh origin/main, currently
  140d8f494482c78e84d15f3d46b9223d3c487af0. Preserve both intents,
  original dispositions, all append-only log entries and newer main evidence.
* Before validation inspect processes/lock; never interrupt another owner,
  duplicate a full gate or clean any receipt environment.
* Install existing project distributions with pip per repo commands. No uv
  or private data. Keep every full-gate group, SQL/browser/Docker/Trivy included.
* Exactly one fresh full gate and official exact-head receipt verification
  against fresh main. If main moves during the gate, finish and report stale.
* Use gh api user-derived local noreply identity and required Copilot trailer.
  Commit complete RPI artifacts before seal; no later repository edits.
* STOP BEFORE PUSH. No push, force push, merge, PR/board mutation, issue ticks
  or closing keywords. Coordinator owns independent assessment/publication.
* No Azure/Graph/tenant/resource mutation, paid calls, deployment, ingress,
  registration/secret/roster access, privilege/network changes or UI edits.
  RG ama/SQL/data/identities protected. October headroom Unknown despite
  USD 700 ceiling valid through 2026-10-25T16:02Z.

## Goals

Deliver the existing sanitized read-only checker on current main, with
auditable preservation and current exact-head local evidence.

## Scope and Non-Goals

Included: local Git reconciliation, existing checker/tests and original RPI
preservation, this dated continuation's artifacts, two generated historical
score patches. Do not edit main-only files, KB log or active rubric scores.
Do not regenerate a score. No new production or web implementation.

## Functional Requirements

Preserve checker/test bytes from initial local HEAD and all original RPI
bytes. Preserve main's unrelated files, entire docs/reference/log.md, latest.json
and badge.svg exactly. Remote score intent is retained in an inert Git patch,
not discarded silently or represented as current.

## Non-Functional Requirements

Local-only history rewrite, no remote write. Explicit commit mapping/range-diff
and byte comparisons establish preservation. All 35 focused tests retained.
No additional authorization, call templates or output schema changes.

## Acceptance Criteria

Rebased history descends from fresh main; all five human checker commits
replayed; only the two generated latest-score commits omitted, with patches
and reasons preserved. No unexpected diff to initial checker or main documents.
Focused tests, isolated no-cache lint/format and diff checks pass.
One original critique and one independent Review recorded with honest outcomes.
Final committed HEAD is clean; one full gate passes and receipt verifies,
or failure/staleness is explicitly reported without another gate or push.

## Sources

.copilot-tracking/research/2026-10-23/issue349-tenant-readiness-preflight-current-main-research.md:
executed/Ready, C1-C6. Original correction3 evidence remains immutable.
src/README.md local commands and local RPI gate; unchanged on fresh main.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [ ] P01: Reconcile local history

<!-- rpi:task id=P01-T01 -->
#### [ ] P01-T01: Preserve phase evidence and both source histories

After critique disposition and Implement activation, generate exactly two
Git format-patch artifacts for 3b881a65 and 6c284d45 under this dated research
evidence directory. Commit only new continuation artifacts with privacy-safe
identity/trailer; this is a real pre-rebase evidence checkpoint, not a final
gate candidate. No prior artifacts overwritten.

<!-- rpi:task id=P01-T02 -->
#### [ ] P01-T02: Rebase preserving known intents

Refresh refs. If remote/main differs, inspect before proceeding. Rebase local
checkpoint onto fetched remote topic to include remote-only commit, then
interactive rebase onto exact main from b4d467cad84535ed106cffa1ae9aa303db7bfed2.
Explicitly drop only 3b881a65 and 6c284d45 from replay, using exact identities;
their Git patches remain historical. Keep all human commits and checkpoint.
No merge or push. No blanket conflict choice, source changes or log rewriting.
Stop on any unfamiliar intent/conflict. Record actual mapping and differences.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate reconciled checker

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Ownership and distribution prerequisites

Inspect live processes/lock before running validation. Create a new isolated
non-receipt pip environment for this continuation unconditionally; establish
that its project distributions are missing, then install the existing five
distributions using component -e commands. Bind focused tests/tools to this
interpreter and record source locations and distribution metadata; no private data.
No dependency-manifest change or unpinned tooling introduction. Preserve old
receipt environments untouched. Log externally without repository caches.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Focused validation and reconciliation invariants

Parent owns tests. Removals: none. Additions: zero methods; generated targets:
only two historical patches, no code generation. Preserve all 35 existing tests.
Run bytecode-disabled focused unittest; Ruff 0.17.1 isolated no-cache check
(E,F,I,B,UP, py312, line length 100) and format --check on checker/tests.
Run strict checker mypy with external cache and git diff --check.
Compare checker/tests/original evidence to initial local, main-only files and
entire KB log/active rubric to exact main. Confirm range-diff only expected.

<!-- rpi:phase id=P03 -->
### [ ] P03: Original Review and committed candidate

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: One independent Review

Fresh worker activates rpi-review once. Scope: reconciliation and preserved
checker, artifacts, real validation; no live acceptance or post-gate assessment.
Only canonical Review record writable. Preserve original critique/Review and
route any new finding once; no repeat Review inside this continuation.

<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: Seal complete RPI evidence

Parent reconciles Review outcome, plan/details/changes/state; preserve
pre-gate pending status. Commit complete dated artifacts with privacy-safe
local author/committer and Copilot trailer. Fetch main and confirm exact base,
inspect lock/process owners again; any movement before launch is a blocker
unless reconciled within authorized scope before this sole gate.

<!-- rpi:phase id=P04 -->
### [ ] P04: Single exact-head full gate

<!-- rpi:task id=P04-T01 -->
#### [ ] P04-T01: Gate once and verify currentness

One invocation: python3 tools/rpi-checks.py --all --base <fresh-exact-main>
--out <new-/tmp/ama-349-current-main-20261023-unique-directory>.
All groups unchanged. Runner owns serialization; never interrupt or duplicate
lock owner. Preserve output, receipt and environment even on failure.
Fetch main after completion. Officially verify receipt against current
origin/main. If moved, report stale, not current. No retry gate or publication.
Final outcomes external to git to keep the exact sealed source/head unchanged.

## Dependencies

P01-T02 depends P01-T01; P02-T01 depends P01-T02; P02-T02 depends P02-T01;
P03-T01 depends P02-T02; P03-T02 depends P03-T01; P04-T01 depends P03-T02.
Host SQL/browser/Docker/scanner prerequisites are not cloud-fallback authority.
Any failed required command, byte/range invariant or unresolved blocking Review
finding stops dependent work. Preserve outputs and report the exact blocker;
no automatic source remediation, repeat Review or gate retry. P03-T02 and
P04-T01 require all preceding checks passed and one Review without unresolved
blockers. Coordinator/hosted/live residuals are not local source defects.
An already running gate still finishes if main moves, then is reported stale.

## Critique Disposition

One final-candidate critique executed, original verdict Revise preserved.
Original correction3 dispositions remain untouched.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 Medium | Accepted and applied directly | P02-T01 and details now require new non-receipt context, actual missing-distribution check, five pip installs and bound command/metadata provenance |
| PC-002 Medium | Accepted and applied directly | Shared Dependencies progression rule and details require pass conditions before sealing/gate, fail-stop with no automatic remediation, and separate residual vs blocker handling |

No significant decision or second critique needed. Plan and details reconciled.

## Follow-Up Items

* Independent coordinator exact-head and rewritten-lineage assessment before
  any publication; current loop explicitly stops before push.
* Live registration, credential, private roster, operator consent, Entra
  sign-in, real API/browser acceptance and private transport remain blocked;
  offline checker tests establish none of these. Hosted checks remain separate.

## Handoff

Changes: .copilot-tracking/changes/2026-10-23/issue349-tenant-readiness-preflight-current-main-changes.md.
Critique: .copilot-tracking/reviews/plans/2026-10-23/issue349-tenant-readiness-preflight-current-main-plan-critique.md.
Review: .copilot-tracking/reviews/logs/2026-10-23/issue349-tenant-readiness-preflight-current-main-review.md.
Planning complete and Ready. No implementation begun. Next: P01-T01.
