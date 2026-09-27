<!-- markdownlint-disable-file -->

# Storytelling Review, Iteration 3: AMA Mentor Progress Review Deck (14 slides)

Scope: analysis only. No content.yaml or PPTX was edited. I reviewed all 14
content.yaml files (on-slide text and speaker notes), the rendered images for
slides 7, 8, 9 and 14, my iteration 1 review and the iteration 2 change log.
I checked the facts against the addendum (current and at commit 3db359c), the
BRD v0.5.0, pilot-measurement-challenge.md, agent-request-challenge.md, the
local UK GDPR snapshot, the BRD quality report (Runs 1 to 6), log.md and git
history.

## 1. Audience and Outcome Summary

| Item | Assessment |
| --- | --- |
| Audience | One AMA mentor, first session (Mentoring stage), 20 to 30 minutes, conversational |
| Desired outcome | The mentor follows the reframe, trusts the evidence and spends most of the time challenging the four decisions on slide 14 |
| Archetype (assumption) | Primary Scientist ("How do you know?"), secondary Therapist (coaching). Slides 8 and 14 should invite a Sergeant reading, because the Panel will read the deck that way |
| New risk since iteration 2 | The deck now has two pivots in one day (value challenge, then reframe to agent-led modernisation). Unless the seam is explained, a Scientist will read slide 7 ("not intelligence") and slide 8 ("agent-led") as a contradiction |

## 2. Verdict on the Iteration 3 Changes

What works:

* **The reframing arc is sound.** Five agents (slides 1 and 2), then the
  value challenge (7), then the digital foundation and bounded agents (8),
  then proof and explanation (9) is a logical sequence: what we build, then
  how we would know and how we would explain it. A Scientist mentor will ask
  "how would you prove it?" straight after slide 8, and slide 9 answers it.
* **Slide 8's new title** ("Agents for the messy work, rules for decisions we
  must explain") is the clearest one-line statement of the proposition in the
  deck, and it matches the addendum's "Where Agents Fit" section.
* **Slide 9 labels the OD-34 outcome as "Proposed"** and states the OD-39
  evidence gap. Both are right.
* **All counts on slides 3, 10 and 12 are correct** (see section 5).

What needs work:

1. **The 7-to-8 seam reads as a U-turn.** Slide 7 ends "The gap is shared
   records, not intelligence". Slide 8 then says "Agent-led modernisation".
   Nothing on either slide or in the notes says why the conclusion is
   agent-led after all. The BRD gives the bridge: agents take on
   "coordination, chasing, re-keying, reconciliation and evidence assembly
   while people keep decisions" (BRD Document Status, owner decision). The
   BRD Executive Summary also warns that this "does not establish that
   administration is the binding delivery constraint". Say both.
