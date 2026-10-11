"""Author a NEW YAML-driven executive draft; rendering uses the HVE builder."""
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).parent
FOREST, CREAM, MOSS, WARM, INK = "#173F35", "#F7F2E7", "#D5E2D4", "#E5B96A", "#183A31"
WHITE, MUTED = "#FFFFFF", "#446056"
STYLE = {
    "dimensions": {"width_inches": 13.333, "height_inches": 7.5, "format": "16:9"},
    "layouts": {"blank": 6},
    "metadata": {"title": "Proper Warm — Council working draft", "author": "AMA project",
                 "subject": "Bounded next-stage proposal; not production approval",
                 "keywords": "Proper Warm, retrofit, council, draft, evidence", "category": "Executive proposal"},
    "defaults": {"speaker_notes_required": True},
    "themes": [{"name": "proper-warm", "slides": list(range(1,18)),
                "colors": {"forest": FOREST, "cream": CREAM, "moss": MOSS, "warm": WARM}}],
}

SOURCES = {
 "E01": "docs/case_study_48_original.md — Business Challenge; Agentic Architecture Brief; Expected Outcomes (2026-09-10, immutable request)",
 "E02": "docs/case_study_48_addendum.md — Business Challenge; Regulatory Evidence and Service Design; Proper Warm at Proper North Homes (2026-10-11, maintained proposal)",
 "E03": "docs/reference/research/company/agent-request-challenge.md — Purpose and Method; Summary (2026-09-26, role-agent hypotheses)",
 "E04": "docs/reference/research/company/agent-what-if-study.md — Purpose and Method; Summary of Revised Verdicts (2026-09-27, role-agent hypotheses)",
 "E05": "docs/reference/research/company/pilot-measurement-challenge.md — Summary; Owner Decision, 2026-09-26; Proposed Measurement Design (2026-09-26, proposed comparisons)",
 "E06": "docs/case_study_48_addendum.md — Owner-Approved Exercise Baseline (2026-10-10); EXA-001/002/004/005/008/010/011/012/013/015/016; Numerical Targets and Attribution (historical accepted exercise assumptions)",
 "E07": "docs/case_study_48_addendum.md — Subsequent Application Exercise Builds (2026-10-11); Current Learning and Parallel Experiment (owner direction; feasibility not benefit)",
 "E08": "docs/prds/proper-warm-retrofit-programme-demonstrator.md — front matter; Executive Summary; CON-009/AC-057 (v0.13.0 candidate 2026-10-11; historical v0.12.0 accepted 2026-10-10)",
 "E09": "docs/adrs/0001-azure-architecture.md — Exercise Applicability (2026-10-11); Decisions; Hybrid M365 and Excel transition; Options still to compare (proposed)",
 "E10": "docs/adrs/0002-pilot-readiness-architecture.md — Exercise Applicability (2026-10-11); Decisions; 1. Durable store (proposed readiness design)",
 "E11": "docs/ideas/typesafe-system-one-agent-fit.md — Observed Feasibility and Parallel Value Experiment (2026-10-11); Microsoft Decision 1 Reassessment (2026-10-10). PR #58 pinned 5136f192d583a5bf53adeeec4b0f21369b005c9d; inspected in maintained documentation 2026-10-11, not runtime reverified",
 "E12": "docs/reference/research/ux/proper-warm-prototype-profile-review.md — Owner Usability Feedback (2026-10-07); Proposed Acceptance Checks UX-01 to UX-08 (reported impressions, unexecuted checks)",
 "E13": "docs/reference/research/ux/prototype-learnings-and-simplicity-review.md — Continuing MVP Learning (2026-10-11); Consensus simplification (synthesis, not acceptance)",
 "E14": "docs/reference/research/company/company-profile-research.md — Confirmed Company Information; Modelled Customer Profile; Role and Decision Map (2026-09-26; not-for-profit owner-confirmed, other attributes modelled)",
 "E16": "docs/reference/method/ama-capstone-assessment-guide.md — Sections A-D; How the outcome is determined; How to prepare (2026-09-30 published rubric)",
}

def txt(text, x, y, w, h, size=18, color=INK, bold=False, font="Aptos"):
    return {"type":"textbox", "left":x, "top":y, "width":w, "height":h, "text":text,
            "font":font, "font_size":size, "font_color":color, "font_bold":bold,
            "margin_left":0, "margin_right":0, "margin_top":0, "margin_bottom":0,
            "word_wrap":True}

