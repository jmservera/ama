# Proper Warm council presentation — independent iteration-2 review

**Date:** 2026-10-11  
**Disposition:** **Revise before council presentation; retain the evidence-led proposition.**  
**Scope:** Read-only storytelling and rendered-image QA, not implementation assurance, penetration testing, legal verification or production acceptance.

## 1. Audience and outcome summary

Reviewed the **current 18 individual images**, `slide-001.jpg` through `slide-018.jpg`, in `slide-deck/validation/render-final-4/`, not the iteration-1 contact sheet or published/stale deck copies. Read `research/final-pptx-text-and-notes.md`, `primary-research.md`, `evidence-register.md`, `subagents/storytelling-review-iteration-1.md`, and the relevant cited source provisions listed below. No PPTX was opened and no slide or other artifact was edited.

The communication job is a 15-minute CEO/CxO/CFO council pitch that explains the request, research, gap clarification, architecture, product offer, Excel transition, stakeholder value, controls and next decision. The legitimate action in this build is **endorsement to prepare a gated evidence-stage proposal**, not purchase, delivery spend, deployment or production adoption.

**Overall judgement:** The product is now identifiable: a staff-facing retrofit workbench with linked cases, role queues, evidence and accountable handoffs. Slides 6–8 explain adoption and process impact substantially better than the iteration-1 account. Slide 14 has a much clearer planning-only ask. Slide 18 supplies the previously missing unscored options framework. These are real improvements.

The remaining blockers are communication defects, not a demand to invent a business case: the central architecture diagram has text outside its panels; access boundaries and the proposed advantage over Excel are stronger in notes than on-screen; slide 18 uses ambiguous and uneven comparator descriptions; and the extracted timing summary misclassifies the appendices and counts citations as speech. No measured superiority, benefit, cost saving, security certification or production readiness can be concluded.

## 2. Recommended archetype strategy

Treat these as audience preferences, not diagnoses of the executives.

| Audience | Primary / secondary preference | Needs to hear / strongest available proof | Trust or attention risk | Intended action |
|---|---|---|---|---|
| CEO | Sergeant / Evangelist | What the product is, why accountable handovers matter, and what is requested today. Case scale and the proposed connected journey are stronger than an unearned growth claim. | A vague “next stage”; technical caveats before the customer offer; ambition mistaken for results. | Nominate a sponsor and agree the planning return. |
| Assets and other CxOs | Scientist / Sergeant | How ownership, readiness, independent decisions and returned work connect across the journey. PRD and EXA lifecycle/authority contracts support design intent. | Diagram ambiguity; “reuse contracts” interpreted as procurement authority; controls presented as deployed. | Nominate workflow/control owners and define review gates. |
| CFO | Scientist / Sergeant | Separate retrofit cash exposure from technology whole-life cost, and require equal-scope options appraisal. Fictional cash arithmetic is an illustration of a control need, not a quote. | £20,000 mistaken for product cost; “open” interpreted as an access weakness; exercise direction treated as an investment winner. | Define affordability/authority review and stop conditions, without authorizing spend today. |
| Resident/service lens within the council | Therapist / Scientist | Supported choices, human contact, minimum-necessary supplier disclosure and no compulsory digital portal. EXA-004/005 and proposed UX checks support these intentions. | Resident-sounding slogan interpreted as a testimonial; implied access to the staff tool; contact confused with consent. | Require accessible co-design and explicit service/access tests. |

Use a deliberate sequence: **offer and planning decision → research and method → connected journey/control mechanism → people and adoption → proof and affordability → bounded ask**. Keep the hopeful future state, but earn excitement through a tangible case journey rather than inflated savings.

## 3. Actionable findings

Severity: **High** = fix before council use because a central message or visual is compromised; **Medium** = material comprehension, evidence or execution risk; **Low** = editorial/maintenance improvement. Proposed changes below are recommendations only, not edits performed.

### F01 — Architecture labels escape the diagram panels

**Slide:** 5  
**Severity:** High  
**Observed:** “EXCEL + SOURCE RECORDS” and “CONNECTED CASE + EVIDENCE” start at or above the rounded panels' top boundaries; their last lines (“import”, “Blob”) extend below the pale panels. “DETERMINISTIC WORKFLOW” also sits against the top edge and “audit” reaches the bottom edge. This is visible panel overflow, even though the text itself remains readable on the slide background. The architecture is the brief's central proof mechanism and should not look unfinished.

