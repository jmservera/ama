<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-119-map-options-correction

## Metadata

* Task ID: 119
* Critique date: 2026-10-23
* Plan: .copilot-tracking/plans/2026-10-23/issue-119-map-options-correction-plan.md
* Phase details: .copilot-tracking/details/2026-10-23/issue-119-map-options-correction-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: docs-only correction of independent-review findings MAP-001 (stale USD500 and USD535.41 versus the USD700 all-in ceiling, expiry 2026-10-25T16:02Z, Unknown headroom) and MAP-002 (vendor claims without draft-unverified labels), with no web retrieval, no provider selection, originals preserved, no full gate.
* Research and evidence considered: .copilot-tracking/research/2026-10-23/issue-119-map-options-correction-research.md; the independent review.md of session b9cc4727; the current text of docs/reference/research/ux/map-tile-provider-options.md (all 153 lines), docs/case_study_48_addendum.md lines 330-345 and 395-414 (read only), docs/adrs/0002-pilot-readiness-architecture.md lines 684-700, docs/reference/README.md line 23, and docs/reference/log.md lines 6700-6740.
* Decisions, dependencies, and acceptance criteria considered: owner single extra-cycle authorization, plan FR1-FR4, AC1-AC6, phases P01-P04.
* Assessment boundary: planning credibility and claim-recurrence coverage against the target files as they stand now. The critique does not verify vendor facts, the recovery-research file W1-W4 evidence (cited by the research, not re-read), or the unwritten implementation.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| MAP-001 cost paragraph (P02-T01, FR2, AC2) | Covered | Options lines 113-127 are the only place USD500/535.41 appear as current in the proposal; addendum anchor `#revised-owner-budget-decision-2026-10-22` matches heading at addendum line 335. See PC-003 for the leftover budget phrase in Table row E and for repeats elsewhere. |
| MAP-002 table rows A-E (P01-T02) | Partial | Rows B-E mapped. Row A is only partly specified (PC-002). Row B mixes a re-read figure and a draft rule in one cell (PC-002). |
| MAP-002 bullets and method (P01-T03) | Partial | B, C, D bullets, Entra premise, cost method Learn sentence and unverified list intro are named. Option A and E bullets, the "Not reviewed" sentence and the Status paragraph "each row records the date it was read" are not all named (PC-002). |
| ADR 0002 delta (P01-T04, FR3) | Partial | Plan names geography, Entra, OS summary. It omits the "Azure Maps terms, paid rate and processor position are not yet verified" sentence (already hedged, fine) and the ADR `ms.date` (PC-004). |
| Index and log (P03-T01, P03-T02, FR4) | Partial | README line 23 and log append are covered. README line 23 text "records dated licence, attribution... evidence" is itself an unlabelled-claim repeat; plan handles it. Log append position is fine (end of file, line 6726 onwards). ADR ms.date missing (PC-004). |
| Tracking honesty (P03-T03, AC3, AC4) | Partial | Contradictory preservation wording (PC-005). |
| Validation (P04, AC6) | Partial | Checks are sound but no mechanical AC1 check and an unplanned path for a failing single Review (PC-006). |

## Verdict

* Verdict: Revise
* Rationale: The plan correctly diagnoses both findings and the addendum link resolves. However, its AC1 ("every claim", "whole document") is not backed by a concrete claim inventory, so recurrences in the Status paragraph, Row A and the Row B mixed cell can be missed, which is exactly how MAP-002 arose in the recovery cycle. A small number of direct planner edits fix this. No user decision is needed.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: AC1 has no enumerated claim inventory or mechanical check, repeating the recovery-cycle failure

* Related IDs: MAP-002, FR1, AC1, P01-T02, P01-T03, P04-T01, research C4, C5, C7
* Evidence: plan AC1 and P01 "Done when: AC1 holds by reading the whole document"; research C5 (recovery plan AC1 and PC-001 were claimed satisfied but not borne out).
* Concern: The only completion test is a read-through, the same style of check that passed falsely last cycle. Phase details list claims by prose category, not by location.
* Impact: A repeat of MAP-002 would consume the single authorized extra cycle with no further correction available.
* Smallest useful change: Add to P01 a claim-location checklist (file:line or table cell: A-F rows, B/C/D bullets, method sentence, unverified list, ADR delta, README line 23) and add to P04-T01 a `grep -n` check that every vendor-claim cell/sentence listed carries one of the three legend labels, with the result recorded in the changes record.
* Action owner: planning parent
* Exact resolving evidence: revised phase details containing the location checklist and a P04-T01 label grep step; later, the changes record shows its output with zero unlabelled entries.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Specific recurrences of unlabelled vendor claims are not named or are mis-specified

