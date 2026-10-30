<!-- markdownlint-disable-file -->
# RPI Plan: Fabric PR 558 reconciliation

## Task Metadata

* Task ID: 558
* Task slug: fabric-rebase-558
* Plan date: 2026-10-30
* Planning status: Ready; single critique Complete / Revise, dispositions resolved
* Phase details: .copilot-tracking/details/2026-10-30/fabric-rebase-558-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-30/fabric-rebase-558-plan-critique.md

## Executive Summary

Rebase the authorized local tracking branch onto fetched main, retain both
documentation histories, and prove that the local candidate is coherent with
focused checks. Preserve all original Fabric research and its dated limitations.
Commit the implementation and full RPI evidence locally; the coordinator owns
push and subsequent hosted checks.

### User Decisions and Requirements Highlights

The owner authorizes local rebase and Conventional Commit, not remote
publication, Azure changes, new runtime features or issue closure.

### What You May Not Know

GitHub says the PR is not draft. The requested venv exists but its editable
installs default to another worktree, so local source paths must lead imports.
Passing local checks cannot update remote mergeability or prove hosted CI.
Main is shared across worktrees and moved during critique; capture one refreshed
execution BASE_SHA and detect later drift rather than mix identities.

### Unresolved Decisions or Blockers

None for local reconciliation. Publication gates, hosted checks and human
merge approval remain outside this task's local-only authority.

## User Decisions and Requirements

* Run all four RPI phases with dated original evidence.
* Fetch origin and rebase origin/main on docs/fabric-rebase-558, tracking the owner branch.
* Preserve both index/log intents; take upstream .github/rubric and scenario manifest.
* Use src-only source and tests outside packages; no legacy application code.
* Use /tmp/mv and explicit local/sibling source/test paths for Ruff, format, mypy and relevant units.
* Never run full API discovery without nonblocking heavy-lock admission.
* No Azure changes, closing keywords, push or merge.
* Commit with Conventional Commit and the supplied Copilot coauthor trailer.

## Goals

Provide a clean local descendant of current main with the original Fabric
assessment retained and all required local evidence recorded.

## Scope and Non-Goals

Shared index/log conflict resolution and dated tracking only. Existing Fabric
assessment and original research should remain byte-identical unless a genuine
rebase defect requires a documented correction. No new executable, web or
infrastructure work; no full API discovery is needed for this docs-only diff.

## Functional Requirements

* Retain original Fabric block and every upstream log block.
* Retain Fabric navigation alongside all upstream navigation and frontmatter repair.
* Retain upstream rubric directory and scenario manifest exactly.
* Expose every actual command/result and any blocked validation.

## Non-Functional Requirements

* No source/test behavior delta relative to main.
* Correct local module origins before tests; no shared venv mutation unless missing dependencies actually block.
* No discarded owner edits or removal of historical evidence.

## Acceptance Criteria

* AC1: origin/main is an ancestor; git reports no rebase/unmerged paths.
* AC2: upstream log is a byte-preserved prefix; original Fabric log block and index entries remain.
* AC3: rubric/manifest match origin/main; original six standalone research documents remain byte-identical.
* AC4: core/API Ruff lint, format and mypy pass; scenario and both dependency-rule modules pass using local imports.
* AC5: changes record contains commands, exits, skips and scope; one critique and one independent Review retained.
* AC6: local Conventional Commit has required trailer and privacy-safe author/committer; clean worktree, no push/Azure/remote mutation.
* AC7: Hosted CI and publication receipt are explicitly unclaimed; coordinator receives current main/head identity and remaining gates.

## Implementation Context Record

| Item | Artifact / state |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-30/fabric-rebase-558-research.md; executed, Ready |
| Plan | .copilot-tracking/plans/2026-10-30/fabric-rebase-558-plan.md |
| Details | .copilot-tracking/details/2026-10-30/fabric-rebase-558-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-30/fabric-rebase-558-plan-critique.md; Complete / Revise, parent dispositions resolved |
| Changes | .copilot-tracking/changes/2026-10-30/fabric-rebase-558-changes.md; full implementation Complete |
| Continuation | Single independent Review Complete / Conformant with justified divergence; parent local commit, coordinator publication |

## Sources

Research C1-C7/W1, user task, component pyprojects and src/README.md local gate.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Reconcile branch

Dependencies: finalized critique. Capture one refreshed execution BASE_SHA,
inspect drift from the historical research base, and use that SHA for every
rebase/preservation/ancestry assertion. Report later movement explicitly.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Rebase and preserve both documentation intents

Use the fetched main; resolve actual conflicts, verify ownership and preserved
bytes, and append one factual reconciliation entry to the knowledge log.
Update index date if materially changed. Details: P01-T01.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and prepare Review

Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run scoped checks and reconcile evidence

Run local module-origin checks, core/API Ruff lint/format/mypy, scenario and
dependency-rule units, migration regression, doc links/frontmatter/whitespace.
Reconcile plan/details/changes for independent Review. Details: P02-T01.