def panel(text,x,y,w,h,fill=FOREST,size=20,color=CREAM,shape="rounded_rectangle"):
    return {"type":"shape","shape":shape,"left":x,"top":y,"width":w,"height":h,
            "fill":fill,"text":text,"text_font":"Aptos","text_size":size,
            "text_color":color,"text_bold":False,"alignment":"left",
            "vertical_anchor":"middle", "margin_left":0.22,
            "margin_right":0.22,"margin_top":0.14,"margin_bottom":0.14,
            "auto_size":"none", "line_spacing":1.05}

def home(text,x,y,size,fill):
    """Editable native house silhouette with upright label; intentional containment."""
    body=panel("",x,y,size,size,fill,shape="pentagon")
    body.pop("text")
    body["rotation"]=270
    label=txt(text,x+.18,y+size*.42,size-.36,size*.48,15 if size<2 else 28,INK,True)
    return {"type":"group","name":"Editable home motif","left":x,"top":y,"width":size,"height":size,
            "elements":[body,label]}

def arrow(x,y,w=.45,h=.45):
    return {"type":"shape","shape":"chevron","left":x,"top":y,"width":w,"height":h,"fill":WARM}

def base(n,title,kicker,footer,dark=False):
    color=CREAM if dark else INK
    return [txt(kicker.upper(),.65,.6,12,.3,11,WARM if dark else MUTED,True),
            txt(title,.65,1.22,12,1.25,38,color,True,"Aptos Display"),
            txt(f"{n:02d}  /  PROPER WARM     •     {footer}",.65,6.7,12,.28,11,color)]

def three(items,y=2.85,h=2.75):
    return [panel(t,.65+i*4.12,y,3.79,h, FOREST if i!=1 else MOSS,20,CREAM if i!=1 else INK)
            for i,t in enumerate(items)]

def two(items,y=2.85,h=2.85):
    return [panel(items[0],.65,y,5.85,h,FOREST,21),panel(items[1],6.85,y,5.8,h,MOSS,21,INK)]

