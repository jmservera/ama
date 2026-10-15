---
title: Stock fabric link 168 research
description: Focused acceptance and implementation evidence for issue 168
ms.date: 2026-10-15
---

## Research Brief

Task 168 / stock-fabric-link-168. Prepare a bounded implementation plan for
linking the retained 980-case lineage to the generated 60,000-home stock and
reproducible, synthetic-labelled fabric. Output mode: convergence.
Research root: `.copilot-tracking/research/2026-10-15/`.

## Research Parameters and Direction Controls

Focused posture selected from the named issue, source targets and accepted ADR.
Reuse PR 246 and moves 296-302. New code and tests only in src/core unless a
consumer requires wiring. Private data stays outside git through ZF_DATA.
No new generator lineage, guessed stock identity, operational approval, consent,
AI authority, deployment or paid inference. No edits to .env, .vscode or
.copilot-tracking/github-issues. Owner-dependent criteria remain unchecked.

## Extension Registry and Participation

Repository copilot instructions and ADR 0006 selected for placement, dependency
boundaries, private data and evidence. RPI research/plan/implement/review selected
for the explicit full-loop request. Research conducted inline because source
inspection is one coupled trace; no research workers dispatched. No interaction
needed: explicit user direction supplies scope, branch and continuation.

## Questions and Candidate Areas

1. What did PR 246 already deliver, and what acceptance evidence remains?
2. Which private generator functions need reuse in src/core?
3. Do malformed, missing or shared stock references resolve honestly?
4. Can local synthetic tests verify full scale without private records?

Candidates: src/core/synthetic, generated-dataset tests, inventory/coverage
contracts, existing support generator source and public synthesis.

## Research Cycle Log

Cycle 1 completed inline:

1. Wider: issue 168 has only three acceptance criteria; PR 246 already provides
   seeded fabric and a link summary. M1-M6 do not move the support generator.
   SN-01 remains partial, explicitly awaiting private register regeneration and
   owner decisions. Reflection: do not create another stock generator.
2. Deeper: the builder and EPC generator import support/zf_stock_fabric;
   core tests add support to sys.path. Fabric uses stable per-home seed v1 but
   its CLI defaults to private files under support. Link reporting collapses
   duplicate case IDs and accepts duplicate stock IDs as if unambiguous.
   Reflection: migrate this module into core, preserve seeded draws, validate
   identities and add per-case resolution provenance.
3. Contrarian: 825 distinct anchors for 980 cases does not prove unit linkage.
   The builder already says flats can share building geography. No private
   register regeneration code or owner reconciliation decision is supplied.
   Reflection: retain anchor semantics and expose shared anchors rather than
   manufacture unique IDs or reconcile home.built/type. Validate at scale with
   fictional register inputs, not private geography.

Synthesis: accept migration, deterministic fabric, explicit missing/ambiguous
links and public assumptions. Reject new stock lineage and fuzzy joins.
Defer private stock reproduction and unit-level reconciliation to the owner.
No further cycle: source trace covers the bounded change; missing external
evidence cannot be obtained by more source inspection.

## Evidence Log

* W1: https://github.com/jmservera/ama/issues/168, retrieved 2026-10-15.
  Three criteria: case resolution or explicit unlinked, seeded synthetic
  attributes, assumption-labelled distributions. Reopened to verify PR 246.
* W2: https://github.com/jmservera/ama/pull/246, retrieved 2026-10-15.
  Prior report claims 980 linked / 825 homes; not independently regenerated.
* W3: https://github.com/jmservera/ama/issues/166 and
  https://github.com/jmservera/ama/issues/167, retrieved 2026-10-15.
  Inventory owner review remains open; use existing inventory and coverage CLI.
* C1: `docs/adrs/0006-src-layout-and-cutover.md:59`: src-only new features;
  core owns synthetic tooling; core imports no workload.
* C2: `src/README.md:15`: merged M1-M6 paths and local suite commands.
* C3: `support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/zf_stock_fabric.py:90`:
  set-based stock matching and dict-based linked cases silently lose ambiguity.
* C4: `support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py:277`:
  fabric/EPC case enrichment; stock_link_kind explicitly distinguishes anchors.
* C5: `src/core/tests/test_generated_dataset.py:19`: support imports and a 6000-row
  wholly fictional register exercise the retained 980-case builder.
* C6: `src/core/src/zava_forward/core/synthetic/provenance.py:17`: reuse source
  revision, nonempty-output rejection and payload hashes.
* C7: `docs/reference/research/retrofit-synthetic-data/needs-inventory.json:19`:
  SN-01 partial, 60,000 homes, private regeneration unavailable; user explicitly
  authorizes the existing volume/scope for this bounded iteration, not approval
  of the full inventory or a claim of generated-output conformity.
* C8: `src/core/src/zava_forward/core/synthetic/__init__.py:8`: reuse ZF_DATA
  destination handling, with explicit refusal of repository output paths.
* C9: `support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/zf_manifest.py:12`:
  fingerprints support .py files only; add the moved fabric dependency so
  builder/EPC provenance continues to cover it.

## Findings, Alternatives and Decision State

Selected: move-not-copy fabric implementation to
`src/core/src/zava_forward/core/synthetic/stock_fabric.py`; typed records, v1
draw compatibility, deterministic links, private-output CLI, no SQL changes.
Wire the retained builder and EPC imports to core. Keep legacy case fields
and show per-case stock linkage as a source-register assertion, never consent,
assessment, EPC or verified unit identity.

Risk: actual private 60,000-home / 980-case outputs are not revalidated.
Local data-only checks are not delivered application acceptance. Real AI,
SQL Server/Azure and human approval/consent gates remain unchanged and unproven.
Missing dependencies: pip show reports all five distributions, ruff and mypy
absent. Restore with pip in a worktree-local ignored virtual environment.

## Planning Readiness

Ready for the bounded source/tooling and fictional-evidence slice.
Research disposition: executed. Parent rpi-quick may continue automatically
under explicit user direction. Acceptance on actual retained private stock
remains unverified; inventory owner review and unit reconciliation remain open.
Self-check: all three waves complete; claims have source pointers; no private
records read, copied or committed.
