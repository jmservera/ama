<!-- markdownlint-disable-file -->
# RPI Plan: Design traceability and review gate

## Task Metadata

* Task ID: 156
* Task slug: issue-156-design-traceability-gate
* Planning status: Ready; single independent critique Pass
* Plan date: 2026-10-18
* Current integration base: 3bc46912684cb4d865572023a6d16da14b9b8463
* Historical documentation source baseline: 3104bb69ddc26c81e0e9d2f57000dac1d99a419a
* Phase details: .copilot-tracking/details/2026-10-18/issue-156-design-traceability-gate-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-18/issue-156-design-traceability-gate-plan-critique.md

## Executive Summary

Extend the existing prototype profile synthesis, not a competing design library.
Record eleven PRD profile rows and four shared core-flow rows with exact journey,
existing task-flow, versioned artifact, check and missing-evidence ownership.
Add a compact decision register and an actual blocked design-review record.
Update only the KB index/log alongside the complete dated RPI record.

### User Decisions and Requirements Highlights

* Fluent 2 is owner-selected; closed #150 does not erase historical partial
  implementation evidence. No UI/runtime edits or new prototypes. The original
  no-rebase boundary was superseded only by the exact coordinator-authorized
  integration recorded below.
* Exactly one independent critique and original Review; no self-pass or amended
  Review. If Review is Not accepted, commit frozen evidence locally and stop.

### What You May Not Know

Existing profile tables and lifecycle model already record flows. Historical
issue wording is not a current absence audit. Eleven perspectives are not
eleven authenticated roles; human acceptance and full backlog coverage are
not supplied. Overall design must remain Blocked.

### Unresolved Decisions or Blockers

None for documentation implementation; missing human/design evidence becomes
explicit open register items, not invented acceptance.

## User Decisions and Requirements

* Execute Research -> Plan plus one independent critique -> Implement -> one
  original Review, with actual 2026-10-18 artifacts committed together.
* Use docs/design-traceability-gate-156 from supplied 3104bb69 source base.
  The 2026-10-18 coordinator continuation authorizes rebase only onto exact
  3bc46912684cb4d865572023a6d16da14b9b8463, with exact old-head lease
  6af9dd81e0089f8998bb8d575329c6bc1d4fc110. No #398 resumption.
* Bounded documentation only; existing UX synthesis/index/log, no UI, runtime,
  workflow, configuration, agent or prompt edits.
* Link each declared row to feature issue, exact journey section, existing
  task-flow section, actual artifact/version, requirement/check, evidence
  status and missing item/owner role/next action.
* Preserve hypotheses, historical evidence, real Fluent 2 choice, missing
  artifacts as `Not supplied`, and accessibility/content/human boundaries.
* Publish a main-target PR with Refs #156 only after accepted original Review;
  do not close issue, change AC/board, merge or self-certify external gates.

## Goals

* Make the declared design inventory navigable and missing evidence actionable.
* Prevent documentation completion being mistaken for screen/user acceptance.

## Scope and Non-Goals

In scope: existing prototype profile synthesis, KB index and append-only log;
eleven PRD profiles plus queue scope/reset, case open/return, blocked
readiness/handoff and AI draft review. These four shared core flows are an
explicit subset, not every audited content surface.

