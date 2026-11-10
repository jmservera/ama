# Issue 86 formal-complaints parent re-alignment: critique

Scope: jmservera/ama#86 only. One independent read-only critique pass (rubber-duck sub-agent) before any rebase; not repeated. Verdict: proceed with changes.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocker | Committing the records before the rebase means HEAD holds more than the six child commits, but the backup pinned only `6ff492adf`. | Accepted. Back up the actual pre-rebase HEAD plus keep `6ff492adf` as its own ref; enumerate `c5edb320..HEAD` and stop on mismatch. |
| 2 | Significant | `c5edb320` is not an ancestor of the new parent (rewritten history); range-diff matched four parent patches and one modified. It is still the right old boundary. | Accepted and verified. Plan keeps `c5edb320` as the onto boundary and stops on missing or materially changed parent patches. |
| 3 | Significant | Research wrongly implied main was not in the parent; two observations cannot prevent later movement. | Accepted. Verified `0f420dc95` is an ancestor of `ad72384f3`; research corrected; recheck parent, worktree and main immediately before and after the replay. |
| 4 | Significant | Equivalence needs explicit failure criteria; blob equality alone can mislead. | Accepted. Range-diff `c5edb320..backup` against `pinned-parent..new-head`, inspect every non-identical patch, stop on skips or unexplained differences. |
| 5 | Minor | Conflict forecast unsupported: parent diff from `c5edb320` does not touch `store.py`, `resident_decisions.py` or the core README; a merge fallback could retain rewritten history. | Accepted. Reassess against the final parent; no automatic merge fallback. |

Publication still needs FULL; historical SQL-backed tests were skipped in focused runs.
