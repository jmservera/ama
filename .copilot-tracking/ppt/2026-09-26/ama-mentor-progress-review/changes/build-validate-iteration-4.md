<!-- markdownlint-disable-file -->
# Build and Validate: Iteration 4

* Date: 2026-09-27
* Trigger: the owner asked for another review of the deck against the latest log and memory, with the mentor-deck process captured as the `ama-mentor-deck` skill
* Branch: `claude/study-agent-challenge-review`, after merge commit baef324 brought in `Review-progress-challenge` (iteration 3, BRD v0.5.0)

## Delta Covered

| Project change since iteration 3 | Deck treatment |
| --- | --- |
| Agent What-If Study: 20 scenarios and a value-versus-complexity grid (27 Sep) | New slide 10 |
| Post-merge review of the study: Article 22 citations corrected to Articles 22A to 22C; nine answers re-run and two relabelled as author hypotheses; grid positioned as a Comparison 2 test order under proposed OD-34 | Slide 10 findings panel and notes; slide 12 lesson on propagating corrections |
| Commit counts: 39 non-merge commits from 10 to 27 Sep; 13 BRD commits | Slides 1, 3, 6 and 15 |
| Memory: no change affecting the deck | None |

## Edits

* Opened a slot for the new slide with `deck_yaml.py insert --at 10`. The old slides 10 to 14 are now 11 to 15.
* Slide 10: a 3x3 grid table covering all 20 scenarios, a legend, a findings panel, a takeaway banner and a source line. The table height was reduced to 1.6 in so the header row fits its text.
* Slide 1: the subtitle date range now runs to 27 September; the agenda sentence was shortened.
* Slide 3: the card and notes now say thirteen BRD revisions; the source says 39 commits.
* Slide 15: the Git history card now says 39 commits, 10 to 27 Sep.

## Storytelling Review Decisions

Review: [storytelling-review-iteration-4.md](../research/subagents/storytelling-review-iteration-4.md)

| Finding | Decision | Reason |
| --- | --- | --- |
| SR4-01: slide 3 card says twelve revisions | Accepted | Confirmed: `git log --no-merges` shows 13 BRD commits |
| SR4-02: notes over budget | Accepted | Main notes cut from 2,158 to 1,921 words |
| SR4-03: SP1 missing from the grid | Accepted | Confirmed: the study's Scoring Table puts SP1 at M/M |
| SR4-04: white cells not in the legend | Accepted | Matches the study's "middle band, do opportunistically" |
| SR4-05: OD-34 stated as settled | Accepted | OD-34 is a proposed resolution |
| SR4-06: "each put to the role agents" | Accepted | Two answers have no role-agent anchor |
| SR4-07: appendix count stale | Accepted | Recounted before publishing: 39 non-merge commits |
| SR4-08: agenda sentence too long | Accepted | |
| SR4-09: slide 7 repeats the table and slide 8 | Accepted | Kept the quality example, introduced with "For example" |
| SR4-10: Q&A preparation | Accepted as a speaker card | See below |
| SR4-11: lesson on propagating corrections | Accepted | Added to the slide 12 notes, which now list four things |
| Notes budget plan, including both optional cuts | Accepted | |

## Speaker Q&A Card

* Did the what-if study change no verdict at all? The headline verdict is unchanged. QV2 and QV3 are slightly stronger, but they remain raise-only evidence.
* Were the role answers given before the reframe? Most were, and they have not been re-run. The nine re-runs used BRD v0.5.0.
* Were the regulatory citations checked? Only against the local snapshots, not against the official sources online.
* What does more grant money mean for our own spend? Grants need co-funding, so more grant means more of our own spend. The addendum illustrates about GBP 66.7 million of provider funding, as an estimate. This answer was moved from the slide 4 notes.

## Validation

| Check | Result |
| --- | --- |
| `build_deck.py` | 15 slides |
| `validate_deck.py` | 0 issues across 15 slides |
| `validate_geometry.py` | 0 issues across 15 slides |
| Slide images | Exported with `Export-SlideImages.ps1`. Slides 3, 10 and 15 were viewed after the final build |
| Main notes | 1,921 words, about 13.7 minutes at 140 words per minute; the appendix has 153 words |

## Delivery

* Published to `docs/presentations/ama-mentor-progress-review.pptx`
* SHA-256 `3D9C8389FFF89CF3D4EF54810C8C185D5381B669AF36488D39F40DEC4583F051`, identical to the build in `slide-deck/`
