---
title: Storytelling Review, Iteration 5, AMA Mentor Progress Review Deck
description: Storytelling and fact review of the iteration 5 delta (slide 10 role-answer re-run, Awaab's Law wording, slides 3 and 15 git evidence) against the Agent What-If Study and the 27 Sep log entry
ms.date: 2026-09-27
---

<!-- markdownlint-disable-file -->

## Verdict

The delta mostly works. The slide 10 figures match the study: 48 role-agent answers were re-run against the current addendum and BRD v0.5.0, six changed materially, and every revised verdict in the summary table still reads "Unchanged" or "Slightly stronger". The slide is not too dense. The panel renders cleanly with space to spare. The new bullet is about robustness and the banner is about sequence, so they do not compete. Slides 3 and 15 show the correct count: `git log --no-merges` returns 41 commits, and there are still 13 BRD commits.

Two fixes are needed before publishing:

* The new slide 10 notes undo an accepted iteration 4 correction. They now say I re-ran all eleven no-agent answers, when nine were re-run and two were relabelled as author hypotheses.
* "No verdict changed" is slightly stronger than the study, which says the verdicts affected by the six material changes "were updated". "Every verdict held" is accurate.

Three low-severity items follow. No structural change is needed.

Main-deck notes impact if SR5-01 to SR5-03 are all applied: +18 words, from 1,951 to about 1,969, still under the 2,000 budget.

## Findings

### SR5-01: The notes say all eleven no-agent answers were re-run

* Severity: Medium
* Slide: 10 (notes)
* Evidence: the notes say "eleven answers from roles that have no agent. I re-ran those, then re-ran every role answer against the reframed proposal." The study's Purpose and Method says "nine of them were re-run with the nearest role agents ... The two governance and internal audit questions have no matching role agent and are labelled as author hypotheses." Reconciliation adds "The two author hypotheses were not [re-run]." This is a regression. The iteration 4 notes and SR4-06 kept this distinction, and slide 10 is where a Scientist mentor is most likely to test the method.
* Recommendation: replace "I re-ran those, then re-ran every role answer against the reframed proposal." with: "I re-ran nine with the nearest roles and labelled two as my own hypotheses. Then I re-ran every other role answer against the reframed proposal."
* Word-count impact: +13

### SR5-02: "No verdict changed" is stronger than the study

* Severity: Medium
* Slide: 10 (findings bullet 4 and notes)
* Evidence:
  * The bullet says "six tightened controls, no verdict changed". The notes say "No verdict changed, but six answers tightened controls to match the BRD."
  * The study's Purpose and Method says "Six were material, and the scenario text, verdicts and stop criteria they affect were updated". Reconciliation says "The affected scenario text, verdicts and stop criteria were updated."
  * Some verdict wording did change. The PS2 revised verdict now ends "Later work: the initial pilot has no supervision agent". The Aggregate Verdict for Programme Supervisor now says "The initial pilot has no supervision agent, and Board and executive narratives stay written by executives".
  * The Damp-and-Mould aggregate verdict still reads "Do not build as an agent", but its stop criteria changed ("never back-dates", earlier-awareness hits go to Legal and Safety).
  * Every verdict still points the same way, and none moves towards an end-to-end agent. The fault is only the word "changed".
* Recommendation:
  * Bullet: "All 48 role answers re-run on the reframe: six tightened controls, every verdict held" (83 characters against 84 now, so it still fits on two lines).
  * Notes: replace "No verdict changed, but six answers tightened controls to match the BRD." with: "Every verdict held; six answers tightened controls to match the BRD."
  * Keep the title. "Twenty what-ifs changed no verdict" compares the what-ifs with the original challenge, and that is still exact.
  * On the Q&A card, add: "Held means the direction is unchanged. The supervisor verdict now says the pilot has no supervision agent at all."
* Word-count impact: -1

### SR5-03: The Awaab's Law wording is vague and reads as conditional

* Severity: Low
* Slide: 10 (notes)
* Evidence:
  * The notes say "Awaab's Law awareness, which can start when a photo arrives". The study is firmer on the latest point and open only on earlier ones.
  * Assessment says "hazard photos can establish Awaab's Law awareness no later than their arrival ... whether an installer's on-site knowledge counts earlier depends on contractor status (BRD OD-29)".
  * DM1 says "the landlord is aware from the moment content arrives, whether or not a human has read it".
  * "Can start" is not an overclaim, but it hides the governance point: the clock does not wait for someone to read the photo.
* Recommendation: replace "which can start when a photo arrives," with: "which starts no later than when a hazard photo arrives, read or not,". Leave OD-29 (earlier awareness) for Q&A.
* Word-count impact: +6

### SR5-04: "Five PRs" tells the mentor nothing, and the latest commit message undercuts the card

* Severity: Low
* Slide: 15 (appendix, Git history card)
* Evidence:
  * The card says "41 commits, 10 to 27 Sep, and five PRs; most messages say what changed and why".
  * `gh pr list` shows #1 to #3 merged and #4 and #5 open. The #5 branch (`Review-progress-challenge`) is already merged into the #4 branch (baef324), so "five" counts work twice.
  * The commit that carries the role-answer re-run, 7bdd952 (study +1,021 lines, log, addendum), is titled "Refactor code structure for improved readability and maintainability". It is already pushed to `origin/claude/study-agent-challenge-review`.
  * Slide 10's source line points the mentor to that re-run. If the mentor opens `git log`, the first message they see contradicts the card.
* Recommendation:
  * Card: "41 commits, 10 to 27 Sep, and three merged PRs; the log records what changed and why". The claim then rests on the log, which is the actual record.
  * Owner decision, not a deck edit: either record the mislabelled commit in the next log entry or accept it. Rewriting pushed history is not recommended.
  * SR4-07 still applies. Committing iteration 5 makes the total 42, so recount slides 3 and 15 just before publishing, or state "to 7bdd952".
* Word-count impact: 0 (on-slide only; appendix notes do not mention PRs)

### SR5-05: "48" invites a "48 of what?" question

* Severity: Low (Q&A only)
* Slide: 10
* Evidence:
  * The panel has 20 scenarios and 48 answers side by side. The study has 50 answers: 48 from role agents and two author hypotheses.
  * The re-runs came in two passes: nine answers after the merge (three material differences), then the remaining 39 (1 unchanged, 32 refined, 6 material, per the log).
* Recommendation: no slide change. Add to the speaker Q&A card: "Fifty answers across twenty scenarios: 48 from role agents, all re-run against BRD v0.5.0 in two passes, and two that are my own hypotheses. Of the last 39, one was unchanged, 32 refined and six material."
* Word-count impact: 0

## Iteration 4 Findings Recheck

* SR4-01 (thirteen revisions): holds. Slide 3 card and notes say thirteen, and `git log --no-merges` on the BRD returns 13.
* SR4-03 and SR4-04 (SP1 in grid, white legend): hold. The M/M cell lists "Condition-photo app", and the legend explains white.
* SR4-05 (OD-34 proposed): holds in bullet 5 and in the notes.
* SR4-06 (method wording): the "focused questions to the role agents" wording holds, but the last paragraph now breaks it (SR5-01).
* SR4-07 (stale counts): fixed for now at 41, but it will go stale again on the next commit (SR5-04).
* SR4-08, SR4-09 and SR4-11: hold.
* SR4-10 Q&A card: consistent with this delta ("The verdict held"). Add the SR5-02 and SR5-05 lines.
* No other deck figure is contradicted by the new log entry. The re-run did not touch the BRD, so v0.5.0, the six quality runs and the slide 11 counts stand. The deck does not quote the addendum's what-if paragraph, which did change.
