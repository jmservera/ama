<!-- markdownlint-disable-file -->
# Review: Issue #220 Criterion 5 — No Retaliation, Inferred Refusal or Delayed Hazard Response

## Scope and Evidence

* Task ID: issue-220-no-retaliation-2026-11-15
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`, `P04` across `P01-T01`..`P04-T03`)
* Assessed boundary: End-to-end runtime non-retaliation, non-refusal, non-closure, statutory/emergency hazard and safeguarding clock preservation, immediate independent hazard intake routing, challenge reopening, representative/nominee and AI/assistant/form proposal challenge coverage, and machine-checkable `non_retaliation_assurance` / `hazard_clock_preserved` records, views, HTTP responses, and audit logs across `src/core` and `src/api` (Focused validation tier; `src/api/src/zava_forward/api/web/role-screens.js` excluded by caller constraint; external human operational/legal/assistive-technology acceptance gates remain owner-owned outside local software checks).
* Plan: .copilot-tracking/plans/2026-11-15/220-no-retaliation-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/220-no-retaliation-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/220-no-retaliation-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/220-no-retaliation-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/220-no-retaliation-research.md (`C1`-`C18`), direct inspection of `git diff` across all 10 modified files and 2 new test modules, `web-design-guidelines` review against freshly fetched `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`, and local Focused Tier + Playwright/axe 4.10.3 browser validation runs.

## Opening Review State

* Interpreted review goal: Verify once with direct artifact, code, and test evidence whether `P01`..`P04` satisfy `FR-1`..`FR-4`, `NFR-1`..`NFR-2`, and critique dispositions `PC-001`..`PC-004` for Issue #220 Criterion 5 without introducing regressions, prohibited phrases, or `web/role-screens.js` edits.
* Review scope: Full task (`P01`..`P04`)
* Evidence readiness: Ready — plan markers, phase-detail index and completion evidence, critique dispositions (`PC-001`..`PC-004`), changes log, and Focused Tier validation outputs are reconciled and current.
* Acceptance basis: Caller prompt requirements, Issue #220 Criterion 5, plan `FR-1`..`FR-4` and `NFR-1`..`NFR-2`, critique findings `PC-001`..`PC-004`, AMA Web Development Guidance (`web-design-guidelines`, Fluent 2 baseline, plain-language `test_content_standard.py`), and ADR 0006 formatting exclusions.
* First comparison boundary: Plan-to-change marker reconciliation across `P01`..`P04` and critique `PC-001`..`PC-004` resolution in source and tests.
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/2026-11-15/220-no-retaliation-review.md` and RPI session state transitions; no production source, plan, detail, critique, or changes-log mutations occur in Review.
* Initial blockers: None.

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass assessment on 2026-11-15 comparing reconciled `plan`, `phase-details`, `plan-critique`, `changes`, `research`, full working-tree `git diff`, `web-design-guidelines` compliance on `src/api/src/zava_forward/api/web/panels.js`, and passing Focused Tier validation across `src/core` and `src/api`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Core Challenge Register, Reopen, Representative Metadata, and Safeguard Contract (`P01`) | Reconciled | All `challenges.py` helpers, adverse-field checks, `reopen`, representative metadata, and `non_retaliation_assurance` / `hazard_clock_preserved` outputs match plan and details. |
| `P02` (`P02-T01`, `P02-T02`, `P02-T03`) | Store-Backed Case Challenge, Reopen, Representative, AI-Task/Form, and Immediate Hazard Routing (`P02`) | Reconciled | `resident_decisions.py`, `sqlstore.py`, `mssqlstore.py`, and `ai_tasks.py` implement `challenge_reopen`, expanded channels, representative metadata, replay-safe `_route_challenge_hazard` (`PC-001`), reopened-correction SQL indexing (`PC-002`), `ai_task`/`form_staging` challenge targets and stale review block (`PC-003`), runtime `assert_no_adverse_challenge_effects` + `_ranking()` checks, and audit/view assurance tags. |
| `P03` (`P03-T01`, `P03-T02`) | Assistant Proposal Challenge Route, HTTP API Endpoint, and Plain-Language Workbench (`P03`) | Reconciled | `assistants.py`, `server.py`, and `web/panels.js` implement `Assistants.challenge`, `POST /api/assistants/proposals/<tid>/challenge`, transient `_view` key stripping + `_withhold_sensors` redaction (`PC-004`), and plain-language workbench challenge reopen/channel/representative/safety controls without touching `web/role-screens.js`. |
| `P04` (`P04-T01`, `P04-T02`, `P04-T03`) | Core & API Test Suites, Module READMEs, and Focused Tier Validation (`P04`) | Reconciled | Exact two planned test modules (`test_challenge_no_retaliation_220.py` and `test_challenge_no_retaliation_api_220.py`) and updated `src/core/README.md` / `src/api/README.md` pass all Focused Tier checks. |
| `## Follow-Up Items` | External human operational/legal/assistive-technology acceptance boundaries noted outside active software scope | Reconciled | Preserves `Refs #220` issue boundary without inflating active `P01`..`P04` tasks. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01` (`P01-T01`, `P01-T02`) | `src/core/src/zava_forward/core/challenges.py` | Expanded `FORBIDDEN_ADVERSE_FIELDS` and `NOT_INFERRED`, added `build_non_retaliation_assurance`, upgraded `assert_no_adverse_challenge_effects` across priority, refusal/no-access/sanction/withdrawn/negative-engagement, work-item closures, and Awaab's Law 24h/7d/14d + `safeguarding` + `awaiting_hazard_action` clocks, added `ChallengeRegister.reopen` + `record_representative` + `submitted_by`/`representative_ref`, preserved `hazard_referral.received_on`, and attached `non_retaliation_assurance` + `hazard_clock_preserved: True` to records and `.view()`. | Verified in `git diff` and `test_challenge_no_retaliation_220.py`. | Passed (`mypy` strict, `ruff`, 5 new core tests + 28 existing challenge tests). | Reconciled and conformant |
| `P02` (`P02-T01`, `P02-T02`, `P02-T03`) | `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/src/zava_forward/core/sqlstore.py`, `src/core/src/zava_forward/core/mssqlstore.py`, `src/core/src/zava_forward/core/ai_tasks.py` | Registered `challenge_reopen`, added `"Assisted visit"` and `"Trusted intermediary"` channels, added `submitted_by`/`representative_ref` with read-only `representative_authority_status`, added replay-safe `_route_challenge_hazard` (`PC-001`), preserved `"Correction recorded"` staleness across reopen in JSON/SQLite/MSSQL (`PC-002`), guarded `ai_tasks.review` against stale `accept`/`edit` (`PC-003`), extended `challenge_catalog` to `ai_task` and `form_staging` (`form:<id>`), enforced runtime `assert_no_adverse_challenge_effects` + `_ranking()` invariance across challenge/nomination/service handlers, and exposed `non_retaliation_assurance` + `hazard_clock_preserved: True`. | Verified in `git diff` and `test_challenge_no_retaliation_220.py` across both `Store` and `SqlStore`. | Passed (`mypy` strict, `ruff`, 502 targeted `src/core` regression tests + 5 new core tests). | Reconciled and conformant |
| `P03` (`P03-T01`, `P03-T02`) | `src/core/src/zava_forward/core/assistants.py`, `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/web/panels.js` | Implemented `Assistants.challenge` (`open`, `update`, `reopen`, `escalate`, `resolve`) with optimistic `revision` fencing, immediate `hazard_referral` + `raise_hazard` intake, `challenged_stale` preservation, transient `_view` key stripping and `_withhold_sensors` redaction (`PC-004`), HTTP `POST /api/assistants/proposals/<tid>/challenge`, and plain-language `affectedChallengePanel` updates (`optional` field flag, intermediary channels, `submitted_by`/`representative_ref`, `hazard_concern`, `#challenge-reopen-<id>`, and safeguard confirmation). `web-design-guidelines` fresh review of `src/api/src/zava_forward/api/web/panels.js`: `✓ pass` (native `<form>`/`<label for>`, `aria-live="polite"`, `aria-invalid` + error focus, `autocomplete="off"`, `spellcheck="false"` on IDs/references, unsaved-draft navigation guard, and owner plain-language sentence case). | Verified in `git diff`, `test_challenge_no_retaliation_api_220.py`, `test_content_standard.py`, and `checks/challenge_browser_check.py`. | Passed (`mypy` strict, `ruff`, `test_content_standard.py` 29/29, `test_resident_api.py` 21/21, `test_assistants.py` 138/138, 5/5 Chromium + axe 4.10.3 journeys). | Reconciled and conformant |
| `P04` (`P04-T01`, `P04-T02`, `P04-T03`) | `src/core/tests/test_challenge_no_retaliation_220.py`, `src/api/tests/test_challenge_no_retaliation_api_220.py`, `src/core/README.md`, `src/api/README.md` | Delivered the exact 2 locked test files (`removals = none`, `additions = 2`), updated `src/core/README.md` and `src/api/README.md` with honest scope boundaries (`ms.date: 2026-11-15`, zero `.copilot-tracking/` links), and passed Focused Tier verification. | Verified test counts, linter/type outputs, and clean `web/role-screens.js` status. | Passed (all Focused Tier checks exit `0`). | Reconciled and conformant |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P04-T02` (`src/api/tests/test_challenge_no_retaliation_api_220.py`) | Local test-fixture update in `_seed_api_case_invariants` adding a linked `case["form_reviews"]` record alongside `case["form_staging"]` (and normalizing `"pas2035-ventilation"`). `_form_staging_records(..., catalog_only=True)` intentionally restricts `challenge_targets` to reviewed form batches so unreviewed staging fixtures in `test_form_staging.py` and `test_form_review.py` stay backward-compatible. | Triggered by `test_challenge_no_retaliation_api_220.py` run during Focused Tier verification; ordinary local judgment requiring no user decision. | Recorded in `.copilot-tracking/changes/2026-11-15/220-no-retaliation-changes.md` under `## Implementation-Time Plan and Detail Updates`. | Not needed (preserves approved `P02-T03` and `P04-T02` intent without altering plan scope or critique `PC-001`..`PC-004`). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four single-pass critique findings (`PC-001` replay-safe `_route_challenge_hazard`, `PC-002` `sqlstore.py` & `mssqlstore.py` `prior_correction_preserved` indexing, `PC-003` `ai_tasks.review` stale-correction block, and `PC-004` `Assistants` transient `_view` key stripping + `_withhold_sensors` challenge-note redaction) were resolved directly in planning, implemented in source, and verified by dedicated assertions in `test_challenge_no_retaliation_220.py`.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No material revision occurred; phase order `P01` -> `P02` -> `P03` -> `P04` was respected without premature resumption.
* Justification assessment: Supported by direct source and test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| None in active plan `## Follow-Up Items` (external Issue #220 human governance, live native SQL Server execution, and resident/assistive-technology acceptance gates remain tracked on `#220`) | Requires named human legal/RAI governance sign-off, provisioned SQL Server runtime, and real assistive-technology sessions outside local Focused Tier software scope. | Programme owner / named governance & accessibility leads before closing `#220` (`Refs #220` maintained). | Open external boundary routed as distinct non-blocking residual follow-up (`RV-001`). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: External operational SQL Server, human RAI/legal governance, and assistive-technology acceptance remain open on Issue #220

* Related scope: Task boundary (`Refs #220`, outside `P01`..`P04` local software scope)
* Evidence: `src/core/README.md` (`Status record, 2026-11-15`), `src/api/README.md` (`Affected-person challenge API and workbench (#220)`), and `src/core/src/zava_forward/core/mssqlstore.py` (`_priority_correction_rows` updated to match `sqlstore.py`, verified by static strict `mypy` and unit coverage rather than a live SQL Server instance in this Focused Tier run).
* Impact: Local software invariants for Issue #220 Criterion 5 are complete and verified across JSON `Store`, SQLite `SqlStore`, `Assistants`, HTTP endpoints, and Chromium + axe 4.10.3 checks, but whole-issue `#220` closure still requires live SQL Server operational verification, named human legal/RAI sign-off on notice/redress wording, and human assistive-technology/resident comprehension testing (`Refs #220`, never `Closes #220`).
* Destination: follow_up
* Smallest useful next action: Keep PR linkage as `Refs #220` and run operational SQL Server + human governance and assistive-technology acceptance in the dedicated pre-release operational acceptance workstream before closing `#220`.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | Distinct follow-up (operational & human acceptance) | Programme owner / governance & accessibility leads (`Refs #220`) | Non-blocking external operational/human acceptance boundary outside local software scope |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001`: Execute live native SQL Server `_priority_correction_rows` verification, named human legal/RAI governance sign-off, and resident/assistive-technology comprehension sessions before marking whole GitHub Issue `#220` closed.

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None (`P01`..`P04` complete)

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `../../.venv/bin/python -m unittest discover -s tests -p "test_challenge_no_retaliation_220.py" -v` | `src/core` | Passed | Ran 5 tests in 0.431s (`OK`) |
| `PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -p "test_challenge_no_retaliation_api_220.py" -v` | `src/api` | Passed | Ran 3 tests in 0.903s (`OK`) |
| `PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -p "test_content_standard.py" -v` | `src/api` | Passed | Ran 29 tests in 0.088s (`OK`; zero prohibited phrases or internal nouns) |
| `../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check .` | `src/core` & `src/api` | Passed | All checks passed; 337 (`src/core`) + 197 (`src/api`) files formatted cleanly (ADR 0006 legacy exclusions preserved) |
| `../../.venv/bin/mypy` | `src/core` & `src/api` | Passed | `Success: no issues found in 337 source files` (`src/core`) and `281 source files` (`src/api`) |
| Targeted challenge/resident/form/assistant regression suites | `src/core` & `src/api` | Passed | 502 tests in `src/core` (`test_challenges`, `test_issue_220_challenge_route`, `test_resident_decisions`, `test_form_staging`, `test_form_review`) + 159 tests in `src/api` (`test_resident_api`, `test_assistants`) all `OK` |
| `checks/challenge_browser_check.py` (all 5 modes with axe-core 4.10.3) | `src/api` (`web/panels.js`) | Passed | `base`, `--history`, `--navigation`, `--refresh-draft`, and `--pending-draft` all `OK` with zero axe violations or page errors |
| `web-design-guidelines` rule audit (fresh fetch of `command.md`) | `src/api/src/zava_forward/api/web/panels.js` | Passed | `✓ pass` — zero guideline violations; `web/role-screens.js` verified untouched |
| Hosted GitHub Actions CI on exact HEAD | Repository workflows | Unavailable (not yet pushed by explicit caller instruction `Do not push`) | Local Focused Tier checks executed directly; hosted CI will run after caller pushes the stacked branch |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every planned requirement (`FR-1`..`FR-4`, `NFR-1`..`NFR-2`), acceptance criterion, backward-compatibility constraint (`web/role-screens.js` untouched, ADR 0006 respected, `test_content_standard.py` and `challenge_browser_check.py` passing, locked 2-test-file boundary honoured), and plan-critique disposition (`PC-001`..`PC-004`) is implemented and verified with zero defects across `src/core` and `src/api`. External operational/human acceptance gates are transparently recorded under `RV-001` (`Refs #220`).

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | No implementation defects found |
| Decision gap or invalid assumption | none | No planning or decision gaps found |
| Material evidence gap | none | No research evidence gaps found |
| Non-blocking residual work | Distinct follow-up (`RV-001`) | Run native SQL Server operational check + human legal/RAI & assistive-technology acceptance before closing `#220` |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused Tier passed across `src/core` and `src/api` (`test_challenge_no_retaliation_220.py`, `test_challenge_no_retaliation_api_220.py`, `test_content_standard.py`, 661 targeted regression tests, 5 Playwright + axe 4.10.3 `challenge_browser_check.py` journeys, `web-design-guidelines` audit, `ruff check .`, `ruff format --check .`, and strict `mypy`); hosted CI pending future push per caller `Do not push` constraint.
* Blockers: None
