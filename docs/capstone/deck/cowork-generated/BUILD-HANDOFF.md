---
title: Zava Forward main presentation - build handoff
description: What was built from the cowork-main-presentation package, deliberate deviations, font substitution, validation performed and remaining gates
ms.date: 2026-10-23
---

## Status in one paragraph

A complete 46-slide 16:9 deck was built from `COWORK-BRIEF.md` and every file in the
`cowork-main-presentation` folder. It has editable text and shapes, native PowerPoint sections, full
speaker notes on every slide, and visible navigation. It has been rendered and inspected slide by slide.
It is a **draft for owner review**. It has not been rehearsed, inspected in desktop PowerPoint, tested
with a screen reader or projector, or approved by anyone. Do not label it "panel ready",
"production ready", "rehearsed", "customer validated" or "rubric passed". Do not publish it to
`docs/capstone/deck/` until it passes review. The existing executive and mentor decks were not touched.

## Deliverables

| File | What it is |
| --- | --- |
| `Zava Forward - More homes ready with control intact.pptx` | The deck: 18 spoken slides, a question index and 27 appendix answers, with sections and complete notes |
| `Zava Forward - More homes ready with control intact.pdf` | Static route: one page per slide, outline (bookmarks), working internal links that mirror the deck's navigation labels, and a selectable text layer |
| `Zava Forward - contact sheet.png` | All 46 slides as labelled thumbnails |
| `Zava Forward - slide previews.zip` | Individual PNG preview of every slide |
| `BUILD-HANDOFF.md` | This file |

The diagram sources (`diagrams/*.excalidraw`, SVG and PNG previews) remain unchanged in the
original `cowork-main-presentation` folder.

## Structure

| Slides | IDs | Section | Narration |
| --- | --- | --- | --- |
| 1-3 | S01-S03 | 1 · Outcome, constraint, human journey | 03:30 |
| 4-7 | S04-S07 | 2 · Operating model, controls, AI and five responsibilities | 06:00 |
| 8-11 | S08-S11 | 3 · Value, cost, runtime and Tokenomics | 06:00 |
| 12-14 | S12-S14 | 4 · HVE, backlog and learning | 04:30 |
| 15-18 | S15-S18 | 5 · Acceptance, next gate, demo and close (S18 is delivered after the demo) | 04:00 |
| 19 | QX | Appendix · navigation only (marked "end of the 18-slide spoken route") | none |
| 20-46 | B01-B27 | Appendix · navigation only (Bn is slide 19 + n) | optional answers only |

Planned narration is 24:00, with a 6:00 discussion reserve and a separate 10:00 demo: 40:00 in total.
Every slide's notes carry the script, timing and clock position, the interruption cue and return line,
related appendix slides, evidence IDs with repository paths and sections, claim classification and
limits, evidence guardrails, and for diagram slides the full text alternative and legend.
Slide titles and on-slide statements are taken word for word from `slides.json`.

## Source baseline and repository check

* Authoring package: `Work/00 - AMA/cowork-main-presentation` (COWORK-BRIEF.md and all 13 top-level
  items, including 7 diagrams with their Excalidraw sources, the evidence register and both evidence
  reports), read in the brief's order on 23 Oct 2026.
* Repository: the public `jmservera/ama` commit history was checked on 23 Oct 2026. The head of `main`
  was `140d8f4` ("docs(requirements): add AI Tokenomics requirements and pitch brief (#433)"), the
  same commit the package is pinned to, so there is no later delta to record. No other repository
  content was used; every on-slide fact comes from `slides.json` and the bundled evidence.
* No internal Microsoft Tokenomics material, private data, credentials or rubric score is used.

## Evidence rules applied

* 60,000 homes (case-brief stock), 980 retained programme cases and small test cohorts are kept
  apart; only 60,000 appears on the main route, labelled as case-study scale.
* "Approximately 180" is described as the owner's historical backlog scale (epics, features and
  stories). The dated figure shown is 189 board items on 23 Oct 2026 07:21 UTC, labelled as board
  status, not accepted delivery.
* Five assistants are never shown as five autonomous managers or workers; Decision 1 is labelled
  learned scoring with no measured cost or speed advantage and has no Azure icon.
* 6,884 tokens over five runs is labelled as a historical observation with no human acceptance;
  cost per accepted proposal is shown as unknown at equal prominence.
* Finite allowances are labelled "not a money cap"; monetary, task, period and per-request limits are
  labelled proposed and not tested.
* USD 700 is labelled as the owner-set October ceiling with paid tranches still blocked and the
  25 Oct 2026 16:02 UTC expiry; USD 450/month is labelled historical. GBP figures are labelled
  fictional exercise arithmetic and kept apart from USD.
