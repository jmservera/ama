<!-- markdownlint-disable-file -->

# Task Research: learning-test-bundles-129

| Field              | Value                                                                      |
|--------------------|----------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                 |
| Researcher / agent | RPI Agent (`rpi-research`)                                                 |
| Status             | Complete                                                                   |
| Artifact path      | .copilot-tracking/research/2026-11-15/learning-test-bundles-129-research.md |
| Research disposition | executed                                                                 |
| Planning Readiness | Ready                                                                      |

## Research Brief

* What to research: Current implementation, API exposure, UI workbench surface, documentation, and unit test coverage for the five journey learning-test bundles and their non-AI comparators under Issue #129, specifically identifying any remaining code-testable gaps across Bundles 1 to 5 (especially Bundle 5: accessible handover and aftercare, non-AI comparator parity, hypothesis/signal/stop-rule fields, plain-language UI exposure on the workbench, and human/resident/usability-study governance boundaries).
* Why it matters: Issue #129 requires running the five candidate bundles as experiments with a non-AI comparator and net-effort comparison while keeping saved minutes framed as capacity until Finance validates them, keeping O10 and O18-O20 out of scope, and leaving Atlas owner confirmation and live usability studies explicitly gated.
* Audience or intended use: Planning, critique, implementation, and review phases of this RPI slice (`Refs #129`) and coordinator review on `feat/ux-129-learning-test-bundles-0023`.
* Scope: `src/core/src/zava_forward/core/learning_test_bundles.py` and related `src/core` modules/CLI, `src/api/` routes/models/static workbench (`role-screens.js`, HTML/CSS, tests), `src/core/tests/`, `src/api/tests/`, `docs/reference/research/ux/journey-learning-test-bundles.md`, `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, and prior `.copilot-tracking/` artifacts for #129.
* Non-goals: Opportunities O10 and O18 to O20; claiming Atlas owner confirmation or DPO retention approval; claiming live usability study execution or Finance cashable savings validation; pushing to remote or opening a PR.
* Criteria: Every bundle (1-5) verified against PRD, ADR-0003, and UX research specification; code-testable gaps clearly identified with `path:line` evidence; governance boundaries (human/resident approval, live study boundary, Finance validation gate, O10/O18-O20 exclusion) verified across backend, API, and UI.
* Requested outputs: Convergence recommendation for remaining code, UI, doc, and unit-test changes in this slice (`Refs #129`).
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                                                                                 |
|--------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | What code-testable invariants, API/workbench plain-language exposures, and unit tests already exist for the 5 learning-test bundles and non-AI comparators, and what exact gaps remain for slice #129? |
| Codebase scope                       | `src/core/`, `src/api/`, `docs/reference/research/ux/`, `docs/adrs/0003*`, `docs/prds/`, `.copilot-tracking/*129*`                                                                                    |
| External scope                       | None required for domain research (local repository contracts are authoritative; `web-design-guidelines` rule source applies in Implement if web files change)                                        |
| Initial internal candidate areas     | `src/core/src/zava_forward/core/learning_test_bundles.py`, `src/core/tests/test_learning_test_bundles.py`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/aftercare.js`, `docs/reference/research/ux/journey-learning-test-bundles.md` |
| Initial external candidate areas     | none                                                                                                                                                                                                  |
| Research posture                     | balanced                                                                                                                                                                                              |
| Posture provenance                   | default (bounded repository task with named targets plus adjacent API/UI/UX contract verification)                                                                                                    |
| Explicit limits / deadline           | Focused validation tier; keep O10 and O18-O20 out of scope; do not push                                                                                                                               |
| Posture-specific completion basis    | balanced scope coverage and adequate evidence across all 5 bundles, API/workbench wiring, UX docs, and tests                                                                                          |
| Edits allowed during research?       | no, research-only                                                                                                                                                                                     |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                                                                                                  |
| Known constraints / excluded sources | `support/` excluded; private datasets (`~/.zava-forward`) excluded; O10 and O18-O20 excluded from implementation                                                                                      |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                                            | Scoped authority or output contract                                              | Selected / skipped reason                                                                 |
|---------------------|---------------------------------------|-----------------------------------------------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`     | `applyTo: "**"` matches workspace inputs and tracking artifacts | Adds knowledge-base, Fluent 2/WCAG/plain-language UX, governance, and tier rules | Selected automatically by repository instructions                                         |
| Skill               | `web-design-guidelines`               | Matches web UI review/edit rule in repository instructions      | Web interface guidelines required before editing/reviewing web files             | Deferred to Implement/Review if `role-screens.js` or HTML/CSS changes are planned         |
| Skill               | `redesign-existing-projects`          | Existing-app UI design improvements                             | Preserves Fluent 2, WCAG 2.2 AA, and plain-language content standard             | Skipped in Research (read-only phase); referenced if UI refinements are needed in Plan    |
| Skill               | `experimental-design`                 | Experiment design domain                                        | Pre-data randomization/DOE methodology                                           | Skipped: #129 implements repository-defined deterministic learning-test bundle contracts   |
| Research specialist | `hve-core-all:rpi-researcher`         | General research lane worker visible in host                    | Independent lane artifact under `.copilot-tracking/research/subagents/`          | Skipped in favor of inline investigation: tightly coupled, bounded set of repository files |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                  | Answers / unanswered       | Resulting decision or selected further research                                  |
|------------------|------------------------------------------------------------------------------------------------------------------------|----------------------------|----------------------------------------------------------------------------------|
| Intake           | Non-interactive automatic RPI session with explicit scope, acceptance criteria, branch, and validation tier supplied.   | No interaction needed/used | Proceed with `balanced` posture in `convergence` output mode across all 5 bundles |
| Direction change | Pending wave execution                                                                                                 | None                       | None                                                                             |
| Convergence      | Pending wave synthesis                                                                                                 | None                       | None                                                                             |

