# RPI record: #229 and #230 operator and programme-role readiness (tracking-only)

Date: 2026-11-13. Base: frozen parent b9d7db29b (feat/demo-home-parent-0555, PR1504). Main baseline 15bfee2d7 is an ancestor. Parent G5 read-only display is not main acceptance. Documentation only: no source, test, infrastructure, web or script change, and no gate, browser, SQL, cloud or model call was run.

## Reading manifest and phase boundaries

* Read in full: the demo run ledger (prior dispositions, searched for #229/#230 and role readiness; 1.08 MB file, so read by targeted ranges, not end to end), live bodies and all comments of #229 and #230 via `gh issue view`.
* Verified present in this worktree (path existence only, contents not re-read): `src/api/checks/data_operator_browser_check.py`, `src/api/checks/data_operator_ai_state.py`, `src/api/checks/programme_paging_browser_check.py`, `src/api/src/zava_forward/api/web/role-screens.js`.
* Not read, by five-minute budget: `docs/case_study_48_*`, `docs/reference/README.md`, `memory.md`, component guides, the two PRD/journey sources. Prior ledger rows already cite them for these issues; this record adds no new claim from them.
* Phases: Research done (bounded); Plan done; independent critique NOT performed by an independent agent (self-critique only, below); Implementation is documentation of the disposition only; Review is a root self-review, not independent. These are limits, not passes.

## Per-AC disposition (literal ACs from live bodies)

| Issue | AC | State | Evidence or precise unknown |
| --- | --- | --- | --- |
| #229 | 1 both source values and provenance | ticked | Checker `data_operator_browser_check.py`; merged PR779, PR1264 into parent; ledger row records engineering on main via #1286/#1376 (no byte-equality or rerun claim) |
| #229 | 2 unresolved eligibility preserved, no replay | ticked | same checker; PR779 |
| #229 | 3 event metadata and recovery context | ticked | `data_operator_ai_state.py`, PR1264 (parent-topic integration only) |
| #229 | 4 WCAG 2.2 baseline, textual state, keyboard | UNMET | Automated keyboard/axe exist (PR779 follow-ups, README 1316-1341 per #229 comment); the remaining predicate is human AT and manual WCAG acceptance owned by #151/#155. Unknown: whether #155 has produced any session; not checked in this budget |
| #229 | 5 design system, no role simulator | ticked | PR496 host; not re-verified |
| #230 | 1-3, 5 | ticked | PR662, 781, 818, 854, 931, 969, 1366; `programme_paging_browser_check.py` |
| #230 | 4 WCAG 2.2 baseline | UNMET | Same human AT predicate; #230 RPI comment 2026-11-04 states no code slice can prove it |

## Findings

* Same pin and same AC finding as the prior ledger rows (role readiness trace 318b3ace2; #229 screen; #230 closure comment): only AC4 remains on both issues and it is a human assistive-technology and manual WCAG acceptance criterion, not missing code. Lane stopped; no repeat of the history.
* Source already implemented but unverified at current head is not missing code. No new local engineering increment is required by these ACs.
* Held and known items (184, c71, 1288, 74b9, 891, 531, 144, 189, 146, 96, AI bdec) were not rediscovered or reopened.
* This worktree is a child of the frozen parent, not an independent main feature. A future change needs real authority, ready inputs, ordering/overlap check and exact-head assessment.

## Plan outcome (exact-slice disposition)

No initial local engineering slice. No dependencies, no shared-file overlap to order, no regression plan to run. Not an owner block: the unmet AC is human/cloud-style evidence that does not block unrelated local engineering.

## Self-critique

* Risk: treating ledger statements as current. Mitigation: path existence checked at this head; live issue comments re-read today; no byte or run claim made.
* Gap: no independent critique or Review agent was run (budget). The disposition should be read as research-grade, not conformant-reviewed.

## Resume condition

Resume only when #155 or #151 supplies actual assistive-technology or manual WCAG 2.2 evidence for the operator or programme screens, or when a current-head defect is observed in the cited checkers. Then re-read the checkers at the exact merged main pin. Do not tick AC4 from automated checks.