2. **The 8-to-9 seam runs backwards.** The slide 8 notes say "after the
   measurement challenge on the next slide, I reframed". The cause (the pilot
   bundled a delivery cell, ring-fenced capacity and agents, so it could not
   attribute benefit) is only explained on slide 9. The "delivery cell" also
   appears for the first time in the slide 8 notes ("The dedicated delivery
   cell is gone"), and the mentor has never heard of it. Move the cause to
   slide 8 and let slide 9 refer back to it.
3. **Slide 9 is in the right place, but its notes contradict the order.**
   "Two further challenges on 26 September changed the proposal after the
   quality review" is true in time, but the quality review is the next slide.
   Also, the measurement challenge came before the reframe and the
   transparency review came after it. The notes should say so.
4. **The deck is too long for a mentoring conversation.** The speaker notes
   total 2,888 words, about 20.6 minutes at 140 words a minute. That leaves 0
   to 10 minutes of a 20 to 30 minute slot for the mentor. Slide 9 alone is
   288 words (2.1 minutes). Target at most 2,000 words (about 14 minutes)
   and 13 main slides.
5. **Some notes are stale.** Slide 10 opens "The last step so far was a
   formal BRD quality review". Slide 1's agenda omits the slide 9 challenges.
   Slide 7 claims the "after" question paraphrases the addendum's strategic
   proposition, but that proposition is now agent-led modernisation, not the
   "governed retrofit delivery service supported by a portfolio control plane"
   it paraphrased (addendum at 3db359c).

## 3. Stale Terminology Check

| Term | Where it appears | Assessment |
| --- | --- | --- |
| "control plane" | Slide 3 notes, slide 6 on-slide and notes, slide 7 notes, slide 8 notes | Historical use is correct: the 11 Sep addendum used it. The rename is explained in the slide 6, 7 and 8 notes, but the first mention (slide 3 notes) and the only on-slide mention (slide 6) have no rename. Add "(now the digital foundation)" on slide 6 |
| "delivery cell" | Slide 8 notes, slide 9 notes | Historically correct (pilot-measurement-challenge.md, Summary reason 2), but it is never introduced. See change 2 |
| "bounded AI" | Slide 7 on-slide ("where does bounded AI beat a checklist?") and notes | It does not contradict the sources: the BRD Executive Summary and the addendum still say "bounded AI". It is inconsistent with the deck's later phrase, "beats the same workflow without it" (slides 8, 9 and 14). Align slide 7 so one phrase runs through the deck |
| "AI" in slide 7 column 4 | "AI reconciles and explains", "AI drafts" and similar | Acceptable. Optional: change to "agent" for consistency with slide 8 |
| "small team" | Slide 7 "after" question | It is a case fact (BRD Executive Summary), but the reframe says "existing teams". Use "existing teams" |

## 4. Hypothesis or Proposal Stated as Fact

| Slide | Text | Status in source | Fix |
| --- | --- | --- | --- |
| 8 | "Each agent capability scales only if it beats the same workflow without it" | OD-34, a proposed owner resolution pending the Sponsor, Executive Director of Assets and Finance (BRD OD-34; pilot-measurement-challenge.md, Owner Decision) | Add "(proposed)" |
| 8 | "Agents earn the right to scale only through safe, accepted, evidence-complete handovers" | Addendum proposition: "safe, resident-accepted and evidence-complete handovers" | Restore "resident-accepted". It preserves resident agency |
| 1 notes | "two weeks of evidence says the value is real" | Addendum Executive Assessment: "The case for improving retrofit delivery is credible". The evidence is role-agent hypotheses and sector benchmarks | "credible" |
| 9 | "All eight roles rejected \"a dashboard to measure acceleration\"" | The quote marks imply a verbatim phrase that is not in the source. The source says all eight roles "accepted the intent" and "rejected the proposal as stated" | Paraphrase without quote marks, and include "backed the intent" |
| 8 notes | Agents take on "coordination, chasing, re-keying..." | Owner framing. The BRD says this "does not establish that administration is the binding delivery constraint" | Add the caveat in one sentence |

## 5. Fact Verification

| Claim (slide) | Result | Source |
| --- | --- | --- |
| BRD v0.5.0 (3, 8, 9, 10) | Correct | BRD frontmatter `version: "0.5.0"` |
| Twelve BRD revisions (3, 6) | Correct as commits: 12 commits touch the BRD, 008bf1c (11 Sep) to 97380bb (26 Sep) | `git log -- docs/brds/agentic-retrofit-programme-brd.md` |
| "After eight BRD revisions" (11) | Correct: 8 BRD commits precede 3db359c | git log |
| 35 commits (3, 12) | Correct today (e32ea9c, 10 Sep, to 97380bb). It becomes 36 as soon as the deck is committed | git log |
| 12 BG, 44 FR, 85 AC, 9 NFR, 6 CON, 24 RULE (10) | Correct: unique IDs BG-001 to 012, FR-001 to 044, AC-001 to 085, NFR-001 to 009, CON-001 to 006, RULE-001 to 024 | BRD |
| Six runs; four new findings on v0.3.0, all fixed; none since (3, 10) | Correct: Run 3 records req-qual-011 to 014 corrected; Runs 4, 5 and 6 "No new findings" | quality-report.yml headers |
| Comparison 1 and Comparison 2 (9) | Correct | pilot-measurement-challenge.md, Owner Decision; BRD RULE-019 |
| About 50 handovers cannot prove a 20% gain (9) | Correct, but the source says "about 50 accepted handovers in 6 to 9 months" | pilot-measurement-challenge.md, Summary reason 5 |
| RULE-024 guardrail breach pauses work (9) | Correct | BRD RULE-024 (AC-078) |
| AC-079 transparency gate before live processing (9) | Correct (under RULE-022) | BRD line 928 |
| FR-042 reason codes, FR-043 register and Board report, FR-044 provenance (9) | Correct | BRD FR-042 to FR-044 |
| OD-39: four sources not held locally (9) | Correct: three standards or codes plus ICO guidance. "Four standards and ICO guidance" on the slide implies five items | BRD OD-39; log |
| **"the local text uses Articles 22A to 22C" (9 on-slide and notes)** | **Wrong.** The local text omits Article 22 and contains Articles 22A to 22D. CON-003 now cites 22A to 22C | log.md, 26 Sep transparency entry; uk-gdpr-current-text.md, Article 22 (omitted) and Articles 22A to 22D headings |
| Slide 11 notes "22A to 22D" | Correct, but inconsistent with slide 9 | same |
| Chain on slide 13 (FR-026, AC-039, CON-005, a72f231, 3db359c, c3e423a) | Correct and unchanged in v0.5.0 | BRD; git |
| OD-31 (L4 quality flags) and OD-32 (L3 booking) still open (11, 14) | Correct | BRD OD-31, OD-32 |
| Addendum decision "capped pilot, not a five-agent rollout" (13) | Still correct after the reframe | addendum, Recommended Executive Decision |

## 6. Story and Length

**Arc as it now reads:** hook (1) > gap (2) > map (3) > discovery (4, 5) >
rising action (6) > turning point (7) > resolution (8) > proof and
explanation (9) > rigour (10) > reflection (11) > system (12, 13) > ask (14).
The arc holds once the two seams (7 to 8, 8 to 9) are bridged in the notes.

**Is slide 9 in the right place?** Yes. Keep it after 8. Do not split it: a
fifteenth slide makes the length problem worse. Do not move it before 8:
Comparison 1 and 2 only make sense after the reframe. Fix the order in the
notes instead (change 2).

**Is 14 slides too long?** Yes, for a conversation. Recommended cuts:

* Move slide 12 (knowledge organisation) to an appendix. Slide 13 proves the
  same point with a real chain. Fold one sentence of slide 12 into the slide
  13 notes. This saves about 1.1 minutes.
* Trim the notes on slides 4, 7, 8 and 9 by about a third. Move the GBP 66.7m
  co-funding paragraph (slide 4) and the ISO 25010 detail (slide 10) to Q&A.
  Slide 9 notes should be 170 words at most.
* Keep slide 6, but deliver it in 45 seconds.
* Target 13 slides and at most 2,000 words of notes, so the mentor gets 10 to
  15 minutes.

**Does slide 14 question 1 still make sense?** Mostly. However, "the
workflow" is vague, and the risk has changed. The proposal is now agent-led,
so the panel risk is no longer "refusing" the brief. It is whether agent
capabilities inside the existing model, with no L4 autonomy and no
supervision agent, count as the five agents the brief asked for. The notes
still say "or as refusing it", which matches the pre-reframe framing.

## 7. Delivery Guidance for the Moments That Matter

| Moment | Guidance |
| --- | --- |
| Slide 7 to 8 transition | This is now the hinge. Pause after the red banner, then ask the question aloud: "So if the gap isn't intelligence, why is this agent-led?" Open palm towards slide 8. This turns a possible contradiction into the reveal |
| Slide 8 | Point bottom to top (foundation, agents, people). Use Sergeant language on the ask box: "The ask changes from X to Y." Say "proposed" when you reach OD-34 |
| Slide 9 | Two halves, two gestures: left hand "prove it", right hand "explain it". Name your own CON-003 error plainly and neutrally. Owning it builds more Scientist trust than the fix itself |
| Slide 14 | Stop, sit back and let the mentor choose. Do not summarise |

## 8. Prioritised Changes (max 10)

1. **Slide 9: fix the Article 22 fact.**
   * On-slide, current: "Fixed my own citation: CON-003 cited UK GDPR Article 22; the local text uses Articles 22A to 22C"
   * Proposed: "Fixed my own citation: CON-003 cited UK GDPR Article 22, which the local text omits; it now cites Articles 22A to 22C"
   * Notes, current: "CON-003 cited UK GDPR Article 22, but the local consolidated text uses Articles 22A to 22C."
   * Proposed: "CON-003 cited UK GDPR Article 22, but the local consolidated text omits it and uses Articles 22A to 22D. CON-003 now cites Articles 22A to 22C and maps human review to the four Article 22C(2) safeguards."
2. **Slide 8 notes: bridge the 7-to-8 seam and move the cause of the reframe here.**
   * Current: "This slide has changed since the first draft. The role challenge confirmed the shared records I proposed on 11 September. Later on 26 September, after the measurement challenge on the next slide, I reframed the proposal as an agent-led modernisation of the existing retrofit model. Existing teams, suppliers and systems stay. Agents take on the manual coordination, chasing, re-keying, reconciliation and evidence assembly. The dedicated delivery cell is gone, and what I called the control plane is now the digital foundation."
   * Proposed: "So if the gap is shared records, not intelligence, why is this agent-led? Because the records do not fill themselves. What swamps a small team today is coordination, chasing, re-keying, reconciliation and evidence assembly, and that unstructured work is where agents help. Later on 26 September, a challenge to my own measurement plan showed the pilot bundled three changes: a new delivery cell, ring-fenced supplier capacity and agents, so it could never tell the Board which one worked. So I reframed it as agent-led modernisation of the existing retrofit model. Existing teams, suppliers and systems stay, the cell and the ring-fence are gone, and what I called the control plane is now the digital foundation. Whether coordination really is the binding constraint is still a Phase 0 question."
3. **Slide 9 notes: fix the order and remove the duplicate.**
   * Current: "Two further challenges on 26 September changed the proposal after the quality review."
   * Proposed: "Two challenges asked whether I could prove the value and whether I could explain it. The first came before the reframe and caused it; the second came after."
   * Current: "The pilot mixed a delivery cell, ring-fenced capacity and agents, so it could not tell the Board which one worked."
   * Proposed: "And, as you saw, it bundled three changes."
4. **Slide 8: label the proposal and restore resident acceptance.**
   * Current: "Each agent capability scales only if it beats the same workflow without it"
   * Proposed: "Each agent capability scales only if it beats the same workflow without it (proposed)"
   * Current banner: "Agents earn the right to scale only through safe, accepted, evidence-complete handovers"
   * Proposed: "Agents earn the right to scale only through safe, resident-accepted, evidence-complete handovers"
5. **Slide 7: align the "after" question and fix the stale note.**
   * Current: "What shared records and gates let a small team deliver more safe, accepted, grant-claimable homes, and where does bounded AI beat a checklist?"
   * Proposed: "What shared records and gates let existing teams deliver more safe, accepted, grant-claimable homes, and where does an agent beat the same workflow?"
   * Notes, current: "The \"after\" question at the top paraphrases the addendum's strategic proposition."
   * Proposed: "The \"after\" question is how I phrase it now. On 26 September the addendum still called agents \"an implementation option\"; later that day it became agent-led modernisation, which is the next slide."
6. **Slide 10 notes: remove "last step".**
   * Current: "The last step so far was a formal BRD quality review. The first run failed hard:"
   * Proposed: "Alongside all of this ran a formal BRD quality review, re-run after every change. The first run failed hard:"
7. **Slide 1 notes: soften the claim and include slide 9 in the agenda.**
   * Current: "two weeks of evidence says the value is real, but end-to-end agents are not the way to get it."
   * Proposed: "two weeks of evidence says the value is credible, but end-to-end agents are not the way to get it."
   * Current: "I will cover five strands in order: research, role agents, BRD iterations, a design thinking challenge of the five agents, and a BRD quality review. Then the challenges, how the repository holds the evidence, and my questions for you."
   * Proposed: "I will cover five strands: research, role agents, BRD iterations, a design thinking challenge of the five agents and a BRD quality review, plus two later challenges on how to prove and explain the value. Then lessons, one traceability chain, and my questions for you."
8. **Slide 14, question 1: name the current risk.**
   * Current: "Will the panel read \"agents only where they beat the workflow\" as answering the brief?"
   * Proposed: "Will the panel read agent-led modernisation, not five end-to-end agents, as answering the brief?"
   * Notes, current: "as answering the brief, or as refusing it?"
   * Proposed: "as answering the brief, or as stepping back from the five agents it asked for?"
9. **Length: 13 slides and about 14 minutes.**
   * Move slide 12 to an appendix, and trim the notes to at most 2,000 words.
   * Slide 13 notes, current: "This slide is the reason for all the structure."
   * Proposed: "This slide is the reason for all the structure: immutable dated sources, cited syntheses, an index and an append-only log, on Karpathy's LLM Wiki pattern."
10. **Slide 9 bullet 1: remove the false quote and keep the roles' fairness.**
    * Current: "All eight roles rejected \"a dashboard to measure acceleration\": speed is not the benefit, and about 50 handovers cannot prove a 20% gain"
    * Proposed: "All eight roles backed the intent but rejected my acceleration dashboard: speed is not the benefit, and about 50 handovers in 6 to 9 months cannot prove a 20% gain"

Lower priority (not in the top 10):

* **Slide 6:** "Addendum proposes a control plane: \"agentic is an implementation option\"" becomes "Addendum proposes a control plane (now the digital foundation): \"agentic is an implementation option\"", if it fits. Otherwise, in the slide 3 notes, "tested an early control plane hypothesis" becomes "tested my early control plane hypothesis, now called the digital foundation,".
* **Slide 9:** "Gap: four standards and ICO guidance are not held locally (OD-39)" becomes "Gap: three standards or codes and ICO guidance are not held locally (OD-39)".
* **Slide 11:** the CON-003 error sits under "Sources that disagree", but it is my error, not a source disagreement, and it repeats slide 9. Either retitle the card "Sources that disagree, and my own errors" or drop the CON-003 clause.
* **Slide 12 (if kept):** "35 commits" becomes 36 once the deck is committed. Recount on the day, or use "35 commits to 26 Sep".

## 9. Additional Q&A to Prepare

* **"Slide 7 says the gap isn't intelligence, so why is it agent-led?"** The
  gap is shared records. Agents do the unstructured labour that fills and
  maintains them, and rules make every explainable decision. Whether that
  labour is the binding constraint is a Phase 0 test.
* **"Twelve revisions, but only version 0.5.0?"** Twelve commits touched the
  BRD. Semantic versioning started at the canonical relabel (0.2.0) on
  26 Sep.
* **"Who approved the reframe?"** It is the owner's framing decision. OD-34
  is still a proposal pending the Sponsor, the Executive Director of Assets
  and Finance. No real stakeholder has approved anything.
* **"Can 50 handovers prove anything?"** Not a 20% gain. Comparison 2
  (task-level, per capability) gives faster evidence. Comparison 1 reports an
  interval estimate until Phase 0 variance sets the minimum detectable
  effect.

## 10. Evidence Gaps, Risks and Next Decision

* **Factual error:** slide 9's Article 22A to 22C statement (change 1).
* **Proposal stated as fact:** slide 8's scaling rule (change 4).
* **No resident or staff evidence** yet. The deck says so on slide 14. Keep it.
* **OD-39 sources** are not held locally. Do not cite ICO explainability
  guidance as checked.
* **Next decision for the owner:** accept the cut of slide 12 to an appendix
  and a 2,000-word notes budget. Without it, the mentor gets under 10
  minutes, and the four questions are the point of the session.
