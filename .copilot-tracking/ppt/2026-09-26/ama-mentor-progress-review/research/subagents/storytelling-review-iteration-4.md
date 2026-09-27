---
title: Storytelling Review, Iteration 4, AMA Mentor Progress Review Deck
description: Storytelling and fact review of the 15-slide mentor deck after the 27 September what-if slide, with a notes budget plan to 2,000 words or below
ms.date: 2026-09-27
---

<!-- markdownlint-disable-file -->

## Overall verdict

The new slide 10 fits well after slide 9. The seam ("Still a proposal: the pilot decides..." then "One more test, on 27 September") works. The post-merge corrections are accurate: Articles 22A to 22C, eleven answers, nine re-run and two author hypotheses, and the grid framed as a Comparison 2 test order. All the iteration 3 changes landed. Four problems remain. The slide 3 card still says "Twelve revisions" while the notes and slide 6 say thirteen. The grid shows 19 of the 20 scenarios. The appendix commit count is stale. The notes are 158 words over budget. No structural change is needed.

## Findings

| ID | Slide | Severity | Issue | Proposed change | Evidence |
| --- | --- | --- | --- | --- | --- |
| SR4-01 | 3 | High | The on-slide card says "Twelve revisions". The slide 3 notes ("thirteen commits") and the slide 6 banner ("Thirteen BRD revisions") disagree with it, and a Scientist mentor will spot the mismatch | Step 3 detail: "Thirteen revisions, with new research and role answers between each" | `git log --no-merges -- docs/brds/agentic-retrofit-programme-brd.md`: 13 commits, 008bf1c (11 Sep) to 97380bb (26 Sep). The merge baef324 is excluded |
| SR4-02 | All main | High | Main notes are 2,158 words, about 15.4 minutes. That is 158 words over budget | Apply the cuts in the Notes budget plan below. The result is 1,899 words, about 13.6 minutes | deck-text-iteration-4.txt totals |
| SR4-03 | 10 | Medium | The grid shows 19 of the 20 scenarios. The Medium value / Medium complexity cell leaves out SP1 (the resident and inspection app with condition photos). The title says "Twenty" | M/M cell: "Condition-photo app, live eligibility, concierge, board narratives" | agent-what-if-study.md, ASCII Quadrant: the M/M cell holds SP1, GF3, CO3 and PS2. Scoring Table: SP1 is M/M |
| SR4-04 | 10 | Low | The legend explains green, amber and grey but not the white middle band (four cells) | "Green: test first, after the foundation. White: opportunistic. Amber: big bets. Grey: defer." | Quadrant, Read the grid by cell: "Housekeeping or selective bets (middle band, M value): do opportunistically" |
| SR4-05 | 10 | Low | Bullet 4 states "the pilot decides what scales" as settled. It is the proposed OD-34 resolution. Slide 9 labels it as proposed, but slide 10 does not | "The grid orders what Comparison 2 tests first; under proposed OD-34, the pilot decides what scales" | Reconciliation With the Current Proposal: "Under the proposed OD-34 resolution, the pilot gate decides..." |
| SR4-06 | 10 notes | Low | "each put to the role agents" overstates the method. Two answers have no role-agent anchor. The last paragraph corrects this, but only after the claim | "twenty scenarios, with focused questions to the role agents." The existing last paragraph then stands without contradiction | Purpose and Method: two governance and internal audit questions are "labelled as author hypotheses" |
| SR4-07 | 15 | Low | The appendix says "35 commits to 26 Sep". Slide 3 says "39 commits, 10 to 27 Sep". Both are correct for their own date range, but they look inconsistent. The post-merge review record and these deck edits are not yet committed, so 39 will also go stale | "39 commits, 10 to 27 Sep, and PR #1; most messages say what changed and why". Recount slides 3 and 15 immediately before publishing | `git log --no-merges`: 39 commits (e32ea9c 10 Sep to b1bab12 27 Sep), 35 of them up to 26 Sep. `git status` shows the review log and slide files staged but not committed |
| SR4-08 | 1 notes | Medium | The agenda sentence now lists eight items (53 words) and repeats what slide 3 shows ten seconds later. This slows the Sergeant-style opening | Replace paragraph 2 with: "I will walk through five strands of work, three later challenges, my lessons and one traceability chain, then my questions." | Slide 3 on-slide strands. The three later challenges are on slides 9 and 10 |
| SR4-09 | 7 notes | Medium | The bridge sentence ("On 26 September the addendum still called agents...") repeats the "Later on 26 September" reframe in the slide 8 notes. Two of the three value examples repeat table rows | Cut "Stock prioritisation means defensible capital allocation. Grant and funding means grant cash without clawback." Keep the quality example, because the "most memorable row" line depends on it. Cut "On 26 September the addendum still called agents \"an implementation option\"; later that day it became agent-led modernisation, which is the next slide." Keep "The \"after\" question is how I phrase it now." | Slide 8 notes carry the reframe. The slide 7 table carries the values |
| SR4-10 | 10 | Low (Q&A) | No slide change is needed, but prepare three answers. (a) "Changed no verdict?" The headline verdict is unchanged. QV2 and QV3 are "slightly stronger" but still raise-only evidence. (b) "Were the answers given before the reframe?" Most were, and they have not been re-run. The nine re-runs used BRD v0.5.0. (c) "Were the regulatory citations checked?" Only against the local snapshots, not the official sources online | Speaker's Q&A card only | Summary of Revised Verdicts (QV2, QV3). Reconciliation, "Role answers". log.md, 27 Sep what-if and post-merge entries |
| SR4-11 | 12 notes | Low (optional) | The strongest new lesson is missing. The what-if study repeated the Article 22 error already fixed in CON-003. That is a lesson about propagating corrections. The budget allows it | Add after the canonical IDs sentence: "And when I fix an error, search every derived document for it; the what-if study repeated my Article 22 mistake." (21 words; total stays under 2,000) | log.md, 27 Sep post-merge review: "This is the same correction made to BRD CON-003 on 2026-09-26" |

