---
title: Research, #134 criterion 2 AC-034 to AC-043 disposition reconciliation
description: Existing-delivery reconciliation of the ten PRD acceptance criteria against the register, the evidence pack and exact source, with a Planning Readiness decision
ms.date: 2026-11-12
ms.topic: reference
---

## Task identity and boundary

* task_id and task_slug: `ac-dispositions-134-1112`; parent task `issue-134-connected-plan-1111` (lineage only).
* Branch `docs/journey-ac-dispositions-134-1112`, worktree `issue-134-ac-dispositions-1112`.
* Declared PR target `feat/demo-ux-integration-1112`; integration lineage #149 to `main`. Actual identities read 2026-11-12 (local, no push): HEAD, `origin/main` and the local `feat/demo-ux-integration-1112` all equal `43b2187b918206666c63cb25d8b338be09791118` (tree `67cbe8ede92d4f9f02ac3a3f71d0de06872f6b55`). `origin/feat/demo-ux-integration-1112` does not exist on the remote; the parent is local only. The #153 employee-copy author shares that parent but owns its own dirty source, which is not touched.
* Model: explicit `claude-sonnet-5.5` for this native task and its subagents. The label is asserted by the launcher; no witness or host attestation exists.
* Scope: one bounded documentation-readiness slice for the literal #134 criterion 2 ("AC-034 to AC-043 ... pass or are recorded as deferred with reason"). Not a source correction, not an eleven-profile audit, not the five-home runbook, not a rerun of the PR 1455 integration. Preserved: A4 and E1 to E4 spent, E5 and E6 unadmitted.

## Sources read

