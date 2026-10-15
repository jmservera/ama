# Review: M1 isolated leaves (refs #199)

Execution: executed once after implementation. Outcome: conformant with open follow-ups.

| Check | Result |
| --- | --- |
| Pure moves, history follows (`git diff -M`) | 6 renames, no content change besides imports |
| No shim, re-export or copy in `mvp/` | confirmed; grep for old names finds none |
| Test count equal or greater than baseline | 719 equals 719; skips 92 equal |
| Hashed requirements not loosened | lock untouched |
| Check names kept | `test`, `image`, `mssql`, `validate` unchanged |
| Docker image build | unverified locally (permission denied); CI to confirm |

## Follow-ups (later, user-selected)

1. Confirm the CI image job with the repository-root build context and the Trivy scan.
2. Update `rulecards.TRACE` test paths when later steps move the other tests it names.
3. Remove the ruff and mypy exemptions for moved files in M6.