* No legal-currentness, WCAG-conformance, production-readiness or completed human-validation claim
  is made. The example home is labelled fictional.

## Font substitution

* **Arial everywhere instead of Aptos.** The review renderer has no Aptos, so line wrapping could
  only be checked with a metric-identical Arial. Every wrap seen in review is the real Arial wrap.
  Aptos is slightly narrower, so a later Replace Fonts (Arial to Aptos) should not create overflow.
  Re-inspect the wrapping if you switch.
* The tenant's sensitivity marking ("Classified as Microsoft Confidential", 10 pt, bottom-left of the
  slide master) is applied by labelling policy, not by the deck. It is the only text under 12 pt and
  it has low contrast on the two green slides (S01, S18). The saved PPTX carries this label with
  protection. The PDF, contact sheet and slide previews were generated from the slide renders. They
  show the marking on every page but do not carry the label's protection. Apply the appropriate
  label to each file under your organisation's policy before sharing any of them outside Microsoft.

## Platform limits and how they were handled

* **No clickable internal links, action buttons or hidden slides could be created.** Navigation is
  visible text instead. Every main slide's footer lists its related answers ("Answers: B10 · B20");
  every appendix slide has a "Return to Sxx · slide n" pill and "Index: slide 19" in its footer; the
  question index lists every answer with its slide number. In Slide Show, type the number and press
  Enter. Slide 19 is the marked end of the spoken route, and the appendix is its own section. To
  make these clickable, use the link map below in desktop PowerPoint (select label, Ctrl+K, Place in
  This Document). Each index entry and return pill is its own shape. Validate the links in the
  target viewer. The PDF already has working links.
* **No dashed lines.** Where the owner's diagrams use dashed boxes (proposed, target or deferred), the
  deck uses an amber box with an amber outline and a status pill. Where they use dashed arrows
  (configured or gated paths), it uses hollow arrows. A legend line on each diagram slide says so in
  words.
* **No animations.** Every slide is fully readable as a static slide. If you want click reveals for
  S04, S06, S10 and S11, add simple Appear or Fade effects in desktop PowerPoint following
  `diagrams/README.md`.
* **Official Azure icons** are placed as 512 px transparent PNG renders of the bundled official
  SVGs, at their own proportions, uncropped and not recoloured. The original SVG bytes remain in the
  package. If byte-exact SVG icons are required, insert the SVGs over them in desktop PowerPoint. No
  Azure icon is used for Decision 1, a person or a role.
* **Tables** (B03, B04, B05, B20) are created at a fixed width of about 8.9 in with default black
  body text and the engine's own row banding, so notes or pills sit in the column to their right.

## Deliberate content and layout deviations

All slide titles and the three on-slide statements per slide are verbatim from `slides.json`. The only
exceptions are typographic: "->" is shown as "→" and "!=" as "≠" in a few places (S12, S13, B03, B06,
B21, B23, B24). Two-line titles break at a hand-balanced point with unchanged words: S02, S07, S10,
S13, S15, S16, S17, B06, B15, B20 and B26. Extra on-slide labels come from the owner's own answer
text, the visual briefs, the notes or the evidence register, unless they are listed below as new
wording.

**Main route (slides 1-19)**

* Sizes: titles 32 pt and appendix questions 28 pt. Statements are 22-24 pt where they fit. On dense
  slides they are smaller: S06 17 pt bold, S09 and S11 18 pt, S17 20 pt. The full argument stays in the notes.
* S01 shows "ZAVA FORWARD" as the brand line, and its footer says Zava North Homes and Zava Forward are fictional. S18
  mirrors S01, with the three statements in the decision panel.
* S02 adds the row labels DEMAND / CONSTRAINT / OUTCOME. S05 puts "CAN BE PREPARED" and "NEEDS
  ITS OWN ACCOUNTABLE DECISION" once each, as column headers.
* S04, S06 and S10 are native rebuilds of diagrams 01-03. They are scaled about 1% horizontally to align
  with the title edge. The S06 middle card is wider so "Learned scoring, not a decision table" fits
  on one line. S10 is compressed vertically to 89% under its two-line title; text sizes are unchanged.
* S09 uses the three statements as the ledger headings. The USD pill is split over two lines:
  "OWNER DECISION 22 OCT / NOT A PRODUCTION PRICE".
* S11 is a simplified view of diagram 07 (the full view is B25). The 6,884 observation and
  "Unknown" are the same size, and there is no diagram status pill.