* Related IDs: MAP-002, P01-T01, P01-T02, P01-T03
* Evidence: docs/reference/research/ux/map-tile-provider-options.md lines 15-16, 55-56, 60, 61, 79-84, 87-88, 134-142.
* Concern: (a) Row A labels the OSM policy terms re-read, but the cell also says "No data processing agreement is offered" and cites the OSMF Privacy Policy, neither established as re-read by research C7 (only the tile policy). Plan row A only labels "ODbL and copyright page". (b) Row B cell 3 combines "Gen1 retired 2026-09-15", "15 tiles per transaction" (Learn, draft) and "5,000 free" (pricing page, re-read) and derives "75,000 free tiles", a mixed-status calculation; the plan must say which label covers the derived figure (draft, unverified). (c) Line 15-16 "each row records the date it was read (2026-10-20)" is repeated in the Read column; P01-T01 covers this but the Read column header and cells for B-E still say "2026-10-20" and need a distinct label for draft read versus re-read. (d) Bullets at lines 79-84 ("Options B and C are the two candidates with a documented UK-relevant fit", "C is Great Britain only", "published attribution and proxy guidance") and the Option A bullet ("policy does not support production traffic") are not individually named in P01-T03. (e) Row E "Protomaps/Geofabrik" is mentioned in AC1 but the OSMF "points to self-hosting" sentence is a W1-derived claim and should be labelled re-read; the plan does not say.
* Impact: Mixed-status cells are the most likely place to leave a claim reading as verified, or to over-label W1/W2 (research Risk noted over-labelling).
* Smallest useful change: In P01-T02 and P01-T03 add the five items above with the intended label for each, and state that the Read column is renamed or footnoted "Draft read" versus "Re-read 2026-10-20".
* Action owner: planning parent
* Exact resolving evidence: revised phase details P01-T02/T03 listing rows A-E cell by cell and bullets A-E by name; implemented document showing the same.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: MAP-001 coverage stops at the cost paragraph; related budget phrasing and the old-figure placement are under-specified

* Related IDs: MAP-001, FR2, AC2, P02-T01
* Evidence: options lines 64 (Row E "Zava costs against the existing monthly budget"), 113-127; addendum lines 330-345 and 395-414; docs/reference/log.md lines 6726-6740 (prior entry restates "USD500 in total" as the owner budget).
* Concern: (a) Row E refers to "the existing monthly budget" without stating it is the USD 700 all-in ceiling, which is a limit and not spending authority; P02 does not touch it. (b) P02-T01 requires keeping old figures as history but does not say how: it should place them in a dated sentence ("2026-10-20 history on a superseded USD 500 basis, 535.41 reported 2026-10-21") after the current position, not as a prefix that reads as current, and AC2's "no sentence presenting" test needs a grep for `USD500`, `USD 500` and `535.41` with each hit required to be inside a history sentence. (c) The addendum states the refresh gate (lines 395-414: refreshed post-change forecast with at least one complete post-change day, "unlikely" before expiry); the paragraph should reference it so "Unknown headroom" is not read as resolvable by arithmetic. (d) The 2026-10-20 log entry is history and must stay; the new log entry should say it supersedes that budget wording, which P03-T02 does imply but does not state.
* Impact: A residual stale cue in Row E or an unscoped history figure would leave MAP-001 partly open.
* Smallest useful change: Add Row E to P02 scope, specify the history-sentence structure and AC2 grep, cite the addendum refresh gate, and have P03-T02 say the new entry supersedes the earlier USD500 budget wording.
* Action owner: planning parent
* Exact resolving evidence: revised P02 details naming Row E, grep hits for USD500/USD 500/535.41 all inside history sentences, link text citing the refresh gate, log entry text containing "supersedes".
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: ADR 0002 and index frontmatter dates not planned

* Related IDs: FR3, FR4, P01-T04, P03-T01
* Evidence: docs/adrs/0002-pilot-readiness-architecture.md frontmatter `ms.date: 2026-10-20`; docs/reference/README.md `ms.date: 2026-10-22`; instruction "update ms.date when the specification changes materially".
* Concern: Plan sets only the options document's ms.date. ADR and README are also edited.
* Impact: Stale dates on edited knowledge-base files; small but the plan is explicit about ms.date elsewhere.
* Smallest useful change: Add ADR 0002 and README ms.date 2026-10-23 to P01-T04 and P03-T01 (ADR edit stays within the delta, dated "corrected 2026-10-23").
* Action owner: planning parent
* Exact resolving evidence: diff showing `ms.date: 2026-10-23` in both files.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Preservation wording is contradictory about editing the original plan and state records

