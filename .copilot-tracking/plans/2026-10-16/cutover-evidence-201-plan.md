# Cut-over evidence plan

Task: issue-201 / cutover-evidence-201. Date: 2026-10-16.

## Executive Summary

Prepare a dated, reproducible gate report, not approval. Check matrix
destinations and local suites, attempt the documented Azure bootstrap and
remote src builds, record actual smoke results and residual gates, publish PR.
Deployment success is an observation to establish, not an assumed deliverable.

## User Decisions and Requirements

* Refs #200 #201; read owner comments first; owner signs only after evidence.
* Never delete mvp/, prototype/ or resource group ama.
* Azure writes confined to ama; no private data or excluded configuration reads.
* pip venv local-first suites, ruff, mypy; no Docker or uv.
* Current parity, deployed proof or honest failure, reference list and rename
  proposal, owner checklist, README/index/log, RPI artifacts, commit/push/PR.
* Mutation check must fail without the new change; PR references never close issues.

## Goals

Give the owner a trustworthy, independently inspectable go/no-go evidence pack.

## Scope and Non-Goals

Evidence and a bounded deployment attempt. No deletion, sign-off, check rename,
private-data migration, tenant registration changes or general product rebuild.

## Functional Requirements

Report all historical matrix outcomes against current src destinations; identify
partial rebuilds and intentional drops. Capture safe commands, exits, resource
IDs and smoke outputs. Inventory tracked references while excluding prohibited
paths. Preserve historical identifiers.

## Non-Functional Requirements

No secrets in artifacts; no SQL portability violations; no broad cleanup.
Use src build context. Tests remain outside import packages.

## Acceptance Criteria

Pack exists under docs/architecture with reproducible evidence and unchecked
owner gates. Existing relevant suites run locally, failures/skips disclosed.
Inventory regeneration and document guard have negative mutation evidence.
PR is pushed with Refs-only issue references and prescribed identity/trailer.

## Test Ownership and Change Budget

Canonical target: docs/architecture/cutover-evidence-pack.md. Generated target:
docs/architecture/cutover-reference-inventory.tsv. At most one src/core audit
module and one src/core/tests test module, using stdlib only, to reproduce
matrix/reference checks. No removals. Semantic coverage: resolves current
matrix destinations and disallows gate overclaim. Regression coverage: missing
destination, prohibited scans, reference changes, missing pack/checklist.
Run real tests before mutation; mutate in-memory/temp fixtures, never tracked
production files, then prove old revision lacks required pack/test contract.

## Phase Checklist

<!-- P01 -->
### P01: Establish execution evidence
* [x] P01-T01 Run five suites, ruff/mypy, infra and rename regressions in pip venv.
* [x] P01-T02 Attempt documented infra deployment/ACR build in ama; bounded
  smoke and post-inventory; no unauthenticated public app workaround.

<!-- P02 -->
### P02: Publish reproducible report
* [x] P02-T01 Add bounded audit/check and mutation-tested regression.
* [x] P02-T02 Write pack, update matrix/README/index/log, generate inventory.

<!-- P03 -->
### P03: Review and hand off
* [x] P03-T01 Reconcile evidence and run one RPI review.
* [x] P03-T02 Commit, push, open PR; owner checklist remains unchecked.

## Critique Disposition

One critique executed, verdict Revise. All seven compatible findings accepted
and directly incorporated below; no owner decision needed; no second critique.

* PC-001: pin subscription e51ebc89-79d0-4a52-a82b-01a292eefd5b and existing
  ama ID; inspect what-if; only incremental group deployment, no governance,
  group/tag/policy workaround or tenant write.
* PC-002: stage two requires existing registration, vault secret metadata,
  real image digests and initialized SQL via repository script. Missing
  prerequisite keeps deployApplications=false; no private seed substitution.
* PC-003: proof requires digest/revision/readiness plus /healthz 200 and
  protected API anonymous denial, then authenticated synthetic SQL read if
  authorized. Probe at most 12 times, 10 seconds apart, 10-second timeout;
  missing endpoint is Not run, never Pass.
* PC-004: shared validator exercises actual source destination removal and
  reference drift; tests instrument reads before exclusions. Run the candidate
  oracle against baseline matrix destinations (not missing imports) and
  demonstrate named mismatch errors; fixture mutations fail the same oracle.
* PC-005: generate row-keyed TSV for every historical per-file/pattern row,
  with outcome, actual target and explicit exception. Compare 719/747 counts
  and current skips without claiming measured line coverage.
* PC-006: run namespace, tracked no-data and JS syntax checks; disposition
  browser/image checks separately. Docker checks remain unavailable locally.
* PC-007: fix this deliverable's integrity defects before publication;
  only existing product/tenant/owner gates may remain open. One review only;
  targeted correction checks are not another review.

## Follow-Up Items

Owner-only private copy/open/encrypted-backup attestation; owner sign-off;
post-cut-over coordinated workflow/required-check rename; separately tracked
worker/transport rebuilds. Not active implementation acceptance.

## Implementation Amendments and Evidence

P01 completed as an execution attempt, not as healthy deployment. Bootstrap
Failed on IoT provider registration and SQL public-interface restriction.
No apps or smoke endpoint. Retained 65 run-created generic resources and
run-created budget, leaving pre-existing budget and group intact.

P02 adds one ACR YAML task and three golden-only ignore rules after real
build failures, within the original evidence intent. Run db8 built all four
images and tested bounded remote contracts; local Docker remains unavailable.
The shared audit reconciles 130 rows including two sandbox patterns, accounting
for all 578 historical names. Tests are nine in one external module.
No document-specific sign-off inference engine was added: source/reference
oracles and baseline context mutation provide the requested substantive
negative evidence; owner checklist integrity is directly reviewed in docs.
All required human gates remain unchecked.

Published evidence commit f5e5f65 on docs/cutover-evidence-pack-201 and PR #341
against main. Publication does not certify deployed proof or accept cut-over.

Publication amendment: merge upstream 79b153b without rewriting history to
resolve #341's log conflict, revalidate changed core/infra, repeat remote
build/contracts as db9 and exercise the newly available canonical deploy
wrapper. Both bootstrap attempts Failed on the same platform prerequisites.
Refreshed evidence remains preparation only; no new critique or Review.
