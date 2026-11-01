# Plan: issue 163 DPIA record drift guard, 2026-11-01

* Research: `.copilot-tracking/research/2026-11-01-issue-163-dpia-record-guard-research.md`.
* Critique (single, self): compatible. Keep scope to a test plus log entry; do not edit DPIA decisions or code. Applied directly.

## Phases

1. Add `src/core/tests/test_chat_dpia_record.py`: (a) every `chat_privacy.DATA_MAP` id is represented in the DPIA data map table; (b) decision pack rows D1 to D8 each end in "Not recorded" while `CHAT_*_REF` env refs are unset; (c) the DPIA record states no retention period as approved (data map retention cells stay Unknown or policy text).
2. Append a `docs/reference/log.md` entry (no index change; no file added to the knowledge base).
3. Validate: unit tests, ruff check, ruff format --check, mypy for `src/core`.
4. Review once, commit, push, PR with `Refs #163`.

## Acceptance

* Test passes and fails if a decision cell is filled without a reference or a data class is dropped from the record.