* S12's ribbon stage names come from the `slides.json` visual brief ("Problem discovery",
  "Prototypes / MVP learning", "Bounded engineering loops"). The status is shown as two pills:
  "OWNER FEEDBACK · PR #26" and "NOT RESIDENT OR WORKFORCE VALIDATION".
* S13 places the API-derived board visual at 7.0 in wide. The image keeps its own small provenance
  line; the readable caption beneath repeats the date, "not a screenshot of GitHub's website" and
  "Board status is not accepted delivery". The statements read as a numbered 1 → 2 → 3 chain, with
  "189" large.
* S15 uses ivory gate cards with an amber PENDING pill each. S16 is a green memo card in which the
  statements keep their "Scope:" and "Owners:" prefixes. S17 emphasises route E with "RECORDED
  EVIDENCE, NOT LIVE".
* The QX index (slide 19) uses two columns of three groups at 13 pt, not three columns. Three columns
  would not fit one line per item at 12 pt or more.

**Appendix (slides 20-46)**

* B01's option-2 lead "Workflow must beat the baseline" is new wording, built from S08's Comparison 1.
* B04 shows the cost equation as a fraction, and its table's first column is headed "Approach".
* B07 omits the diagram subtitle. Its legend is reworded to "Proposal review is not consent, QA or
  Finance", and there is an AI PREPARES pill on the Call step.
* B09 is to scale on a GBP 0-20,000 axis. GBP 22,000 (the envelope) appears only in the statement.
* B10 draws the future split as an amber DEFERRED box with hollow arrows. The current runtime shows one
  API hosting five bounded assistants plus SQL, and there are no Azure icons.
