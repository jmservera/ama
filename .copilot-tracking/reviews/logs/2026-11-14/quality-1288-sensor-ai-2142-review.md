<!-- markdownlint-disable-file -->
# Review: Surface Retained Sensor Values and Ground Quality AI Review Flags (Issue #1288)

## Scope and Evidence

* Task ID: quality-1288-sensor-ai-2142
* Review date: 2026-11-14
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02`)
* Assessed boundary: Issue #1288 acceptance criteria AC 1 through AC 9, caller prompt requirements, Option A architecture from research, `PC-001` through `PC-006` critique dispositions, implementation changes across `src/core` (`sensor_view.py`, `chat_case_answers.py`, `chat_panel.py`, `assistants.py`) and `src/api` (`sensor_badges.py`, `web/ops.js`, `web/assistants.js`, `web/chat.js`), four focused test suites, local static/unit/browser checks, and Web Development Guidance (`vercel-labs/web-interface-guidelines`, Fluent 2, WCAG 2.2 AA, plain-language content standard). Live Azure runtime and hosted GitHub Actions CI are outside the local unpushed boundary.
* Plan: .copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/quality-1288-sensor-ai-2142-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-research.md; git diff across `src/core` and `src/api`; bare `mypy` and `ruff` outputs in `src/core` and `src/api`; targeted `unittest` suites (`650` core tests, `680` API tests); Chromium + pinned `axe-core` 4.10.3 browser checks (`checks.quality_sensors_browser_check`, `test_chat_panel`, `checks.employee_chat_browser_check`); live `vercel-labs/web-interface-guidelines` audit of `ops.js`, `assistants.js`, and `chat.js`.

## Opening Review State

* Interpreted review goal: Verify once, with read-only source authority, that all Issue #1288 requirements, `PC-001`–`PC-006` critique resolutions, plain-language/accessibility/Web Interface Guidelines rules, and static/unit/browser checks are satisfied and reconciled across the task artifacts.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready — research, plan, phase details, single-pass plan critique, changes record, and clean worktree diff are present and reconciled.
* Acceptance basis: Issue #1288 AC 1–AC 9, caller verification/commit constraints, `.github/copilot-instructions.md` validation-tier (`focused`) and Web Development Guidance rules, and `PC-001`–`PC-006` dispositions.
* First comparison boundary: Plan `## Phase Checklist` (`P01-T01` through `P03-T02`) and `## Critique Disposition` against `.copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-changes.md` and the `git diff` in `src/core` and `src/api`.
* Active read-only boundaries: This review creates only `.copilot-tracking/reviews/logs/2026-11-14/quality-1288-sensor-ai-2142-review.md` and does not mutate source files, tests, research, plan, phase details, critique, or changes artifacts.
* Initial blockers: None.

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full-boundary comparison on 2026-11-14 across `.copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-research.md`, `.copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-plan.md`, `.copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-14/quality-1288-sensor-ai-2142-plan-critique.md`, `.copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-changes.md`, all 12 modified/added files under `src/core` and `src/api`, and fresh `web-design-guidelines` rules.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Core Retained Sensor Conflict Propagation and Grounding | Reconciled | `[x]` in plan, `completed` in phase details, and documented in changes record; matches `sensor_view.py`, `chat_case_answers.py`, and `chat_panel.py`. |
| `P02` (`P02-T01`) | Quality AI Review Flag Source Provenance and Conflict Gating | Reconciled | `[x]` in plan, `completed` in phase details, and documented in changes record; matches `assistants.py`. |
| `P03` (`P03-T01`, `P03-T02`) | API Badges, Employee Web Surfacing, and Verification | Reconciled | `[x]` in plan, `completed` in phase details, and documented in changes record; matches `sensor_badges.py`, `ops.js`, `assistants.js`, `chat.js`, and the 4 test files. |
| `## Follow-Up Items` | Pre-existing `employee_chat_browser_check` CSS target-size follow-up and live conflict browser scenario follow-up | Reconciled | Both follow-up items appear in plan `## Follow-Up Items` and changes `## Follow-Up Items` with explicit out-of-scope rationale and owners, outside active `P01`–`P03` acceptance claims. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/sensor_view.py` | Added `conflicts(rows)`, `capture_source()` `conflicting_readings` + `conflict_notice`, conflict branches in `grounding()`, `reading_health()`, `advisory()`, `trend_summary()`, and `_view()`, plus sibling `provenance_class` and `source_text` on clean `grounding()`, keeping `signature()` unchanged (`PC-001`, `PC-004`). | `sensor_view.py` diff; `test_sensor_view_conflicts.py` | Passed (`mypy`, `ruff`, `303` core sensor tests) | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/chat_case_answers.py`, `src/core/src/zava_forward/core/chat_panel.py` | Projected `sensor.conflict` and `sensor.source` facts, registered both in `SENSOR_RULE_PATHS` as `decision-rule`, routed conflicted sensor questions without choosing a value or claiming no readings exist, and cited `{case_id}/sensor.source` on clean readings (`PC-003`). | `chat_case_answers.py` & `chat_panel.py` diffs; `test_quality_sensor_grounding.py` | Passed (`mypy`, `ruff`, `188` core chat tests, grounding API tests) | Reconciled |
| `P02-T01` | `src/core/src/zava_forward/core/assistants.py` | Blocked sensor-only `eligible()` triggers on `conflicting_readings`, added `_sensor_bucket_key()` for same-bucket conflict visibility across widened `provenance_class` sets, downgraded captured/current conflicts in `review_flag()` to `status="conflicting-readings"` (`autonomous=False`, `level=None`), enriched `readings` and `source_provenance` (`locator`, `content_hash`, `provenance_class`, `source_text`), added `cited_provenance_classes` and `invocation_modes` (`kind == "invocation"`), and preserved `withheld=True` redaction (`PC-001`, `PC-006`). | `assistants.py` diff; `test_quality_sensor_grounding.py`, `test_quality_sensors_correlation.py` | Passed (`mypy`, `ruff`, `159` core quality tests, `138` API assistant tests, grounding & correlation suites) | Reconciled |
| `P03-T01` | `src/api/src/zava_forward/api/sensor_badges.py`, `src/api/src/zava_forward/api/web/ops.js`, `src/api/src/zava_forward/api/web/assistants.js`, `src/api/src/zava_forward/api/web/chat.js` | Added `"conflict"` badge and `next_action` prioritized ahead of `"offline"` and `"stale"`; guarded `ops.js` `v.latest` promotion on conflict while keeping `sensorTable` and `data-sensor-conflict`; added `"conflicting-readings"` title, `data-flag-conflict`, per-reading `Source:`, and `data-flag-sources` in `assistants.js`; added `"sensor.source"` and `"sensor.conflict"` to `chat.js` `RULE_PARTS` (`PC-002`, `PC-005`). | `sensor_badges.py` & `web/*.js` diffs; fresh `web-design-guidelines` review (`ops.js` ✓ pass, `assistants.js` ✓ pass, `chat.js` ✓ pass) | Passed (`test_content_standard`, `test_design_system`, `test_accessibility_baseline`, `checks.quality_sensors_browser_check` `42/42` + axe 4.10.3) | Reconciled |
| `P03-T02` | `src/core/tests/test_sensor_view_conflicts.py`, `src/api/tests/test_quality_sensor_grounding.py`, `src/api/tests/test_quality_sensors_correlation.py`, `src/api/tests/test_sensor_staleness_ui_badge.py` | Added strict-typed (`-> None`) semantic unit and API/snapshot correlation tests covering conflict detection, 7-day trend conflict withholding, chat routing, proactive scan blocking, same-bucket L4 downgrade, consent withdrawal redaction, source provenance fields, and context-only conflict badge precedence (`PC-005`, `PC-006`). | Diffs across 4 test files (`0` tests deleted, `4` test files touched) | Passed (`mypy`, `ruff`, `650` core tests, `680` API tests, Chromium + axe checks) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| Plan `## Phase Checklist`, `## Follow-Up Items`, `## Handoff`; Phase details `P01`–`P03` status | Marked `P01`–`P03` completed and recorded two `follow-up-only` discoveries (`origin/main` `#employee-chat-question` CSS `target-size` overflow in `checks.employee_chat_browser_check`, and optional live conflict browser check state). | Triggered during `P03-T02` browser harness verification (`checks.employee_chat_browser_check` hit a pre-existing `origin/main` `f5f76b6cc` `#1690`/`#1718` CSS layout issue unrelated to the 2-token `RULE_PARTS` list update in `chat.js`); no divergent user decision needed. | Reconciled across plan `## Follow-Up Items` / `## Handoff`, phase details status fields, and changes `## Implementation-Time Plan and Detail Updates`. | Non-material (`follow-up-only`); preserves approved plan intent and `PC-001`–`PC-006` resolutions without requiring re-planning or a second critique. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All six findings from `.copilot-tracking/reviews/plans/2026-11-14/quality-1288-sensor-ai-2142-plan-critique.md` (`PC-001` [High], `PC-002` [High], `PC-003` [High], `PC-004` [Medium], `PC-005` [Medium], `PC-006` [Low]) were directly resolved in the plan and phase details prior to implementation and verified in the implemented code and tests.
* Material revisions: None occurred during implementation. No plan assumption was invalidated and no user requirement changed.
* Dependent-work pause assessment: Compliant — single-pass critique completed and resolved before `P01`–`P03` implementation executed.
* Justification assessment: Supported by direct code and test evidence (for example `_sensor_bucket_key()` in `assistants.py`, `!(v.conflicting_readings || []).length && !v.conflict_notice` in `ops.js`, `r.fact("sensor.conflict")` in `chat_case_answers.py`, `conflicts(ordered)` in `sensor_view.trend_summary()`, and strict `-> None` typing on all modified test suites).

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Adjust `#employee-chat` vertical flex/max-height spacing in `src/api/src/zava_forward/api/web/styles.css` for `checks.employee_chat_browser_check` (`demo-disclaimer-model-answer` `#employee-chat-question` `target-size` `partiallyObscured` at 720px height) | Pre-existing `origin/main` (`f5f76b6cc`, post-`#1690`/`#1718`) global employee-chat stylesheet layout issue outside Issue #1288 Quality sensor/flag scope; repository rules forbid unrelated CSS changes. | Distinct UX/CSS follow-up task (`styles.css` + `checks.employee_chat_browser_check`) | Open, valid `follow-up-only` item (`RV-001`); kept outside active `P01`–`P03` defect scope. |
| Add automated browser scenario in `src/api/checks/quality_sensors_browser_check.py` exercising live conflicting-reading state (`data-sensor-conflict`, `data-flag-conflict`, `data-flag-sources`) | API, correlation, DOM-token, and existing 42-assertion `quality_sensors_browser_check` + axe-core 4.10.3 suites already verify all Issue #1288 criteria; adding a new seeded conflict case to the browser script is an incremental harness enhancement. | Distinct test-harness follow-up task (`src/api/checks/quality_sensors_browser_check.py`) | Open, valid `follow-up-only` enhancement (`RV-002`); kept outside active `P01`–`P03` defect scope. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Web Interface Guidelines Audit (`web-design-guidelines`)

