# Plan: #2164 (2026-11-22)

Tier: FULL candidate (security control change in src/core). Details: .copilot-tracking/details/2026-11-22/issue-2164-live-details.md

- [ ] Phase 1: change `Assistants.authorize` so a verified Entra principal with `bound` reads its roster row (by bound email, oid and role must match, disabled/active honoured) and inherits `case_ids`/`areas`; refuse view_only Entra principals.
- [ ] Phase 2: tests in src/api/tests/test_assistants.py (scope inheritance, revocation, oid mismatch, view_only with eligible role, scope bypass on invoke/listing).
- [ ] Phase 3: run targeted tests, mypy, ruff; record changes with per-criterion table; review once; commit.
