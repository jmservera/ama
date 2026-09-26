<!-- markdownlint-disable-file -->
# RPI Plan Critique: Integrate the Proper North Homes sector archetype research into the knowledge base

## Metadata

* Task ID: RPI-2026-09-25-proper-north-homes-sector-archetype
* Critique date: 2026-09-25
* Plan: .copilot-tracking/plans/2026-09-25/proper-north-homes-sector-archetype-plan.md
* Critique execution status: Complete
* Critique depth: standard
* Depth provenance: default (no explicit deep request)
* Invocation consumed: yes
* Attempt ID and kind: PCA-001, initial
* Candidate identity and saved hash boundary: candidate revision 1, SHA256 DEE2D2767753504118551374E998376083DE328C649E9EA7BFF5ACE5E0C8DE6F of the saved plan before reservation metadata; edits confined to the plan's Critique Disposition section are metadata
* Current-run provenance: immediate rpi-plan activation in the same uninterrupted planner execution after the PCA-001 reservation was saved and read back (reserved 2026-09-25T18:33:38+02:00)
* Original attempt and recovery approval: not applicable

## Inputs and Criterion Boundary

* Task context and caller requirements: file the completed archetype research into the primer and company profile research (research next action); D1 to D4 confirmed; DP2 (correct the EPC C line) and DP3 (addendum cross-reference) answered by the user; repository evidence and Markdown conventions in .github/copilot-instructions.md.
* Research and evidence considered: .copilot-tracking/research/2026-09-25/proper-north-homes-sector-archetype-research.md; docs/reference/research/sector/housing-association-primer.md; docs/reference/research/company/company-profile-research.md; docs/reference/README.md; docs/reference/log.md; docs/reference/regulatory/README.md (SRS MEES rows); docs/case_study_48_addendum.md (Purpose and Provisional Sector Baseline); docs/reference/research/sector/uk-social-housing-baseline-research.md (financial baselines); git status and current branch.
* Decisions, dependencies, task Goals, and task Requirements considered: D1 to D4, DP1 to DP3, FR-001 to FR-011, NFR-001 to NFR-005, P01 to P04 and all tasks, Risks and Open Questions, locked candidate boundary.
* Assessment boundary: documentation-only plan with no test suite. The critique can judge coverage, internal consistency and consistency with repository rules and supplied evidence. It cannot verify the external sources themselves.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-001 to FR-005, FR-007, FR-008, FR-010, FR-011 | Covered | Each maps to a task whose Requirements reproduce research Q1 to Q6 figures and sources |
| FR-006 | Partial | Open-question notes overstate what the modelled profile answers for two questions (PC-004) |
| FR-009 | Partial | Comparator size claim not supported by the company profile table (PC-003) |
| NFR-002 | Partial | New legislation and guidance citations have no local snapshot and no change-likelihood record (PC-002) |
| NFR-005, P04-T03 | Partial | Change boundary conflicts with the tracked-but-uncommitted `.copilot-tracking/` artifacts (PC-001) |
| NFR-001, NFR-003, NFR-004 | Covered | P02-T01 table contract, label mapping to role-agent categories, and P04-T03 checks |
| P01 to P04 dependencies | Covered | Fixed `## Modelled Customer Profile` heading removes the P01-T04 to P02-T01 ordering conflict |

## Verdict

* Verdict: Revise
* Rationale: The plan is well-grounded and complete in structure, but four medium findings would make implementation either fail its own check (PC-001) or introduce unsupported or overstated statements into the knowledge base (PC-002 to PC-004). All are direct planner corrections within current user direction.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Change boundary contradicts tracking artifacts that are part of the repository

* Related IDs: NFR-005, P04-T03, Critique Disposition locked boundary
* Evidence: `git status --short` shows `.copilot-tracking/research/2026-09-25/` as untracked, not ignored (`git check-ignore` returns no match), and other `.copilot-tracking/` files are committed. The plan requires "only the primer, company profile research, addendum, index and log change".
* Concern: Implementation must create the changes record, and the plan and critique already exist under `.copilot-tracking/`. A literal reading of NFR-005 fails, or an implementer may exclude or delete legitimate tracking artifacts.
* Impact: False validation failure or loss of RPI evidence.
* Smallest useful change: Scope NFR-005 and the P04-T03 check to `docs/` and `.github/`, stating that RPI tracking artifacts under `.copilot-tracking/` for this task are expected.
* Action owner: planning parent
* Exact resolving evidence: NFR-005 and P04-T03 wording names `.copilot-tracking/` artifacts as expected.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: New regulatory citations have no local snapshot or change-likelihood record

