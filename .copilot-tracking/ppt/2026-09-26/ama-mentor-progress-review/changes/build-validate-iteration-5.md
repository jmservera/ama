<!-- markdownlint-disable-file -->
# Build and Validate: Iteration 5

* Date: 2026-09-27
* Trigger: the owner asked to update the mentor deck again after the what-if role answers were re-run
* Branch: `claude/study-agent-challenge-review` at 7bdd952; nothing new on `origin/main` or `origin/Review-progress-challenge`

## Delta Covered

| Project change since iteration 4 | Deck treatment |
| --- | --- |
| All 48 what-if role answers now current: nine re-run after the merge, the other 39 re-run against the reframe (1 unchanged, 32 refined, 6 material); every revised verdict still "Unchanged" or "Slightly stronger" | Slide 10 findings panel, notes and source line |
| Six tightened controls (shadow-only risk paths, named approval of AI-drafted resident messages, any-channel capacity, no initial-pilot supervision summaries, transcript flags never back-date clocks, awareness deferred to OD-29) | Slide 10 notes carry two examples; the rest are on the Q&A card |
| Awaab's Law wording qualified: hazard photos can establish awareness no later than their arrival; earlier awareness depends on OD-29 | Slide 10 notes |
| Commit counts: 41 non-merge commits from 10 to 27 Sep; 13 BRD commits unchanged; PRs #1 to #3 merged, #4 and #5 open | Slides 3 and 15 |
| Memory: last changed 2026-09-25, no change affecting the deck | None |

## Edits

* Slide 10: new findings bullet "All 48 role answers re-run on the reframe: six tightened controls, every verdict held"; the Awaab's Law and OD-34 bullets were shortened; panel height 3.7 to 3.95 in and bullet spacing 12 to 8 pt; the source line cites the role-answer re-run. The notes now describe both re-run passes and qualify the Awaab's Law awareness wording.
* Slide 3: the source line says 41 commits.
* Slide 15: the Git history card says "41 commits, 10 to 27 Sep, and three merged PRs; the log records what changed and why".

## Storytelling Review Decisions

Review: [storytelling-review-iteration-5.md](../research/subagents/storytelling-review-iteration-5.md)

| Finding | Decision | Reason |
| --- | --- | --- |
| SR5-01: notes say all eleven no-agent answers were re-run | Accepted | The study says nine were re-run and two labelled as author hypotheses; restores SR4-06 |
| SR5-02: "no verdict changed" overstates | Accepted | Scenario verdict text and stop criteria changed; the summary table still reads "Unchanged" or "Slightly stronger", so the bullet and notes now say "every verdict held" |
| SR5-03: Awaab's Law wording vague | Accepted with changes | Used the study's wording, "a hazard photo can establish no later than its arrival"; "read or not" is not in the study and was dropped |
| SR5-04: "five PRs" and commit-message claim | Accepted for the card wording | Commit 7bdd952 has a generic message, so the card now points to the log. Recounting before publishing was rejected: the card is dated 10 to 27 Sep and records the count at build time. The generic commit message is left to the owner |
| SR5-05: "48 of what?" | Accepted as a speaker card answer | See below |

## Speaker Q&A Card

* Why 48 role answers? The study has 50 answers across 20 scenarios. 48 come from role agents and two are my own hypotheses. Nine were re-run after the merge and the other 39 against the reframed proposal: one unchanged, 32 refined and six material.
* Did any verdict change? Every verdict held: the summary table still says "Unchanged" or "Slightly stronger". Six answers tightened controls and stop criteria to match the BRD.
* Which controls tightened? Pre-visit risk paths stay in shadow mode until a RULE-020 release decision; a named person approves every AI-drafted resident message (AC-079); suppliers offer capacity through any channel and a contract manager accepts it (FR-022); the initial pilot has no AI supervision summaries; transcript flags never back-date a clock (FR-004 AC-007); assessment awareness wording defers to OD-29.
* When does Awaab's Law awareness start for photos? A hazard photo can establish awareness no later than its arrival. Whether an installer's on-site knowledge counts earlier depends on contractor status, which is open decision OD-29.
* Were the regulatory citations checked? Only against the local snapshots, not against the official sources online.
* What does more grant money mean for our own spend? Grants need co-funding, so more grant means more of our own spend. The addendum illustrates about GBP 66.7 million of provider funding, as an estimate.

## Validation

| Check | Result |
| --- | --- |
| `build_deck.py` | 15 slides |
| `validate_deck.py` | 0 issues across 15 slides |
| `validate_geometry.py` | 0 issues across 15 slides |
| Slide images | Exported with `Export-SlideImages.ps1`. Slides 10 and 15 were viewed after the final build; slide 3 changed only in its source line |
| Main notes | 1,967 words, about 14 minutes at 140 words per minute; the appendix has 153 words |

## Delivery

* Published to `docs/presentations/ama-mentor-progress-review.pptx`
* SHA-256 `D950070D0E8C1EC50951E33E5B412B6F12E02C5AF24D1272DFD45CE83F645343`, identical to the build in `slide-deck/`
