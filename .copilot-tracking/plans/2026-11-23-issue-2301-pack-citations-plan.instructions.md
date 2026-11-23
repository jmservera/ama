# Plan: pack citation guard (2026-11-23)

Tier: focused; test-only, no src change.

* [x] Add tests to `tools/test_stabilization_checkpoint_2301.py`: pinned commit is an ancestor of HEAD; every backticked code or test entry in the pack rows resolves to a tracked file.
* [x] Run guard, sibling epic audits and ruff.
* [x] Changes record with per-criterion table; review; commit.
