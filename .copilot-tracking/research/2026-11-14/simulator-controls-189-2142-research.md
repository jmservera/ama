<!-- markdownlint-disable-file -->

# Task Research: simulator-controls-189-2142

| Field              | Value                                                                           |
|--------------------|---------------------------------------------------------------------------------|
| Date               | 2026-11-14                                                                      |
| Researcher / agent | rpi-research (RPI Agent)                                                        |
| Status             | Complete                                                                        |
| Artifact path      | .copilot-tracking/research/2026-11-14/simulator-controls-189-2142-research.md   |

## Research Brief

* What to research: How `src/core` enforces and reports the third acceptance criterion of Issue #189 ("Run has an owner, a time limit and a budget alert") across `run_governance.py`, `run_plan.py`, `sensor_stream.py`, tests, and documentation, including evaluation of the partial uncommitted edits present in worktree `feat-189-simulator-controls-2142`.
* Why it matters: Simulator runs must never execute unattended or without an accountable human owner, bounded runtime (`<= 3600` seconds), and validated budget-alert configuration (both mandatory Bicep-aligned USD alert reference/threshold and optional caller-declared GBP spend alert/pre-cap halt), with consistent inspection across `idle`, `running`, and `stopped` states.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` for local `src/core` delivery on branch `feat/iot-189-simulator-controls-2142`.
* Scope: `src/core/src/zava_forward/core/synthetic/run_governance.py`, `src/core/src/zava_forward/core/synthetic/run_plan.py`, `src/core/tests/test_simulator_run_budget_controls.py`, `src/core/tests/test_run_plan.py`, `src/core/README.md`, and read-only cross-checks against `sensor_stream.py`, `infra/modules/iothub.bicep`, `src/api`, PRD FR-050/AC-066, and ADR 0003 Decision 6.
* Non-goals: Live Azure IoT Hub deployment or live `Microsoft.Consumption/budgets` verification (#146), changes to `sensor_stream.py` that alter synthetic `generator_revision` hashes, or pushing to remote (`git push` explicitly prohibited by caller).
* Criteria: Every simulator run requires a non-placeholder owner, bounded time limit, and validated budget alert; status/inspection and enforcement are consistent across states and currencies; strict `mypy`, `ruff check`, `ruff format --check`, and simulator unit tests pass cleanly in `src/core`.
* Requested outputs: Dated primary research artifact with converged implementation recommendation for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                  |
|----------------------------------|--------------------------------------------------------------------------------------------------------|
| Research question(s)             | Q1-Q4 below: current coverage, uncommitted-diff defects, provenance/regression risks, and test scope   |
| Codebase scope                   | `src/core/`, `src/api/` (read-only caller check), `infra/modules/iothub.bicep`, `docs/`                |
| External scope                   | none (codebase and committed specification/regulatory synthesis task)                                  |
| Initial internal candidate areas | `src/core/src/zava_forward/core/synthetic/{run_governance,run_plan,sensor_stream}.py`, `src/core/tests/` |
| Initial external candidate areas | none                                                                                                   |
| Research posture                 | focused                                                                                                |
| Posture provenance               | caller-specified bounded `src/core` scope and explicit verification command                            |
| Explicit limits / deadline       | Local `src/core` delivery only; do not push; `git status --short` must be empty after commit           |
| Posture-specific completion basis| focused scope and materiality: all affected modules, callers, tests, and specifications inspected      |
| Edits allowed during research?   | no, research-only                                                                                      |
| Resolved evidence root           | `.copilot-tracking/`                                                                                   |
| Known constraints / excluded sources | Preserve `sensor_stream.py` `generator_revision` digest; keep live Azure #146 verification distinct |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | Repository custom instructions   | `applyTo: "**"` across repo                       | Focused validation tier, Markdown/test rules | Selected: governs `src/core` and honest `Refs #189` boundary |
| Skill               | `rpi-research`                   | Explicit RPI loop phase 1                         | Read-only three-wave primary artifact        | Selected: active phase skill   |
| Skill               | `python-foundational`            | Python library changes in `src/core`              | General Python conventions                   | Skipped: `src/core/pyproject.toml` strict `mypy`/`ruff` rules already explicit |
| Research specialist | `hve-core-all:rpi-researcher`    | Host-registered delegated research worker         | Subagent lane artifact                       | Skipped (inline): tightly coupled 3-file `src/core` target inspected directly in <5 reads |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit branch, worktree, target criterion, and verification command | Unasked (non-interactive; brief unambiguous) | Proceed in focused convergence mode |
| Direction change | Partial uncommitted diff found in 4 `src/core` files from worktree setup; audited inline rather than discarded | Unasked (non-interactive) | Retain and harden valid parts of the worktree diff while fixing schema, clock-freeze, and `planned_cost_gbp` gaps |
| Convergence      | Evidence across `src/core`, `src/api`, `infra`, and `docs` is complete and consistent | Unasked (non-interactive) | Converge on hardening `run_governance.py`, `run_plan.py`, tests, and `src/core/README.md` |