## Notes budget plan

Cuts are exact sentences from deck-text-iteration-4.txt. Items marked "optional" give headroom only.

| Slide | Now | Target | Cut or tighten |
| --- | --- | --- | --- |
| 1 | 138 | 105 | SR4-08: replace the 53-word agenda paragraph with the 20-word version |
| 2 | 128 | 122 | Optional. "The brief is a one-page solution request. It names five agents with autonomy levels, a business case, and outcomes such as doubling delivery and capturing GBP 40 million of grants." becomes "The brief is a one-page solution request: five agents with autonomy levels, and promises such as doubling delivery and GBP 40 million of grants." |
| 3 | 122 | 122 | None |
| 4 | 188 | 161 | Move the whole "If asked: grants need co-funding... as an estimate." paragraph (27 words) to the Q&A card |
| 5 | 161 | 139 | Cut ", from the asset executive to a frontline housing officer" (the slide lists the roles). "They are anchored to the case, the addendum and the company research, and they label every answer..." becomes "They label every answer..." |
| 6 | 114 | 100 | Optional. Cut "Then came the regulatory context, the open-decision review and the modelled customer profile." (on the timeline) |
| 7 | 179 | 142 | SR4-09 (two value sentences and the bridge sentence) |
| 8 | 196 | 178 | Cut "Existing teams, suppliers and systems stay, and what I called the control plane is now the digital foundation." The ask box shows existing teams and suppliers, and the slide 6 notes already give the rename |
| 9 | 186 | 165 | Cut "The dashboard steers; only a frozen benefits scorecard counts at the gate." and "Some sources are still missing locally, logged as OD-39." (both are on the slide) |
| 10 | 156 | 148 | "When I merged the study with the latest BRD, a review caught two errors:" becomes "A post-merge review caught two errors:". Apply the SR4-06 wording (no net change) |
| 11 | 144 | 129 | Cut "The later edits raised four new findings on version 0.3.0, all fixed, and none since." (it is on the slide) |
| 12 | 156 | 135 | Cut "Regulation moves: EPC C is final policy but not commenced law, and Awaab's Law Phase 2 is planned from 30 November 2026." (it repeats slide 4). Add 21 words if SR4-11 is accepted |
| 13 | 144 | 134 | Cut "The change record: the 26 September log entries and commits." (it is on the slide) |
| 14 | 146 | 119 | "On the right is what comes next on the 85-day plan, which finishes on 5 December: the architecture, a shadow comparison of typed decision models, an optional demo with a static fallback, and CEO, CIO and CFO versions of the pitch." becomes "On the right is what comes next on the 85-day plan, to 5 December." Let the mentor read the list, and keep the close on the question |
| **Total** | **2,158** | **1,899** | About 13.6 minutes. 1,920 if both optional cuts are skipped, and 1,941 if SR4-11 is also added. All three stay at or under 2,000 |

## Checks passed

* **Accepted from iteration 3:** Article 22 wording (slide 9, on-slide and notes); the 7-to-8 bridge and the delivery cell introduced on slide 8; the order of the slide 9 challenges; "(proposed)" and "resident-accepted" on slide 8; the slide 7 "after" question; "credible" on slide 1; slide 14 question 1; OD-39 as "three standards or codes"; no false quote on slide 9; knowledge organisation moved to the appendix; CON-003 removed from the slide 12 card. None of these is repeated here.
* **Slide 10 facts:** 20 scenarios (five agents with 3 each, supervisor with 2, damp loop with 3); "none moves a request to an end-to-end agent"; foundation enriched first; the duties listed (Article 9, Awaab's Law awareness, Construction Act payment notices, Procurement Act 2023); eleven misattributed answers, nine re-run with the Data and Performance Lead and Finance, two labelled author hypotheses; Article 22 citations corrected to 22A to 22C; the grid positioned as a Phase 0 and Comparison 2 order, not a scaling decision. The takeaway matches steps 1 and 2 of the Sequencing section. All the other grid cells match the quadrant.
* **Other facts:** 39 non-merge commits from 10 to 27 Sep; 13 BRD commits from 11 to 26 Sep; dc6561a is the 11 Sep addendum commit; eight BRD commits precede 3db359c (slide 12 "after eight BRD revisions").
* **Story:** slide 10 is in the right place. It tests the verdict before the rigour and reflection slides, and its closing review-catches-errors beat leads naturally into slide 11. Fourteen main slides with a 1,899-word budget leave the mentor about 15 minutes in a 30-minute slot.
* **Voice:** all titles are at most 65 characters (slide 10 is 64, slide 9 is 65); first person; the evidence class appears in every source line (slide 10: "Scores are coarse judgements; role answers are hypotheses"); ASCII only (no non-ASCII characters found); no em dashes.
* **Boundaries:** OD-34 is labelled as proposed on slides 8 and 9 (and on 10 after SR4-05); slide 14 says there is no resident or staff evidence; no approval is claimed.
