<!-- markdownlint-disable-file -->

# Build and Validate Log: Iteration 2

## Inputs

* Storytelling review: `research/subagents/storytelling-review.md` (AMA Presentation Communications Strategist).
* Owner decision on 2026-09-26: tell the turning point as its real origin. The control plane hypothesis appears in the 11 Sep addendum (commit dc6561a). The 26 Sep role challenge tested it for each agent. The priming caveat is stated on the slide.

## Changes Applied (all 8 prioritised recommendations)

* Slide 1: the subtitle line now states the ask ("four decisions"), and the notes open with the ask.
* Slide 2: new title. "Names the solution first" is now shown as the main gap.
* Slide 3: new title ("Five loops, not a line"). Card 4 is marked as the turning point. Each card now has an output line. Commit count corrected to 32.
* Slide 4: new title ("corrected two claims"). The number is labelled "c. 15,600 homes" under "estimate". "Owner-confirmed" added. Added a corrections band: GBP 40m is an opportunity, not an award; EPC C is final SRS MEES policy, not a consultation, and not yet evidenced as commenced law. Awaab's Law Phase 2 is shown as "planned".
* Slide 5: new title. The role chips were shrunk. The banner was replaced by one real exchange (Grant and Funding): the question, the regulatory fact (formula allocation in GM and WM), what is unknown, and the effect on FR-027.
* Slide 6: rewritten as rising action from 11 to 26 Sep, and the duplicate loop chevrons were removed.
* Slide 7: new title. Added the before and after framing. The priming caveat is in the footer and the notes. The notes now give the honest origin.
* Slide 8: "shadow-tested" corrected to "candidates for shadow testing". The ask is now addressed to the board, with a traceability bullet. The notes now give the honest origin.
* Slide 9: new title. The caption now reads "ID traceability". Added the relabel counts (68 BR, 12 OBJ, verified at 3db359c), the extraction examples (FR-022 and RULE-023; CON-004 sent to Legal) and the Given/When/Then advisory.
* Slide 10: three challenges plus three lessons: start the log on day one, use canonical IDs from the start, and run the value challenge earlier and blind.
* Slide 11: the commit claim was softened to "32 commits; most messages say what changed and why".
* Slide 12: replaced with one real chain: the addendum decision, the Stock Prioritisation challenge, FR-026 / AC-039 / CON-005, the WH:SHF annex (Page 3 footnote 1) and the log with commits.
* Slide 13: new title, questions on the left, and a sharper first question. Added "where did the story lose you?", a note that there is no real resident or staff evidence, and a closing band.
* Layout: card paragraphs now default to left alignment.

## Facts Verified Before Use

* dc6561a (11 Sep) addendum text: "'Agentic' is an implementation option", "portfolio control plane".
* FR-026 = BR-059, AC-039; CON-005 cites WH:SHF annex Page 3 footnote 1; FR-027 = BR-060 (funding route).
* agent-request-challenge.md: "Eligibility is a rules question"; formula allocation through integrated settlements; "a pack with no flags ... read as proof of quality".
* log.md: entries before 2026-09-25 were reconstructed from Git history.
* 8 BRD commits precede 3db359c; 32 commits in total.

## Validation

* `validate_deck.py`: 0 issues. `validate_geometry.py`: 0 issues, after fixing adjacent-gap warnings on slides 4, 5 and 6.
* Visual review of all 13 PowerPoint COM exports: no overflow, overlap or clipped text.
* The vision validator (`validate_slides.py`) was not run. Images were reviewed manually.

## Not Changed (flagged to owner)

* Repo inconsistency noted by the strategist: addendum line 32 says the 2030 standard "remains a proposal", while line 49 and the log say it is final SRS MEES policy. This is outside the deck scope and was left for the owner.
