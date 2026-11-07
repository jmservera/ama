<!-- markdownlint-disable-file -->
# Critique: issue #81 parent re-alignment (2026-11-07)

Execution: `executed` once, prospectively, before the rebase. Reviewer: independent `rubber-duck` (read-only). Verdict **Revise**; all findings compatible with current direction and applied directly; none needs a user decision. Not repeated.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | Shared `quality.py` proof underspecified | Accepted. Diff post-rebase `quality.py` against the backup; the only difference must be main's `from typing import Any` and `checklist_rows()`. Separately diff against main to show only the #1226 gate hunks remain |
| 2 | Significant | Base may move after P1 | Accepted. Rebase onto the pinned SHA; re-fetch before freeze; if changed, inspect and re-plan or rebase again with a recorded amendment |
| 3 | Significant | API install may resolve a different core | Accepted. Install local `src/core` and `src/agents` explicitly first, then api with `--no-deps` plus only actually missing dependencies; verify each package's import origin |
| 4 | Significant | API checks optional yet required | Accepted. Core checks are required; API checks are best-effort. An unavailable or failing-to-install API check is recorded `unverified`, never passed, and the final claim says so |
| 5 | Significant | Schema UI tests omitted | Accepted. Add `test_finance_grants_screens` to the API selection; browser harnesses stay excluded |
| 6 | Minor | Env switch names imprecise | Accepted. `env -i` allowlist only; `ZF_RESIDENT_MSSQL`, `ZF_RESIDENT_AZURE_TEST` and all other `ZF_*` and `AZURE_*` switches unset; skips recorded |