**Exact proposed change:** Increase the top-row pale panel heights to contain every line with the same internal padding as the API panel. Increase the workflow panel height or shorten its copy to **“WORKFLOW RULES / Own • route • check • audit”**. Reposition connectors after resizing. Preserve six clearly bounded nodes; do not shrink the labels to footer scale. Replace the production-oriented kicker with **“PROPOSED CONTROL FLOW”** rather than “editable native diagram”.

**Evidence/source:** `render-final-4/slide-005.jpg`; current slide-5 text/notes; PRD, “Executive Summary” and “Proposed platform boundary”; ADR 0001, “Context” and “Exercise Applicability (2026-10-11)” (E08–E10).

**Disposition recommendation:** Fix and re-render slide 5 before council use; inspect all node padding and arrows, not just text extraction.

### F02 — The diagram shows submissions to the API, but not the user's return flow

**Slide:** 5  
**Severity:** Medium  
**Observed:** The three lower arrows point towards the API. They float in whitespace rather than visibly connecting to their source panels. The diagram establishes a control choke point, but does not clearly show the staff view receiving case status or the AI receiving permitted inputs and returning a draft. A non-technical viewer has to obtain that explanation from narration.

**Exact proposed change:** Attach connectors to the relevant panel edges. Label staff ↔ API **“read case / authorized action”**; label AI ↔ controlled boundary **“permitted inputs / draft proposal”**; keep API → SQL/Blob as the authoritative state/evidence path. Add **“Human review before any controlled change”** adjacent to the staff action path. These are proposed logical flows, not a claim about deployed network topology.

**Evidence/source:** Slide-5 image and notes; PRD, “Executive Summary”, “Proposed platform boundary”, CON-003/009 and AC-057; ADR 0001, “Context” (E08/E09).

**Disposition recommendation:** Revise with F01. Do not add infrastructure detail or claim verified identity/network isolation.

### F03 — Give the Excel comparison its main-slide “why better” mechanism

**Slides:** 4–6, with 18 as supporting appendix  
**Severity:** Medium  
**Observed:** The product and transition are clear, but the main slides do not place the proposed replacement mechanism beside the workbook baseline. Slide 6 predominantly explains migration. Slide 18 is an options gate, not proof of improvement. The user specifically asked why this is better and how much better.

**Exact proposed change:** Add a short contrast on slide 6: **“Current: workbook coordination (case fact). Proposed: one linked case, named handoff owner and independently checked transition.”** Follow with **“How much better? Not measured—compare full effort, errors, rework and accepted outcomes on equal tasks.”** Replace existing lower-strip copy if space is needed; keep staff co-design/support in notes rather than crowding the slide. Do not assert that Excel cannot be hardened or that Azure has already won.

**Evidence/source:** Original case, “Business Challenge”; addendum, “Business Challenge” and “Evidence Needed Before a Platform Decision”; ADR 0001, “Options still to compare”; measurement challenge, “Owner Decision” and “Measuring Effort Without Timesheets” (E01/E05/E09).

**Disposition recommendation:** Complete the argument, not the outcome claim. No percentage, cash saving or throughput promise should be inserted without measured evidence.

### F04 — Access and stakeholder service boundaries need to stand alone on-screen

**Slide:** 8  
**Severity:** Medium  
**Observed:** This current render is clean: all three stakeholder strips fit, have readable contrast and no collision. Staff, resident and contractor benefits are now distinct. However, only the notes say residents and contractors are not assumed to log into the staff workbench, that there is no mandatory portal, and that contractors do not receive diagnoses. The slide alone could be read as three tool-user groups.

**Exact proposed change:** Change the row headings to **“STAFF • INTERNAL WORKBENCH”**, **“RESIDENTS • SUPPORTED CONTACT, NO REQUIRED PORTAL”**, and **“CONTRACTORS • APPROVED HANDOFF CHANNEL”**. Retain the benefit lines. Add a compact line **“Assigned scope and necessary adjustments only; no diagnoses.”** if it fits without reducing legibility; otherwise retain that detail in the notes and show **“minimum-necessary information”** in the contractor line. Label the house slogan **“Proposed service principle”** or change it to **“RESIDENT CHOICE BY DESIGN”** so the first-person wording is not mistaken for resident testimony.

