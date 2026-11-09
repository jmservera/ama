<!-- markdownlint-disable-file -->
# Issue 189 C2 browser check critique (2026-11-09)

One critique of the final candidate plan (independent rubber-duck agent, read-only). No blocking finding; three non-blocking, all dispositioned. Not repeated for this task.

| # | Severity | Finding | Disposition |
|---|----------|---------|-------------|
| 1 | Non-blocking | Ten clean repeats are evidence, not proof the race is gone. | Applied: add a deterministic delayed-Stop probe (a Playwright route delays the Stop POST by 1.5 s) run against the old and the new wait, retained outside the repository, besides the ten repeats. |
| 2 | Non-blocking | No collision is shown for the `Permitted` wait at line 149. | Accepted: unchanged; any contrary observation is recorded, not pre-emptively fixed. |
| 3 | Non-blocking | BrokenPipe causation and cycle expenditure are not independently proven by the logs. | Accepted: the research states BrokenPipe as consistent with teardown, not proven; the cycle ledger is quoted from the coordinator brief. |
