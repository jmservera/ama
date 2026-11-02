<!-- markdownlint-disable-file -->
# Employee chat local checks: plan (2026-11-02)

Task: `employee-chat-local-checks-530`. Refs #530. Research: [../../research/2026-11-02/employee-chat-local-checks-530-research.md](../../research/2026-11-02/employee-chat-local-checks-530-research.md).

* [x] Phase 1: install the five distributions into a throwaway venv from this worktree (pip).
* [x] Phase 2: run chat unit tests in core, agents and api.
* [x] Phase 3: run SQL chat tests on a task-owned disposable SQL Server container, then remove it.
* [x] Phase 4: run the employee chat browser and axe checks with the pinned axe-core.
* [x] Phase 5: record results, defects and follow-ups; no source change.

Critique: executed once inline; verdict accepted. The plan is evidence-only with no product change, so the main risk is overclaiming. Mitigation: criterion 8 stays unticked because live verification is separate and still unmet.