**Evidence/source:** Slide-8 image and notes; addendum EXA-004/005/011; PRD, “Product boundary and single-product rationale” and CON-003; UX review, “Outcome and Evidence Boundary”, “Accessibility and Human Validation” and UX-08 (E06/E08/E12).

**Disposition recommendation:** Keep this slide and its people-first emphasis. Improve standalone access semantics; do not imply user acceptance or a tested resident/contractor portal.

### F05 — Options table uses “open” ambiguously and compresses unequal alternatives

**Slide:** 18  
**Severity:** Medium  
**Observed:** All headers and cells fit the current render; no clipping or overlap was seen. The permissions cells “Workbook rights open” and “Tenant roles open” can mean unsecured access rather than “not assessed”. “Small change; data open” states a migration advantage more categorically than the notes' “may minimize change”. “Lists / flows” underspecifies the business-platform comparator, which the addendum explicitly describes as a greenfield Dataverse/Power Apps option, not just SharePoint lists. Azure's proposed controls are described more concretely than the alternatives' control opportunities.

**Exact proposed change:**

* Replace every assessment-status use of **“open”** with **“not assessed”**, **“unverified”** or **“test required”**, as appropriate.
* Excel migration: **“Potentially less change; workbook/data fit unverified.”**
* Business-platform workflow: **“Greenfield Power Apps/Dataverse + flows; fit unverified.”**
* Business-platform permissions: **“Server-side roles/rules proposed; tenant/licensing unverified.”**
* Azure permissions: **“Server-side API checks proposed; proof required.”**
* Resident-access row: state **“Supported non-digital routes required; implementation untested”** for all options, rather than making resident agency look like an Azure-only differentiator.

Keep “no winner scored” and the common-basis evidence gap. If longer cells do not fit, abbreviate the product names in a legend rather than reduce the table text.

**Evidence/source:** Slide-18 image and notes; addendum, “Comparable Implementation Options”, “Fit to the BRD Controls” and “Evidence Needed Before a Platform Decision”; PRD, “Options Gate Scoring Framework”; ADR 0001, “Options still to compare”. The provisional scored ADR illustration is not approval.

**Disposition recommendation:** Retain as Q&A/reference, revise terminology for fair comparison. Do not score a winner or infer a control failure for Excel/business apps without equivalent tests.

### F06 — Correct timing metadata; the actual spoken cut is much shorter

**Slides:** 1–18 / note-budget summary  
**Severity:** Medium  
**Observed:** The extraction labels **all 18 slides “main”** and ends with **“Main notes: 3263 words, about 23.3 minutes at 140 wpm / Appendix notes: 0 words.”** This contradicts slides 15–18's explicit Appendix A–D kickers and mixes source citations with speech. It is not a valid 15-minute budget.

Independently counting whitespace-separated words in each note's spoken prose **before “Evidence:”** gives:

| Slide | Words | Slide | Words |
|---|---:|---|---:|
| 1 | 126 | 8 | 108 |
| 2 | 136 | 9 | 126 |
| 3 | 134 | 10 | 89 |
| 4 | 119 | 11 | 79 |
| 5 | 120 | 12 | 78 |
| 6 | 109 | 13 | 145 |
| 7 | 88 | 14 | 143 |

**Main 1–14: 1,600 words** — approximately **11.4 minutes at 140 wpm**, or **12.3 minutes at 130 wpm**, before pauses or interaction. **Appendices 15–18: 501 words** (109/140/132/120). Reading every slide is approximately 15 minutes at 140 wpm before pauses, so it is not a safe full-deck delivery plan.

**Exact proposed change:** Classify slides 15–18 as appendix/reference in the planning/extraction metadata. Count prose and citations separately. Budget **12 minutes for slides 1–14 and 3 minutes for the ask/discussion buffer**, keeping appendices on demand; confirm by an aloud timed rehearsal. Protect at least a minute for slide 14. Do not read source lists aloud. If a demo is added inside the same slot, allocate it explicitly and shorten the main spoken cut.

**Evidence/source:** Current text/notes, especially final summary and Appendix A–D kickers; `docs/reference/memory.md`, “Presentation Guidance”; capstone guide B5 and “How to prepare” (E16).

