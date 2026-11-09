<!-- markdownlint-disable-file -->
# Issue 189 composed browser check critique (2026-11-09)

One critique, executed once (rubber-duck, read-only) on the committed-to-be plan, details and research. Verdict: Revise, five findings, all dispositioned directly; no confirmed-decision conflict; not repeated.

| # | Severity | Finding | Disposition |
|---|----------|---------|-------------|
| 1 | Blocking | Details did not select the venv interpreter. | Applied: explicit `$S/venv/bin/python` for pip and runs, plus an interpreter proof line. |
| 2 | Blocking | Old-probe exit 1 conflicted with the stop rule. | Applied: expected negative control only with the C3 stdout/stderr signature; otherwise blocker. |
| 3 | Blocking | Lock procedure not executable or separated from later exit codes. | Applied: one FD, `flock -n 9` admission recorded alone, FD held through all runs, release recorded. |
| 4 | Non-blocking | Probe duplicates the wait, not the checker helper. | Applied: described as UI synchronisation evidence only. |
| 5 | Non-blocking | Probe provenance. | Applied: hash the copy against the original capture before execution. |
