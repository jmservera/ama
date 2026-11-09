<!-- markdownlint-disable-file -->
# Issue 189 validation recapture critique (2026-11-09)

One critique of the final candidate plan (independent rubber-duck agent, read-only). Findings: four blocking, two non-blocking; all applied to the details. Not repeated for this task.

| # | Severity | Finding | Disposition |
|---|----------|---------|-------------|
| 1 | Blocking | `python` is not on PATH; only the worktree `.venv` interpreter exists; `node --check` paths unspecified. | Applied: every command uses `../../.venv/bin/python`; node paths are full (details P3). |
| 2 | Blocking | A commit-tree comparison does not prove the files tested were unchanged or imported from this worktree. | Applied: record resolved module paths, `git status --ignored` plus content hash of `src` before and after capture, and verify the equivalence again after the evidence commit exists. |
| 3 | Blocking | The manifest sits beside the logs with no independent anchor. | Applied: the manifest's own sha256 and retained location are written to the changes record, and the manifest is verified with `sha256sum -c` before handoff. |
| 4 | Blocking | Exit capture could miss or misstate a status. | Applied: a fixed wrapper saves `$?` on the next statement, no `errexit`, a missing or empty exit file means not run, never pass. |
| 5 | Non-blocking | Exit 0 alone could misrepresent coverage. | Applied: each summary must show a nonzero run count reconciled with verbose ok and skipped lines; the browser must print every expected state and a completion marker. |
| 6 | Non-blocking | Skips are not guard denials. | Applied: skips and observed refusals are recorded separately; if no actual guard denial occurs, the record says so. |

Reviewer confirmed all ten modules exist, load with the proposed paths and support `-v`; nothing was run.