* Live #134 body and all comments (read 2026-11-12): criteria 3, 4 and 6 are ticked; criteria 1, 2 and 5 are open. The 2026-11-05 audit states the register was "still 6 partial/4 deferred, none passed".
* PRD Zava Forward 0.21.0, `in-review`, blob `c788b917bafa` (HEAD): AC-034 to AC-043 at lines 2130 to 2139; proposed check table 2251 to 2257.
* Register: `src/core/src/zava_forward/core/journey_acceptance.py` and `src/core/tests/test_journey_acceptance.py`, indexed by [src/core/README.md](../../../src/core/README.md#acceptance-register-for-ac-034-to-ac-043-134-slice-2) and the 2026-11-04 log entry.
* Evidence pack sections that trace some of the ten: 2026-11-10 merged-wave (empty-queue coverage), parent 149 coverage, specialist keyboard probe, 2026-11-11 handoff waiting screen, personal handoff HTTP guidance, keyboard probe compatibility, 2026-11-12 post-153 checkpoint.
* Profile review `docs/reference/research/ux/zava-forward-prototype-profile-review.md` (blob `97742e9c`): the #134 journey and gate rows, the AC-034 focus limitation (line 1020 onward) and the #85 hazard referral continuation.
* Dependencies named in the issue (#103, #76, #84, #90, #91, #94): outcomes were read only through the log, the profile review and the pack, not re-audited.

## Existing delivery found

Observed now at HEAD, read-only, local, constructed data: `journey_acceptance.check` returns status `recorded`, no blockers, `passed` empty, `partial` AC-034, 037, 039, 040, 042, 043, `deferred` AC-035, 036, 038, 041. `python -m unittest tests.test_journey_acceptance tests.test_journey_store tests.test_journey_building` (src/core, `PYTHONPATH=src:tests`) ran 15 tests, OK. This is register integrity, not criterion acceptance. No file was changed by the run (`git status` clean).

What already exists and is complete: all ten IDs are recorded with a status, a reason and evidence paths, are blocked by the check when missing, and are indexed. None is recorded as passing.

## Gap analysis

| Question | Finding |
| --- | --- |
| Is every one of the ten recorded as pass or deferred with reason? | Partly. Four are `deferred` with reason. Six are `partial`, a status the literal criterion does not name; their reasons say what is unproven but not that the remainder is deferred. |
| Does any record name an owner and a resume condition? | No. The register has only status, reason and evidence. The evidence pack names owners and gaps only inside per-checkpoint sections, none of which covers all ten. |
| Is the register current against merged evidence? | Not fully. Its reasons say "not mapped yet" for AC-035 and AC-038, but the tree holds a named-update commitment path (`resident_decisions.py` `_res_update_record`, tests at `test_resident_decisions.py:3278` and `:3544`) and a hazard referral contract with `test_hazard_referral.py` (33 run on SQLite in the 2026-10-17 #85 record). AC-036 later gained merged handoff scope, waiting-time and refusal-versus-load-failure guidance (PRs 1444 and 1449 on main, observed in the evidence-pack sections at lines 7148 and 7213). AC-034 and AC-040 gained queue-scope and per-home atlas checks through PR 1376. These are candidate evidence, not a proof of any Given/When/Then. |
| Is one consolidated, document-qualified ten-row disposition in documentation present? | No. The traces are scattered across about ten dated evidence-pack sections, each tracing a subset, so a reader cannot see the complete literal disposition. |
| Can the register be updated? | Not in this slice. It is source under `src/` and the task forbids source changes. The documentation consolidation must say it is a reconciliation record and that the register wording is unchanged and conservative. |

Conclusion: a complete accurate indexed disposition exists for status and reason (the register) but not for owner, resume condition, current candidate evidence or the pass-or-deferred reading of "partial". That is a genuine, small documentation gap. It is a distinct increment, so the lifecycle continues past Research.

## Per-criterion reconciliation (inputs to the plan)

Every observed Pass below is source-qualified and version-qualified by its pack section; none is promoted to a current execution unless stated. The only execution in this task is the register check and the 15 tests above.

| AC | Register | Existing observed evidence (qualified) | Not shown |
| --- | --- | --- | --- |
| 034 | partial | Workbench browser check 108 PASS lines (merged-wave section, 2026-11-10, local synthetic); keyboard and evidence probe at `b23c08e33` (714 PASS lines, 38 role-screen walks, 15 negatives, first listed home); programme paging 89 PASS and role-screens story 230 at 70 PASS (parent 149 section, parent integration before PR 1376) | Focus return to the originating row (profile review states focus goes to main), per-profile reset comparison for all eleven, announcement by assistive technology, a declared-gap producer for unrepresented versus zero match |
| 035 | deferred | Candidate only: commitment record path and two focused tests exist in Core | Mapping to the rejected-handoff Given/When/Then, a screen showing purpose, owner, due basis and safe-route reference |
| 036 | deferred | Merged staff waiting screen (PR 1444, pack section at line 7148, trace row line 7164) and personal handoff guidance (PR 1449, pack section at line 7213, trace row line 7230), local synthetic | Agreement of owner, destination, receiver and chase-owner labels across queue, detail, source and history; the keyboard walk saw only that owner or next-action text exists |
| 037 | partial | Per-measure decision records and `test_resident_decisions.py` (Core) | Pause isolation and consent versus contact checks mapped to the criterion; service and redress owner display |
| 038 | deferred | Candidate only: hazard referral and home-hold contract, `test_hazard_referral.py` (profile review `Hazard referral evidence engineering continuation (2026-10-17, #85)`, lines 589 to 630: 33 run on SQLite, 16 on task-owned SQL Server, original adverse review retained) | Workbench display of awareness, sent reference, chase owner and read-only release reference for the constructed referral; named hazard-service human acceptance |
| 039 | partial | Capacity and package records, `test_quality_procurement.py`; provider capacity continuation #90 | Draft-package readiness display with period, scope, offered versus committed and next reviewer |
| 040 | partial | Source-conflict queue and `test_exception_queue.py`; atlas checker 362 PASS and stories 231 family (parent 149 section, parent integration) | Per-case rationale agreement across all eight fixtures on switching; the Quality Inspector technical note omission stays unasserted |
| 041 | deferred | None mapped | Portfolio figures with population, as-of basis, denominator and filter impact; handover versus accepted handover |
| 042 | partial | Quality and finance records, `test_finance_match_controls.py`, `test_quality_procurement.py` | Incomplete-pack and quantity-mismatch invoice views with independent disposition |
| 043 | partial | Manifest with eleven profiles and nine workflows and `test_scenario_manifest.py`; #1029 JSON-store trace and #1152 building controls (eleven current-source tests, constructed); perspective register eleven by five with zero met | Slice B connected-exception view, all eleven entries and endpoints, Asset, Procurement and Auditor fixture login roles |

## Owners and resume conditions (existing routing, no new assignment)

* Work owners by existing issue: #134 (walkthroughs and AC-034 to AC-043), #152 (queue scope and reset), #83 (handoff display), #85 (hazard referral), #90 (provider package), #153 (plain-language content), #156 (design M1 decision), #73 (workbench epic), #440 (cadence).
* Human acceptance owner: none is named for any of the ten. Each is recorded as unassigned, not invented.
* Resume condition: for each row, a served or executed check that exercises the criterion's Given, When and Then on constructed fixtures, plus, for AC-034 and the status wording, named human or assistive-technology observation that this repository has not recorded.

## Boundaries

* No requirement approval, no owner approval of any deferral, no epic acceptance, no pivot. A recorded limitation is neither.
* Legal and regulatory claims: none are made. AC-038 touches hazard handling; the workbench does not judge release sufficiency and no statutory clock is asserted.
* Not run: Chromium checks, axe, SQL Server, hosted CI, any model, cloud or private data.

## Research disposition and Planning Readiness

* Research disposition: `executed` (reconciliation, one read-only check and 15 existing unit tests).
* Planning Readiness: `Ready` for one documentation integration into the profile review, one index sentence and one log entry. If critique finds any claim unsupported, that row falls back to the register wording.
