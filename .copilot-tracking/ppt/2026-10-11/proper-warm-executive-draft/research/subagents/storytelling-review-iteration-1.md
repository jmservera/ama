# Proper Warm executive draft — independent storytelling review

**Review date:** 2026-10-11  
**Scope:** Review only. Examined the 17-slide rendered `render-final-2` contact sheet, actual PPTX text/notes, `primary-research.md`, `evidence-register.md`, and supporting case-study, company-research, PRD, ADR and research-synthesis sources. No slides were changed and nothing was published.

## Overall verdict

**PARTIAL PASS — strong, credible evidence-led story; resolve the decision-ask and Excel-comparison gaps, qualify the “before” claims, and time the spoken version before presenting.**

The presentation clearly reframes the five-agent request as a controlled workbench with bounded assistance. The architecture is legible and decision-consistent as a target design, and the deck carefully distinguishes owner direction, proposed design, generated exercise data, narrow pinned PR #58 feasibility, and unproved benefit/readiness. The candidate v0.13 PRD is not portrayed as accepted; the PR #58 observations are qualified as narrow and not runtime-reverified.

The review did not find fabricated staff interviews, resident views, corporate approvals, measured company outcomes, or financial commitments. The evidence register and notes consistently identify the eight role agents as research instruments and keep company unknowns visible. Resident consent, non-digital routes, independent human gates and safety routing are prominent. The mixed-council sequence is effective: decision-first opening/close (Sergeant), evidence and controls (Scientist), and resident agency (Therapist). The future-state/“epic” note is present but deliberately restrained; that is appropriate for credibility.

## Actionable concerns

### 1. Make the council decision unambiguous

**Slide:** 14 (reinforced by 13)  
**Severity:** High  
**Concern:** “Back the next stage” sounds like an approval, while the slide also says “proposal, not approval” and “no production or spend approval.” Notes ask the council to sponsor, name owners, and set an affordability envelope, but do not resolve whether today’s requested action is endorsement of planning, authorization to spend, or a future decision after v0.13 review. “Authorize planning around the reviewed candidate” is particularly unclear because v0.13 is still pending fresh review and owner acceptance.

**Suggested edit:** Replace the title/ask with a bounded, immediately answerable decision, for example: **“Today: endorse preparation of a gated evidence stage—not delivery spend or production.”** Add a compact “Council action” strip naming the requested sponsor and owner nominations, the required return pack (reviewed PRD, scoped cost/authority, acceptance evidence and stop conditions), and the decision point/date to be agreed. Say explicitly that no deployment, procurement, or new spend is being authorized today. Do not invent names, delegated authority or a date; mark them “to be agreed” if unknown.

**Evidence:** Draft slides 13–14 and their notes; `docs/prds/proper-warm-retrofit-programme-demonstrator.md` front matter/Executive Summary (v0.13 candidate pending fresh review and owner acceptance); `docs/case_study_48_addendum.md`, “Subsequent Application Exercise Builds” (effective scoped budget/authorization required; no new spending authorization); ADR 0001, “Options still to compare.”

### 2. Complete the requested Excel/platform comparison

**Slide:** 6 (and 4); companion artifact not present in the reviewed draft folder  
**Severity:** Medium  
**Concern:** Slide 6 is a useful mechanism-level “workbook control vs proposed control” contrast, but it does not compare Excel-only improvement against M365/business-platform and Azure-led hybrid options on common criteria. Slide 4 labels those options “still to appraise,” and no companion Excel comparison workbook or equivalent options matrix appears in the reviewed package. This leaves the architecture choice credible as an exercise direction, but not yet persuasive as a comparative council choice.

**Suggested edit:** Provide the requested one-sheet Excel comparison or an equivalent clearly labeled appendix matrix. Compare Excel-only, M365/business-platform, and Azure-led hybrid against the same criteria (workflow/evidence control, permissions, migration/dual-entry risk, resident/safety gates, integration, cost/whole-life effort, and readiness). Mark unknown cost, tenant capability and evidence as **“not yet assessed”**; state owner/evidence needed and avoid scoring a winner without comparable appraisal. On slide 6, distinguish the current case-study fact (spreadsheets are used) from hypothesized workbook limitations.

**Evidence:** `docs/adrs/0001-azure-architecture.md`, “Hybrid M365 and Excel transition” and “Options still to compare”; `docs/case_study_48_addendum.md`, “Implementation Options and Provisional Platform Recommendation” and OQ-012; `docs/case_study_48_original.md`, “Business Challenge” (spreadsheet use, not a measured Excel-control baseline); draft slides 4 and 6.

### 3. Label the “before” mechanisms as hypotheses, not established company findings