**Disposition recommendation:** Close iteration-1 timing concern as **script shortened, rehearsal still unverified**. Correct metadata rather than incorrectly report a 23-minute main pitch or automatically cut another 400 words.

### F07 — Frame the opening as an offer and the same planning-only decision as the close

**Slides:** 1 and 14  
**Severity:** Medium  
**Observed:** Slide 1 says “decision first” but offers “back a bounded, evidence-led next stage”, while the specific staff product first appears on slide 4 and the limited decision appears on slide 14. The title's “chasing” is rhetorical, not measured staff pain.

**Exact proposed change:** Replace the opening proposal line with **“Offer: one staff retrofit workbench linking cases, owners and evidence. Today: endorse preparation of its gated evidence-stage proposal.”** Preserve the warmer-homes ambition, with **“Proposed future”** if necessary. On slide 14 add **“Return date: council to agree”** and change the CFO instruction **“Set authority / stop conditions”** to **“Define authority review / stop conditions”** so it cannot be read as granting delivery authority today.

**Evidence/source:** Slides 1/4/14 and notes; primary synthesis, “Decision” and “Customer Offer”; PRD, “Executive Summary”; company profile, “Role and Decision Map” (actual delegations unknown); E07/E08.

**Disposition recommendation:** The iteration-1 ambiguous-spend ask is substantially resolved. Align opening/close and expose the next scheduling decision; do not invent sponsor names, return dates or approvals.

### F08 — Journey cards have edge-flush text and no visible return path

**Slide:** 7  
**Severity:** Medium  
**Observed:** The first card's “INTAKE +” begins near its top edge and its final “rules” sits near the bottom edge; card padding is visibly less generous than its neighbours. The four stages read as a linear sequence although returned work is important to the process.

**Exact proposed change:** Shorten the first card to **“INTAKE + PRIORITISE / Resolve identity • approved ranking”** and equalize internal padding across all four cards. Add a small labelled backward connector **“Defects or changed evidence → owned re-review”** from verify/close towards the appropriate earlier stage, or replace part of the lower strip with this explicit return mechanism. Preserve independent QA, resident handover and separate financial closure in narration.

**Evidence/source:** Slide-7 render; slide notes; addendum EXA-002/008; PRD, “Executive Summary”, CON-003/007 and lifecycle/return intent (E06/E08).

**Disposition recommendation:** Fix padding before presentation; strengthen the process-change story without adding a fifth dense card.

### F09 — “Contracts” and title lengths obscure the product headline

**Slides:** 4 and 10  
**Severity:** Low  
**Observed:** Both titles wrap to an isolated final word (“agents”; “cloud”), consuming a second line without adding hierarchy. Slide 4's “Reuse the contracts” can mean existing supplier contracts rather than reusable API/data/test contracts.

**Exact proposed change:** Slide 4 title: **“One retrofit workbench—not five autonomous agents.”** Lower line: **“Reuse the data and API contracts. Prove the controls. Platform choice is not corporate approval.”** Slide 10 title: **“Prove security; do not assume it from cloud hosting.”**

**Evidence/source:** Images 4/10; ADR 0001 “Context”; addendum EXA-007 (a fictional call-off does not establish actual procurement authority); E08/E09.

**Disposition recommendation:** Editorial cleanup; keep the honest controls/assurance distinction.

### F10 — The CFO example needs an explicit product-cost boundary

**Slide:** 11  
**Severity:** Low  
**Observed:** The fictional arithmetic is correct and prominently labelled. Nevertheless, it is the only large monetary visual in a pitch asking for a product stage; a listener could mistake it for the workbench cost.

**Exact proposed change:** Add **“Illustrative retrofit-home cash fixture—not workbench price”** beside the illustrative-economics label. Keep the £20,000/£7,500/£12,500 and contingency arithmetic. State once in notes: **“Technology whole-life cost remains unassessed and belongs in the return pack.”**

**Evidence/source:** Slide-11 render/notes; addendum EXA-010/015 and “Numerical Targets and Attribution”; addendum “Illustrative Economics” separates underlying programme and technology costs; E06/E14.

**Disposition recommendation:** Retain the example. No budget, quote, grant receipt or cashable saving should be invented.

### F11 — Funding language and review status should match the planning stage

