<!-- markdownlint-disable-file -->
# RPI Plan Critique: climate-source-evidence-178

## Metadata

* Task ID: 178; task slug: climate-source-evidence-178.
* Critique date: 2026-10-17.
* Plan: .copilot-tracking/plans/2026-10-17/climate-source-evidence-178-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/climate-source-evidence-178-phase-details.md
* Critique execution status: Complete.
* Invocation: exactly one final-candidate assessment; no additional critique requested or performed.

## Inputs and Criterion Boundary

* Caller requirements: execute the ordered Research, Plan, Implement and Review loop with dated committed artifacts and a completion session log. This critique is the bounded Plan-stage contribution, not authorization to execute the other stages.
* Required inputs read in full: the plan, phase details and .copilot-tracking/research/2026-10-17/climate-source-evidence-178-research.md.
* Supporting context: docs/case_study_48_original.md; the purpose and exercise-baseline portion of docs/case_study_48_addendum.md; task-routing portion of docs/reference/README.md; docs/reference/memory.md; and the supplied C1 pointer's historical climate decision, source register, derivation gate and original acceptance audit in docs/reference/research/iot-sensor-analytics-research-plan.md.
* Decisions assessed: #367 is merged and its offline unknowns are historical; owner reuse approval remains UNMET; no fabricated humidity, account creation, paid downloads, terms acceptance for the owner, private-data uploads, large dataset bundles or copied provider pages. HadUK is a conditional contextual recommendation, not adopted replay data. Durham is temperature-only monthly evidence.
* Dependencies assessed: P01-T01 requires retained W5 bytes; P02-T01 depends on measured P01 results; P03-T01 depends on both. Authorized paired records and human reuse approval remain outside this delivery.
* Acceptance assessed: distinguish bounded deliverable AC1-AC3 from the original issue criteria, preserve the unmet temperature/RH and reuse gates, retain unchanged issue checkboxes, use Refs #178 rather than closure language, and deliver evidence through the requested topic PR without merge.
* Assessment boundary: credibility of the supplied plan, research-to-task traceability, data semantics, tests, write scope and recommendation. No external retrieval, legal determination, record derivation, implementation or independent confirmation of the research's provider claims was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Ordered RPI loop and completion evidence | Covered | Plan requires dated tracking, completion log, one implementation review and PR handoff. Existing untracked parent artifacts are not this critique's writes. |
| Branch, bounded writes and delivery | Covered | Current branch is docs/climate-source-evidence-178. Explicit helper/test/report and canonical targets exclude application, private datasets, stock and infrastructure changes. |
| W1-W14 material candidate comparison | Covered | All five candidates plus UKCP18/EA leads have distinct roles and terms/access limitations; no evidence supports dismissing all EA products. |
| P01-T01 input readiness and provenance | Partial | W5 has a URL and SHA-256, but no usable retained-input locator or byte-verification handoff. PC-001. |
| P01-T01 aggregation and quality semantics | Partial | Correctly monthly and temperature-only; usable-window, empty-series and count contracts need an executable definition. PC-002. |
| P02-T01 release-specific recommendation | Partial | Context-only HadUK choice is reasonable, but the recommendation must bind one product representation and its matching terms/citation. PC-003. |
| AC1 and original comparison criterion | Covered | Material verified progress is credible; unavailable exact terms must stay explicitly unavailable, not silently become complete reuse verification. |
| AC2 and owner reuse boundary | Covered | Candidate recommendation and licence metadata do not authorize reuse or establish adoption. Owner approval remains UNMET. |
| AC3 and original paired-bounds criterion | Covered | Monthly Durham statistics are partial evidence, not instantaneous or paired replay bounds. Original issue criterion remains unmet. |
| P03-T01 tests and reconciliation | Partial | Focused tests, independent arithmetic, links and immutable-path checks are appropriate; PC-001/PC-002 must become explicit validation oracles. |
| No new research or unauthorized access | Covered | Local-only helper and no downloader preserve the supplied access and terms boundaries. |

## Verdict

* Verdict: Revise.
* Rationale: The bounded contribution and honest partial acceptance are credible. Three direct planner corrections are needed to make the retained-input dependency, statistical test contract and exact recommended product unambiguous before implementation. None requires reopening the owner's settled scope or relaxing the paired RH/reuse gates.
* Severity summary: Critical 0; High 1; Medium 2; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Make the retained W5 record an executable dependency