* B11 keeps "!=" verbatim in statement 3.
* B13 runs the trace vertically (epic #73 → feature #76 → story #77 → PR #376), with an acceptance
  boundary line and a dated-counts pill.
* B14's bands follow the brief's order, so statement 2 comes before statement 1.
* B15 has no separate "All three are required" heading: plus signs carry it.
* B16 adds an OWNED MANUAL ROUTE lane, and its evidence bar ends with statement 3.
* B17's owner for "Finite test authorised" is set to "Programme + Finance". This follows S16's notes:
  Programme defines scope, and Finance approves any finite spend. **Please confirm.**
* B19's subtitle keeps only its first sentence, because the second refers to dashed steps.
* B21 adds the labels UNTRUSTED EVIDENCE and REVIEW BOUNDARY and drops the diagram's
  "Proposal review never substitutes…" footer line for space.
* B23's rows "Digital route" and "No-digital route" are new.
* B24's pill reads "REPOSITORY CONVENTION · NOT ACTIVATED".
* B25's legend reads "Public Tokenomics framing is draft, not an industry or Microsoft standard",
  in place of the diagram's footer.
* B26 adds "Same held-out cases".
* B27's three call boxes come from the answer.
* "Approved" appears only as a required future step, never as a claim: "Approved policy and human
  review" (S07, B03), "approved communications… remain necessary" (B06), "Finance-approved
  mechanism" (B08) and "Approved control version" (B24). Reword these if you want the word removed entirely.

## Validation performed for this build

* Read the whole package in the brief's order: README, audience and delivery, `slides.json`,
  speaker script, diagram index and all seven previews, demo runbook, appendix copy, Tokenomics
  worksheet, evidence register and both evidence reports, and the validation receipt.
* Checked the public repository history. The head of `main` is `140d8f4` (PR #433), the
  package's pinned baseline.
* Rendered every one of the 46 slides and inspected each one for clipping, overflow, collisions,
  unintended wraps, icon distortion and diagram readability. Fixed the defects found and re-rendered
  the slides touched.
* Ran automated file checks:
  * 46 slides in the planned order, with titles verbatim from `slides.json`.
  * Six sections covering 3 + 4 + 4 + 3 + 4 + 28 slides.
  * Speaker notes on all 46 slides, matching the prepared notes word for word.
  * Every text run 12 pt or larger, apart from the tenant marking.
  * One typeface (Arial) for all deck text.
  * Every navigation label points to the right slide number.
  * A wording scan for unsupported claims (production readiness, rehearsal, validation, savings,
    ROI, payback, percentages, "180 agents"). Every remaining hit is a negation or a required future step.
* The automated render check reports no failures apart from the tenant marking's contrast on the
  two green slides. The remaining warnings are style notes the brief overrides: outlined cards, no
  photographs, and estimated text widths that the renders show fit.

## Not performed: remaining gates before calling it ready

* Inspection in **desktop PowerPoint** (only service renders were inspected), including font
  fallback if you switch to Aptos.
* **Clickable hyperlinks**, return buttons and hidden slides. Add them from the link map, then test
  them in the target viewer.
* **Keyboard, screen-reader, contrast and projection** checks on the final file. No accessibility
  conformance is claimed. The PDF has bookmarks, links, a document language and a selectable text
  layer, but it is image-based and not a tagged, accessibility-conformant PDF.
* A **timed, interruptible rehearsal** of the 24-minute route and a **separately timed demo**
  using the actual route that passes preflight (route E is the default unless L is freshly
  established).
* Checking the full capstone criteria and floors against the delivered deck, as the brief requires.
  The bundled report maps all 20 criteria. This deck contributes to narrative, audience
  calibration, written communication and evidence storytelling. Actual delivery, demo, Q&A,
  rehearsal and the thought-leadership artifact (D1-D3) remain outstanding. **No rubric score is
  claimed.**

## Decisions still needed from the owner

1. B17: confirm "Programme + Finance" as the owner of "Finite test authorised".
2. Keep or reword the four "approved / approval" phrases that describe required future steps (B03,
   B06, B08, B24), and B01's new option-2 lead.
3. Keep Arial or switch to Aptos, then re-check the wrapping.
4. Handle the sensitivity marking before sharing outside Microsoft.
5. The open questions from `audience-and-delivery.md`: exact audience, interpretation of the
   Tokenomics clue, unit denominator and quality floor, whether a fresh measured batch is
   separately authorised, and the demo route that actually passes preflight.

## Link map for desktop PowerPoint

Add each as Insert > Link > Place in This Document. Every main slide's footer label names its answers; every appendix slide's return pill and footer index label name their targets.

| From slide | Visible label | Link to |
| --- | --- | --- |
| 1 (S01) | "B15" in the footer's "Answers" list | slide 34 (B15) |
| 2 (S02) | "B01" in the footer's "Answers" list | slide 20 (B01) |
| 3 (S03) | "B06" in the footer's "Answers" list | slide 25 (B06) |
| 4 (S04) | "B02" in the footer's "Answers" list | slide 21 (B02) |
| 5 (S05) | "B06" in the footer's "Answers" list | slide 25 (B06) |
| 5 (S05) | "B07" in the footer's "Answers" list | slide 26 (B07) |
| 5 (S05) | "B24" in the footer's "Answers" list | slide 43 (B24) |
| 6 (S06) | "B04" in the footer's "Answers" list | slide 23 (B04) |
| 6 (S06) | "B05" in the footer's "Answers" list | slide 24 (B05) |
| 7 (S07) | "B03" in the footer's "Answers" list | slide 22 (B03) |
| 8 (S08) | "B08" in the footer's "Answers" list | slide 27 (B08) |
| 9 (S09) | "B05" in the footer's "Answers" list | slide 24 (B05) |
| 9 (S09) | "B09" in the footer's "Answers" list | slide 28 (B09) |
| 10 (S10) | "B10" in the footer's "Answers" list | slide 29 (B10) |
| 10 (S10) | "B20" in the footer's "Answers" list | slide 39 (B20) |
| 10 (S10) | "B22" in the footer's "Answers" list | slide 41 (B22) |
| 11 (S11) | "B11" in the footer's "Answers" list | slide 30 (B11) |
| 11 (S11) | "B21" in the footer's "Answers" list | slide 40 (B21) |
| 11 (S11) | "B25" in the footer's "Answers" list | slide 44 (B25) |
| 11 (S11) | "B26" in the footer's "Answers" list | slide 45 (B26) |
| 11 (S11) | "B27" in the footer's "Answers" list | slide 46 (B27) |
| 12 (S12) | "B12" in the footer's "Answers" list | slide 31 (B12) |
| 13 (S13) | "B13" in the footer's "Answers" list | slide 32 (B13) |
| 14 (S14) | "B14" in the footer's "Answers" list | slide 33 (B14) |
| 14 (S14) | "B19" in the footer's "Answers" list | slide 38 (B19) |
| 15 (S15) | "B15" in the footer's "Answers" list | slide 34 (B15) |
| 15 (S15) | "B16" in the footer's "Answers" list | slide 35 (B16) |
| 15 (S15) | "B23" in the footer's "Answers" list | slide 42 (B23) |
| 16 (S16) | "B15" in the footer's "Answers" list | slide 34 (B15) |
| 16 (S16) | "B17" in the footer's "Answers" list | slide 36 (B17) |
| 17 (S17) | "B18" in the footer's "Answers" list | slide 37 (B18) |
| 20 (B01) | "Return to S02 · slide 2" pill | slide 2 (S02) |
| 20 (B01) | "Index: slide 19" in the footer | slide 19 (QX) |
| 21 (B02) | "Return to S04 · slide 4" pill | slide 4 (S04) |
| 21 (B02) | "Index: slide 19" in the footer | slide 19 (QX) |
| 22 (B03) | "Return to S07 · slide 7" pill | slide 7 (S07) |
| 22 (B03) | "Index: slide 19" in the footer | slide 19 (QX) |
| 23 (B04) | "Return to S06 · slide 6" pill | slide 6 (S06) |
| 23 (B04) | "Index: slide 19" in the footer | slide 19 (QX) |
| 24 (B05) | "Return to S09 · slide 9" pill | slide 9 (S09) |
| 24 (B05) | "Index: slide 19" in the footer | slide 19 (QX) |
| 25 (B06) | "Return to S05 · slide 5" pill | slide 5 (S05) |
| 25 (B06) | "Index: slide 19" in the footer | slide 19 (QX) |
| 26 (B07) | "Return to S05 · slide 5" pill | slide 5 (S05) |
| 26 (B07) | "Index: slide 19" in the footer | slide 19 (QX) |
| 27 (B08) | "Return to S08 · slide 8" pill | slide 8 (S08) |
| 27 (B08) | "Index: slide 19" in the footer | slide 19 (QX) |
| 28 (B09) | "Return to S09 · slide 9" pill | slide 9 (S09) |
| 28 (B09) | "Index: slide 19" in the footer | slide 19 (QX) |
| 29 (B10) | "Return to S10 · slide 10" pill | slide 10 (S10) |
| 29 (B10) | "Index: slide 19" in the footer | slide 19 (QX) |
| 30 (B11) | "Return to S11 · slide 11" pill | slide 11 (S11) |
| 30 (B11) | "Index: slide 19" in the footer | slide 19 (QX) |
| 31 (B12) | "Return to S12 · slide 12" pill | slide 12 (S12) |
| 31 (B12) | "Index: slide 19" in the footer | slide 19 (QX) |
| 32 (B13) | "Return to S13 · slide 13" pill | slide 13 (S13) |
| 32 (B13) | "Index: slide 19" in the footer | slide 19 (QX) |
| 33 (B14) | "Return to S14 · slide 14" pill | slide 14 (S14) |
| 33 (B14) | "Index: slide 19" in the footer | slide 19 (QX) |
| 34 (B15) | "Return to S16 · slide 16" pill | slide 16 (S16) |
| 34 (B15) | "Index: slide 19" in the footer | slide 19 (QX) |
| 35 (B16) | "Return to S15 · slide 15" pill | slide 15 (S15) |
| 35 (B16) | "Index: slide 19" in the footer | slide 19 (QX) |
| 36 (B17) | "Return to S16 · slide 16" pill | slide 16 (S16) |
| 36 (B17) | "Index: slide 19" in the footer | slide 19 (QX) |
| 37 (B18) | "Return to S17 · slide 17" pill | slide 17 (S17) |
| 37 (B18) | "Index: slide 19" in the footer | slide 19 (QX) |
| 38 (B19) | "Return to S14 · slide 14" pill | slide 14 (S14) |
| 38 (B19) | "Index: slide 19" in the footer | slide 19 (QX) |
| 39 (B20) | "Return to S10 · slide 10" pill | slide 10 (S10) |
| 39 (B20) | "Index: slide 19" in the footer | slide 19 (QX) |
| 40 (B21) | "Return to S11 · slide 11" pill | slide 11 (S11) |
| 40 (B21) | "Index: slide 19" in the footer | slide 19 (QX) |
| 41 (B22) | "Return to S10 · slide 10" pill | slide 10 (S10) |
| 41 (B22) | "Index: slide 19" in the footer | slide 19 (QX) |
| 42 (B23) | "Return to S15 · slide 15" pill | slide 15 (S15) |
| 42 (B23) | "Index: slide 19" in the footer | slide 19 (QX) |
| 43 (B24) | "Return to S05 · slide 5" pill | slide 5 (S05) |
| 43 (B24) | "Index: slide 19" in the footer | slide 19 (QX) |
| 44 (B25) | "Return to S11 · slide 11" pill | slide 11 (S11) |
| 44 (B25) | "Index: slide 19" in the footer | slide 19 (QX) |
| 45 (B26) | "Return to S11 · slide 11" pill | slide 11 (S11) |
| 45 (B26) | "Index: slide 19" in the footer | slide 19 (QX) |
| 46 (B27) | "Return to S11 · slide 11" pill | slide 11 (S11) |
| 46 (B27) | "Index: slide 19" in the footer | slide 19 (QX) |
| 19 (QX) | each index entry B01-B27 | slides 20-46 (B01-B27) |