* Related IDs: NFR-002, P01-T02, P01-T03, Non-Goals
* Evidence: .github/copilot-instructions.md requires citing "the local source, relevant provision or section, source date and retrieval date" and assessing change likelihood as High, Medium or Low. docs/reference/README.md Ingest a New Source places official legislation and guidance snapshots in `regulatory/`. P01-T02 cites Housing Act 1985 Schedule 6, SI 2003/1987, GOV.UK shared ownership guidance and the GMCA WH:SHF copy from the web only, and the Non-Goals exclude regulatory snapshot changes.
* Concern: The plan does not say how these web-only citations meet the local-source and change-likelihood rules, and records no follow-up to snapshot them.
* Impact: The primer would carry regulatory claims that fall outside the repository evidence regime without saying so.
* Smallest useful change: Require P01-T02 and P01-T03 to mark each web-only regulatory citation as "no local snapshot" with its URL and retrieval date, and add a Follow-Up Item to snapshot these sources and add register rows with change likelihood. Snapshot creation stays out of scope.
* Action owner: planning parent
* Exact resolving evidence: updated P01-T02 and P01-T03 Requirements and a populated Follow-Up Items entry.
* Decision route: direct planner correction (keeps the current scope; no user decision needed)

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Comparator size range is unsupported for two comparators

* Related IDs: FR-009, P02-T02
* Evidence: docs/reference/research/company/company-profile-research.md Comparable Organisations gives sizes only for Karbon (34,000), Onward (35,000) and Together (more than 38,000). No size is given for Thirteen or Home Group.
* Concern: P02-T02 requires stating that "the listed comparators are 34,000 to 38,000-home groups".
* Impact: Introduces an unsupported company-comparator claim, against the repository rule not to invent facts.
* Smallest useful change: Limit the statement to the comparators whose sizes are recorded, and say the others' sizes are not recorded.
* Action owner: planning parent
* Exact resolving evidence: revised P02-T02 Requirements bullet.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Open-question notes overstate what is modelled for lease terms and recorded vulnerability

* Related IDs: FR-006, NFR-001, P01-T04, research Q4 and Q5
* Evidence: Research Q4 says actual lease allocation "needs a lease-by-lease review" and is an unknown company detail. Research Q5 says the recorded vulnerable share "is an unknown company detail and probably well below 61%". P01-T04 requires each of the four questions to note that "a modelled estimate is recorded".
* Concern: For the lease-terms and recorded-vulnerability questions, the profile models sector rules, lease-interest counts and prevalence, not the company's lease terms or recorded share and completeness.
* Impact: Readers and role agents may treat the questions as answered when they remain unknown company details.
* Smallest useful change: Require each note to state what is modelled and what remains unknown. Lease terms stay unknown pending lease review; recorded vulnerable share and completeness stay unknown, with only prevalence modelled.
* Action owner: planning parent
* Exact resolving evidence: revised P01-T04 Requirements bullet.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: Current branch is unrelated to this task

* Related IDs: Dependencies, P04-T03
* Evidence: `git branch --show-current` returns `docs/typesafe-open-decision-review`.
* Concern: Implementation would mix this documentation change with an unrelated branch's work.
* Impact: Harder review and commit hygiene; no content risk.
* Smallest useful change: Record in Dependencies or Risks that the user chooses the branch before implementation; the plan does not commit or switch branches.
* Action owner: planning parent (record); user (branch choice)
* Exact resolving evidence: a Risks and Open Questions or Dependencies entry naming the branch.
* Decision route: direct planner correction; branch choice remains the user's operational decision and does not block planning

## Strengths and Residual Risk

* The placement split (DP1) follows the knowledge base placement rules, and every user decision (D1 to D4, DP2, DP3) is reflected in task Requirements.
* The P02-T01 table contract makes numeric fidelity checkable, and the figures reproduce from the stated shares.
* Contradictions (fuel poverty, interest cover basis) are flagged and not overwritten, as the knowledge base ingest rule requires.
* Residual risk: modelled estimates may still be quoted as facts downstream. The plan records this as a high risk with labelling controls.

## Questions or Blocking Evidence Gaps

* None

## Limitations

* External sources were not re-fetched; accuracy relies on the research evidence log.
* Rendered Markdown and Mermaid output were not previewed.

## Recommended Next Action

* Highest-impact finding: PC-002
* Action owner: planning parent
* Smallest next action: Apply PC-001 to PC-005 as one batch of direct corrections, then finalize without a closure critique.
* User response required: no
