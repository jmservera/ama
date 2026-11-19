# Details: issue 146 live, 2026-11-19

Phase 2: the note records the live inventory commands (`az monitor metrics alert list`, `az monitor scheduled-query list`, `az resource list --resource-type microsoft.insights/workbooks`, all with `-g ama`), their summarised outputs without secrets, and a proven/unproven table. Add an index row in docs/reference/README.md and append a log.md entry.
Phase 3: check relative links resolve; `git diff --stat` shows docs only.