## Scope and Success Criteria

* Scope: Inspect `learning_test_bundles.py` and related `src/core` and `src/api` modules, `role-screens.js` workbench UI, `docs/reference/research/ux/journey-learning-test-bundles.md` (note caller prompt wrote `learning-test-bundles.md`, actual path in repo is `journey-learning-test-bundles.md`), ADR-0003, PRD, and existing tests in `src/core/tests/` and `src/api/tests/`.
* Assumptions:
  * Earlier #129 slices (`2026-11-10` and `2026-11-14`) delivered partial or baseline bundle support that must be verified against current `HEAD` (`ab3538521`).
  * `docs/reference/research/ux/learning-test-bundles.md` in the prompt refers to `docs/reference/research/ux/journey-learning-test-bundles.md` (or we should verify whether any link expects `learning-test-bundles.md`).
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and one recommendation is selected in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  1. Inspect existing learning-test bundles and non-AI comparator coverage in `src/core/src/zava_forward/core/learning_test_bundles.py` (or related modules in `src/core` and `src/api`), `src/api/src/zava_forward/api/static/role-screens.js`, and `docs/reference/research/ux/journey-learning-test-bundles.md`.
  2. Verify and complete remaining code-testable learning-test bundle invariants across all 5 bundles (especially Bundle 5: accessible handover and aftercare, plus non-AI comparator parity, hypothesis/signal/stop-rule fields, and plain-language UI exposure on the workbench).
  3. Add or strengthen focused unit tests in `src/core/tests/` and `src/api/tests/` proving all 5 journey learning-test bundles and their non-AI comparators.
  4. Keep human/resident approval and live usability study boundaries explicit.
* Inferred research questions: Q1-Q6 below.
* Caller constraints and non-goals: Focused validation tier; `Refs #129` (do not claim `Closes #129` because Atlas owner confirmation, ADR-0003 owner acceptance, DPO retention decision, and live usability studies remain human gates); do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Focus on code-testable bundle invariants across all 5 bundles, comparator parity, UI exposure, and tests | Caller prompt       | Scopes convergence recommendation to executable/testable and plain-language gaps   |
| exclude                                                  | Keep Opportunities O10 and O18 to O20 out of scope                                                      | Caller / Issue #129 | Enforced as invariant across bundle definitions and tests                          |
| exclude                                                  | Keep human/resident approval and live usability study boundaries explicit; do not push                  | Caller prompt       | Enforced across copy, API payloads, UI disclosures, and final commit step          |

## Research Questions

