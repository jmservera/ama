<!-- markdownlint-disable-file -->
# #184 stage B1: critique (2026-11-12)

Execution: ONE self-run read-only critique of the [plan](./issue-184-start-stop-b1-1112-plan.md) and details, before implementation. Not independent. Not repeated.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | Checking the gate before `pacer.admit` would miss a stop that arrives during the pacing sleep | Applied: gate after admit, immediately before send |
| 2 | A gate exception (for example an unexpected error) must not allow a send | Applied: exception means fenced |
| 3 | Tests only against a lambda gate would not test production | Applied: `attempt_permitted` is a module function and `main` is tested end to end with a patched sink that rewrites the real control file |
| 4 | Per-process attempt cap in the proposal row is not admitted by the owner | Applied: not added, recorded as unmet in changes and Review |
| 5 | Ending the run on a fenced slot could skip a later legitimate restart | Rejected as a concern: a stop is final per the existing run docstring; a restart is a new process |
| 6 | Reading the file per attempt for 100 homes is a cost | Accepted: bounded by cohort cap and rate, local small file, no network |

No finding conflicts with a confirmed owner decision; no owner decision required.
