<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-119-map-options-recovery

## Metadata

* Task ID: 119
* Critique date: 2026-10-20
* Plan: .copilot-tracking/plans/2026-10-20/issue-119-map-options-recovery-plan.md
* Phase details: .copilot-tracking/details/2026-10-20/issue-119-map-options-recovery-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: docs-only issue #119 (map tile licence, cost, privacy options); research for review only; no purchase or selection; retain accessible list; real screen-reader test only if available (not on this host, gate stays unmet); no edits to infra runbook, budget, form schema or cohort docs; no push. Draft commit 69fa487a was authored without RPI skills; the plan discloses this.
* Research and evidence considered: .copilot-tracking/research/2026-10-20/issue-119-map-options-recovery-research.md; docs/reference/research/ux/map-tile-provider-options.md (grep for unverified labels only); git ls-files for the original issue-119 tracking artifacts.
* Decisions, dependencies, and acceptance criteria considered: plan FR1-FR3, AC1-AC4, P01-P03, and the phase-detail tasks.
* Assessment boundary: plan credibility against the supplied research and requirements. Vendor facts, the full options document, the WCAG baseline section, ADR 0002 and the gate tooling were not independently re-verified.

## Coverage Assessment

| ID | Coverage | Evidence or concern |
|----|----------|---------------------|
| Owner direction (no selection, purchase, push; accessible list kept) | Covered | Plan Non-Goals, P01-T02, AC2 |
| FR1 label unverified claims "wherever they appear" | Partial | No task audits every location; P01-T01 edits one cell and P01-T02 checks ranking wording only (PC-002) |
| FR2 OS secondary rate note | Covered | P01-T01 |
| FR3 / AC3 disclosure by appending | Partial | Fits for markdown; JSON state and committed history raise problems (PC-004, PC-005) |
| AC1 | Partial | Limited to prices, allowances and DPA terms; research says other draft claims were not re-read (PC-001) |
| AC2 unmet screen-reader gate | Partial | Stated as acceptance, but no task verifies the protocol and issue-criterion wording say unmet (PC-003) |
| AC4 full gate at final HEAD | Partial | No blocked path or ordering for later evidence and review artifacts (PC-006) |
| In-scope items: WCAG baseline section, ADR 0002, index | Missing | No P0x task covers them (PC-003) |
| Privacy / DPO question | Partial | In research open questions; no plan carry-through (PC-007) |

## Verdict

* Verdict: Revise
* Rationale: The plan is credible in intent, honest about the process defect and respects owner direction. Its executable tasks are thinner than its stated claims. "Re-verified" and AC1 overstate what the research re-read, the verification of in-scope documents is not tasked, and the append-only disclosure mechanism and gate ordering have unaddressed flaws. All fixes are planner-owned and small.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Plan claims the draft is re-verified, but research re-read only part of it

* Related IDs: Executive Summary, AC1, P01, research W1-W4
* Evidence: research "Draft claims about OS Maps API docs, MapTiler and Azure geography/auth pages were read in the earlier pass and are not re-read here; they remain draft and unverified." The plan summary says it "re-verifies that draft against current evidence".
* Concern: Only OSM policy and the Azure pricing page were re-fetched. OS Maps API attribution/auth/rate limits, MapTiler terms, Azure geography and auth claims in map-tile-provider-options.md rest on the unaudited pre-RPI pass. AC1 covers only price, allowance and DPA claims, so these non-price claims pass unchecked.
* Impact: A reviewer may take the options document as recovery-verified; the process disclosure then understates residual risk.
* Smallest useful change: Reword the summary to "re-verified for OSM and Azure pricing; remaining provider claims retained as unverified draft", and widen AC1/FR1 to any vendor claim not re-read in recovery. Either label those cells in the document (small P01 task) or add one bounded re-read lane before implement.
* Action owner: planning parent
* Exact resolving evidence: plan text with the narrowed claim; options document where each non-re-read provider claim carries a dated "not re-verified in recovery" label (or research addendum showing re-read).
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: FR1 "wherever they appear" has no audit task

* Related IDs: FR1, P01-T01, P01-T02
* Evidence: phase details P01 touch one cell and re-check wording; the draft also mentions the OS 0.0331 figure at line 81 context and at line 108 in prose; the WCAG baseline section and index/log entries may repeat claims.
* Concern: The requirement spans the options document, baseline section, ADR delta, index and log, but only one cell is edited.
* Impact: A secondary figure could remain as fact in a place not inspected, failing AC1 silently.
* Smallest useful change: Add P01-T03: grep all in-scope files for GBP, "free", "DPA", "processor" and 5,000, and record each hit as labelled or fixed.
* Action owner: planning parent
* Exact resolving evidence: P01-T03 in details naming the files and search terms; the implement changes record listing every hit and its disposition.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: In-scope documents and AC2 have no verifying task