* Related IDs: W5, P01-T01, P03-T01, input provenance and reproducibility requirements.
* Evidence: .copilot-tracking/plans/2026-10-17/climate-source-evidence-178-plan.md:66-79,114-117,140-143,156-157 promises an already retained record, actual-file execution and a complete 1991-2020 window. .copilot-tracking/details/2026-10-17/climate-source-evidence-178-phase-details.md:24-38 names only "local W5 bytes." The research W5 row supplies the URL and expected SHA-256 but no retained-input locator. The supplied research-directory inventory contains the research Markdown, not the raw record.
* Concern: The supplied handoff does not establish where implementation can read the exact bytes without another network request. This is missing handoff evidence, not proof the file was never retained. An actual-file invocation and independent arithmetic cannot be reproduced from a URL/hash alone.
* Impact: Implementation could stall, use different bytes or fetch again despite the explicit no-further-Met-Office-retrieval boundary. A derived report would then lack the claimed input provenance.
* Smallest useful change: Add a tracking-only locator for the existing session evidence, an exact offline invocation, and a preflight that verifies its hash against W5 before parsing. Name the actual retrieval date as supplied provenance, not an inferred file modification date. If the retained bytes cannot be located or do not match, block P01 and its numeric output without redownloading or manufacturing results; the metadata comparison can still be reported separately.
* Action owner: Planning parent, using the research parent's retained session evidence.
* Exact resolving evidence: Plan/details identify the locally retained input and offline command; a recorded preflight confirms SHA-256 d2c9ff2a443b8502957ce88fe8bfdbbd0d5ac111208eab0842bc574d4d4306f9 and readable bytes. The raw file remains outside committed artifacts, while its URL, retrieval date and hash remain in the derived provenance.
* Decision route: Direct planner correction. No new research or user response is required to locate/verify existing evidence; a missing record is a disclosed implementation blocker, not permission to cross the access boundary.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Resolve complete-window and missing-value behavior before locking tests

* Related IDs: P01-T01, P03-T01, AC3, semantic-test contract.
* Evidence: .copilot-tracking/plans/2026-10-17/climate-source-evidence-178-plan.md:66-71,114-116 calls the selected window complete while also requiring missing/absent/quality-rejected counts. .copilot-tracking/details/2026-10-17/climate-source-evidence-178-phase-details.md:29-36 specifies independent field quality and paired midpoints but does not define completeness or the no-valid-values result.
* Concern: Calendar completeness, valid tmax coverage, valid tmin coverage and valid midpoint coverage are different. "Complete" could mean 360 calendar rows or 360 accepted values in each series. Count categories can also double-count a flagged missing token unless their reconciliation is defined. No explicit contract handles an entirely unusable field or all-invalid midpoint series.
* Impact: Implementers/tests could silently call a quality-filtered subset complete, calculate a midpoint from differently filtered months, or fail unpredictably on empty data. These errors would undermine the claimed record-derived evidence even without fabricated RH.
* Smallest useful change: Define 360 expected unique calendar months for 1991-01 through 2020-12; separately report present, absent and valid coverage per series. Define mutually reconcilable exclusion counts, or explicitly label overlapping diagnostics. Keep midpoint coverage restricted to same-row accepted tmax/tmin pairs. Specify whether an empty series produces an explicit unavailable result or a nonzero error, never numeric defaults. State that incomplete usable coverage is reported as such rather than made complete by filling or relabelling it.
* Action owner: Planning parent for the contract; P01 implementer for locked regression cases.
* Exact resolving evidence: Phase details state the count equations and empty-series policy. Synthetic fixtures assert exact expected counts and extrema for absent months, independent estimated/provisional/missing fields, same-month pairing, ties and an all-invalid field/pair. Include invalid month identifiers and unrecognized quality markers in rejection tests. P03 verifies the real report's counts reconcile to the declared window and that "complete" is used only for the evidenced property.
* Decision route: Direct planner correction. The owner has already required honest record-derived evidence; this is not a request for a new statistical scope or more data.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Bind the contextual recommendation to one exact HadUK product

* Related IDs: W1-W4, Q2, P02-T01, AC1, AC2.
* Evidence: .copilot-tracking/research/2026-10-17/climate-source-evidence-178-research.md distinguishes W2's 1km catalogue from W3's regional catalogue and W4's region/hurs request, but its recommendation says "regional/1km observational context." .copilot-tracking/plans/2026-10-17/climate-source-evidence-178-plan.md:64-65 names the release without a representation; phase details:48-57 requires its exact OGL/citation.
* Concern: A release family is not a unique regional or 1km dataset. The blocked request is for regional RH and the explicit terms/citation summary is tied to the regional catalogue. Without a fixed recommendation identity, a register could attach one representation's access evidence or citation to the other, or imply a regional aggregate represents a Durham station/grid cell.
* Impact: The central source recommendation and reuse register could look more product-specific than the supplied evidence supports, weakening AC2 even while owner approval is correctly left unmet.
* Smallest useful change: Choose one already evidenced representation as the primary conditional context candidate, retaining the other as an explicitly distinct alternative. Bind its catalogue identifier, release, spatial aggregation, variable/cadence, actual retrieval date, applicable terms and citation evidence to the same product. State the decision rationale against the actual replay requirement: no presently accessible candidate qualifies for paired replay adoption; MIDAS is the cadence-oriented future lead; HadUK is only the contextual recommendation. Do not replace the owner-directed UKCP18/EA leads silently.
* Action owner: Planning parent for the product lock and evidence sufficiency; P02 implementer for the canonical comparison/register.
* Exact resolving evidence: Plan/details identify either the W3 regional UUID 386b3c1ee2054ef5ae0d73060963a9f1 with its matching W4 access result, or separately evidenced W2 1km UUID 789b3065d74a4c948ab05d33556c86d0. The canonical register records that product's citation/attribution from already retained evidence; if exact citation text is not retained, mark it unavailable instead of inventing it or treating a licence name as the acknowledgement. Distinct product rows cannot inherit one another's access/terms evidence without an explicit evidential link.
* Decision route: Direct planner correction within the already selected HadUK context direction. No divergent user decision is needed; broadening to a different adopted source would be outside this critique.

