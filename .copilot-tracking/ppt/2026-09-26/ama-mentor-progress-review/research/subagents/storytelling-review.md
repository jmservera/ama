<!-- markdownlint-disable-file -->

# Storytelling Review: AMA Mentor Progress Review Deck (13 slides)

Scope: analysis only. No content.yaml or PPTX was edited. I reviewed all 13
rendered slides, every content.yaml and its speaker notes, and the deck
research notes. I checked facts against the original case, the addendum, the
agent request challenge, log.md, memory.md, the BRD, the quality report and
git history.

## 1. Audience and Outcome Summary

| Item | Assessment |
| --- | --- |
| Audience | One AMA mentor, first mentoring session (stage 3 of Rubric, Masterclasses, Mentoring, Capstone, Panel). One-to-one, 20 to 30 minutes, conversational |
| Desired outcome | The mentor understands the case and the reframing, trusts the method, and gives specific challenge on four open decisions |
| Likely archetype (assumption, confirm if you know the mentor) | Primary **Scientist** (architect-coach: "How do you know?"). Secondary **Therapist** (coaching relationship: "What did you learn?"). Invite the mentor to play **Sergeant** on slides 8 and 13, because the Panel and CxO audiences will |
| What builds trust | Visible provenance, labelled estimates, admitting what failed, and a clear ask |
| What reduces trust | Overclaims the mentor can spot in the repo, a turning point that looks circular, and 13 slides of "what I did" with no "what I learned" |

## 2. Overall Narrative Arc

### What works

* **The title slide states the story in one line.** "From 'build five
  agents' to 'what value do they really need?'" is a strong hook.
* **The situation and complication on slide 2 are clear.** The request and
  its gaps sit side by side, with one working question.
* **The resolution on slides 7 and 8 is strong.** The table reading each
  request as expected value, the red verdict banner and the three-layer stack
  are the best slides in the deck.
* **Evidence honesty runs through the deck.** It shows up in source footers,
  "provisional", "still fail, on purpose" and the four evidence classes. A
  Scientist mentor will value this.
* **The close asks for something specific.** Slide 13's four questions fit a
  mentoring session.

### What weakens the story

1. **The turning point arrives late and lands softly.** The pivot is on slide
   7, after three process slides (3, 5 and 6) that describe activity rather
   than tension. The mentor spends about 8 minutes waiting for the "so what".
   The slide 7 title ("Design thinking read each agent request as expected
   value") describes a method, not the finding. The finding is only in the
   red banner.
2. **The repo tells a more honest, and better, origin story.** The addendum
   already said "'Agentic' is an implementation option, not the business
   outcome" and proposed a portfolio control plane on **11 Sep**
   (commit dc6561a). The BRD gained a "Cross-Functional Challenge to the
   Five-Agent Request" on **19 Sep** (commit 6bbb392). The 26 Sep session
   turned that early hypothesis into evidence for each agent: unanimous role
   verdicts, five bounded AI candidates with stop criteria, and BR-059 to
   BR-068. The slide 8 notes say "Once the real problem was clear, I rewrote
   what we actually need to build". That implies the control plane came out
   of design thinking. A mentor who opens the addendum history will see
   otherwise. The honest arc is stronger: "My first instinct on day one was a
   control plane. I spent two weeks trying to prove myself wrong. On 26 Sep
   reading each 'owns end-to-end' line as expected value turned an opinion
   into evidence."
3. **The obvious objection to the turning point is not addressed.** The role
   agents answered from the case, the **addendum** and the BRD
   (agent-request-challenge.md, Limitations). The addendum already proposed
   a control plane, so "all eight roles agree" is open to a charge of priming
   or circularity. A Scientist mentor will ask this first. Name it before
   they do.
4. **"Design thinking" is not evidenced in the repo.** No file in `docs/`
   uses the term. The log records the session as "Challenge the requested
   agents with the role agents". Be ready to say which method you used (a
   reframe of each request and a check against the value it implies, run
   with role agents and no real users), or label it that way on slide 7.