|  # | Sub-question                                                                                                                                      | Type            | Priority | Status   |
|---:|---------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | What do PRD, ADR-0003, and `docs/reference/research/ux/journey-learning-test-bundles.md` specify for all 5 bundles, comparators, and stop rules?   | depth           | H        | answered |
| Q2 | What is currently implemented in `src/core` (`learning_test_bundles.py`, CLI, exports, models) and what did prior #129 slices already land?        | depth           | H        | answered |
| Q3 | How does `src/api` expose learning-test bundles and non-AI comparators (endpoints, schemas, service wiring, existing API tests)?                  | breadth         | H        | answered |
| Q4 | How does `role-screens.js` (and workbench HTML/CSS/browser check) render learning-test bundles, plain-language fields, and Bundle 5?              | depth           | H        | answered |
| Q5 | What code-testable invariants or parity gaps remain across Bundles 1-5 (especially Bundle 5, comparator parity, hypothesis/signal/stop-rule, UI)? | depth           | H        | answered |
| Q6 | What governance boundaries (human/resident approval, live study gate, Finance capacity-not-cash rule, O10/O18-O20 exclusion) must stay explicit?   | straightforward | H        | answered |

## Cycle 1: Three-Wave Execution

### Wave 1: Wider (Repository Specification, Core Module, and API/Workbench Breadth)

* Audited the authoritative bundle specifications across `docs/reference/research/ux/journey-learning-test-bundles.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, and `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md` (`C1`, `C2`, `C3`).
* Verified actual workspace paths: the UX protocol lives at `docs/reference/research/ux/journey-learning-test-bundles.md` (`C1`), and workbench role screens live at `src/api/src/zava_forward/api/web/role-screens.js` and `src/api/src/zava_forward/api/web/aftercare.js` (`C6`, `C7`).
* Inspected prior `#129` slices (2026-11-03 protocol, 2026-11-04 pure scorer and O16 run reconciliation, 2026-11-10 closed stdin CLI, and 2026-11-14 4-bundle AC1 unit test) (`C4`, `C5`, `C12`).

### Wave 2: Deeper (Code-Testable Bundle Metadata, Fifth-Bundle Gap, and Role-Screen Scenario Surfaces)

* `src/core/src/zava_forward/core/learning_test_bundles.py` defines `COMPONENTS` (six NFR-009 effort components), `ARMS = ("comparator", "workflow")`, `OUT_OF_SCOPE = frozenset({"O10", "O18", "O19", "O20"})`, and `BUNDLES` for all five keys (`story-once`, `pre-visit-pack`, `change-impact`, `handover-aftercare`, `funding-evidence`) (`C4`).
* However, `Bundle` currently stores only `(key, atlas_ids, comparator, zero_measures)` and omits canonical structured protocol metadata from `journey-learning-test-bundles.md` and the PRD: `title`, `linked_requirements`, `learning_question`, `beyond_effort_measures`, and `stop_rule` (`C1`, `C2`, `C4`).
* `src/core/tests/test_learning_test_bundles.py` line 32 (`test_ac1_bundles_each_have_a_non_ai_comparator_and_zero_measure`) checks only four bundle keys and omits `"funding-evidence"`, which the 2026-11-14 review explicitly routed as open follow-up work (`C5`, `C12`). Core tests also lack explicit checks for the resident-effort transfer non-saving rule (`NFR-009`: shifting staff minutes to `resident_effort` is not a net saving) and per-measure stop firing across every target-zero count in all five bundles (`C1`, `C5`).
* Across `src/api/src/zava_forward/api/web/role-screens.js` and `aftercare.js`, each of the five bundles' plain-language stop-rule boundaries is already rendered on the existing role screens (`resident-choice`, `resident-service-issues`, `programme-queue`, `procurement-packages`, `contractor-job-pack`, `technical-queue`, `quality-queue`, `finance-funding`, `finance-invoices`, and `aftercareScreens.evaluatorView`), including Stage 7 `"Open remedies are not closed by handover."` and `AftercareService.evaluator_view()` `unresolved_with_handover_or_financial_closure` (`C6`, `C7`, `C8`). Yet no test in `src/api/tests/` connects the five `learning_test_bundles.BUNDLES` and their non-AI comparators to rendered role-screen and aftercare scenarios (`C9`, `C10`, `C11`).

### Wave 3: Contrarian (Protocol Screen/Storage Gate and Static Conformance Guardrails)

