<!-- markdownlint-disable-file -->
# RPI Plan: issue137-pilot-capability

## Task Metadata

* Task ID: 137; date: 2026-10-18.
* Task slug: issue137-pilot-capability.
* Planning status: Ready; one independent critique completed, both findings directly resolved.
* Phase details: .copilot-tracking/details/2026-10-18/issue137-pilot-capability-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-18/issue137-pilot-capability-plan-critique.md

## Executive Summary

Publish the current read-only regional catalog and quota evidence in the
existing infrastructure environment section, reconcile the actual owner
decision and retain all unselected values and human gates. No infrastructure
or application changes are needed.

### What You May Not Know

Successful catalog calls coexist with empty quota responses and denied/failed
surfaces. SQL catalog zone support is not a SQL-region decision. Model catalog
capacity fields have different unspecified semantics and no returned usage
unit. A regional provider listing is not service admission.

### Unresolved Decisions or Blockers

Complete quota, Container Apps zone/environment-core evidence, IoT exact B1
support, subscription approval/binding and named human review remain unavailable.
These block deployment claims, not accurate documentation delivery.

## User Decisions and Requirements

* Full ordered RPI loop, one independent critique, one original Review;
  preserve all artifacts/adverse receipts and commit them with delivery.
* Pilot uksouth and subscription owner @jmservera come only from the verified
  2026-10-15 comment; no broader approval is implied.
* No cloud writes, private data, installation, runtime/template/example changes.
* Keep the issue open and its unticked criterion unchanged.
* Resume the same supplied branch and authorized dirty batch from initial base
  612cbed78a35a4ab426571aa7d2aeb0ae6d691dd. Owner's 2026-10-19 direction
  supersedes publication and doc-only validation: commit the coherent batch,
  then rebase this unpublished run-owned branch onto approved origin/main
  fa659cfd021100f7c64f8ec73bbff76c03adf234; stop on ambiguous conflicts.
* No push/PR/issue mutation. Coordinator independently reviews exact-head
  source/RPI/primary evidence and the final full-matrix receipt before any
  later publication decision. Keep Refs #137, never closing keywords.

## Goals

* Make support, quota evidence and unknowns reproducible and secret-free.
* Correct only contradicted current region/ownership statements.

## Scope and Non-Goals

In scope: infra/README.md environment/current pipeline prose, ADR 0002 current
dated current-status delta, reference index/log routing and dated RPI artifacts.
Non-goals: all Bicep/parameter files, code, dependencies, policy, actual resources,
deployment/what-if, grants/identity enumeration and unrelated historical prose.

## Functional Requirements

* Publish exact requested config, query date/shapes, scoped values/units and
  Pass/Unknown/Blocked outcomes from R1-R17.
* Explain empty provider results and access/gateway errors without defaults.
* Preserve historical deployment receipts, all placeholders and reviewed gates.
* Explicitly document the unchanged example's stale undecided comment.

## Non-Functional Requirements

* Zero published subscription/tenant/resource IDs, private names/IPs or account
  inventory; allowlisted fields only. Private raw receipts never staged.
* No more than two distinct approaches per missing surface; reproduction may
  rerun the identical command without adding surfaces.
* Stable unchanged source hashes bind evidence to the exact base.

## Acceptance Criteria

* Reader can reproduce every reported check with identifier placeholders.
* Every support claim is narrower than deployability or approval.
* Each reported query is reproduced; changing/failed results remain receipts.
* Sanitization/source binding/links/diff checked; original Review retained even
  if adverse. Named human review stays incomplete.
* All artifacts included in local commits; clean final worktree. Final commit
  precedes mandatory canonical full local gate and external verified receipt;
  no commits after that gate.

## Sources

Research .copilot-tracking/research/2026-10-18/issue137-pilot-capability-research.md
contains W1/W2, C1-C4 and sanitized R1-R17. No further research required.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Publish bounded evidence

Dependencies: completed Research and one critiqued ready plan.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Reconcile prose and add dated evidence

README table and command legend; ADR dated 2026-10-18 current-status delta
separating the 2026-10-15 decision date from retrieval. Leave the explicitly
historical 2026-10-08/09 ADR table unchanged; index/log route.
Preserve existing history and all template/example bytes.

<!-- rpi:phase id=P02 -->
### [x] P02: Reproduce and validate

Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Repeat queries and verify evidence

Repeat R1-R17 once, preserve first-run adverse receipts, compare selected
fields, inspect sanitization and source hashes, verify relative links/diff.
Date reproduction honestly as 2026-10-19; retain 2026-10-18 observations.
Check exact template bytes against both original and approved new base.
The historical doc-only exemption is superseded: full application/SQL/browser/
Docker/scanner matrix is mandatory after the final commit.

<!-- rpi:phase id=P03 -->
### [ ] P03: Original Review and delivery

Dependencies: P02.

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Execute one Review, preserve and deliver

Activate rpi-review once after implementation. Findings route forward, not
corrections or another Review. Commit inspected scope plus all phase evidence
with privacy-safe account email/trailer; no push or draft PR.
After generating the original Review and explicitly staging every delivery
artifact, inventory the final staged paths and inspect all staged additions
and full new artifacts for privacy. No outgoing PR is authorized. Public
handles, source hashes and required privacy-safe attribution are allowed.
Any later content change invalidates this gate. A privacy failure stops
commit/publication and routes to the coordinator, never edits the original Review.
Commit the final candidate and run `tools/rpi-checks.py --all --base
fa659cfd021100f7c64f8ec73bbff76c03adf234 --out <fresh-external-directory>`
with PATH prefixed by /tmp/rpi-413-tools; verify its receipt at the frozen
head/base. Use the runner's shared heavy lock and isolated local test resources.
Record the actual matrix externally, including adverse results and skips;
do not change unrelated baseline application code to obtain a green result.

## Validation Ownership and Change Budget

Parent owns query reproduction, documentation/source/link/sanitization checks.
Exact removals: none (only contradicted prose replacement). Test additions: 0;
test deletions: 0. Canonical target: infra/README.md plus ADR/index/log; generated
targets: none. Semantic coverage: config/metric/unit/authority distinctions.
Regression coverage: unchanged template/example hashes and existing historical
receipts, plus the mandatory canonical full local matrix despite docs-only scope.

## Dependencies

Signed-in Azure GET access and local gate prerequisites; unavailable evidence must
remain explicit, never require a permission/resource change.

## Critique Disposition

One independent critique executed; original verdict Revise preserved.

| Finding | Direct disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Resolved in plan; implementation must execute final gate | P03-T01 now requires staged-tree inventory/privacy gate after Review and staging; no later content changes without repeating gate |
| PC-002 | Resolved in plan; implementation must preserve history | P01-T01 now requires dated delta with separate decision/retrieval dates and no historical-table edits |

No user decision required; neither correction changes scope. No second critique.

## Follow-Up Items

* Owner/coordinator: missing quotas, zone evidence and approved account binding
  require later authorized evidence, not scope expansion here.
* Human reviewer: decide whether region/quota criterion can be accepted; this
  delivery cannot certify it.

## Handoff

Implementation record: .copilot-tracking/changes/2026-10-18/issue137-pilot-capability-changes.md.
P01/P02 complete on 2026-10-19: all seventeen identical GETs reproduced;
allowlisted values/categories match; exact source bytes match both bases.
Changes record owns validation evidence. P03 next: coherent batch commit,
authorized clean rebase, one original Review, final artifacts/commit, full
external gate. Original critique remains immutable; no new loop authorized.
