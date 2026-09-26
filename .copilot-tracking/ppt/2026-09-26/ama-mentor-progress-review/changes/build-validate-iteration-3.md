<!-- markdownlint-disable-file -->

# Build and Validate Log: Iteration 3

## Inputs

* Log entries after the iteration 2 build (20:46, 26 Sep): the pilot measurement challenge, BRD 0.3.0 integration, the agent-led modernisation reframe (BRD 0.4.0) and the explainability and transparency review (BRD 0.5.0).
* `docs/reference/memory.md`: no change since 2026-09-25.
* Storytelling review: `research/subagents/storytelling-review-iteration-3.md` (Presentation Communications Strategist).

## Content Changes (first pass)

* Slide 3: BRD v0.5.0, twelve BRD revisions (git log --follow), six quality runs, 35 commits.
* Slide 6: twelve revisions. The notes now map the control plane to the digital foundation.
* Slide 8: rewritten to the current framing. The layers are now the digital foundation (deterministic), bounded agents and accountable people. The ask is now agent-led modernisation in one locality with existing teams and suppliers. "Agentic is an implementation option" and the delivery cell were removed.
* New slide 9: prove it (Comparison 1 and 2, dashboard versus frozen scorecard, RULE-024) and explain it (CON-003 fix, AC-079, FR-042 to FR-044, OD-39). The takeaway states OD-34 as a proposal.
* Slide 10: 12 BG, 44 FR, 85 AC, 9 NFR, 6 CON, 24 RULE; six runs, with four findings on v0.3.0 fixed and none since.
* Slide 14, question 1: reworded for the new framing.

## Strategist Recommendations Applied

* Slide 9: Article 22 fact corrected. The local text omits Article 22 and holds Articles 22A to 22D; CON-003 now cites 22A to 22C. The dashboard bullet now says the roles backed the intent, and quotes no phrase that is not in the source. OD-39 now reads "three standards or codes and ICO guidance".
* Slide 8: the 7-to-8 seam is bridged in the notes ("why is this agent-led?"), and the cause of the reframe is explained here. The scaling rule is labelled "(proposed)". The banner now says "resident-accepted".
* Slide 7: the "after" question now uses existing teams and "an agent beat the same workflow". The stale proposition note was replaced.
* Slides 1, 10 and 13: notes updated. Slide 13 question 1 now says "agent-led modernisation, not five end-to-end agents".
* Slide 11: the CON-003 clause was removed from "Sources that disagree", because it duplicated slide 9 and was not a source disagreement.
* Length (owner approved): knowledge organisation moved to slide 14 as an appendix, the chain is now slide 12 and the questions slide 13. The main speaker notes total 1,993 words across 13 slides; the appendix has 153.

## Not Applied

* Slide 6 on-slide "(now the digital foundation)": the change is in the notes, and the card keeps the dated 11 Sep quote.

## Validation

* `validate_deck.py`: 0 issues across 14 slides. `validate_geometry.py`: 0 issues.
* PowerPoint COM export of all 14 slides was reviewed visually. No overflow, clipping or wrapped title.

## Delivery

* Delivery copy: `docs/presentations/ama-mentor-progress-review.pptx`, identical hash to `slide-deck/ama-mentor-progress-review.pptx`.
* Why `docs/presentations/` was empty: the pipeline writes only to `slide-deck/`, and no delivery step was defined. The only earlier file, `proper-warm-cxo-initial-proposal.pptx`, was deleted in the working tree by the owner and the deletion was committed in df1de38. The owner confirmed the removal was deliberate. The broken index links now point to the mentor deck, and `.github/copilot-instructions.md` now defines `docs/presentations/` as the delivery location.