Rules refreshed from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` during Review and checked across all changed web files:

* `src/api/src/zava_forward/api/web/ops.js` (`ops.js:89-90`): ✓ pass — `data-sensor-conflict` uses `role="status"` polite live-region semantics, plain-language copy with explicit `Manual route:`, DOM text construction via `h(...)` (no `innerHTML`), non-colour status badges, and suppresses `Latest:` single-value promotion on conflict while keeping `sensorTable` accessible.
* `src/api/src/zava_forward/api/web/assistants.js` (`assistants.js:23, 38-45`): ✓ pass — `FLAG_TITLES["conflicting-readings"]` uses plain sentence-case copy, `data-flag-conflict` uses `role="status"`, `data-flag-sources` renders conditionally only when `(f.source_provenance || []).length > 0`, and all dynamic strings render through safe DOM text nodes within `role="group"` (`aria-label="Review flag status"`).
* `src/api/src/zava_forward/api/web/chat.js` (`chat.js:61`): ✓ pass — data-only `RULE_PARTS` prefix array update (`"sensor.source"`, `"sensor.conflict"`) preserving `[Decision rule]` non-colour text prefixing.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Pre-existing `origin/main` `#employee-chat-question` `target-size` (`partiallyObscured`) axe failure in `checks.employee_chat_browser_check` at 720px viewport height