## Scope and Success Criteria

* Scope: Offline deterministic simulator governance in `src/core` (`run_governance.py`, `run_plan.py`, `test_simulator_run_budget_controls.py`, `src/core/README.md`).
* Assumptions:
  * Existing uncommitted changes in the worktree represent an incomplete draft for `RunController.status()` and `RunMeter.summary()` that must be audited, corrected, tested, and cleanly committed. (Verified via `git diff` and file mtimes.)
  * Live Azure budget alert verification remains an external/hosted gate under #146 and #189, so commit trailer/subject must not falsely claim live Azure verification. (Verified in `docs/reference/research/iot-sensor-analytics-research-plan.md`.)
* Success criteria:
  * Every research question is answered with `path:line` codebase evidence.
  * Findings, decisions, and readiness claims cite Evidence Log IDs (`C1`-`C6`).
  * Alternatives are compared with trade-offs and one recommendation is selected.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Run Research -> Plan -> Implement -> Review for Issue #189 on `feat/iot-189-simulator-controls-2142`; deliver the locally verifiable acceptance criterion "Run has an owner, a time limit and a budget alert" in `src/core`; write all 4 `.copilot-tracking/` artifacts; verify with `mypy`, `ruff check`, `ruff format --check`, and `unittest discover -s tests -p 'test_*simulator*.py' -v`; commit cleanly without pushing.
