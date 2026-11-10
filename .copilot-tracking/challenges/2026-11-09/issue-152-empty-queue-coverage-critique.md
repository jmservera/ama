<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-152-empty-queue-coverage

## Metadata

* Task ID: issue-152-empty-queue-coverage
* Critique date: 2026-11-09
* Plan: .copilot-tracking/plans/2026-11-09/issue-152-empty-queue-coverage-plan.md
* Phase details: .copilot-tracking/details/2026-11-09/issue-152-empty-queue-coverage-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: bounded partial C5 only; declared-unrepresented only on trustworthy version-bound metadata, else explicit Unknown; never infer from empty queue, identity or synthetic labels; no auth/SQL/schema/server change; own-queue authorization, native semantics, keyboard reset and non-colour status preserved; no browser/Playwright/SQL/Docker runs; `Refs #152`; no AC-034/043 acceptance claim; supported devices stay an owner decision.
* Research and evidence considered: .copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-research.md; source checked directly: src/api/src/zava_forward/api/web/app.js (457-475, 770-870, 1901), src/api/checks/workbench-manifest.json, src/api/tests/test_workbench.py, src/api/tests/test_workbench_live_defaults.py, src/api/tests/test_data_operator_ai_state.py (node vm pattern), src/api/checks/workbench_browser_check.py (485-510), plus consumers of the current empty copy found by search.
* Decisions, dependencies, and acceptance criteria considered: plan FR-A..FR-E, AC1..AC5, P01..P03, follow-ups F1..F3.
* Assessment boundary: static reading only. Nothing was executed; no browser, SQL or Docker. Concerns are about plan credibility, not about code that does not yet exist.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Caller: Unknown by default, no inference | Covered | Plan never reads manifest at runtime; research rejects manifest/ID-set producers; app.js has no coverage field today. |
| Caller: no auth/SQL/schema/server change | Covered | Scope is app.js + tests; F1 defers producer. |
| FR-D declaration validation | Partial | Equality rules can pass on missing values (PC-002); trust is shape-only (PC-006). |
| FR-B/FR-C copy | Partial | Existing copy is asserted elsewhere (PC-001); declared text omits provenance (PC-004). |
| AC1/AC2 tests | Partial | Wiring and populated-queue claims untested or tautological (PC-003). |
| AC4 browser expectations | Partial | Only one existing check is named; two others assert current copy (PC-001, PC-007). |
| P03-T02 web-design-guidelines | Partial | Sequenced after edits (PC-005). |
| AC5 / publication / `Refs #152` | Partial | Gate and PR wording not recorded (PC-008). |

## Verdict

* Verdict: Revise
* Rationale: The approach is sound and honest (fail-closed client consumer, explicit Unknown default, no producer). Two defects would break existing checks or make the fail-closed contract leak (old-copy consumers, undefined-equals-undefined binding), and several planning gaps weaken the evidence. All are planner-owned corrections; no user decision is needed.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Existing consumers of the current empty copy are not in scope or AC

* Related IDs: FR-B, AC3, AC4, AC5, P01-T02, P02-T02
* Evidence: src/api/checks/employee_briefing_browser_check.py:70 asserts the Programme Support Officer unassigned empty queue shows "No open cases are assigned to you." in main; src/api/checks/loading_briefing_browser_check.py:611,614 assert "No cases match these filters"; src/core/src/zava_forward/core/store.py:881 and src/api/tests/test_ai_tasks.py:141 hold the same mine-empty sentence for the server briefing (a separate surface). app.js:800 is the list copy.
* Concern: FR-B replaces the mine-empty sentence with Unknown wording. Unless the new text keeps the old substring, the employee briefing check breaks, and it is outside the plan's declared "in scope" files, so AC5 "no file outside scope" would also fail if it is edited. The briefing surface will otherwise say "No open cases are assigned to you" while the list says coverage is Unknown; the plan does not say whether that is acceptable.
* Impact: A regression in a browser check that cannot be run now, discovered only at the later gate; inconsistent wording across surfaces.
* Smallest useful change: Specify the FR-B and FR-A strings exactly, keeping "No open cases are assigned to you." and "No cases match these filters." as leading substrings; list the two browser checks as unchanged consumers to be re-run at the admitted gate; state that the server briefing sentence is deliberately unchanged and note the wording gap as a follow-up.
* Action owner: planning parent
* Exact resolving evidence: plan/details state the literal strings; AC3/AC5 name employee_briefing_browser_check.py and loading_briefing_browser_check.py as unchanged-but-affected; a node test asserts the substrings.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: FR-D binding can pass on missing values

