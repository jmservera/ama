---
description: "Primary evidence artifact for Issue #189 simulator run controls (owner, time limit, budget alert)"
---
<!-- markdownlint-disable-file -->

# Task Research: simulator-run-controls-189

| Field              | Value                                                                      |
|--------------------|----------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                 |
| Researcher / agent | rpi-research (RPI Agent automatic session)                                 |
| Status             | Complete                                                                   |
| Artifact path      | .copilot-tracking/research/2026-11-15/simulator-run-controls-189-research.md |

## Research Brief

* What to research: Existing simulator run-control and governance modules in `src/core` (`run_governance.py`, `run_plan.py`, `sensor_stream.py`, `sensor_injector.py`, `live_readings.py`, `loadcheck.py`), `src/orchestrator`, `src/api` simulator callers, and `infra/` Bicep budget/alert declarations (`governance.bicep`, `iot-hub-live.bicep`, `live-simulator-job.bicep`, `modules/monitoring.bicep`, `modules/iothub.bicep`), plus PRD FR-050/AC-066, ADR 0003 decision 6, and prior `#189` RPI artifacts to determine what gaps remain for the unticked criterion `Run has an owner, a time limit and a budget alert`.
* Why it matters: Closes the sole remaining unticked acceptance criterion of Issue #189 while stacking cleanly onto `feat/demo-164-chat-grounding-provenance-0900` (#1641) without conflicts in `server.py`, `test_role_endpoint_inventory.py`, or `README.md`.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` phases in this automatic RPI session, plus future reviewers of Issue #189.
* Scope: `src/core/src/zava_forward/core/synthetic/*`, `src/core/tests/*`, `src/orchestrator/*`, `src/api/src/zava_forward/api/live_*`, `infra/*.bicep`, `infra/modules/*.bicep`, `infra/tests/*`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md`, and `.copilot-tracking/*/*189*`.
* Non-goals: Editing `server.py`, `test_role_endpoint_inventory.py`, or `README.md`; pushing to remote; altering unrelated API endpoints or UI screens.
* Criteria: Every simulator run configuration/invocation must enforce a non-empty named `owner` (rejecting anonymous/blank/placeholder owners), a bounded `time_limit_minutes` / `max_duration_seconds`, and a linked `budget_alert` contract (threshold + alert rule/owner reference) verified in both runtime preflight and Bicep/infra contract tests, covered by `src/core/tests/test_simulator_run_controls_189.py`.
* Requested outputs: Converged design and exact gap inventory for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                               |
|--------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | How do existing `src/core` simulator modules and `infra/` Bicep files implement run controls, and what exact gaps remain for #189? |
| Codebase scope                       | `src/core`, `src/orchestrator`, `src/api` (read-only caller check), `infra/`, `docs/prds/`, `docs/adrs/`, `.copilot-tracking/`      |
| External scope                       | none (repository-internal contracts and Bicep templates)                                                                            |
| Initial internal candidate areas     | `src/core/src/zava_forward/core/synthetic/run_governance.py`, `run_plan.py`, `infra/governance.bicep`, `infra/live-simulator-job.bicep`, `infra/iot-hub-live.bicep` |
| Initial external candidate areas     | none                                                                                                                                |
| Research posture                     | focused                                                                                                                             |
| Posture provenance                   | caller-specified (bounded internal issue slice with explicit file targets and stack constraints)                                    |
| Explicit limits / deadline           | Do not touch `server.py`, `test_role_endpoint_inventory.py`, or `README.md`; do not push                                            |
| Posture-specific completion basis    | focused scope and materiality                                                                                                       |
| Edits allowed during research?       | no, research-only                                                                                                                   |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                                |
| Known constraints / excluded sources | Stack conflict-free with sibling PRs on `feat/demo-164-chat-grounding-provenance-0900`                                              |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                               | Match and provenance                                   | Scoped authority or output contract                     | Selected / skipped reason                                                       |
|---------------------|-----------------------------------------|--------------------------------------------------------|---------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA) | `applyTo: "**"` matches repository and tracking paths  | Validation tiering, branch/commit hygiene, Markdown style | Selected: governs test commands, focused validation tier, and commit formatting |
| Skill               | `rpi-research`                          | Explicit RPI loop phase 1                              | Primary research artifact and 3-wave cycle contract     | Selected: active phase skill                                                    |
| Skill               | `python-foundational`                   | Python codebase target                                 | General Python practices                                | Skipped: existing `src/core` typing/ruff/mypy conventions are directly inspectable |
| Research specialist | `hve-core-all:rpi-researcher`           | General research lane worker                           | Subagent lane file under `research/subagents/`          | Skipped (inline): tightly coupled bounded internal files inspectable in <=5 direct reads |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                 | Answers / unanswered | Resulting decision or selected further research                                  |
|------------------|-------------------------------------------------------------------------------------------------------|----------------------|----------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit scope, acceptance criterion, file exclusions, and test path | Not applicable       | Proceed in `focused` convergence posture under caller-confirmed automatic mode   |
| Direction change | None                                                                                                  | Not applicable       | Original caller brief remains active                                             |
| Convergence      | Evidence complete across `src/core`, `src/api`, `infra/`, PRD/ADR, and `#189` | Not applicable       | Converged on additive `BudgetAlertContract` + `SimulatorRunControls` preflight and Bicep contract verifier without touching excluded files |

## Scope and Success Criteria

* Scope: Inspect `src/core` simulator run-control and synthetic stream modules, `src/orchestrator`, `src/api` simulator callers, `infra/` Bicep budget/alert definitions, and prior `#189` artifacts; design complete runtime + Bicep contract enforcement and `src/core/tests/test_simulator_run_controls_189.py` without touching excluded files.
* Assumptions:
  * Prior `#189` commits may already exist on `main` / base branch (`run_governance.py`, `run_plan.py`), and we must verify what is already implemented versus what remains incomplete or unaligned for `owner`, `time_limit`, and `budget_alert`.
* Success criteria:
  * Every research question is answered with `C#` `path:line` citations.
  * Exact contract between `src/core` simulator config/invocation and `infra/` Bicep budget/alert resources is verified.
  * Existing tests and callers are checked so no regressions are introduced.

## Task Research Requests

* Explicit requests:
  1. Inspect existing IoT simulator / run-control modules in `src/core` and `src/orchestrator` and `infra/bicep/` budget/alert declarations.
  2. Determine how to enforce `owner`, `time_limit_minutes` / `max_duration_seconds`, and `budget_alert` contract in runtime preflight and Bicep/infra contract tests.
  3. Prepare plan for `src/core/tests/test_simulator_run_controls_189.py` without touching `server.py`, `test_role_endpoint_inventory.py`, or `README.md`.
* Inferred research questions:
  * What did the 2026-11-14 `#189` reviews/plans find as still missing for the third acceptance criterion?
  * Are all simulator entrypoints in `src/core` gated by the run-controls contract, or can any simulator stream/injector invocation bypass `owner`, `time_limit`, or `budget_alert`?
  * How are Bicep budget/alert contracts structured and tested in `infra/` and `src/core`?
* Caller constraints and non-goals: Convergence output for immediate `rpi-plan` handoff; exclude `server.py`, `test_role_endpoint_inventory.py`, `README.md`; do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                        | Source / checkpoint | Effect on active brief, evidence, or revalidation                         |
|----------------------------------------------------------|------------------------------------------------------------------------------|---------------------|---------------------------------------------------------------------------|
| narrow                                                   | Deliver unticked AC `Run has an owner, a time limit and a budget alert`      | Caller intake       | Focuses runtime + Bicep contract verification on owner, duration, budget  |
| exclude                                                  | Do not modify `server.py`, `test_role_endpoint_inventory.py`, or `README.md` | Caller intake       | Constrains implementation and contrarian alternatives to conflict-free files |
| exclude                                                  | Do not `git push`                                                            | Caller intake       | Local commit and clean working tree only                                  |

## Research Questions

|  # | Sub-question                                                                                                              | Type            | Priority | Status   |
|---:|---------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | What do PRD FR-050, AC-066, ADR 0003 decision 6, and prior `#189` artifacts specify for owner, time limit, and budget alert? | straightforward | H        | answered |
| Q2 | What do `run_governance.py`, `run_plan.py`, and other `src/core` / `src/orchestrator` / `src/api` simulator modules currently enforce, and where are bypasses or gaps? | depth           | H        | answered |
| Q3 | How do `infra/*.bicep` (`governance.bicep`, `iot-hub-live.bicep`, `live-simulator-job.bicep`, `modules/*`) declare budgets and alerts, and how do runtime preflight + contract tests verify alignment? | depth           | H        | answered |
| Q4 | What dependency rules (`rename-zava-tests.py`, `test_dependency_rule.py`, ruff, mypy) constrain `src/core` tests reading `infra/` or simulator modules? | straightforward | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (FR-050, AC-066, EXA-012), `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md` (Decision 6), `docs/reference/research/iot-sensor-analytics-research-plan.md`, and `.copilot-tracking/research/2026-11-14/simulator-controls-189-2142-research.md`.
* Reused (verified on `HEAD` `08c36e4dc`): PR #1676 (`54f6418dc`) and PR #1740 (`5f50fc238`) landed `RunGovernance`, `RunMeter`, and `RunController.status()` / `check_time_limit()` on `HEAD`. Issue #189 has its first two criteria ticked and `[ ] Run has an owner, a time limit and a budget alert` remaining unticked.

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow to Issue #189 Criterion 3 runtime preflight + Bicep contract tests; exclude `server.py`, `test_role_endpoint_inventory.py`, `README.md`, and `git push`.
* Active research posture and completion basis: `focused`; all relevant `src/core`, `src/orchestrator`, `src/api`, `infra/`, and specification sources inspected directly.
* Explicit limits or deadline effect: none blocking complete evidence collection.

#### Wave 1: Wider

* Plan and independent lanes: Inline survey across `src/core/src/zava_forward/core/synthetic/*`, `src/core/src/zava_forward/core/{simulation_lane,sensor_ingest,sensor_consumer}.py`, `src/orchestrator/*`, `src/api/src/zava_forward/api/{live_control,live_simulator,iot_stream,simulator_admin}.py`, `infra/*.bicep`, `infra/modules/*.bicep`, PRD FR-050/AC-066, and ADR 0003 Decision 6.
* Worker evidence relationships or inline fallback: Inline (tightly coupled repository contracts): Q1 -> `docs/prds/zava-forward-retrofit-programme-demonstrator.md:382`, `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:72`; Q2 -> `sensor_stream.py`, `run_governance.py`, `run_plan.py`; Q3 -> `infra/modules/iothub.bicep`, `infra/main.bicep`, `infra/governance.bicep`, `infra/live-simulator-job.bicep`.
* Reflection: Confirmed `src/orchestrator` contains no IoT simulator runtime (`C7`). All IoT simulator run-control logic in `src/core` lives in `zava_forward.core.synthetic.{sensor_stream,run_governance,run_plan}` (`C1`–`C3`), consumed by `src/api` (`iot_stream.py`, `live_control.py`, `live_simulator.py`, `simulator_admin.py`).

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Line-by-line audit of `sensor_stream.py`, `run_governance.py`, `run_plan.py`, `infra/modules/iothub.bicep`, `infra/main.bicep`, `infra/governance.bicep`, `infra/live-simulator-job.bicep`, `test_run_plan.py`, `test_simulator_run_budget_controls.py`, `test_dependency_rule.py`, and `pyproject.toml`.
* Plan and independent lanes: Inline audit of owner rejection rules, duration bounds (`time_limit_minutes` vs `max_duration_seconds` / `max_seconds`), budget-alert linking, `Pacer` invocation guards, and Bicep declarations.
* Worker evidence relationships or inline fallback: Inline: Q2 -> `sensor_stream.py:113-155`, `sensor_stream.py:318-355`, `run_governance.py:12-56`, `run_plan.py:55-353`; Q3 -> `infra/modules/iothub.bicep:216-256`, `infra/main.bicep:22-375`, `infra/governance.bicep:1-45`, `infra/live-simulator-job.bicep:51-96`; Q4 -> `src/core/pyproject.toml:26-42`, `src/core/tests/test_dependency_rule.py:1-35`, `tools/rename-zava-tests.py:1-120`.
* Reflection: Identified four specific enforcement and contract gaps:
  1. **Anonymous and non-identifier owners pass validation**: `accountable_text` (`sensor_stream.py:113-120`) and `governed_text` (`run_governance.py:14-21`) reject `"tbd"`, `"tbc"`, `"pending"`, `"none"`, `"unknown"`, `"nobody"`, `"unassigned"`, `"n/a"`, `"na"`, `"todo"`, and `<template>` strings, but accept `"anonymous"`, `"anon"`, `"guest"`, `"unattended"`, `"unowned"`, `"null"`, `"nil"`, `"system"`, `"auto"`, `"automated"`, `"bot"`, control characters, and punctuation-only strings such as `"---"` or `"..."`.
  2. **Direct `Pacer(budget)` invocation bypasses `RunBudget` preflight**: `Pacer.__init__` (`sensor_stream.py:319-336`) validates `speed` (`0 < speed <= 1000`) and sets `self.deadline = clock() + budget.max_seconds`, without checking `budget.owner`, `budget.cost_reference`, `budget.alert_reference`, `1 <= budget.max_seconds <= 3600`, or `0 < budget.max_per_second <= 100`. Likewise `Pacer.set_max_per_second` (`sensor_stream.py:346-349`) does not guard against `rate <= 0` or `rate > 100`.
  3. **No first-class `time_limit_minutes` / `max_duration_seconds` + linked `BudgetAlertContract` preflight**: `RunGovernance` and `RunPlan` accept raw seconds (`time_limit_seconds` / `max_seconds`) and split USD (`alert_threshold`, `alert_reference`) vs optional GBP (`budget_alert_gbp`, `budget_cap_gbp`) fields, without a unified `BudgetAlertContract` (linking `threshold_percent`, `alert_rule_reference`, and named `alert_owner_reference`) or `SimulatorRunControls` preflight supporting bounded `time_limit_minutes` (`<= 60.0`) / `max_duration_seconds` (`1.0..3600.0`) and CLI `--time-limit-minutes` / `--alert-owner`.
  4. **Bicep / Infra contract verification is partial**: `InfraAlignmentTests` in `test_run_plan.py:226-253` checks `iotHubSku`, `iotHubUnits`, `iotHubMonthlyCost`, and `actual80` regex, but does not verify the full three-part `#189` run-control contract across `infra/modules/iothub.bicep`, `infra/main.bicep`, `infra/governance.bicep`, and `infra/live-simulator-job.bicep` (required `owner` governance tag + `ownerTag`, bounded `replicaTimeout: 240 <= 3600` with `replicaRetryLimit: 0` and `--once` + `/certs/control.json`, and linked `Microsoft.Consumption/budgets` `actual80` / `forecast100` notifications wired to validated `alertEmail` contact/owner reference) or cross-check runtime `BudgetAlertContract` / `SimulatorRunControls` preflight against the Bicep declarations.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries:
  1. Does editing `sensor_stream.py` break any pinned `generator_revision` sha256 digest in tests or fixtures?
  2. Does adding dataclass fields directly to `RunPlan` alter `_body(plan)` (`asdict(plan)`) or break existing callers?
  3. Should `infra/*.bicep` be edited, or do existing Bicep templates already declare the required controls?
* Plan and independent lanes: Inline repo-wide grep for `synthetic-stream-v2`, `generator_revision`, `RunPlan(`, `RunBudget(`, and `RunGovernance(`, plus inspection of `test_sensor_stream.py`, `test_run_plan.py`, `test_simulator_run_budget_controls.py`, and `src/api/tests/test_live_control.py`.
* Worker evidence relationships or inline fallback:
  * **Checked `sensor_stream.py` digest sensitivity**: Repo-wide search confirmed zero hardcoded `generator_revision` digests exist for `sensor_stream.py` (`C1`); `test_sensor_stream.py:37-76` computes `descriptor(...)["generator_revision"]` dynamically. Moreover, tightening `accountable_text` in `sensor_stream.py` protects `RunBudget`, `Pacer`, `RunGovernance`, `RunPlan`, and `src/api`'s `live_control.parse()` simultaneously while keeping valid short fixture strings (`"owner"`, `"o"`, `"r"`, `"ref-1"`) valid (`C8`).
  * **Checked `RunPlan` `asdict(plan)` compatibility**: `_body(plan)` (`run_plan.py:181-186`) calls `asdict(plan)`. All existing tests round-trip `record(plan, path)` -> `RunController(plan).start(path)` in temp directories (`C3`, `C9`). Keeping `RunPlan`'s existing field names/defaults intact while adding optional `alert_owner: str | None = None` (defaulting to `self.owner` in `budget_alert_contract()` when `None`) plus `RunPlan.from_controls(...)` / `time_limit_minutes` / `max_duration_seconds` properties and `preflight_controls()` preserves 100% backward compatibility with all `RunPlan(...)` callers in `src/core` and `src/api`.
  * **Checked whether `infra/*.bicep` needs edits**: `infra/modules/iothub.bicep`, `infra/main.bicep`, `infra/governance.bicep`, and `infra/live-simulator-job.bicep` already declare the required owner tag policy, bounded job timeout (`replicaTimeout: 240`), and `actual80`/`forecast100` budget alert notifications with `contactEmails: [alertEmail]` (`C4`–`C6`). Keeping `infra/*.bicep` read-only avoids triggering infrastructure-tier release gates and eliminates sibling-PR merge conflicts while verifying real Bicep sources (and compiled ARM JSON when `az bicep` is present) in contract helpers and `src/core/tests/test_simulator_run_controls_189.py`.
* Reflection: All three contrarian checks converged cleanly; no open uncertainties remain.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs | Parent disposition | Evidence-based rationale | Primary-artifact treatment |
|------------------|--------------|--------------------|--------------------------|----------------------------|
| Harden `accountable_text` and `governed_text` to reject anonymous, unattended, bot/system, null/nil, control-char, and punctuation-only identifiers while preserving alphanumeric role/human identifiers | C1, C2, C8 | accepted | Directly closes anonymous/blank owner bypass across `RunBudget`, `Pacer`, `RunGovernance`, `RunPlan`, and `live_control` without breaking valid fixtures | Selected recommendation |
| Add `RunBudget.preflight()` and enforce it in `Pacer.__init__()` and rate bounds in `Pacer.set_max_per_second()` | C1 | accepted | Prevents unguarded `Pacer` execution with blank/anonymous owners, missing alert references, or unbounded `max_seconds` | Selected recommendation |
| Add `BudgetAlertContract` + `SimulatorRunControls` (`owner`, `time_limit_minutes` / `max_duration_seconds`, linked `budget_alert` rule + threshold + owner reference) and Bicep contract extractor/verifier in `run_governance.py` / `run_plan.py`, wired into `RunGovernance`, `RunPlan`, `RunController`, and `run_plan.main` | C2, C3, C4, C5, C6 | accepted | Enforces all three #189 Criterion 3 controls at runtime preflight and verifies alignment with `infra/` Bicep templates | Selected recommendation |
| Add focused unit and Bicep contract suite in `src/core/tests/test_simulator_run_controls_189.py` without touching `server.py`, `test_role_endpoint_inventory.py`, `README.md`, or `infra/*.bicep` | C4, C5, C6, C10 | accepted | Satisfies caller Requirements 2–4 and stacks conflict-free onto `feat/demo-164-chat-grounding-provenance-0900` | Selected recommendation |
| Mutate `infra/*.bicep` or `src/api/server.py` | C4, C6, C10 | rejected | `infra/*.bicep` already declares required controls; touching `server.py` or `README.md` violates explicit caller conflict-free constraints | Rejected alternative |

## Codebase Evidence Log

| ID  | Workspace-relative `path:line`                                              | Verified fact                                                                                                                                      |
|-----|-----------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| C1  | `src/core/src/zava_forward/core/synthetic/sensor_stream.py:113-155,319-350` | `accountable_text` omits anonymous/unattended/punctuation-only checks; `Pacer.__init__` does not call `RunBudget` preflight validation             |
| C2  | `src/core/src/zava_forward/core/synthetic/run_governance.py:12-156`         | `RunGovernance` and `RunMeter` enforce `MAX_TIME_LIMIT_SECONDS = 3600.0` and GBP alert < cap, but lack `time_limit_minutes` and `BudgetAlertContract` |
| C3  | `src/core/src/zava_forward/core/synthetic/run_plan.py:55-353`               | `RunPlan`, `RunController`, and `main()` validate `owner`, `max_seconds`, `alert_threshold`, and `alert_reference`, using `asdict(plan)` in `_body` |
| C4  | `infra/modules/iothub.bicep:216-256`                                        | Declares `Microsoft.Consumption/budgets@2023-05-01` (`budget-${name}`) with `actual80` (80% Actual) and `forecast100` (100% Forecasted) to `[alertEmail]` |
| C5  | `infra/main.bicep:22-65,335-380` & `infra/governance.bicep:1-45`            | Declares `@minLength(5) param alertEmail`, `ownerTag`, `budget-${prefix}`, and policy `requiredTags` containing `'owner'`                          |
| C6  | `infra/live-simulator-job.bicep:18-96`                                      | Declares `job-live-simulator` with `replicaTimeout: 240`, `replicaRetryLimit: 0`, `--once`, `approvalReference`, and `/certs/control.json`         |
| C7  | `src/orchestrator/src/zava_forward/orchestrator/__main__.py:1-40`           | `src/orchestrator` hosts batch/rebuild/monitor jobs only; IoT simulator run controls reside in `src/core/src/zava_forward/core/synthetic/`         |
| C8  | `src/api/tests/test_live_control.py:22-145`                                 | `live_control` tests rely on `accountable_text` and include short alphanumeric fixture values (`"o"`, `"r"`, `"demo owner"`)                       |
| C9  | `src/core/tests/test_run_plan.py:15-253`                                    | Existing `RunPlan` and `InfraAlignmentTests` read `INFRA = Path(__file__).resolve().parents[3] / "infra"` directly from `src/core/tests`           |
| C10 | `src/core/pyproject.toml:26-42` & `src/core/tests/test_dependency_rule.py:1-35` | `src/core` enforces `ruff` (`line-length = 100`, `E,F,I,B,UP`), `mypy --strict`, and forbids importing non-`core` `zava_forward` packages      |

## Synthesized Findings and Selected Recommendation

* **Q1 (PRD/ADR specification)**: PRD FR-050, AC-066, and ADR 0003 Decision 6 require every synthetic IoT simulator run to declare an accountable human/role owner, a finite time limit preventing unattended execution, and a linked budget alert before traffic can start (`C2`, `C3`).
* **Q2 (`src/core` gaps)**:
  1. Tighten `accountable_text` (`sensor_stream.py`) and `governed_text` (`run_governance.py`) so blank, whitespace, control-character, punctuation-only, `<template>`, placeholder, and anonymous/unattended/system tokens (`anonymous`, `anon`, `guest`, `unattended`, `unowned`, `null`, `nil`, `tbd`, `tbc`, `todo`, `pending`, `n/a`, `na`, `none`, `unknown`, `nobody`, `unassigned`, `system`, `auto`, `automated`, `bot`) are rejected.
  2. Extract `RunBudget.preflight()` and call it in `RunBudget.validate()`, `Pacer.__init__()`, and rate validation in `Pacer.set_max_per_second()`.
  3. Add frozen `BudgetAlertContract` (`threshold_percent`, `alert_rule_reference`, `alert_owner_reference`, optional `budget_cap_usd` / `budget_alert_gbp` / `budget_cap_gbp`) and `SimulatorRunControls` (`owner`, bounded `max_duration_seconds` / `time_limit_minutes` in `1..3600s` / `<=60m`, and `budget_alert: BudgetAlertContract`) in `run_governance.py`, wired into `RunGovernance`, `RunPlan` (`alert_owner`, `time_limit_minutes`, `max_duration_seconds`, `budget_alert_contract()`, `preflight_controls()`, `RunPlan.from_controls()`), `RunController` (`preflight_controls()`, `status()`), and `run_plan.main()` (`--time-limit-minutes`, `--alert-owner`).
* **Q3 (Bicep alignment & contract verification)**: Provide deterministic Bicep contract verification (`verify_bicep_run_controls_contract`) and focused tests in `src/core/tests/test_simulator_run_controls_189.py` validating `infra/modules/iothub.bicep`, `infra/main.bicep`, `infra/governance.bicep`, and `infra/live-simulator-job.bicep` (plus `az bicep build` ARM JSON checks when `az` is installed) against runtime `BudgetAlertContract` / `SimulatorRunControls` preflight, including negative/tampered Bicep text rejection tests.
* **Q4 (Tooling & conflict boundaries)**: All edits stay strictly inside `src/core/src/zava_forward/core/synthetic/{sensor_stream,run_governance,run_plan}.py`, `src/core/tests/test_simulator_run_controls_189.py`, and `.copilot-tracking/*`, leaving `server.py`, `test_role_endpoint_inventory.py`, and all `README.md` files untouched.

## Readiness and Handoff

* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`
* **Unresolved blockers**: None (live Azure Consumption alert firing remains an external hosted check under #146/#189, so commit uses `Refs #189` as instructed).
* **Self-check**: Complete Cycle 1 (Wider -> Deeper -> Contrarian -> Synthesis) recorded; all `Q1`–`Q4` answered with `C1`–`C10` `path:line` evidence; zero source files modified during Research.