SLIDES = [
{
 "title":"From chasing spreadsheets\nto delivering warmer homes",
 "kicker":"Council draft • decision first",
 "footer":"REQUEST + PROPOSAL • E01/E02/E07 • 11 Oct 2026",
 "layout":"hero", "refs":["E01","E02","E07","E14"],
 "notes":"""Proper Warm began with a request to coordinate a complex retrofit programme across sixty thousand homes using five agents, rather than asking a small team to hold everything together in spreadsheets. Our ambition is more compelling than faster administration: every home should have a clear next step, an accountable owner and evidence that survives the handoff.

Today I am asking the council to back a bounded next stage, not a production rollout or accelerated capital commitment. For the CEO, that is confidence in the mission. For Assets, it is a defensible route to accepted handover. For Finance, it is visibility of commitments, exposure and evidence before money moves. The promise is one programme, one evidence trail, human control. The measurable benefits still have to be earned."""
},
{
 "title":"Research changed the question",
 "kicker":"What we found", "footer":"RESEARCH HYPOTHESES • E02/E03/E04 • 26–27 Sep 2026",
 "layout":"research","refs":["E02","E03","E04","E14"],
 "notes":"""The original question was which agents to build. The research asked what actually prevents safe, accepted completions. Spreadsheet dependence is in the case, but it is not proof that administration is the binding constraint. Capital, competent assessors, supplier capacity, access, evidence quality and downstream assurance may matter more.

The role challenge found that every end-to-end agent request mixed deterministic controls, accountable decisions and narrower AI tasks. Richer photos, invoices and sensor inputs did not change that division. Better inputs cannot create consent or professional acceptance.

Our conclusion is to build a shared coordination and evidence foundation, then add assistance where comparative tests show net benefit. The regulatory material is a dated research set. The current register distinguishes final energy policy from proof of a commenced landlord duty. We have not refreshed legal currentness for this pitch."""
},
{
 "title":"We challenged the gaps—not just the technology",
 "kicker":"Who we asked", "footer":"ROLE AGENTS ≠ STAFF INTERVIEWS OR APPROVALS • E03/E05/E06/E12",
 "layout":"roles","refs":["E03","E05","E06","E12"],
 "notes":"""Eight documented role agents challenged the request: Assets, Programme, Finance, Procurement, Resident Engagement, Building Safety, Data and Performance, and the Neighbourhood Housing Officer. Each brought a different failure question. Who approves the investment? Who accepts quality? Who owns a pending handoff? What happens when a resident cannot use a digital channel? Does faster activity simply move the queue elsewhere?

These were research instruments using sector-informed hypotheses, not employee interviews or corporate approval. The measurement challenge forced us to separate programme change from AI contribution.

Later, Programme, Finance, Resident Engagement and Data instruments proposed reconciled exercise assumptions. The project owner accepted the v0.12 baseline on 10 October. Owner UX feedback separately asked for visible readiness, ownership and agent purpose. None of that substitutes for direct staff or resident validation, or acceptance of the current candidate."""
},
{
 "title":"The choice: a control plane with bounded assistance",
 "kicker":"Architecture decisions", "footer":"OWNER DIRECTION + PROPOSED DESIGN • E07–E10 • 11 Oct 2026",
 "layout":"choices","refs":["E03","E07","E08","E09","E10"],
 "notes":""" We chose a home-centred controlled workbench over five end-to-end agents. Deterministic rules govern ranking, permissions, transitions and independent gates. AI returns inspectable proposals, not alternative writes.

Azure SQL and Blob address durable state and versioned evidence; a single controlled API coordinates changes. Actual Azure hosting, real SQL and real AI are mandatory in subsequent accepted application exercise deliveries. That is owner direction, not a conclusion that Azure has already won a corporate procurement appraisal.

We rejected a mounted JSON file as the delivery foundation because whole-file writes cannot supply dependable concurrent transitions. Excel-only improvement and M365 or business-platform approaches remain alternatives to cost on a comparable basis before production selection. An Azure-led hybrid is the current exercise path, with one-way imports and eventual read-only Excel reporting. Premium isolation, separate workers and production identity remain proposed gates, not facts about the observed deployment."""
},
{
 "title":"One controlled route from evidence to action",
 "kicker":"Simple architecture • editable native diagram",
 "footer":"TARGET CONTROL DESIGN—NOT A DEPLOYED TOPOLOGY • E08/E09/E10",
 "layout":"architecture","refs":["E08","E09","E10","E11"],
 "notes":"""Read this diagram from left to right. Existing spreadsheets and other verified source systems supply assertions through a controlled import. Ambiguous identities and conflicting mandatory facts go to quarantine rather than being silently merged. Staff use a role-based workbench over one API, which checks identity, scope, evidence versions and each independent approval before committing a change.

SQL holds connected cases, state and audit references; Blob holds versioned evidence. Deterministic orchestration schedules and records work through the controlled route. The AI task boundary receives only permitted inputs and returns typed selections, cited drafts or raise-only concerns for human review. It has no authority to commit programme decisions.

For a proposed full production topology, identity, workload separation, private access, monitoring and recovery need their own assurance. The narrower observed feasibility does not prove every box or connection here. The architecture is valuable because a failed model can leave human work available without removing any gate."""
},
{
 "title":"Excel stays useful. It stops being the control system.",
 "kicker":"Mechanism before marketing",
 "footer":"PROPOSED SUPERIORITY—PAIRED PROOF STILL REQUIRED • E05/E09/E12",
 "layout":"comparison","refs":["E01","E05","E09","E12"],
 "notes":""" Excel is familiar and useful for reporting. The problem is relying on a workbook to hold a connected programme's authority, evidence and commitments across teams.

The proposed workbench connects the home, building, package and case; separates sent, received and accepted handoffs; and preserves the evidence version behind a decision. Server-enforced permissions, independent acceptance gates and an audit trail make the control basis explicit. Capacity and gross cash exposure can be viewed against the same case state rather than reconciled separately.

Those are mechanisms to test, not measured time savings. We need paired tasks using identical inputs and outcomes, counting review, correction and recording effort. During migration, one-way imports, reconciled snapshots, named quarantine ownership and a time-bounded cutover avoid permanent dual entry. Excel can become an API-fed read-only report. The actual manual baseline and tenant capability remain unknown."""
},
{
 "title":"A home moves forward only when the evidence does",
 "kicker":"The connected operating journey",
 "footer":"EXERCISE JOURNEY + INDEPENDENT GATES • E06/E08 • NOT LIVE WORK",
 "layout":"journey","refs":["E06","E08","E12"],
 "notes":""" Follow one home. Establish identity and intake evidence, then assess technical scope and resident choices. Verify funding, competent capacity and release authority. Provider completion still requires independent quality acceptance and resident handover. Financial closure needs separate evidence.

Our deliberate exception is conflicting EPC evidence. The case stays explicit about what is unknown, which dependent review becomes stale and who must resolve it. A correction should invalidate the affected decisions, not wipe out unrelated work or transfer approval to a sibling case.

Ownership matters at every transition. Sending a handoff does not mean it was accepted: a chase owner and resident-update owner remain visible. This connected exercise can demonstrate control behaviour with fictional records. It cannot show that a real survey, consent conversation, contractor instruction or payment has happened. Accepted handover—not a start count—is the outcome we ultimately want to improve."""
},
{
 "title":"Warmer homes must also mean more resident control",
 "kicker":"Resident value • dignity by design",
 "footer":"PROPOSED SERVICE + OWNER-REPORTED UX • E06/E12 • VALIDATION PENDING",
 "layout":"resident","refs":["E06","E12","E14"],
 "notes":""" A resident should understand what is proposed, what happens next, who is responsible and how to get support. Safe phone, letter, text, email and officer-assisted routes prevent a compulsory resident portal.

Contact preference, accessibility adjustment and consent to a particular measure are separate records. Silence, an appointment or a phone number is not consent. Providers should receive the necessary task and adjustment instructions, not sensitive reasons or diagnoses. A hazard report must reach an accountable human route independently of routine retrofit scheduling or AI availability.

The owner asked for contextual queues, full-case working space, visible blockers and ownership, and a clear explanation of what assistance will do with data. These are reported design learnings, not validated resident outcomes. Direct accessible staff and resident research, privacy review and tested non-digital service remain gates before operational adoption."""
},
{
 "title":"AI prepares the decision. People own it.",
 "kicker":"Two capabilities • one authority boundary",
 "footer":"REAL FEASIBILITY ≠ TASK BENEFIT • E07/E11 • 11 Oct 2026",
 "layout":"ai","refs":["E03","E07","E08","E11"],
 "notes":"""We distinguish typed scoring from text generation. Decision 1 can select from supplied, source-bound candidates or support a bounded evidence check only when its actual task fit is verified. It should expose no-match or uncertainty rather than invent a missing value. A real Foundry generative task can assemble a cited narrative from approved inputs. That narrative is still a draft.

Neither capability owns priority policy, regulatory satisfaction, consent, technical approval, grant submission, quality acceptance or payment. The API enforces that boundary. Individual manual access does not waive required real AI in an application delivery.

Documented feasibility includes source-bound EPC selection and cited generation. Benefit, calibration and broader screening remain unproved. The binary adapter cannot establish a three-class screening score. The parallel experiment is not completed evidence."""
},
{
 "title":"A real foundation exists. Readiness is still a gate.",
 "kicker":"What we can honestly claim",
 "footer":"PINNED #58 DOCUMENTED FEASIBILITY • E07/E08/E11 • 11 Oct 2026",
 "layout":"status","refs":["E07","E08","E10","E11"],
 "notes":"""Maintained main-branch documentation pins a separate PR's observed Azure SQL and Blob deployment, source-bound Decision 1 selection and cited GPT-4.1-mini generation. We use that as recorded feasibility, not as permission to import the branch or claim its whole source is merged.

Later source-tested controls must not be assumed to exist in the deployed image. Full connected workflow, user identity and permissions, cloud performance and recovery, comparative model value and direct human acceptance remain separate gates. This deck does not re-run or regrade those tests.

Keep the data scales distinct: the continuing sixty-thousand-home stock and nine-hundred-and-eighty-case programme lineage are generated exercise data. The single-home story and smaller evaluation cohorts are tests, not replacement records or evidence of company performance. The current v0.13 requirements candidate still needs fresh review and owner acceptance. Confidence comes from showing precisely what remains to be proved."""
},
{
 "title":"The CFO test: cash exposure before grant optimism",
 "kicker":"Illustrative economics • not a corporate budget",
 "footer":"FICTIONAL EXA-010/015 ARITHMETIC • E06 • ACCEPTED EXERCISE 10 Oct 2026",
 "layout":"finance","refs":["E06","E07","E14"],
 "notes":"""Use the deliberately fictional home-level example to see what the ledger must make visible. Base cost is twenty thousand pounds: eighteen thousand contractor cost plus two thousand internal allocation. The selected exercise grant is seven thousand five hundred, leaving twelve thousand five hundred provider funding at base. A two-thousand contingency raises the gross envelope to twenty-two thousand and provider exposure to fourteen thousand five hundred if fully spent.

The important distinction is timing. Before grant cash arrives, gross base cash exposure remains twenty thousand; an application, award or receivable is not cash. Real eligibility, award terms, contractor obligations and covenant headroom are not established by this fixture.

Technology needs a separate scoped authorization, accrued-cost visibility and stop conditions. The older exercise cap was not automatically carried into the later rebuild, and its override is not perpetual approval. The next stage should measure whole-chain effort and cost per accepted outcome before Finance treats saved time as cashable benefit."""
},
{
 "title":"Prove the transformation—and isolate the AI dividend",
 "kicker":"Measurement, not a success dashboard",
 "footer":"PROPOSED COMPARISONS • E05/E11 • NO RESULTS CLAIMED",
 "layout":"measurement","refs":["E05","E06","E11"],
 "notes":"""There are two decisions to inform. Does the modernised programme improve safe accepted handovers? And does a particular AI capability add value over the same controlled workflow without it? Mixing those questions would allow extra capacity or better records to be sold as an AI benefit.

For programme value, use existing teams, matched localities, identical event capture, a frozen cohort and changes against the instrumented pre-period. Include paused, withdrawn, reopened and incomplete cases; do not average only the easiest completions. Record shared suppliers and displacement so improvement in one area does not hide deterioration elsewhere.

For task value, compare the same inputs pairwise with manual/templates and deterministic rules, measuring errors, full human review and correction effort, latency, cost and uncertainty. Safety, consent, equity, quality and cash remain guardrails. The parallel four-arm model protocol is proposed design, not participant or outcome evidence. A negative AI result is useful: retain the simpler task path and report it honestly."""
},
{
 "title":"Fund evidence in gates—not a leap into production",
 "kicker":"Bounded delivery proposal",
 "footer":"PROPOSED NEXT STAGE • E06–E10 • SCOPE/BUDGET/ACCEPTANCE REQUIRED",
 "layout":"gates","refs":["E06","E07","E08","E09","E10"],
 "notes":"""Gate the next stage around decisions, not service counts. First review and accept the current requirements candidate, name accountable owners, freeze the evidence and test contracts, and record effective scope and spending authority. No missing approval is solved by running another model.

Prove connected case controls on continuing generated data using actual Azure, SQL and registered inference. Show version-linked write, read and restart evidence, independent decisions and negative permission tests. Unit-test mocks cannot establish delivered application acceptance.

Then evaluate net task value and engineering readiness, including accessibility, recovery, performance and accrued costs. Finally return a reviewable evidence pack to the owner with pass, fail, blocked and not-run states. The earlier four-week exercise plan was a software delivery scenario, not a physical retrofit programme or unconditional timetable for this candidate. Only subsequent operational appraisal, real user research and formal control-owner approval could justify a live pilot."""
},
{
 "title":"Back the next stage. Make every handover count.",
 "kicker":"Council decision • proposal, not approval",
 "footer":"DRAFT FOR CHALLENGE • E07/E08/E16 • NO PRODUCTION OR SPEND APPROVAL",
 "layout":"decision","refs":["E05","E07","E08","E16"],
 "notes":"""The decision is to back a bounded next stage with a clear return-to-council test, not to buy a promise of doubled throughput. Ask the CEO to sponsor the mission and require an honest scale decision. Ask Assets to own the accepted-handover outcome and the independent technical and quality boundaries. Ask Finance to agree a separately scoped affordability envelope, liquidity view and stop conditions. The exact corporate delegations still need verification.

Authorize planning around the reviewed candidate; do not infer production adoption, procurement or new spending from this presentation. The evidence pack must show whether the connected workflow works, which assistance earns its cost, and which gates remain unmet. If value is absent, simplify. If controls fail, stop and repair.

Our ambition remains bold: move from chasing spreadsheets to delivering warmer homes with one programme, one evidence trail and human control. The reason to back it is not AI theatre. It is making every handover accountable enough to trust."""
},
{
 "title":"Technical Q&A: isolate failure, preserve control",
 "kicker":"Appendix A • target design, not deployment claim",
 "footer":"PROPOSED PATTERNS + OPEN ASSURANCE • E08/E09/E10/E11",
 "layout":"technical","refs":["E08","E09","E10","E11"],
 "notes":"""Threats include unauthorized writes, stale approvals, cross-case leakage, malicious content in evidence, model hallucination and lost or competing state. Proposed controls are one API write path, server-side role/case/field projections, source-bound inputs, schema validation, independent reviewers, row-version concurrency, idempotent transitions and replayable audit.

SQL indexes and server-side paging/clustering address full-file and full-map mechanisms. Queue-separated workers and private-only access remain proposed topology, not deployed facts. Model failure retains manual work; unsupported source facts stay unknown; retries must not duplicate transitions. Blob versions and SQL metadata must identify exactly which evidence was approved. Recovery, ledger verification, replicas, user identity, leakage/injection tests and legal retention decisions need explicit observed evidence before readiness claims."""
},
{
 "title":"Council Q&A: the objections we welcome",
 "kicker":"Appendix B • answers with reversal conditions",
 "footer":"ALTERNATIVES, AFFORDABILITY, AUTHORITY • E05/E07/E09/E11",
 "layout":"qa","refs":["E05","E06","E07","E09","E11"],
 "notes":"""Why not fix Excel? We should cost that option; the proposed control mechanisms, not familiarity alone, decide the comparison. Why not Power Platform? Tenant/licensing and operational fit are unverified and require equivalent appraisal before production selection. Why buy AI now? Do not buy an assumed benefit; verify access, terms and scoped authority, then run paired task tests. Why not launch from #58? Narrow observed feasibility is not full workflow/control or human acceptance.

What is the budget? No new corporate amount is approved. Historical EXA-012 allocated USD450 per month, reviewed at USD360 and paused at USD405; #58 removed that cap only for its rebuild. Each subsequent build needs an effective scoped approval with accrued liabilities. Stop if controls fail, authority is absent or liabilities exceed the agreed envelope. Simplify any AI task that fails net-value testing; keep required real-platform evidence independent."""
},
{
 "title":"Read the evidence label before reading the claim",
 "kicker":"Appendix C • review and provenance",
 "footer":"AS AT 11 Oct 2026 • REPOSITORY-ONLY • NO NEW LEGAL CURRENTNESS CHECK",
 "layout":"evidence","refs":["E01","E03","E06","E07","E08","E11","E16"],
 "notes":"""Evidence categories: REQUEST is the immutable case ambition; RESEARCH is sector evidence or role-agent hypothesis; EXERCISE is a selected fictional fixture or historical owner-approved baseline; DIRECTION is the current owner's delivery requirement; PROPOSED is design or evaluation not yet accepted; OBSERVED FEASIBILITY is a precisely pinned recorded service result; UNPROVED is benefit or readiness still lacking evidence.

All consequential legal adoption requires fresh official-source verification and professional/control-owner approval. v0.12 acceptance on 10 October does not transfer to v0.13. PR #58 evidence is pinned at 5136f192d583a5bf53adeeec4b0f21369b005c9d in maintained main documentation, not imported source or a re-inspected runtime.

The full capstone guide informed the narrative. A deck cannot establish live delivery, Q&A behaviour, working autonomy, operations or publication floors. Independent strategist review and rehearsal remain pending. Detailed source/provision/date/status references are in notes and research/evidence-register.md."""
}
]