* Related IDs: Scope, AC2, P01, P03-T01
* Evidence: plan scope lists the wcag-conformance-baseline.md section and ADR 0002 "read for consistency"; phase details never mention them; P03-T01 runs only the static baseline test, which research C4 says cannot show announcements.
* Concern: The unmet screen-reader gate is the main honesty requirement of #119, yet nothing checks the protocol text, the options document and the ADR delta do not imply a completed test or a satisfied criterion 2. A passing static test could be misread as evidence.
* Impact: Risk of an implied-pass statement surviving.
* Smallest useful change: Add a task: read the baseline section and ADR delta, confirm they state "not run, no assistive technology on host 2026-10-20", and confirm engineering evidence is labelled as such. Add that the static test result is reported as engineering evidence only.
* Action owner: planning parent
* Exact resolving evidence: details task with file:line quotes recorded in changes; AC2 phrased as a checkable statement.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Appending to six original artifacts plus JSON is heavier than needed and not strictly append-only

* Related IDs: FR3, AC3, P02-T02
* Evidence: git ls-files shows the originals are tracked (changes, details, plan, research, critique, review log, rpi-sessions state JSON). The plan appends to each and adds a key to the JSON.
* Concern: Adding a JSON key rewrites the file rather than appending, contradicting "no existing text is edited". Touching seven tracked files from a prior commit also spreads the disclosure and makes the "originals preserved" claim depend on diff inspection. Appending to the pre-RPI critique and review log is questionable: those are the records the owner may need to assess unaltered. The recovery plan, research and log already carry the disclosure.
* Impact: A weakened preserved-history claim, and larger diff for the independent reviewer.
* Smallest useful change: Keep the disclosure in the recovery artifacts and the log entry (adequate, discoverable, dated). Limit appends to markdown originals that name themselves as lifecycle evidence (research, plan, details, changes), or a single pointer line; for the JSON, add a sibling file or skip it. State the choice and add a check: `git diff` of each original shows only added lines at end of file.
* Action owner: planning parent
* Exact resolving evidence: revised P02-T02 plus a done-when that `git diff --numstat` shows 0 deletions on each touched original.
* Decision route: direct planner correction. Disclosure by appending is adequate if it is also pointed to from the recovery artifacts, not the sole mechanism.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: Date and wording of the clarification must not blur chronology

* Related IDs: P02-T01, P02-T02
* Evidence: originals and recovery artifacts share date 2026-10-20.
* Concern: Same-day dating makes the appended text look contemporaneous with the draft. Also "critique was a rubber-duck pass" is a self-characterisation with no cited evidence.
* Impact: A reader could misdate the defect.
* Smallest useful change: Clarification text includes the time or commit (69fa487a vs recovery HEAD) and cites the research Process disclosure section as source.
* Action owner: planning parent
* Exact resolving evidence: appended text containing commit ids and a link to the recovery research.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [High]: AC4 gate path lacks ordering and a blocked-prerequisite outcome

* Related IDs: AC4, P03-T02
* Evidence: repository instructions require implementation and dated original RPI evidence committed before running the gate, any later commit invalidates the receipt, missing SQL/browser/scanner prerequisites block publication with no fallback. The plan has "no later commits" but also requires a Review afterwards and updated changes/review artifacts.
* Concern: Implement changes file, review record and state would be produced after the gate commit unless sequenced first. There is no statement of what happens if prerequisites are missing, nor of the verify-receipt step against current origin/main. AC4 treats a pass as assured.
* Impact: Plan could end with an invalid receipt or a fabricated-looking "done".
* Smallest useful change: Specify order (implement, changes file, commit, gate, verify receipt, independent review of exact head with the receipt external, no commits after); add "if prerequisites are missing, record Blocked with the exact missing prerequisite and do not claim gate success"; note that local passes do not satisfy hosted or human approval.
* Action owner: planning parent
* Exact resolving evidence: revised P03-T02 with ordering and a Blocked branch; AC4 reworded to "receipt verifies, or the blocker is recorded".
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Low]: Privacy and DPO question not carried into the deliverable

* Related IDs: research Q2 and open questions, P01
* Evidence: research states a tile request exposes IP, user agent, Referer and tile z/x/y, and that whether a tile area is personal data is a DPO question.
* Concern: No task confirms the options document records the DPO question and the zoom-level location-inference caveat; the owner's "no private coordinates on the wire" constraint is only a limit, not a checked claim.
* Impact: The privacy dimension, one of three issue axes, could be under-reported.
* Smallest useful change: Add to P01-T02 a check that the document names the DPO question, the exposed fields and the no-case-data statement with source C1/C3.
* Action owner: planning parent
* Exact resolving evidence: document lines quoted in the changes file.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Honest process disclosure in plan and research; draft preserved, not backdated.
* Owner direction is faithfully carried: no selection, no purchase, no push, accessible list retained, screen-reader gate unmet, no touching of forbidden docs.
* Evidence is dated with retrieval dates and distinguishes official from secondary sources. Research C5 supports the unmet gate.
* Accepted residual risk: vendor terms, paid rates and DPAs stay unverified until an owner-approved check.

## Questions or Blocking Evidence Gaps

* None that need the user. All findings are planner-owned corrections. The screen-reader result remains an unmet human gate by owner direction.

## Limitations

* Plan, details and research were read in full. The options document, WCAG baseline, ADR and gate tooling were sampled by grep only. Vendor claims were not re-checked. Original draft artifacts were not read beyond file listing.

## Recommended Next Action

* Highest-impact finding: PC-006 (with PC-001 equal in weight)
* Action owner: planning parent
* Smallest next action: Revise the plan and details directly for PC-001 to PC-007, without a second critique.
* User response required: no