* Inferred research questions: What already landed in PR #1676 (`54f6418dc`), what the uncommitted worktree diff adds, what defects or gaps remain in `run_governance.py` and `run_plan.py`, and whether any sibling modules (`sensor_stream.py`, `src/api`) constrain the design.
* Caller constraints and non-goals: `src/core` local scope; no `git push`; clean working tree at closeout.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Deliver locally verifiable criterion 3 in `src/core` and verify with bare `mypy`, `ruff`, and `test_*simulator*.py` | User prompt (intake) | Keeps implementation confined to `src/core` while preserving `src/api` compatibility |
| exclude                                                  | Do not push to remote; `git status --short` must be empty | User prompt (intake) | Local commit only; hosted CI and live Azure #146 remain explicitly noted as not run |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status   |
|---:|------------------|------------------------------------------|-----------|----------|
| Q1 | What simulator owner, time-limit, and budget-alert controls already exist on `HEAD` and in callers? | breadth | H | answered |
| Q2 | What does the uncommitted worktree diff add, and what schema, state, or validation defects remain? | depth | H | answered |
| Q3 | Can `sensor_stream.py` or `RunPlan` serialisation be broken by naive governance changes? | depth | H | answered |
| Q4 | Which tests match `test_*simulator*.py` vs sibling suites (`test_run_plan.py`, `test_sensor_stream.py`)? | straightforward | M | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-14/issue-189-c1-governance-wiring-research.md`, `.copilot-tracking/reviews/2026-11-14/issue-189-c1-governance-wiring-review.md`, `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md`, `docs/reference/research/iot-sensor-analytics-research-plan.md`, and GitHub Issue #189 comments.
* Reused (verified) findings: PR #1676 (`54f6418dc`) added `run_governance.py` (`RunGovernance`, `RunMeter`) and wired optional `budget_alert_gbp`, `budget_cap_gbp`, and `planned_cost_gbp` into `RunPlan` and `RunController.admit()`; `RunPlan` remained a JSON-serialisable frozen dataclass so `_body(plan)` sha256 digests stay deterministic.
* Superseded / stale: Issue #189's body text "Existing delivery and status: Not started" is stale relative to merged PRs #637, #707, #845, #1092, #1313, and #1676; closure comments confirm criteria 1 and 2 are ticked while criterion 3 remains open pending complete run-level governance status/controls locally and live alert verification (#146).

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow to `src/core`; exclude `git push`.
* Active research posture and completion basis: `focused`; all target modules, callers, and specifications inspected directly.
* Explicit limits or deadline effect: none blocking local `src/core` evidence.

#### Wave 1: Wider

* Plan and independent lanes: Inline survey of `src/core/src/zava_forward/core/synthetic/`, `src/api/src/zava_forward/api/`, `infra/modules/iothub.bicep`, PRD FR-050/AC-066, and ADR 0003 Decision 6.
* Worker evidence relationships or inline fallback: Inline (small bounded file set): Q1 -> `run_governance.py`, `run_plan.py`, `sensor_stream.py`, `iot_stream.py`, `live_simulator.py`, `simulator_admin.py`, `iothub.bicep`.
* Reflection: `src/core` has two complementary layers: `RunPlan`/`RunBudget`/`Pacer` (mandatory owner, `max_seconds <= 3600`, USD budget + `alert_threshold` + `alert_reference` aligned with Bicep `actual80`) and `RunGovernance`/`RunMeter` (GBP threshold alert + pre-cap halt + deadline halt). Worktree already contains an uncommitted draft adding `RunMeter.summary()` and `RunController.status()`.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Detailed line-by-line inspection of `run_governance.py`, `run_plan.py`, `test_simulator_run_budget_controls.py`, `test_run_plan.py`, and `pyproject.toml`.
* Plan and independent lanes: Inline inspection of state transitions (`idle` -> `running` -> `stopped`), JSON digest serialisation in `record()`, `mypy` strictness, and `unittest` discovery pattern `test_*simulator*.py`.
* Worker evidence relationships or inline fallback: Inline: Q2/Q4 -> `run_governance.py:95-131`, `run_plan.py:67-250`, `test_simulator_run_budget_controls.py:1-208`, `pyproject.toml:34-40`.
* Reflection: Found four concrete issues in the draft and current `RunPlan`/`RunController` contract:
  1. `RunController.status()` has inconsistent keys: when `self.meter is None`, it returns `"budget_alert_gbp": None` (even if `plan.budget_alert_gbp` is set while `state == "idle"`) and omits `alert_reference`, `alert_fires_at_usd`, `elapsed_seconds`, `remaining_seconds`, `active_homes`, `halt_reason`, and `alert_raised`; when `self.meter` is set, `"budget_alert_gbp"` disappears and is named `"alert_gbp"` instead.
  2. Neither `RunMeter` nor `RunController` freezes elapsed time when halted or stopped (`self.clock() - self.started` keeps advancing after `stop()` or halt).
  3. `RunPlan.governance()` skips `planned_cost_gbp` validation when `budget_alert_gbp` and `budget_cap_gbp` are `None`, allowing invalid (`"nan"`, `"-1"`) or nonzero (`"3.00"`) `planned_cost_gbp` without GBP budget-alert governance, and non-`str` GBP fields on `RunPlan` could bypass `StreamError("INVALID_BUDGET")` and fail `json.dumps` with `TypeError`.
  4. `RunController.admit()` narrows `cost_gbp` to `str | int` instead of `Decimal | int | str`, and `RunController` lacks a direct `check_time_limit()` / deadline enforcement helper for runs inspected or stepped outside `Pacer._wait_until()`.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge whether placeholder checks should be updated in `sensor_stream.py`, whether `_body(plan)` should be altered, and whether GBP governance should become mandatory on `RunPlan`.
* Plan and independent lanes: Inline check of `sensor_stream.revision_sources`, `test_run_plan.py`, and `src/api/tests/test_iot_stream.py`.
* Worker evidence relationships or inline fallback:
  * Disproved editing `sensor_stream.py`: `sensor_stream.py:255` includes `Path(__file__)` in `revision_sources`, which hashes file bytes into `generator_revision` for synthetic stream provenance (`C5`). Any placeholder tightening (`"tbc"`, `"pending"`) must live in `run_governance.py` / `run_plan.py`, leaving `sensor_stream.py` untouched.
  * Disproved making `budget_alert_gbp` mandatory on `RunPlan` or changing `_body(plan)` top-level keys: existing `test_run_plan.py` and `src/api/tests/test_iot_stream.py` construct `RunPlan` with USD `budget_usd`, `alert_threshold`, and `alert_reference` (`C3`, `C6`), and `RunController.start()` checks exact `_body(self.plan)` equality. Keeping GBP fields optional-as-a-pair while exposing both the mandatory USD alert (`alert_reference`, `alert_fires_at_usd`) and GBP alert (`budget_alert_gbp` / `alert_gbp`, `alert_raised`) in `RunController.status()` satisfies Criterion 3 for every run without breaking callers.
* Reflection: Contrarian checks prevented two subtle regressions (provenance hash drift in `sensor_stream.py` and caller compatibility in `src/api`). No material uncertainty remains.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment  |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|-----------------------------|
| Normalize `RunController.status()` and `RunMeter.summary()` with consistent owner, time-limit,frozen elapsed/remaining time, and USD + GBP budget-alert fields | C1, C2, C4 | accepted | Eliminates key mismatch (`budget_alert_gbp` vs `alert_gbp`), idle-state false `None`, and post-stop clock drift | Selected recommendation |
| Enforce `str` type and `planned_cost_gbp == 0` when GBP governance is omitted; reject `"tbc"`/`"pending"` owner/alert placeholders in `run_governance.py`/`run_plan.py`; widen `RunController.admit` to `Decimal \| int \| str` and enforce deadline via `check_time_limit()` | C1, C3, C4 | accepted | Closes silent un-governed `planned_cost_gbp` loophole, prevents raw `TypeError` in `record()`, and enforces time limit deterministically | Selected recommendation |
| Modify `sensor_stream.py` `_PLACEHOLDERS` directly | C5 | rejected | `sensor_stream.py` is hashed in `revision_sources()`; touching it alters `generator_revision` for unrelated synthetic stream provenance | Rejected alternative |
| Verify live Azure Consumption budget alert in this local task | C6 | deferred | Requires live Azure subscription/Consumption run under #146; out of `src/core` offline scope | Unresolved external gate (`Refs #189`) |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Focused scope covered; all code paths, callers, and contrarian regression vectors verified from primary codebase files.
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: bounded 4-file `src/core` target with direct cross-check of `sensor_stream.py`, `src/api`, and `infra/modules/iothub.bicep` completed in fewer than five reads per wave.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`)           | Tool                                | Confidence       | Notes       |
|----|-----------------|----------------------------------|-------------------------------------|------------------|-------------|
| C1 | `RunGovernance` and `RunMeter` validate accountable `run_owner`, `1 <= time_limit_seconds <= 3600.0`, and `0 < budget_alert_gbp < budget_cap_gbp`, emitting one `budget_alert` event at threshold and halting with `RUN_BUDGET_HALT` before cap or `RUN_DEADLINE` at limit | `src/core/src/zava_forward/core/synthetic/run_governance.py:31` | view | high | Merged in PR #1676 (`54f6418dc`) |
| C2 | Draft `RunMeter.summary()` computes `round(self.clock() - self.started, 3)` without recording halt/stop timestamp, so `elapsed_seconds` keeps advancing after halt; `"tbc"` and `"pending"` placeholders present in sibling modules (`live_control.py:29`, `device_provision.py:22`) are not rejected | `src/core/src/zava_forward/core/synthetic/run_governance.py:95` | view / grep | high | Uncommitted worktree draft + cross-module grep |
| C3 | `RunPlan` mandates `owner`, `max_seconds`, `budget_usd`, `alert_threshold`, and `alert_reference`, plus optional `budget_alert_gbp`, `budget_cap_gbp`, and `planned_cost_gbp`, but `RunPlan.governance()` ignores `planned_cost_gbp` when alert/cap GBP are `None` and does not guard non-`str` GBP fields before `json.dumps(asdict(plan))` | `src/core/src/zava_forward/core/synthetic/run_plan.py:67` | view | high | Allows nonzero or malformed `planned_cost_gbp` when GBP alert/cap omitted |
| C4 | Draft `RunController.status()` drops `"budget_alert_gbp"` when `self.meter` is active (`summary()` uses `"alert_gbp"`), reports `"budget_alert_gbp": None` in `idle` even when `plan.budget_alert_gbp` is set, omits mandatory `alert_reference`/`alert_fires_at_usd`/elapsed/remaining fields when `meter is None`, and narrows `admit()` to `str \| int` | `src/core/src/zava_forward/core/synthetic/run_plan.py:193` | view | high | Key inconsistency between ungoverned/idle and governed states |
| C5 | `sensor_stream.revision_sources()` hashes `sensor_stream.py` into `generator_revision`, whereas `run_governance.py` and `run_plan.py` are excluded | `src/core/src/zava_forward/core/synthetic/sensor_stream.py:255` | view | high | Keep `sensor_stream.py` untouched |
| C6 | `InfraAlignmentTests` binds `RunPlan` tier (`B1`), units (`1`), and `0.8` `alert_threshold` to `infra/modules/iothub.bicep` (`actual80`, `forecast100`), while only `test_simulator_run_budget_controls.py` matches `-p 'test_*simulator*.py'` in `src/core/tests` | `src/core/tests/test_run_plan.py:211` | view / glob | high | Targeted simulator test file must thoroughly cover Criterion 3 |

### External Evidence

| ID | Claim / finding | Source (title) | URL     | Retrieved      | Version/date | Confidence       |
|----|-----------------|----------------|---------|----------------|--------------|------------------|

### Contradictions / Conflicts

* Issue #189 body says `Not started`, whereas merged commits (`b70345a4f`, `640342230`, `54f6418dc`) and issue closure comments (2026-11-03, 2026-11-09) show Criteria 1 and 2 ticked and Criterion 3 locally partially delivered; resolved by recency and primary `main` git history -> deliver remaining local `src/core` Criterion 3 contract and reference `#189` honestly (`Refs #189`) because live Azure alert verification (#146) remains external.

