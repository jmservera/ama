<!-- markdownlint-disable-file -->
# Plan: Issue #104 controlled-record non-mutation proof

* Research: [104-controlled-nomutate-0230-research.md](../../research/2026-11-14/104-controlled-nomutate-0230-research.md)
* Details: [104-controlled-nomutate-0230-details.md](../../details/2026-11-14/104-controlled-nomutate-0230-details.md)
* Validation tier: Focused (system `python3`, no `uv`). Not a full gate receipt.
* Critique (single, inline): compatible findings applied. Snapshot must use raw SQL, not API projections; add a positive control; keep audit growth separate; avoid editing `pyproject.toml`; no production code change.

## Phases

* [x] P1: Build a real HTTP fixture (SQLite `SqlStore`, `App` password login, configured `Assistants`, stubbed provider) and seed controlled records through authorised human routes.
* [x] P2: Snapshot helper over raw rows, hazard, consent, sign-off, finance and ranking archive bytes.
* [x] P3: Tests for adversarial chat, assistant invoke/claim/dispatch/complete/review/reject, proactive scan, absent approve/execute routes, and the human positive control.
* [x] P4: Ruff, format check and focused unittest; commit with `Refs #104`; no push.
