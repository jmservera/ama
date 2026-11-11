# Plan: issue 80 entrypoint runtime check (diagnostic, proposal only)

* Date: 2026-11-10
* Task: `issue-80-entrypoint-runtime-1110`
* Research: `.copilot-tracking/research/2026-11-10/issue-80-entrypoint-runtime-1110-research.md`
* Details: `.copilot-tracking/details/2026-11-10/issue-80-entrypoint-runtime-1110-details.md`
* Critique: `.copilot-tracking/plans/2026-11-10/issue-80-entrypoint-runtime-1110-critique.md`
* Status: plan only. No implementation, no review and no source, test, workflow, dependency or config change occurred or is authorised. Whole every-list criterion stays UNPROVEN. Criterion 4 thresholds are human and open; parent #73 and criterion 2 stay open. No new source allowance.

## Position after research

Runtime evidence exists only for the default "My cases" `cases.csv` control (no `report` parameter). Targets 1 and 2, and the rest of target 3, were not observed because of two disposable-driver defects. The plan does not turn that into a finding about the application.

## Phases

1. Phase 1, Root decision (human): decide whether to admit one further bounded browser session with the corrected disposable driver. Nothing below runs without that separate admission.
2. Phase 2, corrected observation (only if admitted): reuse the preserved driver `ROOT/phase80-entrypoint-runtime-evidence-1110/driver/entrypoint_driver.py` with exactly these two corrections, still external and disposable: (a) wait for `a[download='cases.csv'][href]` before reading the href, and use the click-captured download URL as the authoritative value; (b) record `pageerror` and non-GET requests into the observations file incrementally. Same admission (`flock -n`), same owned `ZF_DATA` assertion, same fixture, same role (pam). Stages as already coded: My cases, All cases, progress dashboard (plain, filtered, URL probe), overview, capacity, specialist screens index, Package queue and case ZF-1, case page, then the server GET comparison for interpretation.
3. Phase 3, interpretation rules (applied only to observed data):
   * A CSV control is "dynamically located" only with its route, DOM element (selector, text, href), role, and a captured download URL and filename.
   * Absence is stated only for the observed scenario (role pam, this fixture, listed routes and states), never as whole-product absence or a defect.
   * A direct GET of `/api/packages.csv`, `/api/workorders.csv` or `/api/cases.csv?report=progress` proves the server route only, not UI reachability or correct rows.
4. Phase 4, conditional minimal fix proposal (only if a control is absent in the observed scenario, and only after Root consumes the evidence): propose, without implementing, the smallest change through the existing route, role and data contract. Candidate shape, to be confirmed against the observed DOM:
   * `packages.csv`: one `Download for Excel` anchor with `href="/api/packages.csv"` and `download="packages.csv"` beside the Packages heading of `capacityView`, shown to the same manager roles that already read `/api/packages`, with the existing one-way read-only sentence used by the other list exports.
   * `workorders.csv`: the same pattern beside the Work orders heading, `href="/api/workorders.csv"`.
   * `cases.csv?report=progress`: no change is proposed unless Root's reading of the criterion needs a progress download control; the existing closed-cases download and the progress dashboard are separate registers, and adding a variant control would be a requirement decision, not a fix.
   * Regression selector for each: `a[download='packages.csv'][href='/api/packages.csv']` and `a[download='workorders.csv'][href='/api/workorders.csv']` on `#/capacity`, plus a denied-role case reusing the existing list-export role test (`api/tests/test_list_export_api.py` registry and role checks); no new endpoint, role, projection or retention change. Any web edit additionally needs the web-design-guidelines fetch and the Fluent 2, WCAG and plain-language precedence read, which has not occurred.
5. Phase 5, handoff: report exact evidence, the commands and exits, the unresolved targets and the decisions Root owns.

## Not in scope

No UI redesign, no new list fields, no other registers (see the supplement's remaining scope), no owner thresholds, no Excel writeback, no acceptance, assistive-technology or live approval, no push, PR or GitHub mutation, no rebase or main adoption.

## Decisions Root owns

1. Admit or decline a further bounded run (Phase 2).
2. After real evidence, whether any absence is a requirement gap and whether to authorise a fix.
3. Whether the progress variant needs a UI control at all under the criterion wording.
