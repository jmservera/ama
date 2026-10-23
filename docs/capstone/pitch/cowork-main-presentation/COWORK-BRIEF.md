---
title: Cowork Authoring Job
description: Complete instructions for building the Zava Forward main capstone presentation from this portable folder
ms.date: 2026-10-23
ms.topic: reference
---

## The Job

Build a remarkable, executive-first 16:9 PowerPoint from this folder.
The audience is a mixed customer CXO group and AMA assessment panel.
Use the exact factual core, distinguish evidence from proposals, and tell one
connected story. Do not turn this into a tour of cloud products.

Desired audience action: agree the next gated validation path, with accountable
owners, required evidence and a refreshed finite cost boundary. This is not
a request for production rollout, autonomous operation or retrospective
approval of spending.

## Current v2 Revision Direction (2026-10-23)

The owner-selected [54-slide v2 deck](../../deck/zava-forward-cowork-v2-draft.pptx)
is the current presentation, not the original 18-slide authoring inventory
below. Preserve its visual language, main-route timing and appendix navigation.
Integrate these owner-requested refinements without claiming delivery:

* Bring IoT into the main architecture story: labelled sensors or simulators
  send temperature/humidity observations through IoT Hub Basic to API
  validation and Azure SQL; deterministic signals request human review.
  Explain the intended value of in-use monitoring after retrofit. This is
  accepted exercise design, not verified live transport, diagnosis or benefit.
  Resident hazard reports always retain their independent human safety route.
* Replace categorical "no resident portal" language with "optional resident
  self-service under assessment". [Issue #441](https://github.com/jmservera/ama/issues/441)
  proposes reusing case/API authority, portal/workflow first and a separately
  gated resident-answer task. Test fewer avoidable status calls and staff
  interruptions; do not claim measured time or cash savings. Phone, email,
  visits and accessible assisted channels remain available without detriment.
* Issue #441 is open and its latest comment reports a Research-stage
  integration blocker, with no published PR. The owner's reported local
  work-in-progress is not inspected implementation or an approved handoff.
  Keep per-message human review normative and routine automation off pending
  explicit requirements-owner disposition and separate release approval.

## Read in This Order

1. `README.md` and `audience-and-delivery.md`.
2. `slides.json`, then `speaker-script.md` for the intended spoken narrative.
3. `diagrams/README.md` and all seven previews.
4. `demo-runbook.md`, `backup-slides.md` and `tokenomics-worksheet.csv`.
5. `evidence/README.md`, `sources.json` and both evidence reports.
6. `validation.md`, especially the checks still outstanding.

`slides.json` owns IDs, timing, copy, notes and source associations.
Do not silently diverge the PPTX from it. Record intentional wording or layout
changes in a handoff change list and preserve the factual classifications.
The 18 main slides and 27 backups are the proposed complete inventory.
Use PowerPoint sections and hyperlink navigation rather than putting
45 slides into the spoken route.

## Narrative and Pacing

Lead with the recommendation, business constraint and a fictional home's
journey. Show the simple architecture on S04. Explain AI placement on S06,
the five-responsibility challenge on S07, value and cost on S08-S09, runtime
detail on S10, and Tokenomics on S11. Only then explain how HVE, design
thinking, prototype/MVP learning and the hierarchical backlog generated from
the BRD, PRD and ADRs built
the solution, on S12-S14.

S15-S16 set acceptance and the decision. S17 introduces the separate demo;
S18 closes after it. Planned narration is 24 minutes, with six minutes of
interruptions inside the presentation allocation, plus a ten-minute demo.
Do not add another ten-minute Q&A.

## Art Direction

Think confident boardroom editorial, not a generic consulting template.
Use warm ivory `#FAF9F6`, deep Zava green `#173F35`, restrained pale blue
for evidence/configuration, pale purple for AI and amber for
unknown/proposed/held. Text labels must carry status even without colour.
Use generous space, strong conclusion-led titles and one principal visual
per slide. Never shrink a detailed topology to fit.

Use Aptos or an available legible sans-serif consistently; if substituting a
font, record it and inspect line wrapping. Target 30-36 pt titles and 22-28 pt
body text. Source lines can be smaller but must not collide with content.
Use no more than the provided three on-slide statements on ordinary slides.
The full argument belongs in notes, not in tiny text.