* Related scope: Plan `## Follow-Up Items` (observed during `P03-T02` auxiliary browser check)
* Evidence: .copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-changes.md (`## Validation Record`); `src/api/src/zava_forward/api/web/styles.css`; `src/api/checks/employee_chat_browser_check.py` (`demo-disclaimer-model-answer` state reports `#employee-chat-question` `18.0px` unobscured height `< 24px` WCAG 2.5.8 target-size threshold due to `origin/main` `#1690`/`#1718` chat header controls).
* Impact: Does not affect Quality `#sensors`, Quality AI `review_flag` (`checks.quality_sensors_browser_check` passed `42/42` checks and all 9 axe scans), or `test_chat_panel` Chromium verification (`OK`), and was not introduced by `chat.js:61`, but blocks standalone `checks.employee_chat_browser_check` runs on `main` until `#employee-chat` vertical flex spacing is adjusted.
* Destination: follow_up
* Smallest useful next action: Open or select a focused UX follow-up task adjusting `#employee-chat` body/composer flex sizing at `720px` viewport height in `src/api/src/zava_forward/api/web/styles.css` and re-running `python3 -m checks.employee_chat_browser_check`.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Live conflicting-reading DOM state is verified by API/correlation/DOM tests rather than a dedicated `checks.quality_sensors_browser_check` scenario