def visuals(s):
    k=s["layout"]
    if k=="hero":
        return [txt("Request: coordinate retrofit across 60,000 homes.\nProposal: back a bounded, evidence-led next stage.",.65,3,7.5,1.05,23,CREAM),
                panel("ONE PROGRAMME\nONE EVIDENCE TRAIL\nHUMAN CONTROL",.65,4.55,7.5,1.4,WARM,23,INK),
                home("Evidence",9,2.95,1.65,MOSS),
                home("Choice",11,2.95,1.65,WARM),
                home("Handover",9.8,4.95,1.4,MOSS)]
    if k=="research":
        return three(["THE CONSTRAINT\nCapital, capacity, access and quality may bind—not just administration.",
                      "THE FOUNDATION\nShared records, clear lifecycle states and accountable handoffs.",
                      "THE AI OPPORTUNITY\nRead, reconcile, draft and flag—inside the controls."]) + [
                      txt("Better inputs do not confer authority. Faster activity is not accepted handover.",.65,6,12,.38,19)]
    if k=="roles":
        return [panel("ASSETS + FINANCE\nInvestment authority • gross cash • attributable value",.65,2.85,5.85,1.35),
                panel("PROGRAMME + PROCUREMENT\nCapacity • professional review • supplier accountability",6.85,2.85,5.8,1.35,MOSS,20,INK),
                panel("RESIDENTS + FRONTLINE\nChoice • safe contact • accepted handoffs",.65,4.6,5.85,1.35,MOSS,20,INK),
                panel("SAFETY + DATA\nHazard route • missingness • independent evaluation",6.85,4.6,5.8,1.35)]
    if k=="choices":
        return three(["CHOSEN FOR THE EXERCISE\nControlled workbench\nReal Azure + SQL + AI\nVersioned evidence",
                      "NOT FIVE END-TO-END AGENTS\nDeterministic priority\nIndependent gates\nHuman decisions",
                      "STILL TO APPRAISE\nExcel-only improvement\nM365 / business platforms\nFull production topology"]) + [
                      txt("Reuse the contracts. Prove the controls. Do not equate cloud choice with corporate approval.",.65,6,12,.38,18)]
    if k=="architecture":
        e=[panel("SOURCE RECORDS\nControlled snapshot import",.65,2.85,3.45,1.15,MOSS,19,INK),
           panel("AZURE-HOSTED API\nIdentity • versions • gates",4.94,2.85,3.45,1.15,FOREST,19),
           panel("CASE + EVIDENCE\nAzure SQL / versioned Blob",9.22,2.85,3.43,1.15,MOSS,19,INK),
           panel("STAFF WORKBENCH\nRole-specific human reviewers",.65,5,3.45,1.2,FOREST,19),
           panel("ORCHESTRATION\nDeterministic tasks through API",4.94,5,3.45,1.2,MOSS,19,INK),
           panel("FOUNDRY AI\nTyped choices / cited drafts\nProposals—not decisions",9.22,5,3.43,1.2,FOREST,17),
           arrow(4.32,3.25,.4,.45),arrow(8.59,3.25,.4,.45)]
        for x,end in [(2.37,6.1),(6.66,6.66),(10.93,7.2)]:
            e.append({"type":"connector","connector_type":"straight","begin_x":x,"begin_y":4.7,"end_x":end,"end_y":4.3,
                      "line_color":MUTED,"line_width":2,"tail_end":"arrow"})
        return e
    if k=="comparison":
        return two(["BEFORE • WORKBOOK CONTROL\nRepeated status reconciliation\nEvidence assembled at handoffs\nManual baseline: not measured",
                    "AFTER • PROPOSED CONTROL\nConnected cases / accepted owners\nPermissions / versions / audit\nGates / capacity / cash visibility"],h=2.85)+[
                    txt("One-way import → reconciled cutover → Excel as read-only reporting. No permanent dual write.",.65,6.03,12,.3,16)]
    if k=="journey":
        labels=["ESTABLISH\nIdentity + intake","ASSESS\nTechnical + resident","RELEASE\nFunding + capacity","ACCEPT\nQA + handover"]
        e=[panel(t,.65+i*3.08,2.85,2.7,1.7,FOREST if i%2==0 else MOSS,20,CREAM if i%2==0 else INK) for i,t in enumerate(labels)]
        e += [panel("EXCEPTION: conflicting evidence → dependent review held → named resolution owner",.65,5,12,1,WARM,21,INK)]
        return e
    if k=="resident":
        return [home("MY HOME.\nMY CHOICE.",.65,2.85,3.05,WARM),
                panel("UNDERSTAND\nClear next step and named contact",4.45,2.85,8.2,.85,MOSS,20,INK),
                panel("CHOOSE\nMeasure-specific consent—not inferred from access",4.45,4,8.2,.85,FOREST,20),
                panel("GET SUPPORT\nNon-digital routes • adjustments • human hazard intake",4.45,5.15,8.2,.85,MOSS,20,INK)]
    if k=="ai":
        return two(["TYPED SCORING\nDecision 1\nSupplied candidates and bounded checks\nExplicit no-match / uncertainty\nPlacement conditional on verified task fit",
                    "CITED GENERATION\nFoundry generative model\nDraft narrative from permitted sources\nReview every required field\nNo invented facts or submission"],h=2.85)+[
                    txt("NEVER AI-OWNED: priority policy • compliance • consent • technical approval • claims • QA • payment",.65,6.05,12,.36,16,INK,True)]
    if k=="status":
        return three(["DOCUMENTED FEASIBILITY\nAzure SQL + Blob\nSource-bound EPC selection\nCited GPT-4.1-mini drafts",
                      "REQUIRED NEXT DELIVERY\nGenerated 60,000-home stock\nRetain 980-case lineage\nActual Azure / SQL / AI",
                      "STILL UNPROVED\nWorkflow / permissions\nCloud recovery / performance\nAI benefit / human acceptance"]) + [
                      txt("v0.12 accepted 10 Oct • v0.13 candidate pending fresh review • #58 source/revision boundaries retained",.65,6,12,.35,16)]
    if k=="finance":
        return [txt("£20,000",.65,2.85,3.75,.85,47,INK,True),txt("gross base cash exposure",.65,4.05,3.75,.4,18),
                txt("£7,500",4.78,2.85,3.75,.85,47,INK,True),txt("fictional grant—not cash yet",4.78,4.05,3.75,.4,18),
                txt("£12,500",8.91,2.85,3.75,.85,47,INK,True),txt("provider base funding",8.91,4.05,3.75,.4,18),
                panel("IF CONTINGENCY SPENT   £22,000 gross envelope / £14,500 provider exposure",.65,4.9,12,.9,FOREST,22),
                txt("Application ≠ award ≠ claim ≠ cash. Actual terms, liquidity and delegated authority remain unknown.",.65,6.1,12,.3,16)]
    if k=="measurement":
        return two(["COMPARISON 1 • PROGRAMME\nExisting teams / matched localities\nSame event capture and frozen cohort\nAccepted handovers + whole-chain cost\nLog shared resources and displacement",
                    "COMPARISON 2 • CAPABILITY\nPaired manual/rules versus assistance\nSame inputs and reviewed outcomes\nFull review effort + errors + latency + cost\nParallel experiment: no results yet"],h=2.95)+[
                    txt("Guardrails: safety • resident choice • quality • equity • peak cash. Include unfinished and withdrawn cases.",.65,6.12,12,.28,17)]
    if k=="gates":
        e=[]
        for i,(a,b) in enumerate([("1 • ACCEPT","Reviewed candidate + owners + scoped spending authority"),
                                  ("2 • CONNECT","Real Azure/SQL/AI + continuing lineage + negative controls"),
                                  ("3 • PROVE","Paired task value + engineering/accessibility/recovery evidence"),
                                  ("4 • DECIDE","Owner evidence review: continue / simplify / stop")]):
            e += [panel(a,.65,2.85+i*.83,2.35,.53,WARM,18,INK),
                  txt(b,3.4,2.85+i*.83,9.25,.53,19)]
        return e
    if k=="decision":
        return three(["CEO\nSponsor the mission\nRequire an honest scale decision",
                      "ASSETS CxO\nOwn accepted handovers\nProtect professional and quality gates",
                      "CFO\nSet scoped affordability\nControl cash exposure and stop conditions"]) + [
                      txt("Return with evidence: connected control behaviour • net task value • unmet gates • recommendation",.65,6,12,.4,18,CREAM)]
    if k=="technical":
        return three(["STATE & SCALE\nSQL row versions / idempotency\nIndexed queries / paging\nBlob evidence versions\nRestart and restore tests",
                      "TRUST BOUNDARIES\nRole / case / field rights\nPermitted model inputs\nSchema / source validation\nNo agent decision writes",
                      "FAILURE & OPERATIONS\nManual route on AI failure\nUnknown facts hold reviews\nAudit / cost telemetry\nRecovery still to prove"],h=3.1)
    if k=="qa":
        return [panel("WHY NOT EXCEL / M365?\nCost equivalent options; control mechanisms must win.",.65,2.85,5.85,1.35),
                panel("WHY NOT LAUNCH NOW?\nFeasibility is not full workflow or human acceptance.",6.85,2.85,5.8,1.35,MOSS,20,INK),
                panel("WHAT BUDGET?\nNew scoped authority needed; prior cap/override is historical.",.65,4.6,5.85,1.35,MOSS,20,INK),
                panel("WHAT IF AI FAILS?\nKeep manual work; simplify failed tasks; preserve gates.",6.85,4.6,5.8,1.35)]
    if k=="evidence":
        return three(["REQUEST / RESEARCH\nOriginal ambition is not an outcome.\nSector patterns are not company facts.\nRole instruments are not interviews.",
                      "EXERCISE / DIRECTION\nFictional fixtures are not budgets.\nAccepted v0.12 is historical.\nv0.13 is pending fresh review.",
                      "PROPOSED / OBSERVED\nTarget topology is not deployed proof.\nPinned feasibility is narrow.\nBenefit and readiness are unproved."]) + [
                      txt("Full source/provision/date/status citations in notes • Independent review and rehearsal still pending",.65,6,12,.35,17)]
    raise ValueError(k)