**Slides:** 13 and 17  
**Severity:** Low  
**Observed:** Slide 13's imperative “Fund evidence in gates” is more immediate than slide 14's planning-only decision, despite its qualifying footer. Slide 17 says independent review is still pending even though iteration-1 review exists and this review is now being supplied.

**Exact proposed change:** Slide 13 title: **“Prepare the evidence stage around four decision gates.”** Slide 17 line: **“Independent findings recorded; closure and timed rehearsal pending.”** Do not imply that this read-only review closes implementation, full capstone or user-acceptance gates.

**Evidence/source:** Slides 13/14/17; current notes; iteration-1 report; PRD “Current v0.13.0 Candidate Handoff”; capstone guide B5/B6.

**Disposition recommendation:** Maintain as draft-status housekeeping; separate review performed from findings resolved.

## 4. Full visual and storytelling coverage

All 18 images were inspected individually. “Retain” below means no additional actionable visual defect beyond the findings above, not production approval.

| Slide | Assessment / recommended disposition |
|---|---|
| 1 | Strong contrast and memorable mission framing; offer/ask alignment needed (F07). |
| 2 | Retain. Hypothesis wording (“may bind”) and evidence qualification are appropriate; three findings are readable. |
| 3 | Retain. Four paired lenses fit. Notes name the eight instruments; footer explicitly rejects interviews/approval. Say that distinction aloud early, not only via the footer. |
| 4 | Product is materially clearer; title and “contracts” wording need polish (F09); main-slide superiority mechanism still needed (F03). |
| 5 | Revise before council use: panel overflow and incomplete user/proposal return semantics (F01/F02). |
| 6 | Retain adoption approach and hypothesis restraint; add short mechanism contrast (F03). No visible overflow. |
| 7 | Complete journey is understandable, but first-card padding and return path need work (F08). |
| 8 | Clean current layout; no crowding/collision. Revise access and service-principle semantics (F04). |
| 9 | Retain. Clear two-capability distinction and conspicuous human authority boundary; no task benefit asserted. “No invented facts” should be spoken as a requirement, not model infallibility. |
| 10 | Retain proposed-controls/assurance-open content; shorten title (F09). No certification or verified deployment claim inferred. |
| 11 | Correct fictional arithmetic and readable numbers; distinguish retrofit fixture from product price (F10). |
| 12 | Retain. “AI dividend” presumption is removed. Programme/capability comparisons and no-results wording are clear. |
| 13 | Readable four-gate structure; align title with preparation-only ask (F11). |
| 14 | Strong bounded close with clear executive actions; agree return date and authority-review wording (F07). |
| 15 | Retain as appendix. Readable technical patterns, explicitly target/proposed; not observed controls. |
| 16 | Retain as appendix. Useful objections and reversal conditions; no assumed budget or launch permission. |
| 17 | Retain provenance distinctions; update review status (F11). |
| 18 | Table fits and is suitable for close-view Q&A/reference, not a fast spoken walkthrough. Fairer terminology and comparator scope needed (F05). |

The forest/cream/gold palette, generous outer margins and repeated rounded-panel motif are coherent. Essential evidence distinctions often live in relatively small footers; state the consequential distinction aloud and place it near the claim when ambiguity is material. There is no need for more decoration, more technology logos or fabricated performance charts.

### Iteration-1 finding dispositions

| Prior issue | Iteration-2 assessment |
|---|---|
| Ambiguous council approval/spend ask | Substantially addressed by slide 14 and notes; residual opening/funding/authority wording in F07/F11. |
| Missing comparable options framework | Addressed by new slide 18; fairness and terminology revisions in F05. This is still not a completed appraisal. |
| Workbook failure modes asserted as facts | Addressed on slide 6: case fact and hypotheses now explicit. Do not reintroduce categorical Excel failure claims. |
| 15-minute risk | Spoken main cut is now 1,600 words; metadata is wrong and rehearsal still absent (F06). |
| Presumed AI dividend | Addressed on slide 12. |

## 5. Delivery guidance for the moments that matter