* Related IDs: FR-D, P01-T01, AC1
* Evidence: FR-D says `as_of` and `policy_version` "equal the page". Page values come from `d.as_of` / `d.policy_version`; `policy` is initialised to "" (app.js:~778) and `as_of` is not yet tracked. A declaration lacking `as_of` compared with an absent or empty page value is `undefined === undefined` or `"" === ""`.
* Concern: Strict-equality on unvalidated values lets an empty declaration plus an empty page validate, contradicting "fail closed". Also unspecified: `typeof` checks, arrays/objects as `coverage`, extra keys, and `contract` when `work_queues.version` is missing.
* Impact: The one safety property the brief insists on (never declare without version-bound metadata) has a loophole, and AC1's variant list does not cover it.
* Smallest useful change: In FR-D require each of `contract`, `as_of`, `policy_version`, `perspective`, `fixture_version`, `source` to be a non-empty string and the page/ctx values to be non-empty strings before comparing; add test variants: both values undefined, both empty, number or array instead of string, `coverage` an array, missing `work_queues.version`, ctx page values absent (before first load).
* Action owner: planning parent
* Exact resolving evidence: FR-D text and AC1 list include non-empty/typeof rules and these variants; the node test asserts each returns null.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: The call-site wiring and the populated/PM-default claims are untested or tautological

* Related IDs: AC1, AC2, P02-T01, P01-T02
* Evidence: Details P02-T01 extracts two pure functions by name; `filtered` is computed in listView from `listState` (app.js:800) and ctx from `me`, `d.as_of`, `d.policy_version`. For PM `ZF-5` the helper is "not used" and the proof is the manifest default read from workbench-manifest.json; AC2 asserts a populated queue never shows coverage wording, but a populated queue never calls the helper. test_workbench_live_defaults.py already covers default ids over HTTP.
* Concern: The tests prove the helper in isolation but not that listView passes the right role, version, as_of and filtered value, nor that populated lists skip it. The PM and populated assertions are vacuous (manifest data compared with itself).
* Impact: A wrong call site (for example stale `asOf`, `filtered` computed against a non-default state, wrong role) passes all runnable checks; the only guard is the unexecuted browser check.
* Smallest useful change: Move `filtered` derivation and the `rows.length === 0` gate into the helper (inputs: `listState`, `view`, `total`, `coverage`, ctx) so the tested code owns them; add cases for populated (returns null) and for a PM with a filter that matches nothing (no-match); drop the manifest-reading PM assertion or replace it with an explicit comment that the live-default HTTP test is the data check. Optionally add a text-level assertion that the call site passes `d.as_of`.
* Action owner: planning parent
* Exact resolving evidence: details list the helper signature with those inputs, AC2 maps to a populated-returns-null case, and the PM/Coordinator cases are described without manifest-vs-manifest comparison.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Declared-unrepresented copy does not surface its provenance

* Related IDs: FR-C, P01-T01, AC1
* Evidence: FR-C text mentions the declared fixture version only; `source` and `as_of` are validated but not displayed. The test asserts only "does not contain complete".
* Concern: A claim that a perspective is unrepresented is a declaration by someone; without showing source, fixture version and as-of date the reader cannot tell who declared it or for which dataset, and the claim reads as a system fact.
* Impact: Weakens the "declared, not established" distinction required by the brief and the PRD AC-034 wording.
* Smallest useful change: Require the declared text to include `fixture_version`, `source` and `as_of`, phrase it as "declared by <source>", and assert those substrings plus absence of "complete" and "no work" in node tests.
* Action owner: planning parent
* Exact resolving evidence: FR-C and P02-T01 list the substrings; the test asserts them.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Web guidance steps are sequenced after the edits they must precede

* Related IDs: P03-T02, P01, plan Non-Functional Requirements
* Evidence: Repository instructions require loading relevant skills and fetching the web-design-guidelines source before web edits; the plan places the fetch in P03 (last), although details say "before edits and again before review".
* Concern: The checklist order contradicts the details; an implementer following phases in order edits app.js first. The selected skill set (web-design-guidelines, redesign/ux standards used for copy) is not named in the plan.
* Impact: Process non-compliance that can invalidate the review; missing disclosure if the fetch fails.
* Smallest useful change: Add a P00/P01-T00 precondition: read web-design-guidelines SKILL.md, fetch the source, record result or failure; keep P03-T02 as the second fetch and review with `file:line` findings and disclosure of unperformed visual checks.
* Action owner: planning parent
* Exact resolving evidence: checklist shows the precondition before P01-T01 and the Implement changes record cites the first fetch.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: "Trustworthy" is overstated and a dormant branch can silently become live