5. **There is no "what I learned" or "what I would do differently" beat.**
   Slide 10 lists challenges, but a mentor wants reflection. The repo gives
   honest material for this (see section 3).
6. **The ask comes only at the end.** In a mentoring session, say on slide 1
   what feedback you want, so the mentor listens with those questions in
   mind.
7. **The middle repeats itself.** Slide 6's bottom loop (Research, Ask role
   agents, Rewrite requirements, Log) repeats slide 3's banner. Slides 11 and
   12 both explain the repo. Both pairs can stay only if each slide does a
   different job (see section 3).
8. **Timing is tight.** At 13 slides and about 1.3 minutes each, the talk runs
   about 17 minutes. That leaves 5 to 13 minutes of the 20 to 30 for
   conversation. Treat slide 11 as a 45-second "glance" slide and keep the
   rest tight.

### Recommended arc (still 13 slides, no new slide needed)

| # | Beat | Slide job |
| --- | --- | --- |
| 1 | Hook and ask | Story in one line, plus "four decisions I want your challenge on" |
| 2 | Situation and complication | The brief names the solution but not the problem |
| 3 | Map | Five loops, not a line |
| 4 | Discovery | Research filled gaps and corrected two claims in the brief |
| 5 | Method | Role agents, with one concrete exchange |
| 6 | Rising action | The case against five agents built up from 11 to 26 Sep |
| 7 | **Turning point** | Each request states a value; none needs an end-to-end agent |
| 8 | Resolution | Control plane first, then bounded AI; the ask changes |
| 9 | Rigour | Relabelling fixed traceability; the gate still fails, on purpose |
| 10 | Reflection | Challenges and what I would do differently |
| 11 | System | The repo is the project memory (glance) |
| 12 | Proof | One real chain, walked end to end |
| 13 | Ask | Four decisions for your challenge |

## 3. Slide-by-Slide Recommendations

Title rules: 65 characters or fewer, plain ASCII, no em dashes. Character
counts are shown in brackets.

### Slide 1: Title. KEEP, small addition

* Keep the headline. It is the thesis.
* Add one line under the strands, or replace the strands line: "Today: four
  decisions I would value your challenge on". The five strands repeat slide 3.
* Notes: open with the ask, not the agenda. For example: "I want to leave
  with your view on four decisions, especially whether reframing the brief
  will read as refusing it."

### Slide 2: The request and its gaps. KEEP, retitle, sharpen

* New title: **The case names five agents but not the problem they solve**
  [57]
* Make "The brief already names the solution" a visible gap. It is currently
  buried in slide 10, but it is the real complication. Replace or merge the
  fifth gap bullet with: "The brief names the solution before the problem;
  each agent has one 'owns end-to-end' line".
* The working question in the banner is good. Keep it.

### Slide 3: Five loops. KEEP, retitle to match the notes

* New title: **Five loops, not a line: each finding sent me back to research**
  [61]
* The current title ("each one feeding the next") and the linear chevrons
  contradict the notes ("not a straight line"). Add a return arrow or a small
  "back to research" label. If the shapes cannot change, the title alone
  fixes the message.
* Make the fourth card (Design thinking) the visual hinge. It is already
  red. Add "turning point" to its date line: "26 SEP | TURNING POINT".

### Slide 4: Research. KEEP, retitle, add the "so what"

* New title: **Research filled three gaps and corrected two claims in the
  brief** [64]
* The two corrections, both supported by the repo:
  * The brief says "captures GBP 40 million of available grants". Research
    shows it is an opportunity, not an award (addendum, recommended
    decision).
  * The brief calls EPC C by 2030 "a consultation proposal". The local
    snapshot shows the final SRS MEES policy position from 1 April 2026, not
    yet evidenced as commenced law (log 2026-09-25 correction; addendum).
* Put the estimate label on the big number itself: "c. 15,600 homes (est.)".
  At present only the small header says "provisional".
