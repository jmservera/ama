<!-- markdownlint-disable-file -->
# Plan critique: issue-1294-validation-policy-priority-e1

* Execution: executed once, 2026-11-09, by a fresh-context rubber-duck subagent (read-only; proxy independence: a separate context, not a human or the canonical host-bound critic).
* Verdict: Revise (one High, three Medium). All findings compatible with confirmed decisions; applied directly, no user decision needed.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-1 | High | Final-head checks and review sequenced before the commit, so they could not bind the final SHA | Accepted. P05 reordered: commit, then final-head checks and the one Review on that exact SHA; any later edit repeats them |
| PC-2 | Medium | Coordinator step 8 (lines 759-770) can restore a blanket `--changed` refresh for focused candidates | Accepted. Add a sentence: a focused candidate without a receipt refreshes with targeted local checks; a partial receipt is used only when one was produced and is cited |
| PC-3 | Medium | Rubric steps 1 and 3 still require a full-receipt assessment | Accepted. Qualify both steps (and the receipt verification) by selected tier |
| PC-4 | Medium | The sensor selection rule ignores that inert paths are excluded first (`tools/rpi-checks.py:725-726`) | Accepted. State the rule for non-inert paths and probe a sensor-named Markdown path |

No scope creep into #1296/#1298 and no proxy overclaim was found. The critique is not repeated for this task.