## Strengths and Residual Risk

* The plan makes genuine progress beyond #367's offline-only unknown audit without claiming the original issue is complete.
* It correctly separates monthly averages of daily maxima/minima, an arithmetic midpoint statistic, sample extrema and instantaneous/replay-scale bounds. The midpoint must remain labelled an arithmetic construction, not a retrieved monthly mean temperature variable.
* HadUK's interpolated observational basis, ERA5 reanalysis, MIDAS calculated RH and CIBSE design-year construction are not interchangeable direct station measurements.
* The owner has explicitly retained unmet paired RH, reuse and adoption gates. Those are accepted delivery limitations, not defects to fix by inventing humidity, expanding access or seeking another critique.
* Conditional contextual recommendation is appropriate if its identity and purpose remain exact. Durham remains a separate temperature-only cross-check, not the recommended paired source.
* Bounded standard-library tooling, synthetic fixtures, a derived-only JSON report and unchanged runtime/tests are proportionate. A tool/report does not itself prove licence approval, operational suitability or North East regional representativeness.
* P02's audit should show both local deliverable progress and original issue statuses, so a completed local AC3 cannot be read as a completed issue temperature-and-humidity criterion. The existing no-closure/no-checkbox direction already resolves this framing.

## Questions or Blocking Evidence Gaps

* No unresolved decision-critical user question. The owner has already settled access, approval and partial-delivery boundaries.
* PC-001 is a concrete local evidence handoff gap. Resolve from retained session evidence; if unavailable, mark the derivation blocked. No additional external research is authorized or needed for this critique.
* Missing exact CIBSE redistribution terms, paired RH records and owner reuse approval remain declared unknown/unmet, not reasons to fabricate completion.

## Limitations

* Provider URLs and retrieval assertions were assessed from supplied research, not fetched again. No opinion here establishes legal permission or terms acceptance.
* This review did not open the station bytes or inspect a parser implementation; neither was supplied as a critique input. Statistical correctness and determinism remain implementation validation obligations.
* Git status showed existing untracked plan/details/research/session artifacts on the requested topic branch. They were left untouched. Only this critique artifact was written.
* No code tests were run because no source changes were made. No plan, phase details, research, state, log, source, canonical documentation or other review was edited; no delegation or additional critique was run.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Locate and hash-check the retained W5 input, record its offline locator/invocation, and make the PC-002/PC-003 contract corrections directly before implementation.
* User response required: No. Preserve all existing human approval gates.
* Critique disposition: Return this complete finding set to the active parent; parent finalizes after dispositions without running another plan critique.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-17/climate-source-evidence-178-plan.md](.copilot-tracking/plans/2026-10-17/climate-source-evidence-178-plan.md) | Final-candidate plan assessed |
| [.copilot-tracking/details/2026-10-17/climate-source-evidence-178-phase-details.md](.copilot-tracking/details/2026-10-17/climate-source-evidence-178-phase-details.md) | Phase and task contracts assessed |
| [.copilot-tracking/research/2026-10-17/climate-source-evidence-178-research.md](.copilot-tracking/research/2026-10-17/climate-source-evidence-178-research.md) | Supplied C1/W1-W14 evidence record |
| [docs/reference/research/iot-sensor-analytics-research-plan.md](docs/reference/research/iot-sensor-analytics-research-plan.md) | Existing canonical source register and original acceptance audit |
| [.copilot-tracking/reviews/plans/2026-10-17/climate-source-evidence-178-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/climate-source-evidence-178-plan-critique.md) | This single completed critique |

## Next Steps

The active planning parent should disposition PC-001 through PC-003 directly, preserve the original unmet issue gates, finalize the plan and continue the authorized ordered RPI loop. No user response or second critique is required. This critique task stops after writing this artifact.
