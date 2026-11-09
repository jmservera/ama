<!-- markdownlint-disable-file -->
---
title: Issue 159 validation-refusal receipts initial implementation plan
description: Revised prospective plan, written against the qualified #189 parent before any merge or source edit
ms.date: 2026-11-09
---

## Task Metadata

* Task slug: issue-159-validation-receipts-initial. Refs #159, Refs #189. No closing keyword.
* Research: .copilot-tracking/research/2026-11-09/issue-159-validation-receipts-initial-research.md
* Details: .copilot-tracking/details/2026-11-09/issue-159-validation-receipts-initial-details.md
* Critique: one independent critique of this final candidate, committed before any merge or source edit: .copilot-tracking/reviews/plans/2026-11-09/issue-159-validation-receipts-initial-plan-critique.md
* Supersedes (does not erase) the PREPARATION plan `issue-159-route-validation-receipts-plan.md`, whose self-conducted critique stays as recorded history.
* Base: ordinary `--no-ff` merge of LOCAL parent `e192bc74732e824a3488c49a4875df9bd4463cd8` into `b851a9e2c793246494085c34a906845a97603b7d`. Intended PR target: the declared parent topic `feat/demo-simulator-control-189-1109`, not main.

## Entry gates

* [x] G1: parent qualified clean by the coordinator (brief).
* [x] G2: re-research of the exact parent done (research file) before merge.
* [x] G3: coordinator disposition 2026-11-09: initial feature increment, consumes no correction cycle, grants no new cycle. Historic count 1 confirmed, 1 possible, true total unrecorded.
* [x] G4: critique committed before merge and source edits (this plan commit).

## Scope

* Exactly three authenticated `_chat` HTTP 400 branches: unstored-ask extra keys; stored ask extra keys; stored ask explicit `skill: null`.
* Each keeps its 400 and message, and appends exactly one metadata-only validation-refusal receipt with zero model calls and unknown tokens. Exact shapes (critique PC-001): stored is the full `_receipt(tid)` (tokens `None`, provider_outcome `not-called`, cost "Unknown"); unstored mirrors the existing unstored refusal payload `{outcome, model_calls: 0}` with no token or cost field.
* No question text, unknown field names or values, or raw invalid skill in the receipt or audit. Unstored target empty; stored `tid` only after the existing thread and permission checks.
* Valid asks keep exactly one normal receipt; permission denial, missing or foreign thread and workflow fallback unchanged. No duplicate normal plus rejected receipt.
* Excluded: anonymous 401 and no-actor policy, other 400 branches, UI, assistive technology, provider activation, real models, cloud, private data, schema, migration, framework, parent repairs, whole-issue closure.

## Phases

* [ ] Phase 1 (core): add `ChatPanel.record_validation_refused(user, tid=None)` in src/core/src/zava_forward/core/chat_panel.py using the existing audit seam. Recheck with `iso.current_user`; if refused, write nothing and return (existing 400 preserved). Stored: audit `chat.turn` with `_receipt(tid)` (outcome `rejected`). Unstored: audit `chat.turn.unstored` with `{"outcome": "rejected", "model_calls": 0}` and empty target.
* [ ] Phase 2 (api): call the helper immediately before each of the three `ValueError` raises, keeping messages and the generic 400 mapping. No other branch changes.
* [ ] Phase 3 (tests, existing files, red first): src/api/tests/test_chat_panel.py HTTP tests with a model-call spy and audit-delta count for each branch with sensitive canaries in question, field name and value, and raw skill; normal-ask positive control (exactly one receipt); existing denial, foreign and missing thread controls re-run; a pre-check refused-user control keeping the existing 403 and one `access-rejected` row (PC-002a). The post-check race is a core helper test (refused user, no row, PC-002b). src/core/tests/test_chat_panel.py helper tests for stored and unstored shape, empty unstored target, and refused-user no-op. Show red before the source change, then green.
* [ ] Phase 4 (validation, demo-targeted): the two test modules above (full modules), pinned Ruff 0.17.1 `check` and `format --check` on changed files, API and Core strict mypy 2.4.0 with the repository CI profile, no Any, casts, ignores or config changes. No standalone disposable SQL, Docker or browser unless the audit seam changes, which would STOP scope; the full existing core and API modules still run as they are, and a focused helper persistence check uses the existing core fixture for both stores (PC-003).
* [ ] Phase 5 (record): changes file, authored Review, state, handoff. Frozen clean local commit with the privacy-safe identity and trailer. No push, PR, issue or board write.

## Decisions

* D1 (revised): a user refused by the recheck gets no new receipt and keeps the current 400; permission policy and the no-actor question stay out of scope.
* D2: unstored target empty.
* D3: reuse outcome vocabulary `rejected`; no new outcome string, action name or schema.

## Validation and budget notes

* Owner demo-targeted tier replaces the older full-gate wording for this slice; hosted CI and independent exact-head review remain mandatory and unobserved here.
* Ordinary initial red-green debugging allowed. After the completed Review, any corrective source pass needs a bounded coordinator history disposition; stop rather than self-authorize.

## Unmet after this slice (expected)

* Criterion 6 named screen-reader and announcement acceptance, anonymous 401 and no-actor tokenomics policy, other 400 branches, OD-51 cost. Whole #159 stays open.
