<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue 83 table inventory D1

## Metadata

* Task ID: issue-83-table-inventory-d1-1111
* Critique date: 2026-11-11
* Plan: .copilot-tracking/plans/2026-11-11-issue-83-table-inventory-d1-1111-plan.md
* Phase details: .copilot-tracking/details/2026-11-11-issue-83-table-inventory-d1-1111-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: hosted CI failed `test_every_table_has_a_caption_and_column_headers` (13 != 12) after dd3c32910 added a table. D1 allows only audit plus test-count and baseline-record correction; product bytes identical; no new issue, push or D2.
* Research and evidence considered: .copilot-tracking/research/2026-11-11-issue-83-table-inventory-d1-1111-research.md; src/api/tests/test_accessibility_baseline.py; src/api/src/zava_forward/api/web/*.js (at 7880b95b1 and HEAD); docs/reference/research/ux/wcag-conformance-baseline.md; docs/reference/README.md; docs/reference/log.md.
* Decisions, dependencies, and acceptance criteria considered: literal 13, no new regression, stop on a real defect, original review routing.
* Assessment boundary: source and plan reading only. Hosted CI, browser tests and the 69-test count were not run.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| C1 to C4 count claim | Covered | Re-ran the regex `h\("table", \{\},\s*` per file: 12 at 7880b95b1, 13 at HEAD; only app.js changes (5 to 6). Matches C3. |
| C5 audit of waiting table | Covered | app.js lines 849 to 868: caption first, 7 `th scope="col"`, `th scope="row"` link, named `table-scroll` region with tabindex 0, text-only cells. Matches. |
| C2 `ops.js` line 28 uncounted | Partial | Confirmed: `h("table", { "aria-label": title }` is not matched and has no caption. The record wording does not account for it (PC-001). |
| P02 test edit | Covered | Single `assertEqual(tables, 12, ...)` at test line 130; comment lines 121 to 122. |
| P03 record updates | Partial | Baseline row, index and log are named, but frontmatter date and the G-4 decision are open (PC-002, PC-003). |
| P04 validation and byte proof | Partial | Proof depends on a commit the plan never schedules; hosted CI not observable (PC-004, PC-005). |
| P05 Review | Covered | Independent lens and root reconciliation. |
| Boundaries (no D2, no push) | Covered | Explicit. |

## Verdict

* Verdict: Revise (small, direct planner corrections only)
* Rationale: The count, audit and test mechanism claims are verified against source and the D1 scope is respected. The gaps are wording and procedure: the record could overstate "the inventory" while a captionless table is uncounted, the commit and proof mechanics are unscheduled, and the hosted outcome cannot be claimed.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: "Inventory now 13" can read as all tables, but the regex excludes ops.js line 28

* Related IDs: C2, C7, P03
* Evidence: src/api/src/zava_forward/api/web/ops.js:28 (`h("table", { "aria-label": title }`, no caption); baseline Tables row line 54 says "all 11 script-built workbench tables" and "the inventory is now 12".
* Concern: P03 appends "inventory now 13" without saying it is the regex-counted set of tables with an empty attribute object. A reader will take 13 as every script-built table, and the record would still claim captions throughout.
* Impact: A recorded count that conflicts with a known uncounted, uncaptioned table is a misstatement in a WCAG evidence record.
* Smallest useful change: Add to the P03 text: "13 is the count of `h("table", {}` sites; one further `aria-label` table (ops.js:28) is outside the check and was not audited here (pre-existing, out of D1 scope)". Keep it out of scope as planned, but state it.
* Action owner: planning_parent
* Exact resolving evidence: The baseline Tables row contains the count qualification and the ops.js:28 exclusion.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Low]: G-4 and baseline frontmatter date left undecided

* Related IDs: P03
* Evidence: baseline line 209 (G-4 "Tables other than chart tables and sign-in were not fully audited"); frontmatter `ms.date: 2026-11-04` although the 2026-11-10 entry was added without updating it.
* Concern: "G-4 context if needed" and the date are not decided.
* Impact: Stale or ambiguous record; a reviewer cannot tell whether omission was deliberate.
* Smallest useful change: State: leave G-4 unchanged (the source audit of one table does not close it), and either bump `ms.date` to 2026-11-11 or record why not.
* Action owner: planning_parent
* Exact resolving evidence: Phase details P03 names both decisions.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: Index and log edits lack concrete form

* Related IDs: P03
* Evidence: docs/reference/README.md line 1054 (baseline entry, date 2026-10-15); log.md heading convention `## [YYYY-MM-DD] update | title (Refs #N)` and entries ending with an evidence-class line and a `.copilot-tracking` pointer.
* Concern: The plan says "update summary and date column" and "append one entry" without the heading shape, evidence class (documentary plus test metadata) or the non-claims, which the log convention carries.
* Impact: Review churn; risk of an entry that implies conformance or approval.
* Smallest useful change: Specify the heading, the evidence-class sentence (test count literal only, no product change, no conformance claim, no criterion tick, no approval) and the tracking pointer. Confirm the date column takes the latest change date.
* Action owner: planning_parent
* Exact resolving evidence: P03 lists the heading and the evidence-class wording.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Byte-equality proof assumes a commit the plan never schedules

* Related IDs: P04, Boundaries
* Evidence: Plan Boundaries use `git diff --stat dd3c32910 -- src ':!src/api/tests'`; phase details use `git diff --name-only dd3c32910 HEAD`. Working tree has only untracked .copilot-tracking files; no commit step, identity step or message appears.
* Concern: `dd3c32910 HEAD` is empty of the change until committed. The repository rules require the `gh api user` noreply identity set locally and the Co-authored-by trailer. Also the untracked tracking files include the pre-change log.
* Impact: The proof either runs against an uncommitted tree (use `git diff dd3c32910` without HEAD) or the commit procedure is skipped or done wrongly.
* Smallest useful change: Add a step: set the local noreply identity, commit tests, docs and tracking evidence on the PR 1444 branch (no push), then run both proofs against the new HEAD and also `git status --short` clean. Name the commit type (`test` or `docs`) and `Refs #83`.
* Action owner: planning_parent
* Exact resolving evidence: P04 records the commit SHA, the empty product diff and a clean status.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Hosted CI outcome is unverifiable under the no-push boundary

* Related IDs: Objective ("to clear hosted failure"), P04, P05
* Evidence: Plan Boundaries forbid push; repository instructions say an unobserved hosted workflow is not a success.
* Concern: The objective says the change clears the hosted failure, but only the local reproduction and fix can be shown. The plan does not say the hosted job stays unobserved until the owner pushes.
* Impact: Risk of overclaiming in the Review or closeout.
* Smallest useful change: Reword the objective to "clears the same test locally" and add a Follow-Up item: hosted API job for the new head remains unobserved until a push the owner authorises.
* Action owner: planning_parent
* Exact resolving evidence: Plan objective and Follow-Up Items carry the wording.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: "69 selected tests, zero skips" is an unsourced expectation

* Related IDs: Validation
* Evidence: Plan Validation; no source in the research for 69.
* Concern: A fixed count with no derivation may be wrong or drift. Browser tests require Chromium and `ZF_BROWSER_TESTS=1`.
* Impact: A false failure or false confidence in a validation criterion.
* Smallest useful change: Replace with "record the count and skips actually observed; zero skips required" or cite where 69 was derived.
* Action owner: planning_parent
* Exact resolving evidence: Validation text and the recorded P04 output agree.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Count and audit claims independently reproduced; the fix is a literal 13 that preserves the force-an-audit mechanism.
* D1 boundaries are explicit, with a stop rule for a real defect.
* Residual risk: the regex-based count misses attribute-bearing table forms, which is accepted as out of scope if PC-001 is recorded.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* No tests, browser or hosted CI run. The commit, identity and the 69-test count were not verified.

## Recommended Next Action

* Highest-impact finding: PC-004 (with PC-001 for record accuracy)
* Action owner: planning_parent
* Smallest next action: Revise plan and phase details directly for PC-001 to PC-006; no further critique needed.
* User response required: no

## Related Artifacts

| Path | Description |
|---|---|
| [.copilot-tracking/plans/2026-11-11-issue-83-table-inventory-d1-1111-plan.md](.copilot-tracking/plans/2026-11-11-issue-83-table-inventory-d1-1111-plan.md) | Plan critiqued |
| [.copilot-tracking/details/2026-11-11-issue-83-table-inventory-d1-1111-phase-details.md](.copilot-tracking/details/2026-11-11-issue-83-table-inventory-d1-1111-phase-details.md) | Phase details critiqued |
| [.copilot-tracking/research/2026-11-11-issue-83-table-inventory-d1-1111-research.md](.copilot-tracking/research/2026-11-11-issue-83-table-inventory-d1-1111-research.md) | Research evidence |

## Next Steps

* Standalone critique: planning parent applies the direct corrections in PC-001 to PC-006, then proceeds to P01. No user action is required.
