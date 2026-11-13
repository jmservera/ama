# Plan: Epic #104 criteria 3 and 5 cross-capability invariant suite

Task `epic104-ai-nonmutation-limits`. Research: `.copilot-tracking/research/2026-11-13/epic104-ai-nonmutation-limits-research.md`. Details: `.copilot-tracking/details/2026-11-13/epic104-ai-nonmutation-limits-details.md`.

## Phases

* [x] Phase 1: registry guard and five-assistant non-mutation tests
* [x] Phase 2: ranking immutability, human route, chat, concern pack and held-out boundaries
* [x] Phase 3: NFR-012 limit enforcement across every registered capability
* [x] Phase 4: focused validation (agents and core tests, ruff, mypy) and clean commit

## Constraints

* Write only `src/agents/tests/test_epic104_bounded_ai_invariants.py` plus tracking artifacts; touch no #146 file or `infra/`.
* Fix production code in `src/agents/` only if a test proves a real bypass; none is expected.
* Focused tier, pip venv `/tmp/venv-104-2244`, remove it at the end. No push or PR.

## Critique

Critique executed once (verdict Revise, findings applied): `.copilot-tracking/critiques/2026-11-13/epic104-ai-nonmutation-limits-critique.md`.
