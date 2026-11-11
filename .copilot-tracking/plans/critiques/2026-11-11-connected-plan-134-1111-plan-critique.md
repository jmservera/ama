<!-- markdownlint-disable-file -->
# Plan Critique: Issue 134 connected same-home walk (2026-11-11)

Execution: one independent rubber-duck critique pass over the research, plan and details, with source verification (store persistence, role-screens render and menu code, probe selectors). Verdict: Revise. No second critique is run for this task.

| # | Severity | Finding (retained) | Disposition |
| --- | --- | --- | --- |
| 1 | High | Missing evidence could count as success: assertions may be `gap` and `chain_failures` did not require journey markers, so an empty journey could exit zero | Applied directly. Required markers now fail when absent; `gap` limited to declared deferrals or a P1-proven render limit (plan success criteria, details `chain_failures`) |
| 2 | High | Factory snapshot path wrong: `Store` saves to `live_path` (`live.json`), the seed file is unchanged (`store.py` lines 57 to 70, 114 to 119), `store.data_path` does not exist | Applied directly, verified by reading `store.py`. Snapshot is `copy.deepcopy(store.data)` before cleanup; a pure test checks the snapshot holds the journey records |
| 3 | High | Reset after each screen drops `case`, so carry between screens would not be shown; the probe's screen-link selector omits `case=` | Applied directly. No reset between steps 1 and 2; prefix selector with `case=ZF-1`; reset is its own final step |
| 4 | Medium | "Resolved" is not the rendered word (it is "Reconciled (recorded by a named person)", `role-screens.js` line 132); the programme table rows do not name the home, its panel heading does | Applied directly, verified in source |
| 5 | Medium | Sibling negative control too broad: generic words and portfolio panels cause false results | Applied directly. Distinctive markers, scoped to `.screen-evidence` |
| 6 | Medium | "No state clears another" is a source design hypothesis, not demonstrated by one snapshot | Applied directly. Reported as source text only; state-change testing deferred to a separate admitted scope |

Rejected advice: none. Significant or divergent decisions needing the user: none; the correction-balance classification question stays recorded in the plan for Root and is not decided here.

Unverified by the critique and by this task: the login heading for each journey role (the probe waits for "My cases today" or "Your jobs" and passed on its own fixture); recorded as a P1 confirmation, not assumed.