## Dependencies

Fetched main, clean intake, available /tmp/mv Python 3.12/dev tools, local path
overrides and independent critique/Review. Local commit requires authenticated
GitHub identity. Missing checks stay blocked, never success-shaped.

## Locked Change and Validation Budget

Test ownership: existing src/core/tests and src/api/tests. Removals: none.
New tests: zero; existing semantic preservation assertions cover the exact
requirement, existing regression modules cover manifest/dependency boundaries.
Canonical targets: docs/reference/README.md and docs/reference/log.md plus
dated tracking. Generated targets: none. Maximum new tracking files: seven
(state, research, plan, details, critique, changes, Review). Original standalone
assessment/research bytes are protected. Validation outputs remain external.
No new helper/framework is needed. Use task-owned external session files for
logs, TMPDIR and mypy caches; disable bytecode and Ruff caches. Do not modify
shared /tmp/mv installations or create candidate-local cache inputs.

## Critique Disposition

Single critique execution Complete; original verdict Revise, two Medium findings.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Applied | P01/details now distinguish original research and refreshed execution BASE_SHA; all predicates bind to that SHA and final drift is detected |
| PC-002 | Safety intent applied; unsupported path mandate rejected | P02/details now bind logs/temp/cache to finite task-owned session files, disable bytecode/Ruff caches, preserve shared venv. The claim that supplied constraints forbid system-temp or require project-relative scratch is not present in the caller/repository instructions; repository retention policy instead prefers external scratch. No repository-local generated files will be introduced |

No repeat critique. Neither finding requires a new owner decision.

## Follow-Up Items

* Coordinator must fetch/verify the final base, satisfy the applicable complete local publication gate and independent exact-head assessment, push the rebased owner branch under owner authority, observe hosted checks and leave merge to the owner. None of those publication actions is authorized here.

## Handoff

Implementation changes record: .copilot-tracking/changes/2026-10-30/fabric-rebase-558-changes.md.
Implementation P01/P02 is complete with all planned scoped checks passing.
No remaining active implementation marker. The single independent Review is
Complete / Conformant with justified divergence, with no implementation defects.
Parent owns final local commit; coordinator owns publication and hosted gates.

## 2026-10-31 Local Recovery Continuation

The sections above preserve the original 30 October execution and its Review.
The current owner request extends that historical docs-only scope to all
remaining conflicts and both unresolved PR comments. The owner selected
`rebase`, explicitly local-only and without force-push.

* Active topic: `jmservera/fabric-research`; original published head
  `bde84d8bc9f920ddc58f4b885970abc33371a724`.
* Recovery branch: `chore/fabric-558-pre-rebase-20261031`.
* First execution main: `18602ae7103ceee89fa4c87ca312b04a57ca0dba`.
  Completed rebase head: `9719326437a874e23b6ef8698dffb39c21ef462a`.
* Latest observed main: `ec2d784255c3377ab39e5d2d1b5140e76c8e7f36`.
  This separate drift identity is not substituted into earlier results.

### [x] P03: Recover conflicts and correct review feedback

Preserved both index/log histories. Kept main's stricter gate implementation
and its tests instead of duplicating browser dispatch; retained the intentional
hosted browser command and its exact workflow hash. Main's scores and scenario
manifest are byte-identical. Later capstone registry changes remain intentional;
the original AC3 whole-rubric equality does not erase those intervening changes.
All six reviewed Fabric research inputs match the published tip byte-for-byte.

The exact LF source convention is documented and the real Verify action
revalidates the unchanged delivery. All four finite guards now use APIs
available in Windows PowerShell 5.1; 32 native-shape checks pass on Linux.
Actual Windows PowerShell/PowerPoint execution remains unperformed.

Core/API static checks, 12 owning units, 35 gate regressions, 25 migration
regressions, nine PDF checks and the actual Chromium selector pass.
All 17 broader rubric failures reproduce on unchanged execution main, which
also has an additional registry failure. Those pre-existing failures are not
changed, skipped or relabelled as a pass.

### [x] P04: Rebind to latest main and independently review

The validated correction was committed as `b7772aaa` and replayed cleanly onto
the separately observed `ec2d7842` main, producing
`aedc67139e51215b3f1dce39715e60dbdaf3f82a`. Fresh ancestry, upstream-owned bytes,
unchanged research/delivery, receipt equality and four new documentation
links/anchors pass. Core/API lint, format and typing pass again; ten core units
and three API units, including actual Chromium execution, pass without skips.
The single independent continuation Review is Conformant within its bounded
scope, with zero correctness findings. Its original response is retained in
the existing Review log, including the reviewer's read-only persistence limit;
the parent persisted that response without changing the historical prefix.
The final metadata-only local commit records this closeout, not a new
publication exact-head approval. Keep the remote branch and both unpublished
threads unchanged; publication gates and owner merge approval remain outstanding.
