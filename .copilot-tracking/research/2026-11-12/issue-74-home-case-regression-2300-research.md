<!-- markdownlint-disable-file -->
# Research: #74 home case regression slice G1/G2/G3 (issue-74-home-case-regression-2300)

Date 2026-11-12. Base and HEAD: eac1206c6ca08bd551e3d0d2384bb87a1f05c24f (origin/main, re-fetched). Branch research/demo-74-followup-2250. Disposition: reused (prior read-only readiness result `rpi-74-refill-2250-result.json`, history reports 1923/1964/1989) plus fresh bounded reads and fixture probes today. Planning Readiness: Ready.

## History read

* #74 body and comments: criteria 1, 3, 4 ticked; criterion 2 open. PR #907 core, #1038/#1177 API and UI, qualified audit PR #1406, follow-up #1409 is a planning record only.
* Adverse history preserved: the audit log count was corrected (16 PASS plus COMPLETE); the 2026-11-09 populated two-home replay was session-local and unarchived, so it is not counted as maintained regression; criterion 2 stays unproven.
* Prior readiness: gaps G1 shared systems, G2 own-home documents and quality plus sibling home never opened in the browser, G3 non-finance restriction and G4 finance amounts over HTTP. G5 (case_ids and package_ids applicability display), the outcome tuple (handover, intended versus measured performance) and G6 are not local engineering scope and are not touched.

## Admission recheck (today)

* Owned paths: `src/api/checks/home_case_browser_check.py`, `src/api/tests/test_home_case_api.py` plus these RPI artifacts. No product source edits; `home_case.py`, `app.js`, `server.py` and the core test are unchanged since the audit base (prior result; HEAD equals origin/main).
* #82 funding readers (worktree issue-82-funding-readers-2250, c4fe717ef, tip 4ce5bae61): its branch diff DOES list `src/api/tests/test_home_case_api.py` (one new test inserted between the first and second tests) and `src/core/tests/test_home_case.py`, plus `home_case.py`, `store.py` and others. Adverse precision against the brief's "disjoint" statement: path-level overlap, hunk-level disjoint. Mitigation: new tests are appended after the last test of the class and no imports or existing lines are edited, so a textual merge is expected to be clean. No assertion reads `funding_confirmed`. A later rebase is the later owner's check.
* #176 cohort (da436be3e): `test_generated_dataset.py`, runbook, synthetic-data README. Disjoint.
* Non-finance login exists: `sam@example.test` (Resident Liaison Officer, not in `FINANCE_VIEW`) in the shared `building_fixture`/`dataset`; finance: `pam@example.test` (Retrofit Programme Manager).

## Fixture facts (probe, synthetic only)

* ZF-2 documents: SYN-EPC, SYN-Survey.pdf, SYN-Design, SYN-Consent, synthetic-commitment.txt; no quality. ZF-3: SIBLING-EVIDENCE ("Synthetic survey metadata only") first, SYN-EPC, SYN-Design, SYN-Consent; quality "Loft insulation" Accepted.
* Both homes show building SYN-B1 systems SYS-1 "Shared ventilation", DEP-1, HOLD-1, WORK-1 and COST-1 GBP 12000.00 for finance roles; non-finance view returns `cost_allocation` None with `cost_allocation_restricted` true and `costs_restricted` true.
* `app.js` `homeCaseView` (lines 1324-1368) renders systems under the building region only; documents and quality under "This home only".

## Limits

No criterion 2 closure, owner outcome tuple, G5, SQL Server, assistive technology or real acceptance. Validation tier: focused (test-only; no permission, workflow, dependency, deployment or security-control change). Complete gate not run.