* Related IDs: FR-C, FR-D, R1, F1, Counter 5
* Evidence: Every declaration field comes from the same `/api/me` the client already trusts; `fixture_version` and `source` are only checked for non-emptiness; `contract` equals the queue contract version, not a fixture identity (research C8, C14). No producer exists, so the branch is unreachable in production.
* Concern: The client check is necessary but not sufficient for trust; the plan and PR wording could read as though the declared state is validated end to end. Nothing stops a later change from adding a `coverage` key without the full-tier reassessment F1 requires.
* Impact: Over-claim risk in the PR and docs; the no-producer boundary is only prose.
* Smallest useful change: State in plan, README note and PR text that validation is a client consistency check, the declared state is unreachable until an authorised producer exists, and is not provenance. Add a tripwire assertion (in the new test file or the existing HTTP defaults test) that `/api/me` `work_queues` has no `coverage` key today; adjust scope to allow that one assertion if it lands in test_workbench_live_defaults.py.
* Action owner: planning parent
* Exact resolving evidence: plan Scope lists the tripwire file; the assertion exists and passes; the README/PR wording contains the "unreachable until producer" statement.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Low]: Browser-check expectations are thin for the stated cases

* Related IDs: AC4, P02-T02, FR-B
* Evidence: workbench_browser_check.py:493 already waits for "No cases match these filters." on the all-view search; the Coordinator/Unknown step and a PM-default step have no text assertion planned beyond "Unknown text"; the manifest `empty_reason` ("no representative scenario supplied") is a static label.
* Concern: Without an assertion that the empty default does not surface the manifest label or a declared claim, a future regression to inference would not be caught; PM `ZF-5` default is not explicitly asserted as having no empty-state element.
* Impact: Weak regression value once the browser gate is admitted.
* Smallest useful change: Add expectations: Coordinator empty default shows the Unknown sentence and not "unrepresented"/"no representative scenario"; PM default has no `.empty` element; no-match text names that it is not a coverage statement. Keep them marked unexecuted.
* Action owner: planning parent
* Exact resolving evidence: details P02-T02 lists these three assertions with their check names.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-008 -->
### PC-008 [Low]: Publication and claim boundaries are implicit

* Related IDs: AC5, F3, Handoff, P03-T03
* Evidence: Plan has no step for `Refs #152` with unmet criteria, the required focused gate (`python3 tools/rpi-checks.py --changed`) before publication, or journey_acceptance staying `partial`; P03-T03 is conditional on a README section existing.
* Concern: A reviewer cannot tell that publication is blocked pending the gate (caller forbids running it now), or what the PR must say about AC-034/043 and the owner's supported-device decision.
* Impact: Risk of a closing keyword or acceptance wording at publication.
* Smallest useful change: Add to Handoff: PR body uses `Refs #152` and lists C5 remainders (runtime producer, browser run, supported devices owner decision); publication blocked until the focused gate, independent exact-head review and hosted CI; no change to src/core journey_acceptance.py. Make P03-T03 decide yes/no explicitly with the section name.
* Action owner: planning parent
* Exact resolving evidence: Handoff section contains those statements; P03-T03 names the README section or records "no suitable section".
* Decision route: direct planner correction

## Strengths and Residual Risk

* Fail-closed default, rejected inference routes and deferred full-tier producer match the caller brief; no auth/SQL/schema/server change.
* Reuse of the existing node vm test pattern keeps tests runnable without a browser.
* Residual (accepted by brief): no runtime producer; browser checks unexecuted; supported devices remain an owner decision; the two manifests' status semantics stay unreconciled (F2).

## Questions or Blocking Evidence Gaps

* None. No user decision is required for any finding.

## Limitations

* Static assessment only; no tests, node or browser were run. The final copy strings do not exist yet, so PC-001 is judged on the substrings currently asserted.

## Recommended Next Action

* Highest-impact finding: PC-001 (with PC-002 as equal-priority safety correction)
* Action owner: planning parent
* Smallest next action: revise plan and details directly for PC-001..PC-008 (exact strings, non-empty typeof binding, helper owns filtered/total gate, provenance in declared text, precondition fetch, tripwire and wording, browser assertions, handoff), then finalize without another critique.
* User response required: no

## Artifacts

| Artifact | Description |
|---|---|
| [.copilot-tracking/plans/2026-11-09/issue-152-empty-queue-coverage-plan.md](.copilot-tracking/plans/2026-11-09/issue-152-empty-queue-coverage-plan.md) | Plan under critique |
| [.copilot-tracking/details/2026-11-09/issue-152-empty-queue-coverage-phase-details.md](.copilot-tracking/details/2026-11-09/issue-152-empty-queue-coverage-phase-details.md) | Phase details under critique |
| [.copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-research.md](.copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-research.md) | Supplied research |

## Next Steps

No user action required. Standalone critique: the planning parent (`/rpi-plan`, or the active parent if dispatched) applies PC-001..PC-008 directly and finalizes.
