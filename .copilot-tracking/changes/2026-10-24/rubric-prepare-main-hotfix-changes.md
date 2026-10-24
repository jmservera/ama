<!-- markdownlint-disable-file -->
---
title: Rubric preparation direct-main hotfix evidence
description: Original bounded implementation and Review evidence before the required publication gate
ms.date: 2026-10-24
---

## State and Scope

All state is managed through the .copilot-tracking folder files. External gate
receipts remain outside the checkout as required by the publication policy.
This original pre-gate record is immutable evidence, not a publication receipt.

* Task ID: rubric-prepare-main-hotfix
* User request: make a one-time fix directly to main and push prepare.py
* Reviewed base: f1e2d830f17558efd868919de1973ea7244a8841
* Isolated worktree: /tmp/ama-prepare-main-hotfix-20261024
* Original branch: docs/capstone-cowork-story, unchanged by this candidate
* Tracking artifact: .copilot-tracking/changes/2026-10-24/rubric-prepare-main-hotfix-changes.md
* Artifact completion: 100% of original pre-gate implementation/Review evidence
* Overall request: incomplete until all required gates and direct push succeed

## Phase 1: Research

Complete. Trusted main has the deck's 20,000,000-byte override, but
.github/rubric/scripts/prepare.py passes the global 2,000,000-byte limit
to match_files for every active artifact. The previously measured deck is
2,643,853 bytes. PR preparation uses scripts from trusted main.

## Phase 2: Plan

Complete. Apply the existing two-line override handling to latest main in
an isolated worktree. Preserve the registry, wildcard, deck, score records,
presentation branch and hosted workflow configuration. Run focused regression
checks, record original Review, commit, run the complete local gate, obtain
independent exact-head review and verify the receipt before a normal push.
Do not dispatch scoring, force-push, change protections or merge the PR.

## Phase 3: Implement

Complete for code and focused validation; publication validation remains pending.
Only .github/rubric/scripts/prepare.py changes behavior. compute_state now
resolves each entry's max_file_bytes with the existing global value as fallback.

Existing deck_size_override cases from the presentation branch were executed
against the isolated main prepare module using importlib and pytest, with
bytecode and pytest cache writes disabled. Result: 3 passed, 52 deselected.
The cases verify global fallback, inclusive override boundary, rejection above
the override and unchanged non-deck limits. No new test file was added.
git diff --check passed. Editor diagnostics reported no errors for the script.

## Phase 4: Review

Original bounded Review: focused behavior passes; publication remains pending.

1. The change controls file selection before extraction, directly addressing
   the demonstrated size-based exclusion rather than changing the deck.
2. Global fallback and other artifacts' limits remain unchanged, as verified
   by the focused regression cases. No public interface changes.
3. The user-authorized root-level wildcard remains intact. No configuration,
   deck content, score file or unrelated presentation work is included.
4. Complete local gate, receipt verification and independent exact-head review
   are still required. Focused tests alone do not establish publication readiness.
5. Deck recognition does not establish rubric acceptance, rehearsal, delivery,
   Q&A or thought-leadership evidence. No score is manually changed.

## Phase 5: Discover

Ordered follow-up work, conditional on successful publication:

1. Confirm the normal direct push updated main to the exact reviewed candidate;
   retain any gate or remote rejection rather than bypassing it.
2. Obtain a fresh hosted assessment only with owner authorization. Check that
   capstone-deck is fingerprinted and the global-limit skip warning is absent.
3. Compare the new score and criterion floors with the existing 55 baseline;
   preserve all genuine delivery and thought-leadership evidence gaps.
4. Reconcile stale exact-v2 registry tests and documentation separately if
   authorized; do not narrow the wildcard or repair unrelated fixtures here.