Non-goals: all present/future screen backlog, import/export, operations/account,
direct resident/representative screens (#154), regulatory chat/alerts (#215),
new wireframes, framework adoption, site audit or operational release.

## Functional Requirements

* Fifteen rows map feature -> exact journey section -> existing flow section
  -> versioned actual prototype/engineering artifact -> requirement/check
  -> status -> missing item/role/action.
* Decision register records date, source, rationale, affected rows, status and
  open questions; source-derived interpretation is not owner direction.
* Gate checklist and actual record require exact versions, reviewer/date,
  expected versus actual, outcome and findings with owners/actions.
* Missing required trace, design, accessibility or content evidence blocks
  overall design Pass. Human and user validation stay independently reported.

## Non-Functional Requirements

* Plain language, ASCII, descriptive links, valid relative paths/anchors and
  matching table cell counts; preserve existing evidence and headings.
* Sources pinned at 3104bb69 unless explicitly historical; no private inputs.
* Zero modifications outside the declared documentation and tracking allowlist.

## Acceptance Criteria

* Exactly eleven profile and four named core rows are present, with every
  required column and honest `Not supplied` current design status.
* Historical prototype H has immutable revision; current shared IA evidence
  E has pinned baseline and is not mislabelled an approved screen design.
* Live #150 closed status and owner choice coexist with stale pinned
  "stays open"/partial source evidence, without altering historical text.
* Named-person review, resident wording approval, direct user research and
  full backlog coverage remain open; no #156 AC closure claim.
* KB index routes to new section, ms.date changes only materially edited
  synthesis (index already current), and log is appended.
* Link/anchor, table/heading, scope and whitespace checks succeed before Review.

## Implementation Context Record

| Context | Artifact / state |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-18/issue-156-design-traceability-gate-research.md; executed, Ready |
| Plan/details | Paths in Task Metadata |
| Critique | Executed once; Pass; no actionable PC findings |
| Changes | .copilot-tracking/changes/2026-10-18/issue-156-design-traceability-gate-changes.md; implementation-owned |
| Continuation | Caller-authorized automatic full loop; no follow-up child work authorized |

## Sources

* Research C1-C9/W1-W5: source locations, version pins, contradictions and limits.
* docs/reference/research/ux/zava-forward-prototype-profile-review.md:
  eleven flows, UX-01 to UX-08, owner feedback, sequencing and later shared IA.
* docs/prds/zava-forward-retrofit-programme-demonstrator.md:
  Profile Journey Contract and Case lifecycle, role handoffs and return path.
* docs/reference/research/ux/design-system.md, wcag-conformance-baseline.md,
  content-standard.md: retain separate implementation/approval evidence.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Curate existing evidence and gate

* Dependencies: completed Research and one critique disposition.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add finite trace and decision registers

* Evidence: C1-C4/C8/C9, W1-W3.
* Expected result: fifteen explicit rows, pinned sources, missing evidence and
  source-qualified decisions in existing synthesis.
* Details: P01-T01 in phase-details artifact.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Record gate and KB navigation

* Evidence: C5/C6; depends on P01-T01 inventory.
* Expected result: actual blocked review with separate evidence categories;
  accessibility/content DoD and index/log update.
* Details: P01-T02 in phase-details artifact.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and hand off original candidate

* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Check documentation and reconcile evidence

* Expected result: all new links/anchors independently resolved, tables and
  diff reviewed, scope constrained, checks/limits recorded in changes.
* Details: P02-T01 in phase-details artifact.

## Validation Ownership Lock

Parent owns docs checks; original Review independently evaluates sources and
results. Exact test removals: none. Maximum added repository test files: zero.
Canonical targets: three production Markdown files above plus dated RPI state,
research, plan, details, critique, changes, Review and required documentation
session record. Generated production targets: none. A small session-local
standard-library link/anchor checker is permitted, not new tooling/dependencies.
Semantic coverage: finite row shape/status, links, gate logic and claim/source
review. Regression coverage: unchanged historical content, appended log,
allowlisted diff and git diff --check. No browser/SQL/Docker/Azure/model checks:
not applicable to this documentation-only slice. Hosted checks remain Pending CI.

## Dependencies

* #150 live CLOSED; owner Fluent choice confirmed, historical partial scope retained.
* #149 is parent, not approved acceptance. #152/#225-233 feature links are
  trace targets, not declarations that those issues are delivered.
* #399 merged; coordinator-authorized exact-base integration is recorded below.

## Coordinator-authorized integration receipt (2026-10-18)

Integration only, not a feature change, correction, new critique or Review.
Original published head 6af9dd81e0089f8998bb8d575329c6bc1d4fc110 was rebased
from 3104bb69ddc26c81e0e9d2f57000dac1d99a419a onto exact
3bc46912684cb4d865572023a6d16da14b9b8463. Replayed head before this metadata
commit: 23b2d8758cbcceedf251d6c87c79f2a01e44d9a8. The metadata commit that
contains this receipt is the final publication candidate; PR #400 identifies
its exact published head.

Only log.md conflicted: retain the entire upstream #172 prefix, then the
unchanged original #156 append. Index merged automatically and equals upstream
plus the original single-row replacement. Eleven other upstream files are
byte-identical, including fixture implementation/tests, dictionary and agents
README. Own synthesis and original critique/Review are byte-identical to old
published head; fifteen rows, Blocked gate and historical source pins unchanged.
Source-parity and documentation checks passed as recorded in changes.

Original P01/P02 completion and original Review verdict remain historical.
Independent complete gate on the integrated final head is still required;
integration checks do not self-certify acceptance. No new active plan work or
follow-up implementation is added.

## Critique Disposition

| Critique run and finding | Disposition | Response |
| --- | --- | --- |
| Original 2026-10-18 final-candidate critique; Pass; no PC findings | Accepted | No revisions required; original artifact preserved unchanged |

Residual human evidence gaps remain outside documentation acceptance; overall
design stays Blocked. No second critique authorized or executed.

## Follow-Up Items

* Design owner: supply exact current designs and named human reviewers; outside
  documentation curation because no artifacts/acceptance are supplied.
* Coordinator: enumerate remaining current/future screen features; finite
  inventory does not satisfy universal #156 coverage.
* Accessibility/content/research owners: record actual manual, named wording
  and representative-user evidence; no test or approval can be invented.

## Handoff

Implementation P01/P02 complete; original Review executed Complete / Conformant
for the original candidate. Exact-base integration only is now complete locally,
pending lease-protected publication and independent final-head gate.
Single independent critique dispositioned. Preserve original
critique and Review bytes; after original Review no implementation correction
or rerun in this task. Coordinator later routes at most two corrections.