def main():
    (ROOT/"content/global").mkdir(parents=True,exist_ok=True)
    (ROOT/"slide-deck/validation").mkdir(parents=True,exist_ok=True)
    (ROOT/"content/global/style.yaml").write_text(yaml.safe_dump(STYLE,sort_keys=False,allow_unicode=True),encoding="utf-8")
    dump=["<!-- markdownlint-disable-file -->","# Review-ready slide text and notes",
          "14 main slides; 3 appendices. Working draft; no publication.\n"]
    total=0
    for n,s in enumerate(SLIDES,1):
        dark=n in (1,14)
        elements=base(n,s["title"],s["kicker"],s["footer"],dark)+visuals(s)
        citations="\n\nEvidence:\n"+"\n".join(SOURCES[r] for r in s["refs"])
        notes=s["notes"]+citations
        if n<=14: total+=len(re.findall(r"\b[\w’'-]+\b",s["notes"]))
        content={"slide":n,"title":s["title"],"section":"Main council pitch" if n<=14 else "Appendix",
                 "layout":"blank","background":{"fill":FOREST if dark else CREAM},
                 "elements":elements,"speaker_notes":notes}
        d=ROOT/f"content/slide-{n:03d}"
        d.mkdir(exist_ok=True)
        (d/"content.yaml").write_text(yaml.safe_dump(content,sort_keys=False,allow_unicode=True,width=110),encoding="utf-8")
        visible="\n\n".join(e.get("text","") for e in elements if e.get("text"))
        dump += [f"## Slide {n:02d} — {s['title'].replace(chr(10),' ')}",visible,"### Speaker notes",notes]
    dump.insert(3,f"Main spoken-note words (excluding citation blocks): **{total}**.\n")
    (ROOT/"research/review-ready-text.md").write_text("\n\n".join(dump),encoding="utf-8")
    print(f"Authored {len(SLIDES)} slide YAML files; main spoken-note words: {total}")

if __name__=="__main__": main()