* Related scope: Plan `## Follow-Up Items` (`P03-T02` optional harness extension)
* Evidence: .copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-plan.md (`## Follow-Up Items`); `src/api/checks/quality_sensors_browser_check.py`; `src/api/tests/test_quality_sensor_grounding.py`; `src/api/tests/test_quality_sensors_correlation.py`.
* Impact: Non-blocking; current `checks.quality_sensors_browser_check` (`42/42` passed + 9 axe scans) verifies clean, stale, fault, and withheld Quality sensor/flag states while unit/correlation suites verify conflict payloads and `ops.js` / `assistants.js` DOM hooks, so adding a dedicated browser scenario in `quality_sensors_browser_check.py` is an optional defense-in-depth improvement.
* Destination: follow_up
* Smallest useful next action: Add one seeded conflicting-reading case to `src/api/checks/quality_sensors_browser_check.py` asserting rendered `[data-sensor-conflict]`, `[data-flag-conflict]`, and `[data-flag-sources]` elements under pinned `axe-core` 4.10.3.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | Distinct follow-up item (`follow_up`) | Select post-Review follow-up #1 to adjust `#employee-chat` vertical flex spacing in `src/api/src/zava_forward/api/web/styles.css` | Pre-existing `origin/main` CSS layout issue outside Issue #1288 scope (non-blocking residual follow-up, not a task defect) |
| `RV-002` | Distinct follow-up item (`follow_up`) | Select post-Review follow-up #2 to add a seeded conflict scenario to `src/api/checks/quality_sensors_browser_check.py` | Incremental browser-harness coverage enhancement recorded in plan `## Follow-Up Items` |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Hosted GitHub Actions CI checks remain unobserved locally because the caller explicitly instructed `"Do NOT push"`; read hosted CI checks on the exact head commit once the owner pushes or opens a PR.
* Distinct follow-up items `RV-001` and `RV-002` remain available for user selection at the automatic post-Review checkpoint.

## Blockers and Remaining Work

* Blockers: None for local RPI completion (human review and hosted CI remain standard post-push PR merge gates on Issue #1288).
* Remaining active work: None (`P01`, `P02`, and `P03` are complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .` | `src/core` | Passed | `Success: no issues found in 317 source files`; `All checks passed!`; `264 files already formatted` |
| `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .` | `src/api` | Passed | `Success: no issues found in 280 source files`; `All checks passed!`; `196 files already formatted` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -k "sensor\|chat\|quality"` | `src/core` | Passed | `303` sensor + `188` chat + `159` quality tests passed (`650` total, `0` failures) |
| `PYTHONPATH=../core/src:../agents/src:src:tests:../core/tests:../agents/tests python3 -m unittest ...` | `src/api` | Passed | `542` sensor/grounding/correlation/UX/content-standard tests + `138` `test_assistants` tests passed (`680` total, `0` failures) |
| `python3 -m checks.quality_sensors_browser_check --axe axe-4.10.3.min.js --out ...` | `src/api` Chromium + axe 4.10.3 | Passed | `42 checks passed`, `0` page errors, `0` serious/critical axe violations across 9 sensor/flag states |
| `ZF_BROWSER_TESTS=1 python3 -m unittest -v test_chat_panel.PanelTests.test_browser_warning_failure_keyboard_refusal_and_live_log` | `src/api` Chromium chat panel | Passed | `Ran 1 test in 3.153s - OK` |
| `python3 -m checks.employee_chat_browser_check --axe axe-4.10.3.min.js --out ...` | `src/api` Chromium employee chat | Failed (pre-existing `origin/main`) | Disclosed pre-existing `#employee-chat-question` `target-size` (`partiallyObscured`, 18px < 24px at 720px height) on `origin/main` (`f5f76b6cc`); routed as `RV-001` |
| Hosted GitHub Actions CI | Branch `feat/quality-1288-sensor-ai-2142` | Skipped | Branch intentionally unpushed per caller instruction (`"Do NOT push"`) |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every planned phase (`P01`, `P02`, `P03`), Issue #1288 acceptance criterion (`AC 1`–`AC 9`), caller constraint, Web Development Guidance rule, and critique resolution (`PC-001`–`PC-006`) is implemented and verified with zero defects, zero decision or evidence gaps, passing strict `mypy` and `ruff` checks in both `src/core` and `src/api`, `1,330` passing unit/correlation/UX/content tests, and `42/42` passing Quality sensor Chromium + `axe-core` 4.10.3 checks. Only distinct out-of-scope follow-up items (`RV-001`, `RV-002`) and post-push hosted CI/human PR review remain.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct_follow_up (`RV-001`, `RV-002`) | Present ranked follow-up choices at automatic post-Review checkpoint |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier verified locally (`mypy`, `ruff check`, `ruff format --check` in `src/core` and `src/api`; `650` `src/core` unit tests; `680` `src/api` unit/correlation/content/UX tests; `checks.quality_sensors_browser_check` `42/42` + axe 4.10.3; `test_chat_panel` Chromium test `OK`; `web-design-guidelines` audit passed on `ops.js`, `assistants.js`, and `chat.js`; hosted CI unobserved on unpushed branch).
* Blockers: None