## Findings Mapped to Questions and Evidence

| Question | Finding             | Evidence IDs | Confidence          | Decision or readiness implication    |
|----------|---------------------|--------------|---------------------|--------------------------------------|
| Q1       | `RunPlan`/`RunBudget`/`Pacer` enforce owner, `max_seconds <= 3600`, and USD budget alert reference/threshold; `RunGovernance`/`RunMeter` enforce GBP alert, pre-cap halt, and deadline halt | C1, C3, C6 | high | Build on existing `RunGovernance`, `RunMeter`, `RunPlan`, and `RunController` |
| Q2       | Worktree draft adds `RunMeter.summary()` and `RunController.status()`, but has key mismatch (`budget_alert_gbp` vs `alert_gbp`), post-halt/stop clock drift, unvalidated `planned_cost_gbp` when GBP alert/cap are `None`, missing `"tbc"`/`"pending"` placeholder guard, and narrow `admit()` typing | C2, C3, C4 | high | Fix all five gaps in `run_governance.py` and `run_plan.py` |
| Q3       | Editing `sensor_stream.py` would change `generator_revision`, and altering `_body(plan)` structure or requiring GBP fields on every `RunPlan` would break existing `RunPlan` callers in `src/core` and `src/api` | C3, C5, C6 | high | Keep `sensor_stream.py` and `_body(plan)` intact; validate in `run_governance.py` and `run_plan.py` |
| Q4       | Only `src/core/tests/test_simulator_run_budget_controls.py` matches `-p 'test_*simulator*.py'`, while `test_run_plan.py` and `test_sensor_stream.py` provide sibling regression coverage | C6 | high | Put new Criterion 3 unit tests in `test_simulator_run_budget_controls.py` and also run `test_run_plan.py` + `test_sensor_stream.py` |