Do not invent residents, testimonials, company approvals, measured financial
returns or feature screenshots. A fictional home is explicitly labelled as
such. The visuals do not require photographs or stock AI-brain artwork.

## Diagrams and PowerPoint Editing

Use the bundled `.excalidraw` sources and their 1600x900 SVG/PNG previews.
Every view already fits one 16:9 slide. Keep boxes, text and arrows editable
where practical: open in Excalidraw and export as needed, or reconstruct the
same geometry as native PowerPoint groups. Preserve official Azure icon bytes
and proportions. Never substitute an Azure icon for the custom Decision 1
model or a human role.

For S04, S06, S10 and S11, follow the staged reveal instructions in the diagram
index. Animations are optional; the complete static slide must make sense.
Prefer simple appear/dissolve clicks with a matching static/PDF route.
No autoplay, zooming camera tour or animation dependency.

Link every backup slide back to its recorded main-slide ID. Add a compact
question index immediately before the appendix, as navigation only, outside
the 18-slide spoken route. Put a hidden or clearly marked section break before
backup slides so normal advance never enters the appendix accidentally.
Use hyperlinks/action buttons compatible with the eventual target viewer;
validate them there.

## Notes and Evidence

Every slide needs notes with the script, evidence IDs, source paths/sections,
claim classification, timing and interruption/return cue.
For diagram slides include the full text alternative from the diagram index.
Put compact evidence labels on the slide itself where a number or status
would otherwise be ambiguous.

Key evidence rules:

* The 60,000-home stock, 980-case retained programme and small test cohorts
  are different populations.
* Approximately 180 describes the owner's historical backlog scale, counting
  epics, features and user stories, not agents, stories alone or accepted
  completion. Use the verified dated snapshots in E16 for exact figures.
* Five assistants are not five autonomous managers or five active workers.
* Decision 1 is learned scoring, not deterministic rules. Its cheaper/faster
  advantage is not yet measured and it is not a proven deployed Foundry tier.
* 6,884 tokens across five runs is a historical observation without human
  acceptance, not a price, quality result or accepted-outcome denominator.
* Cost per accepted proposal above a quality floor is a proposed unit.
  Cost per accepted home/hand-over is a different end-to-end measure.
* Finite call/token allowances and expiry are not a currency cap.
  Complete metering, monetary/task/period budgets and request/depth limits
  are proposed requirements, not observed controls.
* USD 700 is the owner-set October all-in forecast ceiling, not a monthly
  production cost or unconditional tranche authority. Execution prerequisites
  remain blocked and authority expires 2026-10-25T16:02Z.
  USD 450/month is historical.
* GBP retrofit fixture arithmetic is not a technology quote or real award.
* Saved time is capacity until Finance confirms a real value destination.
* No legal-currentness, WCAG-conformance, production-readiness or completed
  human-validation claim follows from the package.

Do not include the internal Microsoft Tokenomics deck, its slides, its quotes
or internal-only summaries. The public community framing is draft, not an
industry or Microsoft standard. The requirements and repository observations
are sufficient to tell this story without proprietary content.

## Deliverables

Produce a final `.pptx` with editable text, native navigation and complete
speaker notes; an accessible static PDF; a contact sheet; and a short build
handoff recording deliberate content/layout deviations, font substitutions,
validation and remaining limitations. Retain the diagram sources and
individual slide previews beside the working project.

Do not overwrite the existing executive deck until the new one passes review.
The repository delivery location for a validated executive deck is
`docs/capstone/deck/`; the mentor deck is separate.

## Acceptance Before Calling It Ready

Inspect every rendered slide for clipping, collisions, small text, unintended
wraps, icon distortion and unreadable diagrams. Check notes, slide IDs, section
order, links/returns and the complete static animation alternative.
Check the full capstone criteria and floors in the bundled evidence report,
not only presentation aesthetics. Do not invent a rubric score.

Run a timed, interruptible rehearsal and a separate timed demo using the
actual planned route. Inspect the final file in native PowerPoint, not just
an image export. Test keyboard/navigation, accessibility and projection
readability. Record not-run checks plainly. Authoring this folder has not
performed any of those final-deck or human-delivery checks.