* **Opening/close (Sergeant + Evangelist):** Upright, still posture and a deliberate pause after the exact planning decision. Use “the offer is” and “today's action is”; warm confidence, not urgency to spend. One purposeful open-hand gesture for the proposed future, then no pacing while the council considers the ask.
* **Diagram/options (Scientist):** Stand to the side, move only to trace the case/API/review flow, and slow the voice. Use “the proposed process is” and “the proof still required is”. Avoid rapid acronym delivery or treating a diagram as deployed evidence.
* **Resident/service moment (Therapist):** Open gestures and a warmer facial expression; say “let us understand what people need”. Do not perform the house slogan as a resident quote. Explicitly separate supported contact from consent.
* **CFO question:** Stay still, restate whether the question concerns retrofit cash or technology cost, and answer that question first. The supported answer to “how much better/cheaper?” is “not measured; here is the equal-scope test”, not a speculative benefit.
* **Dress:** Use business-appropriate council attire consistent with the setting; avoid a theatrical “epic” costume or styling that weakens the stewardship/assurance message.

These are recommended delivery choices, not observed presenter behaviours or a rehearsed timing pass.

## 6. Evidence gaps, risks and next decision

### Evidence integrity

No fabricated staff interviews, real resident testimonials, measured company outcomes, actual grants, cost savings, certification or production acceptance were found in the reviewed factual core. The eight role agents are consistently identified as research instruments. v0.12 exercise acceptance is separated from the v0.13 candidate; pinned #58 feasibility is separated from current deployment/control proof and net benefit. Regulatory currentness is explicitly unrefreshed.

The source-backed architecture decision is **exercise direction plus proposed design**, not a settled customer procurement decision. The unanswered financial/benefit questions should remain unanswered until measured; they are not a reason to invent an “epic” ROI.

### Source provisions read

In addition to all current review materials:

* `docs/case_study_48_original.md`: full original request.
* `docs/case_study_48_addendum.md`: Purpose/Status; Owner-Approved Exercise Baseline, EXA register and numerical attribution; Subsequent Application Exercise Builds and Current Learning; Proper Warm/Business Challenge; Executive Assessment/Regulatory Evidence; Modernised Objective/Solution; Implementation Options and related control/value/evidence sections; Trade-Offs/Business Case/Recommended Executive Decision.
* `docs/reference/README.md`: knowledge-base routing and evidence catalog.
* `docs/reference/research/company/company-profile-research.md`: confirmed information, modelled profile and Role/Decision Map.
* `agent-request-challenge.md`: Purpose/Method, Summary, shared foundation/value and limitations.
* `agent-what-if-study.md`: Purpose/Method and Summary of Revised Verdicts.
* `pilot-measurement-challenge.md`: Purpose/Method, Summary, Owner Decision, measurement/analysis/effort and guardrails.
* PRD `proper-warm-retrofit-programme-demonstrator.md`: front matter, Executive Summary, exercise authority, product/platform boundary, Options Gate, simplicity/adoption, constraints, relevant acceptance criteria including AC-057 and current/historical handoff status.
* ADR 0001: status/current applicability, context/decisions/access, transition/measures/options and provisional appraisal; ADR 0002: status/current applicability, decisions and durable-store design.
* `docs/ideas/typesafe-system-one-agent-fit.md`: status, pinned feasibility/parallel experiment and Decision 1 reassessment/product limits.
* UX `proper-warm-prototype-profile-review.md`: evidence boundary, accessible human validation, owner feedback and proposed UX checks; `prototype-learnings-and-simplicity-review.md`: continuing learning, complexity, simplification and preserved controls.
* Sector primer purpose/evidence/association context; regulatory source register authority/current-use sections; project memory presentation guidance; complete capstone assessment guide; capstone storage map and artifact registry.

No external legal/product refresh, runtime reinspection, PPTX inspection or private exercise answer-key access was performed.

### Next decision and acceptance conditions

1. Resolve F01 and improve the material comprehension issues F02–F08; apply low-severity edits where useful.
2. Re-render the affected slides, especially **5, 7, 8 and 18**, and inspect the changed images for new wrapping/connector/cell problems.
3. Correct the main/appendix speech budget and perform an aloud 15-minute rehearsal with a protected decision window.
4. Present as a **draft planning proposition**, with named sponsor/control-owner nominations and a council-agreed return date still to be decided.

This review does not ratify the narrative as approved, clear capstone floors, close security/privacy/legal gates, authorize billable work or validate live user acceptance. **Stop at the planning endorsement; return with comparable options, scoped cost/authority, reviewed requirements and separately evidenced acceptance/stop tests.**