* Change "confirmed not-for-profit on 26 Sep" to "owner-confirmed
  not-for-profit, 26 Sep". That matches the addendum and company profile
  wording.
* Notes: add the implication in one sentence. "Grants are capped and need
  co-funding, so more grant means more of our own spend. The addendum
  illustration is about GBP 66.7m provider funding against a GBP 40m
  opportunity, as an estimate. Grant capture cannot pay for the technology
  on its own."

### Slide 5: Role agents. KEEP, retitle, add one concrete exchange

* New title: **Eight role agents stood in for the company I cannot
  interview** [61]
* The eight name boxes use half the slide and carry little information.
  Shrink them to one line of role names, or keep them and replace the banner
  with **one real exchange** labelled by evidence class. A good example
  from agent-request-challenge.md (Grant and Funding, Challenge) follows. The
  question is my paraphrase:
  * Question to the Finance role: "Would a grant-drafting agent add value?"
  * Answer, regulatory fact (local snapshot): in Greater Manchester and the
    West Midlands, WH:SHF Wave 3 is allocated by formula through integrated
    settlements, not by competitive bid.
  * Unknown: whether Proper North Homes operates in either area.
  * Effect: the value of drafting depends on the funding route, so this
    became a BRD sponsor question and part of FR-026 and FR-027.
* This shows the labelling rule working and a role answer changing a design
  decision. That is more persuasive than listing the rules.
* Keep the "question that would change each answer most" idea in the notes.

### Slide 6: BRD iterations. REWRITE as rising action (or cut if time is short)

* New title: **The case against five agents built up across two weeks** [54]
* The slide currently repeats slide 3. Give it a new job: show that the doubt
  grew before the turning point. Relabel the timeline with facts the repo
  supports:
  * 11 SEP: addendum proposes a control plane; "agentic is an implementation
    option"
  * 19 SEP: cross-functional challenge to the five-agent request added to
    the BRD; WH:SHF Wave 3 annex
  * 20 SEP: regulatory context; TypeSafe review of open decisions
  * 25 SEP: modelled customer profile; knowledge base restructure
  * 26 SEP: role challenge of each agent; BR-059 to BR-068; relabel
* Drop the bottom four-chevron loop, or shrink it to one caption line: "Each
  pass: research, ask the roles, rewrite, log". It duplicates slide 3.
* Keep "ten revisions" in the notes (git confirms 10 commits touching the
  BRD).
* If you need time back, cut this slide and add "10 BRD revisions" to slide
  3, card 3.

### Slide 7: Design thinking challenge. REWRITE: this is the turning point

* New title: **Each request states a value; none needs an end-to-end agent**
  [59]
* Add a before and after framing line in place of the current green subhead
  (the missing beat):
  * Before: "How do we build five agents to double delivery?"
  * After: "What shared records and gates would let a small team deliver more
    safe, accepted, grant-claimable homes, and where does bounded AI beat a
    checklist?"
  * The after line paraphrases the addendum's strategic proposition. Say so
    in the notes.
* Footer: add the priming caveat: "Roles read the case, addendum and BRD;
  verdicts are sector-informed hypotheses, not validation."
* Delivery: pause after the red banner. Walk one row, not five. Quality
  Verification is the most memorable: "every role said the real risk is the
  reverse: a pack with no flags gets read as proof of quality."

### Slide 8: What we really build. KEEP title, fix one overclaim

* Keep: **What we really need: a control plane first, then bounded AI** [59]
* **Fix the overclaim.** "Five shadow-tested candidates" is not supported.
  They are candidates for Phase 1 shadow testing (agent-request-challenge.md,
  Recurring Bounded AI Candidates). Change it to "Five candidates for shadow
  testing".
* Add "to the board" after "The ask changes", so the audience for the ask is
  explicit.
* Fix the notes sequencing (see section 4).

### Slide 9: BRD quality review. KEEP, retitle, reframe the 0% to 100% visual

* New title: **Relabelling fixed traceability; the gate still fails on
  targets** [63]
