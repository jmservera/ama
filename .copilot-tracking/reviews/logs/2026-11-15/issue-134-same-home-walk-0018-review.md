<!-- markdownlint-disable-file -->
# Review: Issue #134 Profile Journey Contract and Connected Same-Home Journey Acceptance

## Scope and Evidence

* Task ID: issue-134-same-home-walk-0018
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P02-T03`, `P03`, `P03-T01`, `P04`, `P04-T01`)
* Assessed boundary: Code-testable profile journey contract and connected same-home walkthrough invariants across the six staff profiles (`Retrofit Programme Manager`, `Retrofit Coordinator`, `Resident Liaison Officer`, `Building Safety Liaison`, `Quality Inspector`, `Grants and Evidence Officer`), `Programme Support Officer`, `Contractor`, and read-only `ResidentPreview` (`GET /resident/view`), specialist screen plain-language next-action continuity (`role-screens.js`), canonical UX contract documentation (`docs/reference/research/ux/profile-journey-contract.md` + KB index/log), explicit `not-established` human/resident/accessibility boundaries (`Refs #134`), and Focused-tier verification.
* Plan: .copilot-tracking/plans/2026-11-15/issue-134-same-home-walk-0018-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-134-same-home-walk-0018-phase-details.md
* Plan critique: .copilot-tracking/critiques/2026-11-15/issue-134-same-home-walk-0018-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-134-same-home-walk-0018-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/issue-134-same-home-walk-0018-research.md, `src/core/src/zava_forward/core/profile_journey_contract.py`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/core/tests/test_profile_journey_contract.py`, `src/api/tests/test_same_home_profile_journey_acceptance.py`, `docs/reference/research/ux/profile-journey-contract.md`, `docs/reference/README.md`, `docs/reference/log.md`, and live `web-design-guidelines` review.

## Opening Review State

* Interpreted review goal: Assess once, against reconciled workspace artifacts and Focused-tier validation outputs, whether the delivered implementation satisfies all approved requirements, acceptance criteria, critique dispositions (`PC-001`–`PC-006`), and human/resident/AT governance boundaries for Issue #134 (`Refs #134`).
* Review scope: Full task (`P01` through `P04`)
* Evidence readiness: Ready; research, plan, phase details, single-pass critique, and changes record are complete and reconciled.
* Acceptance basis: Caller prompt scope items 1–5 (`Refs #134`), plan requirements `FR-01`–`FR-06` and `NFR-01`–`NFR-04`, acceptance criteria `AC-01`–`AC-05`, and critique dispositions `PC-001`–`PC-006`.
* First comparison boundary: Compare `P01-T01` (`profile_journey_contract.py`) and `P02-T01` (`role-screens.js`) against `FR-01`–`FR-05`, `PC-001`, `PC-002`, and `PC-004`.
* Active read-only boundaries: This review creates only `.copilot-tracking/reviews/logs/2026-11-15/issue-134-same-home-walk-0018-review.md` and mutates no source code or prior RPI phase artifacts.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Full task boundary reviewed on 2026-11-15 across all seven changed/created workspace files, all five prior `.copilot-tracking/` phase artifacts, Focused-tier `mypy`/`ruff`/`unittest` runs in `src/core` and `src/api`, and refreshed `web-design-guidelines` evaluation.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01` | Connected same-home contract helpers in `src/core` (`profile_journey_contract.py`) | Reconciled | `[x]` in plan, `Complete` in changes record, verified by `mypy`, `ruff`, and 8 unit tests. |
| `P02`, `P02-T01` | Plain-language next-action continuity on `role-screens.js` (`data-same-home-next-action`) | Reconciled | `[x]` in plan, `Complete` in changes record, verified by Node `vm` screen tests and `web-design-guidelines`. |
| `P02`, `P02-T02`, `P02-T03` | Core and full-stack API/ResidentPreview/Node same-home acceptance suites | Reconciled | `[x]` in plan, `Complete` in changes record, single new test file (`PC-003`), zero skipped tests (`PC-006`). |
| `P03`, `P03-T01` | Canonical UX profile journey contract reference, KB index row, and KB log entry | Reconciled | `[x]` in plan, `Complete` in changes record; minor prose symbol-name mismatch recorded in `RV-001`. |
| `P04`, `P04-T01` | Focused validation, traceability/link guards, and `web-design-guidelines` review | Reconciled | `[x]` in plan, `Complete` in changes record (`105` `src/core` + `123` `src/api` tests `OK`). |
| `Follow-Up Items` | Live human/resident/AT perspective walkthroughs (`#155`, `#151`) and optional Chromium `role_screens_browser_check.py` assertion | Reconciled | Kept outside active automated completion claims (`Refs #134`, `accepted = False`) and mirrored in changes record. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/profile_journey_contract.py` | Added `SIX_STAFF_PROFILES`, `REASON_STAFF_PROFILES`, `REDACTED_STAFF_PROFILES`, `BANNED_INTERNAL_TERMS`, `SAME_HOME_NOTICE`, `check_shared_facts`, `check_vulnerability_redaction` (with `private_markers` and `contractor_private_markers`), `check_handover_dependencies`, `check_next_action_continuity`, `project_same_home_bundle`, and `validate_same_home_walk` while preserving `validate()`, `gaps()`, `BOUNDARIES` (`not-established`), and `accepted = False`. | Code diff and passing unit/acceptance tests covering both clean end-to-end transitions and negative tamper cases. | Passed (`mypy`, `ruff`, `test_profile_journey_contract.py`) | Reconciled |
| `P02-T01` | `src/api/src/zava_forward/api/web/role-screens.js` | Added `<p data-same-home-next-action="${c.id}">` inside `section.screen-evidence` showing `Current owner` and plain-language `Next action` when `c.work?.next_action` is present on staff projections while omitting internal `work` continuity on contractor payloads. | Code diff, Node `vm` assertions across all six staff specialist screens plus `contractor-job-pack`, existing connected-journey/stage-map regression suites, and `web-design-guidelines` `pass`. | Passed (`123` `src/api` tests, `web-design-guidelines`) | Reconciled |
| `P02-T02` | `src/core/tests/test_profile_journey_contract.py` | Added `ConnectedSameHomeContractTests` testing shared facts, sibling isolation, vulnerability/free-text redaction, safety/stock/consent/handoff/worker-receipt/independent-QA preconditions, plain-language next-action continuity, and `accepted = False` boundaries over live `Store` transitions. | `8` tests pass with zero skips alongside `test_perspective_walkthroughs.py` and `test_journey_acceptance.py`. | Passed (`Ran 105 tests in 1.773s — OK`) | Reconciled |
| `P02-T03` | `src/api/tests/test_same_home_profile_journey_acceptance.py` | Added single consolidated full-stack HTTP (`App`) + live loopback `ResidentPreview` (`GET /resident/view`, `GET /resident/home/ZF-1`) + Node `vm` `role-screens.js` acceptance module verifying same-home transitions, unassigned (`404` / `[]`) vs assigned contractor redaction, `403` on contractor `/job-pack`, and human/AT `not-established` boundaries. | `2` comprehensive end-to-end tests pass with zero skips (`nodejs` `/usr/bin/node` v20.20.2). | Passed (`mypy`, `ruff`, `Ran 123 tests in 4.242s — OK`) | Reconciled |
| `P03-T01` | `docs/reference/research/ux/profile-journey-contract.md`, `docs/reference/README.md`, `docs/reference/log.md` | Authored canonical UX profile journey contract reference in AMA Markdown style (`*` bullets, plain ASCII punctuation, valid PRD/BRD IDs, explicit `not-established` boundaries), indexed it in `docs/reference/README.md`, and appended `[2026-11-15] create` to `docs/reference/log.md`. | `test_needs_inventory.py` and `test_documentation_links.py` pass; one minor prose code-identifier drift recorded as `RV-001 [Low]`. | Passed (`test_needs_inventory`, `test_documentation_links`); see `RV-001` | Minor doc gap (`RV-001`) |
| `P04-T01` | Workspace validation record | Executed Focused-tier `mypy`, `ruff check .`, `ruff format --check .`, targeted `src/core` (`105`) and `src/api` (`123`) suites, and refreshed `web-design-guidelines` review without modifying `role_screens_browser_check.py` or `scenario-manifest.json`. | Recorded in `.copilot-tracking/changes/2026-11-15/issue-134-same-home-walk-0018-changes.md`. | Passed locally; hosted CI unobserved pre-push (`RV-002`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` / `P02-T03` local signature refinement (`contractor_private_markers` parameter on `check_vulnerability_redaction` and `validate_same_home_walk`; HTTP `404` expectation for unassigned contractor `/api/cases/ZF-1`) | Separated `contractor_private_markers` (such as `resident.phone`, which internal staff roles legitimately view while contractor, job-pack, work-order, and resident-preview surfaces strip) from `private_markers` (secrets redacted from non-reason staff as well), and aligned unassigned contractor `/api/cases/ZF-1` assertion with existing HTTP `404` anti-enumeration behavior. | Observed during `P02-T03` test execution against live `projection.for_role` and `App` behavior; classified as ordinary local implementation judgment preserving approved intent (`FR-02`, `AC-02`). | Recorded in `.copilot-tracking/changes/2026-11-15/issue-134-same-home-walk-0018-changes.md` under `## Plan and Detail Updates`. | Plan `Ready`; `PC-001`–`PC-006` preserved without needing re-critique. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All six single-pass critique findings (`PC-001` [High], `PC-002` [Medium], `PC-003` [Medium], `PC-004` [Medium], `PC-005` [Medium], `PC-006` [Low]) were applied directly before implementation and verified in the delivered code, tests, and documentation (subject to minor prose identifier note `RV-001`).
* Material revisions: None occurred during implementation; no confirmed user constraint or architectural boundary changed.
* Dependent-work pause assessment: Phases `P01` -> `P02` -> `P03` -> `P04` ran in dependency order with no premature resumption.
* Justification assessment: Fully supported by source inspection and passing test runs.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Execute and record human/resident and assistive-technology perspective walkthroughs (`#155`, `#151`) for `AC-034`–`AC-043` | Requires live human role representatives, residents, and screen-reader/keyboard AT sessions; repository rules forbid fabricating human/accessibility acceptance from synthetic tests (`Refs #134`). | Named UX/accessibility and housing role owners under Issues `#155` and `#151`. | Open distinct human-gated follow-up (`follow_up`). |
| Optionally extend `src/api/checks/role_screens_browser_check.py` and refresh `scenario-manifest.json` recipe SHA in a browser-harness slice | `role-screens.js` continuity was verified deterministically via Node `vm` + live loopback HTTP in `test_same_home_profile_journey_acceptance.py` without mutating frozen scenario-manifest recipe SHAs in this Focused-tier slice. | Optional future browser-harness maintenance slice. | Open distinct non-blocking follow-up (`follow_up`). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Prose symbol-name drift in `docs/reference/research/ux/profile-journey-contract.md` for `perspective_walkthroughs.register()` and `BOUNDARIES` keys

* Related scope: `P03-T01`
* Evidence: `docs/reference/research/ux/profile-journey-contract.md` (`## Five-element profile journey contract across eleven perspectives` and `## Explicit human, resident and accessibility boundaries`) compared with `src/core/src/zava_forward/core/perspective_walkthroughs.py` (`register()`) and `src/core/src/zava_forward/core/profile_journey_contract.py` (`BOUNDARIES`)
* Impact: Low (documentation accuracy only; zero runtime, security, redaction, continuity, link, or `test_needs_inventory` failures). The Markdown prose references `perspective_walkthroughs.PERSPECTIVES` instead of `perspective_walkthroughs.register()` (whose 11 PRD perspective keys include `assessor-designer`, `retrofit-case-team`, and `digital-auditor`), and labels the four-row governance table `Boundary key in BOUNDARIES` (`human_approval`, `resident_consent`, `live_accessibility_walkthrough`, `perspective_walkthrough_signoff`) whereas `profile_journey_contract.BOUNDARIES` defines the three exact dict keys `human_approval`, `resident_approval`, and `accessibility_walkthrough`.
* Destination: `rpi-implement`
* Smallest useful next action: Update those two symbol references in `docs/reference/research/ux/profile-journey-contract.md` to name `perspective_walkthroughs.register()` (with its exact 11 perspective IDs) and the exact three `profile_journey_contract.BOUNDARIES` keys (`human_approval`, `resident_approval`, `accessibility_walkthrough`) alongside the fourth `perspective_walkthroughs` / `journey_acceptance` gate row, then re-run `test_needs_inventory.py` and `test_documentation_links.py`.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Hosted GitHub Actions CI, PR human review, and live perspective/AT walkthroughs (`#155`, `#151`) remain post-commit / human-owned gates

* Related scope: `P04-T01` and caller publication boundary (`Refs #134`)
* Evidence: `.copilot-tracking/changes/2026-11-15/issue-134-same-home-walk-0018-changes.md` (`## Validation Record`); caller prompt (`Do NOT push; leave a clean frozen local commit for coordinator review`)
* Impact: Focused-tier local checks (`mypy`, `ruff check .`, `ruff format --check .`, `105` `src/core` tests, `123` `src/api` tests, and `web-design-guidelines`) all passed, while hosted GitHub Actions CI and independent PR review remain unobserved until the coordinator pushes `feat/ux-134-same-home-walk-0018` against `feat/demo-233-same-home-tensions-0825`, and live walkthroughs (`#155`, `#151`) remain open (`Refs #134`).
* Destination: `follow_up`
* Smallest useful next action: Coordinator reviews the local commit on `feat/ux-134-same-home-walk-0018`, pushes and opens the stacked PR targeting `feat/demo-233-same-home-tensions-0825` (`#1639`) to observe hosted CI and complete human review, and keeps Issue `#134` open (`Refs #134`) until `#155` and `#151` complete.

## Defects

* `RV-001` [Low]: Align `perspective_walkthroughs.register()` and `profile_journey_contract.BOUNDARIES` key names in `docs/reference/research/ux/profile-journey-contract.md` -> destination `rpi-implement`.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Align two Python symbol mentions in `docs/reference/research/ux/profile-journey-contract.md` | Low-severity documentation symbol-name drift within accepted architecture |
| `RV-002` | Distinct follow-up | Coordinator branch push / stacked PR targeting `feat/demo-233-same-home-tensions-0825` + hosted CI + `#155`/`#151` human walkthroughs | Unpushed local commit requested by caller; human/AT sign-off remains outside code tests |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Coordinator review, push of `feat/ux-134-same-home-walk-0018`, stacked PR creation against `feat/demo-233-same-home-tensions-0825` (`#1639`), and hosted CI verification on the exact head (`RV-002`).
* Human role-representative and resident walkthroughs (`#155`) plus live screen-reader/keyboard assistive-technology testing (`#151`) required before `AC-034`–`AC-043` and Issue `#134` can close (`Refs #134`).
* Optional Chromium `role_screens_browser_check.py` assertion for `[data-same-home-next-action]` paired with a `scenario-manifest.json` recipe SHA update.

## Blockers and Remaining Work

* Blockers: none for local commit completion on `feat/ux-134-same-home-walk-0018` (human PR review, hosted CI, and `#155`/`#151` live walkthroughs remain open external gates, so commit uses `Refs #134`).
* Remaining active work: none in this RPI loop (`P01`–`P04` complete; review complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m ruff check . && python3 -m ruff format --check .` | `src/core` | Passed | `All checks passed!`, `262 files already formatted` |
| `python3 -m mypy` | `src/core` (317 source files) | Passed | `Success: no issues found in 317 source files` |
| `python3 -m unittest tests/test_profile_journey_contract.py tests/test_perspective_walkthroughs.py tests/test_journey_acceptance.py tests/test_scenario_manifest.py tests/test_needs_inventory.py tests/test_documentation_links.py -v` | `src/core/tests` (105 tests) | Passed | `Ran 105 tests in 1.773s — OK` |
| `python3 -m ruff check . && python3 -m ruff format --check .` | `src/api` | Passed | `All checks passed!`, `200 files already formatted` |
| `python3 -m mypy` | `src/api` (286 source files) | Passed | `Success: no issues found in 286 source files` |
| `PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest tests/test_same_home_profile_journey_acceptance.py tests/test_connected_home_check.py tests/test_role_screens_same_home_identity.py tests/test_role_screens_connected_journey.py tests/test_role_screens_stage_map_focus.py tests/test_content_standard.py tests/test_prd_traceability.py -v` | `src/api/tests` (123 tests) | Passed | `Ran 123 tests in 4.242s — OK` (zero skipped tests) |
| Refreshed `web-design-guidelines` review (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`) | `src/api/src/zava_forward/api/web/role-screens.js` | Passed | `role-screens.js`: `✓ pass` (zero `file:line` findings) |
| Hosted GitHub Actions CI | `feat/ux-134-same-home-walk-0018` | Unavailable | Unobserved locally because caller instructed `Do NOT push` (`RV-002`) |

## Outcome

* Outcome: Defects found
* Outcome rationale: All code-testable profile journey contract and connected same-home invariants (`FR-01`–`FR-06`, `NFR-01`–`NFR-04`, `AC-01`–`AC-05`, `PC-001`–`PC-006`) are implemented and verified with zero functional, security, redaction, continuity, typing, lint, or test failures across `105` `src/core` tests and `123` `src/api` tests; review identified one `[Low]` prose Python-identifier drift in `docs/reference/research/ux/profile-journey-contract.md` (`RV-001`, routed to `rpi-implement`) alongside post-push CI and human/AT walkthrough gates (`RV-002`, routed to distinct follow-up).

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` | `RV-001` [Low]: Align `perspective_walkthroughs.register()` and `BOUNDARIES` key names in `docs/reference/research/ux/profile-journey-contract.md` |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | Distinct follow-up | `RV-002` [Low]: Coordinator push/PR against `feat/demo-233-same-home-tensions-0825` + hosted CI + `#155`/`#151` live walkthroughs + optional Chromium `role_screens_browser_check.py` assertion |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: Focused-tier local checks passed (`src/core` ruff/mypy/105 tests `OK`; `src/api` ruff/mypy/123 tests `OK`; refreshed `web-design-guidelines` `pass` on `role-screens.js`); hosted CI unobserved pending coordinator push
* Blockers: none
