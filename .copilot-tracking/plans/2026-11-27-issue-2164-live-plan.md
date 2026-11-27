# Issue 2164 plan (2026-11-27)

* [x] Phase 1: add one test that a roster-bound, view_only Entra principal with an eligible role is denied by `assistants.authorize`, for both a scoped and an unscoped row (closes the only uncovered combination).
* [x] Phase 2: run the targeted tests; record the per-criterion table.

Tier: focused (test-only change, no src behaviour change, no workflow or dependency edits). Basis: owner decision D4/D6.