* The current title ("made the requirements testable") conflicts with the
  FAIL. The log records "FAIL, Define exit blocked".
* The red "0%" reads as if the requirements were missing. The 0% was an
  identifier-format artefact: legacy BR and OBJ IDs could not be traced.
  Relabel the caption to "ID traceability, FR-to-AC and FR-to-BG".
* Add a before line: "68 BR and 12 OBJ rows relabelled; four compound rows
  split; no meaning changed". The counts come from the BRD at 3db359c and
  the log.
* Add a concrete example of what the review extracted. For example: CON-004
  was flagged for Legal because its source is outside the local corpus, and
  FR-022 was split into FR-022 and RULE-023 (quality report dispositions).
  This supports your goal of "extracting more FR, NFR and objectives"
  without overstating it.

### Slide 10: Challenges. REWRITE to three challenges and three lessons

* New title: **Keeping evidence honest was hard; here is what I would
  change** [61]
* Keep three challenges: "No company data", "Agents that sound certain" (add
  "and share my framing") and "Sources that disagree". "Regulation that
  moves" and "Too much material" can go to the notes. "A brief that names
  the solution" moves to slide 2.
* Add three "what I would do differently" cards, all grounded in the repo:
  * **Start the log on day one.** Entries before 25 Sep were reconstructed
    from Git history (log.md, Conventions).
  * **Use canonical requirement IDs from the first draft.** The first
    quality run scored 0% only because of legacy IDs, and relabelling cost a
    full pass.
  * **Run the value challenge earlier, and blind.** It came after nine BRD
    revisions, and the roles could read my addendum. Next time, run one
    pass without the addendum to test for priming.
* Change "Awaab's Law Phase 2 starts 30 Nov 2026" to "planned from 30 Nov
  2026". The implementing instrument is not in the local corpus
  (agent-request-challenge.md).

### Slide 11: Knowledge organisation. KEEP as a 45-second glance, soften one claim

* New title: **The repo is the project memory, so knowledge compounds** [54].
  "Second brain" is fine too; the change is optional.
* **Soften the overclaim.** "31 commits and PR #1; messages say what changed
  and why" is not fully true. Commit cfe06d4 reads "Implement feature X to
  enhance user experience and optimize performance". The count is now 32.
  Use "30+ commits and PR #1; most messages say what changed and why", or
  drop the second clause.
* Do not read the boxes aloud. Say one sentence per column and move to
  slide 12.

### Slide 12: Traceability chain. KEEP, make the example real

* New title: **One real chain, from a decision down to its dated source**
  [56]. Alternatively keep the current title (61).
* Replace the generic box text with the actual chain. Every link below is
  verified in the repo:
  * Decision: addendum, "do not approve a five-agent portfolio rollout".
    Stock Prioritisation is not built as an end-to-end agent.
  * Evidence: agent-request-challenge.md, Stock Prioritisation: "eligibility
    is a rules question".
  * Requirement: FR-026 (legacy BR-059), a deterministic pass, fail or
    unknown eligibility result; AC-039; CON-005.
  * Source: WH:SHF Wave 3 technical annex, Page 3, footnote 1 ("in scope"
    does not mean eligible), retrieved 19 Sep 2026.
  * Change record: log.md, 2026-09-26 entries; commits a72f231 and 3db359c.
* A named chain the mentor could open is far more convincing than a pattern.

### Slide 13: Next steps and mentor questions. KEEP, retitle, sharpen

* New title: **Four decisions where I would value your challenge today** [55]
* Sharpen question 1 so it names the risk: "Will the panel read control
  plane plus bounded AI as a stronger answer, or as refusing the brief?"
* Add one line of feedback you want on the storytelling itself: "Where did
  the story lose you?" That invites the Therapist and coaching mode.
* Optional: put the questions on the left and next steps on the right, so
  the ask is read first.

## 4. Speaker Note Improvements

