<!-- markdownlint-disable-file -->
# RPI Plan Critique: Journey Learning-Test Bundles and Role-Screen Scenario Verification (Issue #129)

## Metadata

* Task ID: issue-129-learning-test-bundles-0023
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/learning-test-bundles-129-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/learning-test-bundles-129-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Assess the candidate plan and phase details for `issue-129-learning-test-bundles-0023` (`learning-test-bundles-129`) on branch `feat/ux-129-learning-test-bundles-0023` (`Refs #129`), implementing five-bundle learning-test metadata and unit/role-screen scenario verification in `src/core/tests/` and `src/api/tests/`, keeping `O10` and `O18` to `O20` out of scope, respecting the `docs/reference/research/ux/journey-learning-test-bundles.md` screen-wiring and run-storage gate pending Atlas-owner confirmation and DPO retention approval, framing saved minutes strictly as `capacity` until Finance validates them, running focused tests plus `ruff` and `mypy`, and leaving one local commit with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing.
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/learning-test-bundles-129-plan.md, .copilot-tracking/details/2026-11-15/learning-test-bundles-129-phase-details.md, .copilot-tracking/research/2026-11-15/learning-test-bundles-129-research.md, docs/reference/research/ux/journey-learning-test-bundles.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md (lines 2848-2875), docs/adrs/0003-journey-derived-capabilities-runtime-fit.md (lines 1-140), src/core/src/zava_forward/core/learning_test_bundles.py, src/core/tests/test_learning_test_bundles.py, src/api/src/zava_forward/api/web/role-screens.js, src/api/src/zava_forward/api/web/aftercare.js, src/api/pyproject.toml, and src/core/pyproject.toml.
* Decisions, dependencies, and acceptance criteria considered: ADR 0003 Decisions 1-5 (`C3`), UX protocol five-bundle table, six-part NFR-009 net-effort rules, per-bundle learning questions, target-zero stop rules, and screen/storage gate (`C1`), PRD candidate journey learning tests table (`C2`), focused validation tier under owner decision D4 / issue #1294, Node.js runtime dependency for Node-VM screen rendering, strict `mypy` configuration in `src/core/pyproject.toml` and `src/api/pyproject.toml` (`follow_imports = "skip"` on `zava_forward.core.*` and `zava_forward.api.server`), and acceptance criteria `AC-1` through `AC-7`.
* Assessment boundary: Evaluates completeness, internal consistency, source-to-code fidelity, typing/linter compatibility, and governance compliance across all supplied artifacts. Does not verify unpushed hosted CI execution, live human usability sessions, Atlas-owner mapping ratification, DPO retention sign-off, or files referenced only indirectly via research log summaries (`src/core/README.md`, `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/aftercare.py`, and existing API test files).

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1, AC-1, AC-2 (`C1`, `C2`, `C4`) | Covered | `P01-T01` adds defaulted `title`, `linked_requirements`, `learning_question`, `beyond_effort_measures`, and `stop_rule` fields after `zero_measures` on `Bundle` and read-only keys on `compare_bundle`; literal values match `docs/reference/research/ux/journey-learning-test-bundles.md` (lines 25-29, 79-83) and `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (lines 2857-2861) while preserving 4-argument `Bundle` calls, `_validate_input` exact `zero_measures` checks (`src/core/src/zava_forward/core/learning_test_bundles.py:287`), and `render_report` output. |
| FR-2, AC-3 (`C1`, `C4`, `C5`, `C12`) | Covered | `P01-T02` closes the missing fifth key (`funding-evidence`) in `src/core/tests/test_learning_test_bundles.py:32` and adds unit assertions for protocol metadata parity, `NFR-009` resident-effort transfer non-saving, individual target-zero breach firing across all six `zero_measures` in both arms, and five-bundle `reconcile_o16` campaign consistency. |
| FR-3, AC-4 (`C1`, `C3`, `C6`, `C7`, `C8`, `C9`) | Covered | `P02-T01` verifies constructed two-arm scenarios across all five bundles (`story-once`, `pre-visit-pack`, `change-impact`, `handover-aftercare`, `funding-evidence`) against real Node-VM renders of `src/api/src/zava_forward/api/web/role-screens.js` and `src/api/src/zava_forward/api/web/aftercare.js` plus `AftercareService` (`unresolved_with_handover_or_financial_closure`), matching exact copy verified in both JS modules. |
| AC-5 (`C1`, `C3`, `C4`, `C10`, `C11`) | Covered | `P01-T02` and `P02-T01` verify `OUT_OF_SCOPE` (`O10`, `O18`-`O20`) exclusion, `representative_data_retained is False`, `capacity` framing, and absence of any unapproved learning-bundle screen among the 13 `registerRoleScreen` registrations in `src/api/src/zava_forward/api/web/role-screens.js` or stored run-record routes in `server.py`. |
| NFR-1, AC-6 (`C10`, `C11`) | Covered | `P02-T01` accounts for `src/api/pyproject.toml:58` (`zava_forward.core.*` with `follow_imports = "skip"` under `strict = true`) by requiring explicit parameter and return annotations on test helpers; `P03-T01` runs `ruff check .`, `ruff format --check .`, `mypy`, and targeted `unittest` plus UI conformance guardrails in `src/core` and `src/api`. |
| NFR-2, AC-7 | Covered | `P03-T02` enforces zero `.copilot-tracking/` strings in `src/`, `docs/`, and commit messages, configures repository-local privacy-safe noreply email via `gh api user`, commits with `Refs #129` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and leaves the branch unpushed per caller direction. |
| P01 (`P01-T01`, `P01-T02`) | Covered | Self-contained core metadata and unit-test phase with exact field specifications, change bounds, and validation commands. |
| P02 (`P02-T01`) | Covered | Bounded to one new test file (`src/api/tests/test_learning_test_bundle_scenarios.py`), avoiding edits to `role-screens.js`, `aftercare.js`, or `server.py` so pinned WCAG table/attribute counts (`C10`), plain-language copy rules (`C11`), and the protocol screen/storage gate (`C1`) remain intact. |
| P03 (`P03-T01`, `P03-T02`) | Covered | Properly classifies the slice under the focused validation tier (owner decision D4 / #1294), discloses unobserved hosted CI due to no-push execution, and sequences RPI artifact closeout and frozen local commit. |

## Verdict

* Verdict: Pass
* Rationale: The candidate plan and phase details are complete, internally consistent, and grounded in the supplied PRD, ADR 0003, UX protocol, Python, JavaScript, and `pyproject.toml` contracts. Every bundle's canonical attributes, non-AI comparator, six-part NFR-009 net-effort rule, target-zero stop rule, and rendered role-screen/aftercare copy align verbatim with the supplied sources, backward compatibility with `learning-bundle-constructed-input-v1` and strict `mypy` rules is explicitly preserved, and all governance boundaries (`O10`/`O18`-`O20` exclusion, screen-wiring and run-storage prohibition, `capacity` framing, and `Refs #129`) are enforced without plan defects.

## Findings

None. Zero actionable `PC-xxx` findings require plan revision or user decision across the supplied boundary.

## Strengths and Residual Risk

* Exact source-to-code fidelity: All five bundle definitions in `P01-T01` match `docs/reference/research/ux/journey-learning-test-bundles.md` (lines 25-29, 79-83) and `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (lines 2857-2861), using the UX protocol's uniform `"Stop if ..."` stop-rule phrasing while keeping `zero_measures` unchanged so `_validate_input` (`src/core/src/zava_forward/core/learning_test_bundles.py:287`) and `render_report` stay 100% backward-compatible.
* Governance and guardrail discipline: Keeping `role-screens.js`, `aftercare.js`, and `server.py` unchanged directly honours `docs/reference/research/ux/journey-learning-test-bundles.md:102-103` and preserves pinned accessibility and lexical invariants (`C10`, `C11`).
* Implementation watchouts verified from supplied sources (no plan change needed):
  * In `src/api/src/zava_forward/api/web/role-screens.js`, `journeyStageMap` (which renders Stage 3 `"Generic consent is not accepted."`, Stage 4 `"An offer is not a booking."`, Stage 7 `"Open remedies are not closed by handover."`, and Stage 8 `"No award is inferred from an invoice."`) is appended by `roleScreensView()` at line 154 for screens where `!screen.ownsStageMap` (only `programme-queue` calls `journeyStageMap` inside `screen.render` at line 696), and `contractor-job-pack` restricts `roles` to `["Contractor"]` at line 1442 while manager/specialist screens require their permitted role (`Retrofit Programme Manager`, `Resident Liaison Officer`, `Retrofit Coordinator`, `Quality Inspector`, or `Grants and Evidence Officer`). Executing `roleScreensView()` with an installed role per screen in `P02-T01` naturally exercises both `overview`/`render` and `journeyStageMap`.
  * In `src/api/pyproject.toml:58`, both `zava_forward.core.*` and `zava_forward.api.server` have `follow_imports = "skip"` under `strict = true`. Static source inspection of `server.py` route registrations in `test_protocol_screen_wiring_and_run_storage_remain_gated` and explicit type annotations on helpers calling `zava_forward.core.learning_test_bundles` keep `mypy` clean without adding `pyproject.toml` overrides.
* Accepted external residual risks (`Refs #129`): Atlas-owner confirmation of bundle-to-opportunity mapping (including `O16`), DPO representative-data retention approval, live human experiment runs, Finance validation of saved capacity minutes, and hosted CI execution (unobserved locally because the branch is intentionally not pushed) remain open follow-up gates explicitly recorded by the plan.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Direct inspection was bounded to the caller-supplied read-only artifacts and source files. Adjacent files referenced by the plan and research log (`src/core/README.md`, `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/aftercare.py`, `src/api/tests/test_aftercare_screen.py`, and `src/api/tests/test_role_screens_connected_journey.py`) were assessed via `C8`-`C11` in `.copilot-tracking/research/2026-11-15/learning-test-bundles-129-research.md` and `src/api/pyproject.toml` typing rules rather than opened outside the supplied input boundary.
* Hosted GitHub Actions workflows are unobserved in this local-only slice because pushing to `origin` is excluded by caller direction.

## Recommended Next Action

* Highest-impact finding: none
* Action owner: planning_parent
* Smallest next action: Record the `Pass` critique disposition in `.copilot-tracking/plans/2026-11-15/learning-test-bundles-129-plan.md` and proceed directly to implementation starting at `P01-T01`.
* User response required: no
