# Issue 1818 c2 plan

1. Make `put` override signature match `Seed.put` and forward all arguments.
2. Add a typed `get_map()` helper wrapping the untyped `request` (single targeted ignore), used by both call sites; cast result.
3. Verify: mypy in src/api and src/core, ruff, unittest. Commit locally; no push.
