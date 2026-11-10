**Verdict: Revise.** The change is mostly correct, with one medium finding and two low ones.

Frontmatter is unchanged. The diff against `7ae4159` has a single hunk, in the Liveness admission bullet (diff line 114), which is outside the frontmatter.

**Checked and correct**
* More than 20 open PRs bars new issues and starts a drain, recorded on the first confirmed count above 20.
* While draining, no admission even at 16 to 20, until a confirmed count of 15 or fewer. The target of 10 to 15 is kept.
* A run that never drained is admitted at 20 or fewer.
* The eight-assignment cap stays separate, and existing-PR continuations stay permitted within it.
* The no-relaxation sentence covers dependency, validation, publication, review and human gates.
* Cross-references at lines 372, 384, 544 and 585 point to the Liveness rule and do not contradict it.
* The old "more than 20, take no new issues" bullet no longer exists in HEAD, so there is no stale duplicate.
* `origin/main` has no "Admit new" text, so the old wording I compared against is the one in the base diff. I could not match your "lines 183-190" reference exactly.

| id | severity | requirement | evidence | smallest fix |
|---|---|---|---|---|
| F1 | Medium | A run that never entered drain must not be barred at 16-20; a stop/idle decision needs a classification and a bounded recovery action | Lines 119-120: "treat the run as draining when the state or a confirmed count is unavailable". A lost or unreadable ledger row with a confirmed count of 17 bars admission, although no drain was ever entered. This conflicts with the line 127 idle-slot defect and the line 146 recovery duty. | Replace with: "if the count is unavailable, admit none and re-read `gh pr list --state open` this tick as the next action; if only the ledger state is unavailable, rebuild it from evidence, and bar admission only while a confirmed count is above 15." Also list unresolved drain state as an `unknown` row, which is research work for this tick and never `human-blocked`. |
| F2 | Low | Traceable drain state | Lines 118-124: the entry is recorded in the ledger, but clearing it is not. The ledger table is also unnamed, while the other tables are named (`tick_log`, `closure_review`). | Say "record the clear when a confirmed count is 15 or fewer" and name the table, for example `drain_state`. |
| F3 | Low | Clarity | Lines 124-127: the wrap leaves "Existing-PR" orphaned mid-line. "One at a time" during a drain could be read as a cap on concurrent repairs alongside the eight-assignment cap. | Re-wrap the paragraph. Add "one PR per merge step; sessions still count against the eight-assignment cap." |

**Limits**
* Static read only, with no behavior simulation.
* I did not open the hve-builder `requirements-catalog.md` or `review-rubric.md`. I judged against the owner rule and the issue criteria.
* Only the admission bullet and its cross-references were reviewed in depth, not the whole 800-line file.