## Key Discoveries

* `RunController.status()` must expose a unified schema across `idle`, `running`, and `stopped` states and across USD-only and USD+GBP plans so callers always see `run_owner`, `time_limit_seconds`, frozen-on-stop `elapsed_seconds`, `remaining_seconds`, `alert_reference`, `alert_fires_at_usd`, `budget_alert_gbp`, `alert_raised`, and `halt_reason` (`C2`, `C4`).
* `RunPlan.validate()` / `RunPlan.governance()` currently ignores `planned_cost_gbp` when `budget_alert_gbp` and `budget_cap_gbp` are omitted, allowing un-governed or malformed `planned_cost_gbp` (`C3`).
* `sensor_stream.py` participates in `generator_revision` hashing (`C5`), so placeholder alignment (`"tbc"`, `"pending"`) belongs in `run_governance.py` / `run_plan.py`.

### Complete Examples

```python
status = controller.status()
# Consistent keys before start, during run, and after stop/halt:
# state, run_owner, time_limit_seconds, elapsed_seconds, remaining_seconds,
# active_homes, alert_reference, alert_fires_at_usd, budget_alert_gbp,
# alert_raised, halt_reason (plus meter fields when GBP governance is active).
```

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Harden `run_governance.py` and `run_plan.py` (without touching `sensor_stream.py` or changing `_body(plan)` digest layout) so every simulator plan and controller run enforces and reports a non-placeholder owner (including `"tbc"`/`"pending"` refusal), a bounded time limit (`1 <= max_seconds <= 3600`, with `check_time_limit()` deadline enforcement and frozen `elapsed_seconds`/`remaining_seconds` on halt or stop), and a validated budget alert (mandatory `alert_reference` + `alert_fires_at_usd` plus optional paired `budget_alert_gbp`/`budget_cap_gbp` with strict `str` serialisation and `planned_cost_gbp` validation). Expand `test_simulator_run_budget_controls.py` and update `src/core/README.md`.
* Rationale: Delivers a complete, consistent, fail-closed `src/core` contract for Criterion 3, preserves all existing `src/core` and `src/api` callers and `sensor_stream.py` provenance hashes, and ensures `test_*simulator*.py` directly verifies every edge case.
* Evidence refs: C1, C2, C3, C4, C5, C6
* Implementation impact: `src/core/src/zava_forward/core/synthetic/run_governance.py`, `src/core/src/zava_forward/core/synthetic/run_plan.py`, `src/core/tests/test_simulator_run_budget_controls.py`, `src/core/README.md`.
* Confidence: high: all callers and strict type/lint rules in `src/core/pyproject.toml` are directly verified.