**Slide 1 (opening).** Replace the first paragraph with:
"I have three things to show and four decisions I want your challenge on.
The short version: the brief asks for five agents; two weeks of evidence
says the value is real, but the agents are not the way to get it."

**Slide 3.** Add: "Loop 4, on 26 September, is the turning point. Everything
before it built the case; everything after it made the case testable."

**Slide 7 (turning point).** Replace the first two paragraphs with:
"This is the turning point. I had suspected since 11 September that a
control plane mattered more than agents. It was in the first addendum. What
I did not have was evidence for each agent. So on 26 September I stopped
treating the five agents as a specification and treated each 'owns
end-to-end' line as the business telling me what value it expects...
One caveat before you ask: the role agents read my addendum, so their
agreement is a sector-informed hypothesis, not validation. The eight
questions they raised are how we validate it with the real company."
Keep the existing closing line ("A lack of intelligence is not the
problem").

**Slide 8.** Replace "Once the real problem was clear, I rewrote what we
actually need to build" with:
"The challenge confirmed and sharpened the control plane I had proposed on
11 September. What changed on 26 September is that every layer now traces to
a role verdict, ten new BRD rows (BR-059 to BR-068) and five bounded AI
candidates, each with a comparator and a stop criterion. They are candidates
for shadow testing, not tested yet."

**Slide 9.** Add: "The 0 percent was an identifier-format problem, not
missing requirements. Relabelling fixed traceability. It did not fix
measurability. That is why the gate still fails."

**Slide 10.** Add a line to lead into the lessons: "If I started again
tomorrow, I would change three things."

**Slide 13.** End with silence, not a summary. Say: "Those are my four
questions. Which one would you take first?"

## 5. Delivery Guidance for the Moments That Matter

| Moment | Observable | Guidance |
| --- | --- | --- |
| Slide 1 open | Language, posture | Lead with the ask (Sergeant-friendly). Sit upright and still. No preamble about the programme |
| Slides 2 to 6 | Voice, gestures | Measured pace for a Scientist: "the evidence is", "the source is". Point to footers when you cite them. Keep the pace brisk, about 1 minute per slide |
| Slide 7 hinge | Voice, movement, facial expression | Slow down, pause after the red banner for 2 to 3 seconds, lean slightly towards the mentor. Volunteer the priming caveat yourself. That builds more trust than any number |
| Slide 9 FAIL | Facial expression, language | Say "it fails, and I chose that" with a neutral, confident face. Do not apologise. Then ask for the mentor's view |
| Slide 10 lessons | Voice, gestures | Warmer, reflective tone (Therapist). Use open palms and "I" statements |
| Slide 13 ask | Posture, language | Stop presenting: sit back, pick up a pen and take notes visibly. Let the mentor talk |
| Throughout | Dress | Business casual, matching the mentor. This is a coaching session, not the Panel. On video, look at the camera on slides 1, 7 and 13 |

## 6. Top 5 Mentor Questions and Suggested Answers

1. **"Weren't your role agents primed by your own addendum, so the unanimous
   verdict is circular?"**
   Partly, yes. They read the addendum, which proposed a control plane on
   11 Sep, so the verdict is a sector-informed hypothesis. It is validated
   only by the eight discovery questions and Phase 0 readiness data.
2. **"Will the panel see this as refusing the brief?"**
   No. Every requested outcome survives (delivery, grant capture, damp and
   mould timescales, bills). The five capabilities become bounded AI modules
   with value tests, and the addendum recommends a capped readiness and
   pilot stage, not a rejection.
3. **"What exactly was the design thinking, and who took part?"**
   A value reframe of each "owns end-to-end" line, run with eight role
   agents in parallel on 26 Sep and recorded in agent-request-challenge.md.
   No real residents or staff took part, so resident evidence is still zero.
4. **"If the GBP 40m isn't secured, what is the business case?"**
   Grants are capped and co-funded, so value rests on more accepted
   handovers, less rework, avoided clawback and faster cash. Targets stay
   unset until company data or board decisions arrive (OD-01, OD-08, OD-09
   and others). The GBP 66.7m provider-funding figure is an addendum
   estimate.
5. **"Where is the architecture?"**
   It is next on the 85-day plan to 5 Dec. The control plane records and
   the five AI candidates are its inputs, and IDEA-001 compares typed
   decision models in shadow mode.

## 7. Evidence Gaps and Risks Found During Review

* **Overclaim, slide 8:** "Five shadow-tested candidates". They are
  untested candidates.
* **Overclaim, slide 11:** "messages say what changed and why". Commit
  cfe06d4 does not, and the commit count is now 32.
* **Sequencing, slide 8 notes:** the notes imply the control plane came from
  the 26 Sep session. It dates from the 11 Sep addendum.
* **Unlabelled date, slide 10:** Awaab's Law Phase 2 appears as a fact. The
  implementing instrument is not in the local corpus.
* **Method evidence:** the repo does not record "design thinking" artefacts.
  Be ready to describe the method verbally.
* **Repo inconsistency (outside the deck):** addendum line 32 says "the 2030
  standard remains a proposal", while line 49 and the log say final SRS MEES
  policy, not yet commenced law. A mentor reading the addendum may notice.
* **No resident evidence** exists anywhere. Keep saying so.
* **Archetype assumption:** I assumed a Scientist mentor with Therapist
  traits. If you know the mentor is a fast, decision-first Sergeant, move
  slides 7 and 8 up to positions 3 and 4, and treat 4 to 6 as backup.

## 8. Prioritised Changes (max 8, each a small YAML edit)

1. **Slide 7: land the turning point.** Change the title to "Each request
   states a value; none needs an end-to-end agent". Replace the green subhead
   with the before and after framing line. Add the priming caveat to the
   footer. Use the rewritten notes from section 4.
2. **Fix the overclaims.** On slide 8, "shadow-tested" becomes "candidates
   for shadow testing". On slide 11, soften the commit claim and update the
   count. On slide 10, Phase 2 becomes "planned from". On slide 4, add
   "(est.)" to 15,600 and "owner-confirmed" to not-for-profit.
3. **Slides 1 and 13: put the ask up front.** Add the "four decisions" line
   to slide 1. Retitle slide 13 to "Four decisions where I would value your
   challenge today". Sharpen question 1 and add "Where did the story lose
   you?"
4. **Slide 8 notes: tell the honest origin.** The control plane hypothesis
   dates from 11 Sep; the 26 Sep session turned it into evidence for each
   agent.
5. **Slide 10: add the reflection beat.** Retitle it "Keeping evidence honest
   was hard; here is what I would change". Keep three challenges and add
   three lessons: start the log on day one, use canonical IDs from the first
   draft, and run the value challenge earlier and blind.
6. **Slide 12: walk one real chain.** Use the addendum decision, the Stock
   Prioritisation challenge, FR-026 (BR-059) with AC-039 and CON-005, WH:SHF
   annex Page 3 footnote 1 (retrieved 19 Sep), and the log for 26 Sep with
   commits a72f231 and 3db359c.
7. **Slide 5: show one role-agent exchange.** Replace the banner with the
   Finance funding-route example, labelled as regulatory fact, unknown and
   effect. Retitle it "Eight role agents stood in for the company I cannot
   interview".
8. **Slides 6 and 9: give each a distinct job.** Slide 6 becomes the rising
   action, "The case against five agents built up across two weeks", with
   the 11 and 19 Sep milestones and without the duplicate loop. Slide 9
   becomes "Relabelling fixed traceability; the gate still fails on
   targets", with the "ID traceability" caption and the "68 BR and 12 OBJ
   rows relabelled" line.

## Next Decision

You have one decision to make: will you present the origin honestly (a
control plane hypothesis from 11 Sep, tested on 26 Sep) rather than as a
reframe that came entirely from the 26 Sep session? I recommend the honest
version. It is more defensible, it answers the priming question before it is
asked, and it shows the mentor how you think.
