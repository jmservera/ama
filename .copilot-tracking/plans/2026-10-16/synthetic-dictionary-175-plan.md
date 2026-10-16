# Plan: synthetic dictionary and provenance

Task: issue-175 / synthetic-dictionary-175. Date: 2026-10-16.

## Executive Summary

Correct sensor/chat coverage and provide executable public/snapshot validation
without private datasets. Preserve existing deterministic payloads and explicitly
audit missing external provenance as unmet, not a successful guarantee.

## User Decisions and Requirements

* Deliver issue #175, with RPI artifacts, tests, README/log updates and a PR using
  Refs #175. Keep issue checkboxes for coordinator review at merge.
* Offline only. Build only in src/infra; do not edit legacy trees, setup-entra.py,
  private datasets, environment/identity files or unrelated code.
* Synthetic-demo authority is not operational approval. Juan Manuel Servera is
  the exercise Legal, Compliance and DPO owner; invent no other approvals.

## Goals

Make current dataset coverage navigable and privacy/separation checks executable.

## Scope and Non-Goals

Core synthetic validation module, existing provenance tests, generated chat test
integration, dictionary/register, relevant READMEs, index/log and RPI artifacts.
No generator format changes, cloud operations or universal PII certification.

## Functional Requirements

* Validate public CSV/JSON and explicitly supplied fresh scale/sensor/chat
  snapshots, with row-label rules and exact manifest inheritance where needed.
* Detect email, UK telephone, NI and UK postcode patterns without echoing values.
* Fail nonzero on violations, missing labels, malformed/extra snapshot files,
  mismatched manifest hashes and absent/provisional source metadata.
* Keep real anchors/private runtime outside public scans and publishing.

## Non-Functional Requirements

Standard library only; typed code; preserve deterministic payload bytes.
Use temporary fixtures, never inspect private generated output.
Existing source CI must execute the tests without private support data.

## Acceptance Criteria

1. Every known dataset family, including scale, sensor, chat/runtime and evals,
   has a dictionary anchor and provenance entry.
2. Each external source has verified licence, retrieval date and attribution:
   blocked for three historic sources; strict audit must report this honestly.
3. Pattern/label mutations demonstrably fail the executable checker.
4. Public/private classification and generated output separation are tested
   without depending on local private datasets.

## Phase Checklist

<!-- P01 -->
### P01: Implementation

* [x] P01-T01: Add typed validators and CLI, public/eval coverage, snapshot contracts.
* [x] P01-T02: Replace stale private-reading tests; add mutation and chat tests.
* [x] P01-T03: Update dictionary/register and directly related README/index/log.

<!-- P02 -->
### P02: Evidence and delivery

* [x] P02-T01: Targeted tests, ruff/mypy, local CLI and local app smoke.
* [ ] P02-T02: One post-implementation Review, criterion audit, commit/push/PR.

## Locked Test Ownership

Replace src/core/tests/test_synthetic_provenance.py (remove private-file reads and
obsolete not-generated assertions only). Add at most one agents test module
for generated chat integration. No test/package changes elsewhere.
Semantic coverage owns label/source/separation rules; mutation regressions own
pattern rejection and nonzero CLI status. Existing determinism, sensor/fabric,
eval registry and chat fixture tests preserve payload behavior.
Canonical documentation is the data dictionary and provenance register;
generated targets are temporary small snapshots only, never committed.

## Critique Disposition

One critique executed, verdict Revise; all findings dispositioned directly:
PC-001 adds explicit public collection/exemption contracts in details;
PC-002 requires rehashed pattern/label mutations and separate integrity failures;
PC-003 adopts project-local scratch and isolated runtime configuration.
The critique's assertion that system temporary directories are prohibited is
unsupported by caller instructions, but project-local scratch is compatible.
No user decision required; final plan ready. No second critique.

## Follow-Up Items

AC2: owner must verify the three external source retrieval dates/licence terms.
Operational reliance, full-stock materialization and actual chat/DPO approval
remain out of scope, not claimed as complete.

## Handoff

Research: .copilot-tracking/research/2026-10-16/synthetic-dictionary-175-research.md.
Details: .copilot-tracking/details/2026-10-16/synthetic-dictionary-175-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-16/synthetic-dictionary-175-changes.md.