File tree:

```text
src/core/
  README.md                                              (modified)
  src/zava_forward/core/synthetic/run_governance.py      (modified)
  src/zava_forward/core/synthetic/run_plan.py            (modified)
  tests/test_simulator_run_budget_controls.py            (modified)
```

### Alternative: Make `budget_alert_gbp` and `budget_cap_gbp` mandatory on `RunPlan`

* Approach: Require every `RunPlan` caller to supply `budget_alert_gbp` and `budget_cap_gbp` in addition to `budget_usd`, `alert_threshold`, and `alert_reference`.
* Trade-offs: Simplifies `RunController` to always construct `RunMeter`, but breaks existing `RunPlan` callers in `src/core/tests/test_run_plan.py` and `src/api/tests/test_iot_stream.py` where the Azure IoT Hub budget is modelled in USD (`B1_MONTHLY_USD = 10.0`).
* Evidence refs: C3, C6
* Rejection rationale: Unnecessary breaking change across `src/api`; `RunPlan` already mandates `budget_usd`, `alert_threshold`, and `alert_reference`, and unifying `RunController.status()` + `check_time_limit()` covers both USD-only and USD+GBP runs cleanly.

### Alternative: Extend `_PLACEHOLDERS` in `sensor_stream.py`

* Approach: Add `"tbc"` and `"pending"` directly to `sensor_stream._PLACEHOLDERS`.
* Trade-offs: Centralises placeholder strings in one constant, but mutates `sensor_stream.py` bytes and alters `generator_revision` digests produced by `sensor_stream.descriptor()`.
* Evidence refs: C2, C5
* Rejection rationale: Avoids synthetic provenance digest churn by keeping a small helper in `run_governance.py` imported by `run_plan.py`.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Live Azure `Microsoft.Consumption/budgets` alert firing and real subscription quota headroom cannot be proven by offline `src/core` unit tests (#146); commit and review artifacts must use `Refs #189` rather than `Closes #189`.
* Follow-up: Live exercise verification of Azure budget notifications when owner runs bounded IoT Hub telemetry (#146, #189).
* Residual uncertainty: none within `src/core` offline scope.

## Current Decisions

| Decision     | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale     | Evidence IDs | Implications                       |
|--------------|-------------------------------------------------------|-----------------------------------------------|---------------|--------------|------------------------------------|
| Harden `run_governance.py` and `run_plan.py` with unified `status()`, frozen stop/halt elapsed clock, `check_time_limit()`, strict `planned_cost_gbp` / `str` validation, and `"tbc"`/`"pending"` refusal | confirmed | evidence | Fixes all defects in worktree draft without breaking `src/api` or `sensor_stream.py` provenance | C1, C2, C3, C4, C5 | Scoped 4-file `src/core` implementation |
| Keep `sensor_stream.py` and `_body(plan)` top-level structure unchanged | confirmed | constraint | Preserves `generator_revision` and recorded estimate JSON compatibility | C3, C5, C6 | Zero regression in `test_sensor_stream.py`, `test_run_plan.py`, and `src/api` |
| Use `Refs #189` in commit message rather than `Closes #189` | confirmed | constraint | Repository instructions prohibit closing keywords when live Azure verification (#146) remains unmet | C6 | Honest issue linkage |

## Unresolved Decisions

| Decision     | Smallest evidence or answer needed     | Owner                                  | Impact     | Blocker status                       |
|--------------|----------------------------------------|----------------------------------------|------------|--------------------------------------|
| Live Azure budget alert verification (#146 / #189) | Live Azure subscription budget check and observed alert rule state during an approved exercise | Project owner | Required before ticking final #189 checkbox on GitHub | follow-up (non-blocking for local `src/core` slice) |

## Potential Next Research

| Priority  | Research item                  | Expected value     | Trigger                            | Selected?               | Related questions / evidence |
|-----------|--------------------------------|--------------------|------------------------------------|-------------------------|------------------------------|
| L         | Live Azure Consumption alert receipt capture (#146) | Closes remaining non-local #189 gate | Owner-authorized live Azure hub exercise | deferred | Q1; C6 |

## Planning Readiness

* Status: Ready
* Decision state: Converged on 4-file `src/core` hardening (`run_governance.py`, `run_plan.py`, `test_simulator_run_budget_controls.py`, `src/core/README.md`).
* Evidence basis: C1, C2, C3, C4, C5, C6
* Preconditions met: All target files, sibling callers, strict `mypy`/`ruff` settings, and test discovery selectors verified.
* Blockers: none
* Smallest action to change readiness: none (already `Ready`)

## Closeout Record

| Field                            | Record                                                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                                       |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian completed in order                                                                      |
| Lane evidence or inline fallback | Inline execution across bounded `src/core`, `src/api`, and `infra` targets; no subagent overhead required                      |
| Research disposition             | executed                                                                                                                       |
| Planning Readiness               | Ready (C1-C6)                                                                                                                  |
| Blockers                         | none                                                                                                                           |
| Continuation owner and state     | confirmed automatic RPI Agent; automatic continuation to `Plan` (`rpi-plan`)                                                   |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (C1-C6)                                                                                                |
| Output mode and planning support | convergence; yes, Planning Readiness is `Ready`                                                              |
| Acting owner                     | confirmed automatic RPI Agent                                                                                |
| Required gates or confirmations  | Research disposition recorded (passed); Planning Readiness `Ready` (passed); pre-transition state write (passed) |
| Continuation result              | automatic continuation to `Plan`                                                                             |
| Primary evidence file            | .copilot-tracking/research/2026-11-14/simulator-controls-189-2142-research.md                                |
| Notes for planning or re-entry   | Preserve `_body(plan)` digest compatibility and leave `sensor_stream.py` untouched; validate with bare `mypy`, `ruff`, `test_*simulator*.py`, plus sibling `test_run_plan.py` and `test_sensor_stream.py`. |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All in-scope `src/core` files, callers, and regression boundaries are verified with primary codebase evidence; further research would be redundant.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry, User Participation, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings, Key Discoveries, Alternatives, Open Questions, Current/Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources.
* Missing or limited sections: none
