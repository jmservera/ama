<!-- markdownlint-disable-file -->
# PR 1295 CxO story recovery plan (2026-11-09, prospective)

Details: [phase details](../../details/2026-11-09/pr-1295-cxo-story-recovery-phase-details.md). Research: [research](../../research/2026-11-09/pr-1295-cxo-story-recovery-research.md).

## Scope

Assess the frozen 54-page CxO story and architecture deck at head `b671116d`. No new deck, narrative rewrite, slide financial value, navigation, page count or protected cost change. Not a mapping of issue 435.

## Owner-selected demo-targeted tier

Pure documentation scope; no blanket gate and no `rpi-checks --all`. Run only existing focused checks that cover the deck contract and navigation:

* `node --test docs/capstone/source/diagrams/architecture/test-architecture.mjs`
* `pytest -q tools/capstone/test_render_preview.py` in a session-local venv (PyMuPDF, pytest from `tools/capstone/requirements.txt`).
* Read-only source-locator, package, page-count and financial-figure comparison against `origin/main`.

Hosted checks and independent exact-head review stay mandatory.

## Phases

* [x] Phase 1: research claims against source and original evidence.
* [x] Phase 2: run the focused checks above; a failing check is not waivable.
* [x] Phase 3: no confirmed coupled bug; no deck change.
* [x] Phase 4: record changes, review, state and handoff; commit only the recovery artifacts.

## Boundaries

No push, PR edit, merge, issue close or tick, deploy, real model call, spend, or settings change. Original FAIL, interrupted-gate and stopped-attempt records are preserved.
