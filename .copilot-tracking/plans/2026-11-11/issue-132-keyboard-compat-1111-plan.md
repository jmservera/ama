---
title: Issue 132 keyboard probe compatibility plan
description: Prospective plan to declare staff-job-pack-intake in the existing specialist keyboard probe and guard against future undeclared screens (issue 132 follow-up)
ms.date: 2026-11-11
---

## Task

Task `issue-132-keyboard-compat-1111`. Research: [issue-132-keyboard-compat-1111-research.md](../../research/2026-11-11/issue-132-keyboard-compat-1111-research.md). Details: [issue-132-keyboard-compat-1111-details.md](../../details/2026-11-11/issue-132-keyboard-compat-1111-details.md). Critique: [issue-132-keyboard-compat-1111-critique.md](issue-132-keyboard-compat-1111-critique.md). State: `.copilot-tracking/rpi-sessions/2026-11-11/issue-132-keyboard-compat-1111-state.json`.

Candidate base `35eb0e559c7d0660ab87594732675b71be7bee67`, target `main`. This is a planning candidate only. Nothing here is implemented, run in a browser or authorized for correction cycle E4.

## Objective

Make the existing specialist keyboard probe account for the `staff-job-pack-intake` screen added by #132 PR1425, while `region_failures` keeps rejecting every genuinely undeclared screen. No product, role, approval, grant or unrelated fixture change; no new browser checker; no helper signature change.

## Smallest delta (two files, both existing)

* `src/api/checks/specialist_keyboard_browser_check.py`: add `"staff-job-pack-intake"` to the tuple inside `NO_REGION_GAPS`. Source shows the maintained fixture has no work orders, so the screen renders no evidence table (research, "Which declaration is correct"). The predicate, signatures, `EXPECTED_REGIONS`, walk and negative controls are unchanged.
* `src/api/tests/test_specialist_keyboard_check.py`: one new test, `test_staff_intake_screen_is_declared_and_unknown_screens_still_fail`, which fails before the repair and whose drift guard fails on unparseable registration forms.

No README edit by default (see Dependencies). No other file.

## Phases

* [ ] Phase 1: add the failing regression first (see details), confirm it fails on base for the stated reason only.
* [ ] Phase 2: add the screen id to `NO_REGION_GAPS`; rerun the targeted unit test to green.
* [ ] Phase 3: static checks on the two files; then, only under an admitted E4 and a free lock, one affected browser run of the existing probe to confirm `regions == []` for all seven roles. If the render shows a table, stop and re-plan instead of widening the gap.
* [ ] Phase 4: changes record and one Review, handled by the later run.

## Role and screen matrix

| Role (seven permitted) | Served the screen | Expected regions on this fixture | Basis |
| --- | --- | --- | --- |
| Retrofit Coordinator | Yes | none (declared gap) | no work orders in `synthetic_data()` |
| Resident Liaison Officer | Yes | none (declared gap) | same |
| Building Safety Liaison | Yes | none (declared gap) | same |
| Grants and Evidence Officer | Yes | none (declared gap) | same |
| Quality Inspector | Yes | none (declared gap) | same |
| Retrofit Programme Manager | Yes | none (declared gap) | same; manager behaviour needs an order |
| Programme Support Officer | Yes | none (declared gap) | same |
| Contractor (eighth manifest role) | No, not in `intakeRoles` | not walked | menu never lists it |

There is no per-role difference to encode. The `NO_REGION_GAPS` mapping is role-independent, which matches the source.

## Dependencies and conflict avoidance

* Same-function inputs: `walk_screen`, `region_failures`, `NO_REGION_GAPS` (all in the existing probe), `staff-intake.js` (read-only), `workbench_browser_check.synthetic_data` and `workbench-manifest.json` (read-only, unchanged).
* Root134 adds `connected_home_browser_check.py`, `test_connected_home_check.py` and a short README paragraph and imports existing helper APIs read-only. This plan changes only data in `NO_REGION_GAPS`, so there is no signature change and no file overlap. It does not edit the README.
* Stale README count: `src/api/README.md:4162` says "five screens have no evidence table". After the repair it is six. Decision for root at E4 admission: if the 134 README hunk does not touch lines 4146-4166, change the single word to "six" in the same candidate; otherwise leave the README unchanged and record the stale count as a named follow-up. The README edit is not required for the code to be correct.
* Heavy lock: #134 owns the single final connected-browser admission. This plan neither queues nor acquires it.

## Validation plan

Smallest targeted proof, not blanket suites (details give exact commands):

* Regression plus existing helper tests, from `src/api`: `tests/test_specialist_keyboard_check.py` only.
* Static: ruff check and format check, and mypy, on the two changed files only, using the pinned repository configuration.
* Browser (E4 only, free lock, no earlier): `python -m checks.specialist_keyboard_browser_check` once, with the existing pinned Chromium and the existing keyboard-probe axe/helper origins supplied by root. Expect gap observations for `staff-job-pack-intake` for each of the seven roles and no new FAIL; this admits only that no table rendered, not the empty-order cause. No full gate, SQL, image or cloud work.

## Correction authority

Original #132 C5 is exhausted. The owner's separate five-cycle extension of 2026-11-10 has used E1, E2 and E3; two remain (E4, E5). This plan consumes no source correction, authorizes no E4, and preserves the E2 chronology and adverse record and the E3 limitations. Root decides separately whether a concrete safe delta exists and admits E4. No extra five, cycle reset or #134 grant is inferred.

## Risks

* The gap is predicted from source. If the admitted render shows a table or a failure, the declaration is wrong and the plan must be revised, not the predicate loosened.
* Declaring a gap means this probe does not exercise populated intake states; #132's opt-in browser test remains the evidence for those and is not replaced.
