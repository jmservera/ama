# Review: M2 core hub (refs #199)

Execution: executed once after implementation. Outcome: conformant with open follow-ups.

| Check | Result |
| --- | --- |
| Pure moves, history follows | renames detected; edits limited to imports, paths and exemptions |
| No shim or copy in `mvp/` | grep for old module paths finds none; `mvp/policies` removed |
| Test count | 742 total against baseline 742; skips 92 equal |
| Hashed requirements | untouched |
| Check names | `mvp-ci`, `mvp-validation`, `src-*` unchanged |
| SQL portability | no SQL edits; portability test passes |
| Docker image, SQL Server job | unverified locally; CI to confirm |

## Follow-ups (later, user-selected)

1. Confirm CI `image`, `mssql` and `src-*` jobs.
2. Move the four server-bound tests in M5 and split `ai_registry` and `assistants` to `agents` in R1.
3. Remove ruff and mypy exemptions in M6; check `tools/rename-zava.py` for the old `mvp/policies/` path.