* Counter-evidence against wiring a new bundle-runner screen or API route into `role-screens.js` or `server.py`: `docs/reference/research/ux/journey-learning-test-bundles.md:102-103` explicitly states `"Wiring it to a screen or storing run records waits for the owner mapping and the DPO retention decision."` (`C1`). Adding an unapproved runtime screen or stored-run endpoint would violate that explicit protocol boundary as well as closed-inventory guardrails in `test_role_endpoint_inventory.py`, `test_role_screens_conformance.py`, `test_accessibility_baseline.py` (pinned 13 script-built tables), and `test_content_standard.py` (`C9`, `C10`, `C11`).
* Counter-evidence against altering `Bundle.zero_measures` or CLI input keys: `_validate_input` enforces `_exact(data["counts"], bundle.zero_measures, ...)` on `learning-bundle-constructed-input-v1` (`C4`). Adding optional-default metadata fields (`title`, `linked_requirements`, `learning_question`, `beyond_effort_measures`, `stop_rule`) to `Bundle` and exposing read-only protocol metadata in `compare_bundle` preserves 100% CLI and unit-test compatibility while making every PRD/protocol field code-testable (`C4`, `C5`).

## Evidence Log

| ID  | Source (`path:line`)                                                          | Evidence summary                                                                                                                                   |
|-----|-------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| C1  | `docs/reference/research/ux/journey-learning-test-bundles.md:23-103`          | Canonical 5-bundle table, O16 overlap rule, O10/O18-O20 exclusion, 6-part net-effort rule, per-bundle learning questions, and screen/storage gate. |
| C2  | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:2850-2867`         | PRD "Candidate journey learning tests (hypotheses)" table defining the 5 bundles, Atlas IDs, linked requirements, comparators, and stop rules.     |
| C3  | `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:92-112`           | ADR 0003 Decisions 1-5: deterministic SQL records, server-side authority/closure rules, 5 registered assistants, non-AI comparators, capacity rule.|
| C4  | `src/core/src/zava_forward/core/learning_test_bundles.py:22-335`              | Existing `Bundle`, `BUNDLES`, `case_net_effort`, `compare_bundle`, `run_report`, `reconcile_o16`, `render_report`, and closed-envelope CLI.        |
| C5  | `src/core/tests/test_learning_test_bundles.py:26-265`                         | Existing core tests; `test_ac1_bundles_each_have_a_non_ai_comparator_and_zero_measure` (line 32) covers only 4 bundles, omitting `funding-evidence`.|
| C6  | `src/api/src/zava_forward/api/web/role-screens.js:597-1897`                   | Eight-stage `journeyStageMap` (stages 3, 4, 6, 7, 8 boundaries) and specialist role screens preserving choice, offer, sign-off, defect, and Held boundaries. |
| C7  | `src/api/src/zava_forward/api/web/aftercare.js:1-160`                         | Staff-assisted accessible aftercare views (`formView`, `receiptView`, `evaluatorView`) keeping representative basis and unresolved concerns visible.|
| C8  | `src/api/tests/test_aftercare_screen.py:1-125`                                | Node VM harness feeding real `AftercareService` payloads (`unresolved_with_handover_or_financial_closure`) into `aftercare.js`.                    |
| C9  | `src/api/tests/test_role_screens_connected_journey.py:1-120`                  | Node VM harness executing `roleScreensView()` across specialist roles and verifying same-home journey stage navigation.                            |
| C10 | `src/api/tests/test_accessibility_baseline.py:88-145`                         | Static WCAG 2.2 baseline checks pinning 8 `aria-invalid` sites and 13 script-built `<table>` elements across `web/*.js`.                           |
| C11 | `src/api/tests/test_content_standard.py:14-95`                                | Lexical copy audit forbidding internal terms (`gates`, `holds`, `provenance`, `traces`, `snapshots`, `envelopes`) in served web scripts/pages.     |
| C12 | `.copilot-tracking/reviews/2026-11-14/129-learning-bundles-1848-review.md:1-8`| Prior slice review routing `funding-evidence` (5th AC1 item) evidence, while keeping Atlas-owner confirmation and DPO retention as human gates.     |

## Parent Synthesis and Convergence Recommendation

### Answered Questions Summary

* **Q1 & Q6 (Specifications and Governance Boundaries):** All five bundles (`story-once`, `pre-visit-pack`, `change-impact`, `handover-aftercare`, `funding-evidence`), their non-AI comparators, six-component net-effort sum (`NFR-009`), stop rules, `O10`/`O18`-`O20` exclusion, capacity-not-cash rule, AI-unavailable manual continuity, and explicit screen/storage gate pending Atlas-owner confirmation and DPO retention are settled in `C1`, `C2`, and `C3`.
* **Q2 (Current Core State):** `learning_test_bundles.py` scores all five bundles and validates closed stdin JSON envelopes without storage (`C4`), but `Bundle` lacks canonical title, linked-requirement, learning-question, beyond-effort signal-measure, and stop-rule metadata, and `test_learning_test_bundles.py` omits `funding-evidence` from its AC1 comparator/zero-measure assertion (`C5`, `C12`).
* **Q3 & Q4 (API and Role-Screen Surfaces):** `role-screens.js` and `aftercare.js` render plain-language, non-colour-cued, read-only role views enforcing every bundle's stop-rule boundary on the same home without wiring an unapproved bundle runner or storing run records (`C1`, `C6`, `C7`).
* **Q5 (Remaining Code-Testable Gaps):** (1) Enrich `Bundle` and `compare_bundle` in `learning_test_bundles.py` with additive protocol metadata (`title`, `linked_requirements`, `learning_question`, `beyond_effort_measures`, `stop_rule`) while keeping `zero_measures` and `learning-bundle-constructed-input-v1` unchanged; (2) complete 5-bundle parity, resident-effort transfer non-saving, all-6-zero-measure stop-rule firing, and 5-bundle O16-reconciled constructed campaign tests in `src/core/tests/test_learning_test_bundles.py`; (3) add end-to-end constructed bundle-to-role-screen scenario verification in `src/api/tests/test_learning_test_bundle_scenarios.py` exercising all five bundles (including accessible handover and aftercare across `quality-queue`, Stage 7 `journeyStageMap`, `resident-choice`, and `AftercareService` + `aftercare.js`) in Node VM while asserting the screen/storage governance gate.

### Alternatives Evaluated

| Option | Summary | Trade-offs | Disposition |
|---|---|---|---|
| Option 1 (Selected) | Additive protocol metadata on `Bundle`/`compare_bundle` in `src/core`, complete 5-bundle unit tests in `src/core/tests/test_learning_test_bundles.py`, and add Node-VM + `AftercareService` role-screen scenario verification across all 5 bundles in `src/api/tests/test_learning_test_bundle_scenarios.py` (`src/core/README.md` updated if public `Bundle` fields are documented). | Preserves CLI envelope compatibility, respects the explicit `journey-learning-test-bundles.md:102` prohibition on screen wiring/run storage before Atlas-owner and DPO sign-off, avoids touching pinned UI table counts, and proves all 5 bundles end-to-end against real rendered role-screen copy and core stop rules. | **Accepted** (`C1`, `C4`, `C5`, `C6`, `C7`, `C10`, `C12`) |
| Option 2 | Wire a new interactive learning-bundle screen or `/api/learning-bundles` endpoint into `role-screens.js` and `server.py`. | Directly violates `docs/reference/research/ux/journey-learning-test-bundles.md:102-103` ("Wiring it to a screen or storing run records waits for the owner mapping and the DPO retention decision") before those human gates clear. | **Rejected** (`C1`) |
| Option 3 | Update only `test_ac1_bundles_each_have_a_non_ai_comparator_and_zero_measure` in `src/core/tests/test_learning_test_bundles.py` to add `"funding-evidence"`. | Closes the narrow 5th-key assertion gap from `C12` but leaves PRD/protocol metadata (`title`, `linked_requirements`, `learning_question`, `beyond_effort_measures`, `stop_rule`) unverified in code and provides no role-screen scenario verification in `src/api/tests/`. | **Rejected** (`C1`, `C2`, `C6`, `C7`) |

## Risks, Open Human Gates, and Further Research

* **Open Human Gates (`Refs #129`, never `Closes #129`):**
  1. Atlas owner confirmation of the bundle-to-opportunity mapping, specifically the `O16` overlap between `change-impact` and `funding-evidence` (`C1`, `C2`).
  2. DPO decision on representative-data retention (`representative_data_retained` must stay `False`) (`C1`, `C3`, `C4`).
  3. Live usability/experiment execution with human participants (#155 / #129) and Finance validation before any saved minutes leave the `capacity` classification (`C1`, `C3`).
* **Validation Tier Classification:** Focused tier (owner decision D4 / #1294) — bounded `src/core` metadata enrichment and `src/core/tests/` + `src/api/tests/` verification with no infrastructure, deployment, SQL migration, workflow, Dockerfile, dependency-manifest, or security-control impact.
* **Self-Check:** All Q1–Q6 answered with `C1`–`C12` `path:line` citations; all three waves completed in order; no source files edited during Research; `Planning Readiness: Ready`.