* Related IDs: AC3, AC4, P03-T03, research "Chosen direction"
* Evidence: research says "append dated corrections to the changes, plan and state records"; plan AC3 says corrections are "appends to the changes-only record, state file and log" while P03-T03 says "Create the changes record and a new state file"; plan "Critique Disposition: Pending"; caller requirement "preserve all original artifacts".
* Concern: It is unclear whether the 2026-10-20 recovery plan, its changes record, the existing state file and the recovery critique are edited (append) or untouched. The acknowledgement that the recovery PC-001/AC1 claims were not borne out must not be written into the original recovery plan or critique.
* Impact: An append to an original artifact breaks AC3 and the "preserve unchanged" owner direction; a missing disposition update is the only legitimate edit to this plan.
* Smallest useful change: State explicitly: no edits to any 2026-10-20 or 2026-10-21 artifact; the acknowledgement lives only in the new 2026-10-23 changes record, new state file and the log entry; the only edit to this plan after critique is the Critique Disposition line, recording each PC finding as applied or rejected. Add `git diff --stat` showing no changes under .copilot-tracking/*/2026-10-20 and 2026-10-21 to P04-T01.
* Action owner: planning parent
* Exact resolving evidence: revised AC3/P03-T03 wording and the diff-stat check in the changes record.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: One-Review rule has no planned path if the Review returns a defect

* Related IDs: P04-T02, AC6, follow-up items
* Evidence: plan Executive Summary ("a further finding or phase-order deviation stops the work") and P04-T02 ("findings route to follow-up, no second Review").
* Concern: A Review finding against the correction itself is neither a follow-up nor allowed to be fixed; the plan does not say whether to commit locally, stop, or report to the owner.
* Impact: Ambiguity at the end of the authorized cycle could lead to an unauthorized extra fix or a silent publish-ready claim.
* Smallest useful change: Add: if the Review returns an unresolved Medium or higher, do not push or amend, record it, commit nothing beyond what is listed (or leave uncommitted per owner), and report to the coordinator for an owner decision.
* Action owner: planning parent
* Exact resolving evidence: P04-T02 text stating the stop path and coordinator handoff.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Addendum anchor and figures (USD 700, 2026-10-25T16:02Z, Unknown headroom, history of 500, 400/450/475, 535.41, no retirement authority) are accurately taken from addendum 330-345 and 395-414.
* No web retrieval, no provider selection, no paid execution and no gate are properly bounded; both issue criteria remain unmet.
* The plan keeps W1 and W2 as re-read, addressing the over-labelling risk.
* Residual: vendor facts remain unverified by design; the recovery-research W1-W4 mapping was taken from the research file without re-reading the 2026-10-20 recovery research.

## Questions or Blocking Evidence Gaps

* None. No user decision is required; every finding is a direct planner correction.

## Limitations

* The recovery research (.copilot-tracking/research/2026-10-20/...) and recovery plan were not re-read; their content is relied on through the correction research C5 and C7 and the independent review.
* No implementation exists to assess; only the plan's sufficiency was reviewed.

## Recommended Next Action

* Highest-impact finding: PC-001 (with PC-002 on the specific recurrences)
* Action owner: planning parent
* Smallest next action: Revise phase details to add the claim-location checklist and label grep (PC-001), the cell-by-cell recurrences (PC-002), Row E and history-sentence structure (PC-003), ADR/README dates (PC-004), preservation wording (PC-005) and the Review stop path (PC-006), then record dispositions and proceed to implement without a second critique.
* User response required: no

## Linked artifacts

| Artifact | Description |
|---|---|
| [.copilot-tracking/plans/2026-10-23/issue-119-map-options-correction-plan.md](.copilot-tracking/plans/2026-10-23/issue-119-map-options-correction-plan.md) | Plan under critique |
| [.copilot-tracking/details/2026-10-23/issue-119-map-options-correction-phase-details.md](.copilot-tracking/details/2026-10-23/issue-119-map-options-correction-phase-details.md) | Phase details under critique |
| [.copilot-tracking/research/2026-10-23/issue-119-map-options-correction-research.md](.copilot-tracking/research/2026-10-23/issue-119-map-options-correction-research.md) | Correction research |

## Next Steps

Active parent action: the planning parent applies PC-001 to PC-006 directly, records dispositions in the plan, and proceeds to implement. No user command needed.