**Slide:** 6  
**Severity:** Medium  
**Concern:** The visible “BEFORE • WORKBOOK CONTROL” statements—“Repeated status reconciliation” and “Evidence assembled at handoffs”—read as observed Proper North Homes facts. The case establishes spreadsheet-based management by a small team, but the reviewed sources do not establish these exact failure modes or quantify their prevalence. “Manual baseline: not measured” helps, but does not fully qualify the two categorical statements.

**Suggested edit:** Rename the panel **“CURRENT-STATE HYPOTHESES TO VALIDATE”** and phrase the items as questions, e.g. “Where is status reconciled repeatedly?” and “Where is evidence reassembled at handoff?” Keep “baseline not measured.” In narration, say these are discovery hypotheses, not findings about staff performance.

**Evidence:** `docs/case_study_48_original.md`, “Business Challenge”; `docs/reference/research/company/pilot-measurement-challenge.md`, “Owner Decision” and “Proposed Measurement Design” (instrumented baseline/comparable measurement required); draft slide 6 and `evidence-register.md` E01/E05.

### 4. Protect the 15-minute limit with a timed, trimmed spoken cut

**Slides:** 1–14 (appendices 15–17 are appropriate as Q&A/reference)  
**Severity:** Medium  
**Concern:** The extracted notes report **1,991 spoken words** for the 14 main slides, excluding citations. That is about 13.3 minutes at 150 words/minute and 15.3 minutes at 130 words/minute before visual pauses, transitions or audience interaction. No timed rehearsal is evidenced. The content is careful, but the full notes are unlikely to leave reliable room for pauses or the council decision.

**Suggested edit:** Rehearse aloud with a timer. If the limit includes the full pitch, target roughly 1,650–1,750 spoken words and reserve explicit time for the decision/brief discussion; put detailed implementation and repeated caveats in appendix notes. Add per-slide time budgets and protect the ask on slide 14 from being rushed. Do not claim the timing is validated until rehearsed.

**Evidence:** `research/final-pptx-text-and-notes.md`, opening word-count statement (1,991 main-note words); `docs/reference/memory.md`, “Presentation Guidance” (15-minute limit and time rehearsal); draft has 14 main slides and three Q&A/reference appendices.

### 5. Avoid presuming an “AI dividend”

**Slide:** 12  
**Severity:** Low  
**Concern:** “Prove the transformation—and isolate the AI dividend” rhetorically presumes a positive AI return, while the slide body and notes correctly say no results exist and a negative result is useful.

**Suggested edit:** Use **“Measure programme change—and test any AI contribution”** or **“Prove the transformation; test whether AI adds value.”** This preserves the distinction between programme impact and task-level AI contribution without implying the result.

**Evidence:** `docs/reference/research/company/pilot-measurement-challenge.md`, “Owner Decision” and “Proposed Measurement Design”; `docs/ideas/typesafe-system-one-agent-fit.md`, “Observed Feasibility and Parallel Value Experiment”; draft slide 12 explicitly says “NO RESULTS CLAIMED.”

## Checks that passed

- **Request and research:** Slide 1 summarizes the 60,000-home request and bounded proposal; slides 2–3 explain the research shift and name all eight role-agent lenses in speaker notes. The notes explicitly say role agents are not staff interviews or approvals.
- **Architecture and AI-vs-Excel calibration:** Slides 4–5 present an understandable API-centered target diagram; notes identify it as target/proposed, not deployed. Slides 9–10 correctly separate typed selection and cited generation from authority, and narrow PR #58 feasibility from full workflow acceptance, model quality/value, and readiness.
- **Resident value and controls:** Slide 8 and its notes separate contact preference, adjustment and measure-specific consent; preserve non-digital access and human hazard intake; and label owner UX feedback as unvalidated. Independent safety, technical, QA, funding and payment decisions are retained.
- **Economics and evidence:** Slide 11’s fictional cash arithmetic matches EXA-010/015 and is labeled as neither budget nor cash receipt. Slides 12–13 describe proposed comparisons and gates without presenting results. Slide 17 and the evidence register expose provenance and limits.
- **Visual/story structure:** The 17 rendered slides are coherent and visually consistent; the architecture diagram is simple enough for an executive overview. The sequence moves from bottom line, through evidence and mechanisms, to resident value, proof gates and ask, with appendix slides suited to Q&A.
- **Readiness restraint:** The deck preserves the historical v0.12 acceptance versus pending v0.13 review distinction and does not promote #58 into company performance, production readiness or a new spend authorization.

## Recommended disposition

Resolve findings 1–3 before using this as a council decision deck. Complete or explicitly defer the Excel comparison as a separate deliverable. Time and trim the spoken script before asserting it fits 15 minutes. The evidence/storytelling foundation is sound; these changes would make the requested action and option trade-off as disciplined as the technical and resident-control narrative.
