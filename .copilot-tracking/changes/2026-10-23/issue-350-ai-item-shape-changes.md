---
title: Offline feedback AI item shape correction changes
description: Original implementation and validation evidence for bounded correction
ms.date: 2026-10-23
---

## Metadata

Task ID/slug: issue-350-ai-item-shape.
Plan: .copilot-tracking/plans/2026-10-23/issue-350-ai-item-shape-plan.md.
Details: .copilot-tracking/details/2026-10-23/issue-350-ai-item-shape-phase-details.md.
Implementation date: 2026-10-23.

## Execution Status

P01 complete: P01-T01/P01-T02. P02/P03 remain parent lifecycle/delivery work,
not implemented completion. No implementation blockers.
Critique executed once: PC-001 rejected as inapplicable, PC-002 applied before
source edits; original critique retained.

## Execution Summary

Approved write boundary: two checker/test files and this correction's dated
tracking artifacts. Begin tests only, record genuine red, then checker guard/docs
and focused green. No source edits occurred during research/planning.

## Completed Work

### P01-T01: Genuine red-first structural regression tests

Added six AiEvidence methods with missing/wrong/empty field matrices, mixed
valid/invalid items/cites and both user reproductions. Renamed the positive
fixture test to avoid implying real AI execution. Another positive calls
`priority_items` against synthetic source labels (no inference), asserts shape
PASS and explicit unchanged blocked/not-run/not-accepted boundaries.
Existing uncited fixture now contains a valid reason, isolating cites failure.
No removed tests or generated targets. Before checker changes: 16 AiEvidence
tests, 44 failing subtests, exit 1; external red.log retains full output.

### P01-T02: Bounded guard and focused green

Extended only the existing item predicate with nonempty_str case_id/reason and
all citation elements. Uses existing Verdict FAIL and "cited items" diagnostic.
Module documentation clarifies shape versus source/provenance; no new imports,
IO, activation, semantic rules or arbitrary limits in checker.

Validation: 70 focused tests pass in installed-package venv, Ruff lint/format
pass on both changed tools and git diff --check passes. All previous 64 tests
retained. Mixed/late malformed items fail and a two-item runtime-validator
positive passes. Existing safety test still forbids broad catches/network/
environment imports. No significant divergence or additional critique.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| System Python focused baseline | Installed-package import | Failed | Missing zava_forward; new dedicated venv installed per package guide |
| Installed venv baseline | Focused checker module | Passed | 64 tests |
| Supplied reproductions | ai_evidence | Reproduced | Both malformed lists incorrectly PASS before correction |
| Red | P01-T01, AiEvidence | Failed as expected | 16 tests, 44 failing subtests; external red.log |
| Green | Entire focused checker module | Passed | 70 tests, external green.log |
| Ruff lint/format | Both changed tools | Passed | E,F,W,B,BLE,I; E501 ignored; isolated/no-cache |
| Whitespace | git diff --check | Passed | No whitespace errors |
| Full exact-HEAD gate | P03 | Not run | Requires original Review and committed clean candidate |

## Pre-Review Reconciliation

Ready: P01 implementation/validation complete, plan markers/details and handoff
current. No unrelated follow-up or unresolved implementation blocker.
P02 original Review then commit and P03 full gate/receipt/publication remain
pending. Residual live acceptance is excluded, not a local source blocker.
Logs: `/tmp/ama-350-ai-item-shape-20261023-evidence-0752/`.
Dedicated venv: `/tmp/ama-350-ai-item-shape-20261023-0752-venv/`.
Task-created ignored egg-info/bytecode will be cleaned before exact-head gate.

## Parent Post-Review Handoff

P02-T01 complete: one original Review Complete / Residual work; no in-scope
blocking defect, no repeated Review. RV-001 is pending authorized delivery,
RV-002 is later independent coordinator/live acceptance. The parent reconciled
plan markers/details/changes without changing source or Review outcome.
P02-T02/P03 remain pending in the candidate snapshot; actual exact-head receipt
and delivery status will be external and recorded in PR, not another commit.

GitHub account resolved by `gh api user`: id 8036360, login jmservera.
Repository-local name and privacy-safe email configured for author/committer:
8036360+jmservera@users.noreply.github.com. Main fetched and remains exact caller
base. Normal push is authorized only after focused/full-gate/receipt success.
