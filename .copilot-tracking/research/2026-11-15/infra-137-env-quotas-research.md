---
description: "Primary evidence artifact for Issue #137 environment strategy, parameterized region and quota choices, fail-closed recorded checks, deterministic validation, and architecture documentation"
---
<!-- markdownlint-disable-file -->

# Task Research: infra-137-env-quotas

| Field                | Value                                                                          |
|----------------------|--------------------------------------------------------------------------------|
| Date                 | 2026-11-15                                                                     |
| Researcher / agent   | RPI Agent (`rpi-research`)                                                     |
| Status               | Complete                                                                       |
| Research disposition | executed                                                                       |
| Planning Readiness   | Ready                                                                          |
| Artifact path        | .copilot-tracking/research/2026-11-15/infra-137-env-quotas-research.md         |

## Research Brief

* What to research: Current parameterization, fail-closed guard behavior, CLI preflight checks, recorded check ledger (`R1`-`R17`), test coverage, and architecture/runbook documentation for environment strategy (`dev`, `test`, `pilot`) region and quota choices under Issue `#137` (`- [ ] Region and quota choices are parameters with recorded checks, not assumptions`).
* Why it matters: Ensures every region and quota-bearing choice across `dev`, `test`, and `pilot` is an explicit, bounded parameter backed by fail-closed recorded-check validation (rejecting assumptions, placeholders, whitespace, and secret/UUID leakage), verified offline in `infra/tests/test_environment_quota_parameters.py`, and documented accurately in `docs/architecture/` and `infra/README.md`.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` within this automatic RPI session, plus human reviewers auditing Issue `#137`.
* Scope: `infra/main.bicep`, `infra/modules/guard.bicep`, `infra/modules/sql.bicep`, `infra/modules/foundry.bicep`, `infra/modules/iothub.bicep`, `infra/modules/containerapps.bicep`, `infra/main.bicepparam`, `infra/main.test.bicepparam`, `infra/main.pilot.example.bicepparam`, `infra/iot-hub-live.bicep`, `infra/resident-demo.bicep`, `infra/resident-assistant.bicep`, `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, `infra/README.md`, `infra/tests/`, and `docs/architecture/`.
* Non-goals: Live Azure resource mutations, fabricating live Azure quota reservations or private subscription bindings, editing `infra/tests/test_monitoring_alerts.py` (to avoid cross-worktree conflicts), touching unrelated pre-existing `infra/` scripts, or pushing to remote.
* Criteria: Every region and quota parameter across `dev`, `test`, and `pilot` is inventoried with exact `path:line` evidence; all bypasses, unbounded inputs, implicit `.bicepparam` omissions, and documentation discrepancies are identified; compatibility with existing `infra/tests` (especially `test_bicep_policy.py` ARM expression evaluation and `test_governance.py` `.bicepparam` assertions) is verified.
* Requested outputs: Convergence recommendation with exact `C#`/`W#` evidence IDs, contrarian boundary checks, alternatives considered, and `Ready` planning state.
* Output mode: convergence

## Research Parameters

| Field                             | Value                                                                                                       |
|-----------------------------------|-------------------------------------------------------------------------------------------------------------|
| Research question(s)              | Q1-Q4 covering region/quota parameters, recorded-check enforcement, test invariants, and documentation gaps |
| Codebase scope                    | `infra/`, `docs/architecture/`, `docs/adrs/`, `docs/case_study_48_*.md`, `docs/reference/`, `.github/workflows/src-ci.yml` |
| External scope                    | Live GitHub Issue `#137` body and owner/audit comments via `gh issue view 137`                              |
| Initial internal candidate areas  | `infra/main.bicep`, `infra/main*.bicepparam`, `infra/modules/guard.bicep`, `infra/README.md`, `infra/tests/test_bicep_policy.py`, `docs/architecture/README.md` |
| Initial external candidate areas  | `https://github.com/jmservera/ama/issues/137`                                                               |
| Research posture                  | focused                                                                                                     |
| Posture provenance                | caller-specified (bounded infrastructure/documentation slice with Focused validation tier)                  |
| Explicit limits / deadline        | Single continuous automatic RPI run; new test file `infra/tests/test_environment_quota_parameters.py`; do not push |
| Posture-specific completion basis | Focused materiality: all target Bicep modules, parameter sets, CLI scripts, tests, and docs audited         |
| Edits allowed during research?    | no, research-only                                                                                           |
| Resolved evidence root            | `.copilot-tracking/`                                                                                        |
| Known constraints / excluded sources | Never put subscription or tenant UUIDs in committed artifacts; preserve honest boundaries between offline contracts, dated read-only Azure catalog observations (`R1`-`R17`), and unexecuted live pilot reservation/approval |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                         | Match and provenance                           | Scoped authority or output contract                   | Selected / skipped reason |
|---------------------|-----------------------------------|------------------------------------------------|-------------------------------------------------------|---------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` matches workspace and evidence | Repository documentation, honesty, validation, git rules | Selected: mandatory repository instructions |
| Skill               | `documentation` / `owasp-infrastructure` | Optional plugin skills                  | Advisory documentation and IaC guard patterns         | Skipped: repository Bicep guard module and Markdown style rules already define the exact schema |
| Research specialist | `hve-core-all:rpi-researcher`     | Available subagent for independent lanes       | Bounded lane artifact writer                          | Skipped (inline preferred): tightly coupled Bicep/ARM evaluator invariants require direct exact-line inspection |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                          | Answers / unanswered | Resulting decision or selected further research |
|------------------|--------------------------------------------------------------------------------|----------------------|-------------------------------------------------|
| Intake           | Non-interactive continuous RPI run with explicit target files, test path, and commit instructions | N/A (autonomous) | Proceed with `focused` posture in `convergence` mode |
| Direction change | None                                                                           | N/A                  | Maintain caller scope and conflict-avoidance constraint |
| Convergence      | All four research questions answered with `C1`-`C19` and `W1`-`W2` evidence    | Complete             | Converged on 5-part Bicep/CLI/parameter-set/docs/test slice (`Ready` for `rpi-plan`) |

## Scope and Success Criteria

* Scope: Parameter definitions and bounds for regions (`location`, `sqlLocation`, `zoneRedundant`, plus explicit regional boundaries of `iot-hub-live.bicep`, `resident-demo.bicep`, `resident-assistant.bicep`), quota/SKU/capacity inputs (`sqlTier`, `sqlVCores`, `sqlAutoPauseDelayMinutes`, `apiMinReplicas`, `chatModelName`, `chatModelVersion`, `chatModelSku`, `chatModelCapacity`, `modelDeployments`, `iotHubSku`, `iotHubUnits`, `iotHubMonthlyCost`, `monthlyBudget`), fail-closed recorded-check references (`regionCheckReference`, `quotaCheckReference`), CLI helpers (`deploy.py`, `pipeline.py`), architecture docs (`docs/architecture/`), runbook parity (`infra/README.md`), and deterministic offline tests (`infra/tests/test_environment_quota_parameters.py`).
* Success criteria:
  * Every codebase finding cites a workspace-relative `path:line` (`C#`) and external GitHub issue evidence cites URL and retrieval date (`W#`).
  * Contrarian checks verify that proposed Bicep/parameter edits will not break `test_bicep_policy.py`, `test_governance.py`, `test_sql_tier.py`, `test_deploy.py`, or `test_pipeline.py`.

## Task Research Requests

* Explicit requests:
  1. Inspect `infra/` Bicep parameter sets (`dev`, `test`, `pilot`), region/quota parameter definitions, and `infra/tests/`.
  2. Ensure region and quota choices are parameterized and validated by deterministic checks in `infra/tests/test_environment_quota_parameters.py` (new test file to avoid conflicts with `test_monitoring_alerts.py`) and documented in `docs/architecture/`.
  3. Run `python3 -m unittest infra/tests/test_environment_quota_parameters.py -q` and `python3 -m ruff check infra && python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_environment_quota_parameters.py`.
  4. Commit all changes and `.copilot-tracking/` artifacts with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`. Do not push.
* Inferred research questions:
  * Q1: Which region and quota parameters exist across `infra/main.bicep`, child modules, non-main Bicep entry points, and the three environment parameter sets (`dev`, `test`, `pilot`), and where do unbounded parameters or implicit assumptions remain?
  * Q2: How are `regionCheckReference`, `quotaCheckReference`, `location`, and `sqlLocation` mechanically enforced in Bicep (`guard.bicep` / `main.bicep`) and Python (`deploy.py` / `pipeline.py`), and what bypasses exist?
  * Q3: How are environment strategy, region/quota parameters, and recorded capability/quota checks (`R1`-`R17`) documented in `docs/architecture/` and `infra/README.md`, and where has documentation drifted from compiled templates?
  * Q4: What invariants in existing `infra/tests/` (`test_bicep_policy.py`, `test_governance.py`, `test_sql_tier.py`, `test_container_hosting_completeness.py`) constrain edits, and how does `ruff` behave on `infra/` in this environment versus hosted CI?

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect on active brief, evidence, or revalidation |
|--------------|-----------------------|---------------------|---------------------------------------------------|
| narrow       | Put new deterministic tests in `infra/tests/test_environment_quota_parameters.py` to avoid conflicts with `test_monitoring_alerts.py` | Caller intake | Isolates new test suite; preserves existing suites intact |
| narrow       | Focused validation tier; commit locally and do NOT push | Caller intake | Constrains validation and git closeout |

## Research Questions

| #  | Sub-question | Type | Priority | Status |
|---:|--------------|------|----------|--------|
| Q1 | Region and quota parameter coverage, bounds, and `.bicepparam` explicitness across `dev`, `test`, `pilot` | depth | H | answered (`C1`-`C9`) |
| Q2 | Mechanical fail-closed enforcement of `regionCheckReference`, `quotaCheckReference`, and deployment locations in Bicep and CLI helpers | depth | H | answered (`C1`, `C2`, `C10`, `C11`) |
| Q3 | Architecture documentation (`docs/architecture/`) and runbook parity (`infra/README.md`, `ADR 0002`) | breadth | H | answered (`C12`-`C14`, `W1`, `W2`) |
| Q4 | Existing `infra/tests` ARM evaluator/governance constraints and `ruff` configuration behavior | straightforward | H | answered (`C15`-`C19`) |

## Prior Knowledge Gate

* Reviewed baseline documents (`docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/adrs/0002-pilot-readiness-architecture.md`) and prior tracking artifact `.copilot-tracking/research/2026-10-18/issue137-pilot-capability-research.md`.
* Verified live GitHub Issue `#137` (`W1`, `W2`): four of five checklist items are ticked; only `- [ ] Region and quota choices are parameters with recorded checks, not assumptions` remains unticked. Owner comment `6192754703` (2026-10-15) selected pilot primary region `uksouth` and subscription owner `@jmservera`, leaving separate `sqlLocation`, availability zones, SKU/quota sizing, and live subscription check completion gated on recorded checks and human review.

## Cycle 1 Execution Log

### Wave 1: Wider

* Audited `infra/main.bicep`, all child modules (`guard.bicep`, `sql.bicep`, `foundry.bicep`, `iothub.bicep`, `containerapps.bicep`, `storage.bicep`, `registry.bicep`, `monitoring.bicep`), standalone templates (`iot-hub-live.bicep`, `resident-demo.bicep`, `resident-assistant.bicep`), all `.bicepparam` files (`main.bicepparam`, `main.test.bicepparam`, `main.pilot.example.bicepparam`, `iot-hub-live.bicepparam`), CLI scripts (`deploy.py`, `pipeline.py`), `infra/README.md`, `docs/architecture/`, `.github/workflows/src-ci.yml`, and `infra/tests/` (`C1`-`C19`).

### Wave 2: Deeper

* **Region & quota parameter bounds and `.bicepparam` coverage (`Q1`)**:
  * `infra/main.bicep` parameterizes primary `location` (`uksouth` guard), separate `sqlLocation` (allowing an alternate SQL server region when primary region restricts SQL server creation while keeping the SQL Private Endpoint in `endpointLocation: location`), `zoneRedundant` (`bool = false`), `sqlTier` (`serverless` | `provisioned`), `sqlVCores` (`int = 2`), `sqlAutoPauseDelayMinutes` (`-1` or `15..10080`), `apiMinReplicas` (`0..4`), `chatModelName` (`gpt-4.1-nano`), `chatModelVersion` (`2025-04-14`), `chatModelSku` (`GlobalStandard` | `Standard`), `chatModelCapacity` (`@minValue(1) = 1`), `modelDeployments` (`@minLength(1)` array), `iotHubSku` (`B1`), `iotHubUnits` (`1..1`), `iotHubRetentionDays` (`1..7`), `iotHubMonthlyCost` (`1..700`), and `monthlyBudget` (`int = 150`) (`C1`, `C3`-`C6`).
  * **Gap 1 (Missing numeric bounds)**: `sqlVCores` in `infra/main.bicep:110` and `infra/modules/sql.bicep:24` has no `@minValue` or `@maxValue` (allowing `0`, negative, or invalid vCore values), and `monthlyBudget` in `infra/main.bicep:99` has no `@minValue(1)` (`C1`, `C3`). Adding `@minValue(1) @maxValue(80)` to `sqlVCores` and `@minValue(1)` to `monthlyBudget` closes silent invalid capacity inputs.
  * **Gap 2 (Implicit quota parameters in `.bicepparam` files)**: `infra/main.bicepparam` (`dev`) and `infra/main.test.bicepparam` (`test`) omit `sqlVCores`, `apiMinReplicas`, `chatModelName`, `chatModelVersion`, `chatModelSku`, `chatModelCapacity`, `iotHubSku`, and `iotHubUnits`, while `infra/main.pilot.example.bicepparam` (`pilot`) declares `sqlTier = 'provisioned'`, `sqlVCores = 2 // PLACEHOLDER`, and `apiMinReplicas = 1`, but omits the model and IoT Hub quota parameters (`C7`, `C8`, `C9`). Declaring the full region and quota parameter set explicitly in all three `.bicepparam` files (marking unapproved pilot quota choices with `// PLACEHOLDER` comments) eliminates implicit defaults disguised as reviewed environment choices.
* **Mechanical guard & CLI bypasses on recorded check references (`Q2`)**:
  * **Gap 3 (Bicep guard accepts whitespace, placeholders, assumption tokens, and bare UUIDs)**: `infra/main.bicep:206-208` evaluates `regionCheckMustBeRecorded: !empty(regionCheckReference) ? 'ok' : ''`, `quotaCheckMustBeRecorded: !empty(quotaCheckReference) ? 'ok' : ''`, and `deploymentLocationsMustBeSelected: !empty(location) && !empty(sqlLocation) ? 'ok' : ''` (`C1`). In ARM/Bicep, `!empty('   ')` is `true`, and strings such as `'PLACEHOLDER'`, `'TBD'`, `'TODO'`, `'assumed'`, `'assumption'`, `'unverified'`, `'pending'`, `'unknown'`, `'none'`, `'n/a'`, `'example.invalid'`, or a bare 36-char subscription/tenant UUID (explicitly forbidden by `@description('... never put subscription or tenant IDs here.')` at `main.bicep:29-33`) all pass `!empty(...)` (`C1`, `W2`). Likewise `sqlLocation = '   '` or `'placeholder'` passes `deploymentLocationsMustBeSelected`.
  * **Gap 4 (CLI helper check-reference validation gap)**: `infra/scripts/pipeline.py:130-154` checks `OVERRIDES` only for empty or uppercase `"PLACEHOLDER"` (and `example.invalid` on `alertEmail`), missing case-insensitive placeholder/assumption tokens and embedded subscription/tenant UUIDs in `regionCheckReference` / `quotaCheckReference` (`C11`). `infra/scripts/deploy.py` performs no check-reference or location validation when `--parameter` overrides (`regionCheckReference=...`, `quotaCheckReference=...`, `location=...`, `sqlLocation=...`) are passed (`C10`).
* **Architecture & runbook documentation gaps (`Q3`)**:
  * **Gap 5 (`docs/architecture/` missing environment/region/quota specification + `infra/README.md` drift)**:
    * `docs/architecture/README.md` indexes nine architecture notes (`cutover-evidence-pack.md`, `hosting-cost-comparison.md`, etc.) and has no architecture specification for the three-environment strategy (`dev`, `test`, `pilot`), region/quota parameter contract, fail-closed guards, recorded check ledger (`R1`-`R17`), and offline vs live verification boundaries (`C13`).
    * `infra/README.md` `## Environments` table (`lines 985-1006`) has two stale rows that contradict compiled Bicep: `Service SKUs` claims `pilot` uses `SQL GP_S_Gen5/2 max vCores` (same as `dev`/`test`), whereas `infra/main.pilot.example.bicepparam:19` sets `sqlTier = 'provisioned'`, which `infra/modules/sql.bicep:28` compiles to `GP_Gen5` (provisioned, no auto-pause); and `Model SKU/quota inputs (modelDeployments)` claims `standard: gpt-4.1-mini; capable: gpt-4.1; both version 2025-04-14, GlobalStandard, capacity 30`, whereas `infra/main.bicep:116-142` defaults to a single `standard` deployment (`gpt-4.1-nano`, `2025-04-14`, `GlobalStandard`, capacity `1`) backing both logical tiers unless `modelDeployments` is explicitly overridden (`C1`, `C3`, `C9`, `C12`).

### Wave 3: Contrarian

* **Contrarian check 1 (`test_bicep_policy.py` custom ARM expression evaluator)**:
  * `infra/tests/test_bicep_policy.py:125-169` evaluates compiled ARM expressions from `main.bicep` using a restricted Python `scope` (`if_`, `or_`, `and_`, `not_`, `equals`, `greaterOrEquals`, `lessOrEquals`, `empty`, `trim`, `greater`, `coalesce`, `length`, `split`, `toLower`, `take`, `skip`, `reduce`, etc.) and a single hardcoded lambda translation: `lambda('remaining', 'digit', replace(lambdaVariables('remaining'), lambdaVariables('digit'), ''))` (originally added for `public-edge-existing.bicep:29`) (`C15`, `C16`).
  * Any Bicep expression added to `main.bicep` `parameter-guard` MUST compile exclusively to functions in that `scope` (and if using `reduce`, must use exact lambda parameter names `(remaining, digit) => replace(remaining, digit, '')`). Furthermore, `test_bicep_policy.py` passes synthetic valid strings `"synthetic-region-check"` and `"synthetic-quota-check"` (`lines 1217-1218`, `2401-2402`), `test_deploy.py:405-407` passes `"reviewed-region-record"` and `"reviewed-quota-record"`, and `test_pipeline.py` passes `"synthetic-reviewed-reference"`. Our forbidden-token list (`placeholder`, `todo`, `tbd`, `assumed`, `assumption`, `unverified`, `pending`, `unknown`, `example.invalid`, plus exact `'none'`, `'n/a'`, `'na'`, `'skip'` and 36-char hex UUID detection) rejects assumptions/placeholders/UUIDs while accepting all synthetic test strings and real dated document/check references (`C15`).
* **Contrarian check 2 (`containerapps.bicep` replica expressions and `governance` `.bicepparam` assertions)**:
  * `infra/tests/test_bicep_policy.py:768`, `test_resident_demo_deploy.py:182`, and `test_container_hosting_completeness.py:115` assert the exact string `maxReplicas: enablePublicSimulationLane ? 1 : 4` (and `maxReplicas: 5` on `agents`) (`C15`, `C18`). Therefore `containerapps.bicep` replica ceilings must remain untouched rather than refactored into new parameter names.
  * `infra/tests/test_governance.py:55-73` and `test_bicep_policy.py:900-947` assert exact lines in `main*.bicepparam`, including `param regionCheckReference = '' // PLACEHOLDER`, `param quotaCheckReference = '' // PLACEHOLDER`, `param location = ''` (for pilot) / `'uksouth'` (for dev/test), every `= ''` line carrying `PLACEHOLDER`, and exact failing guard sets `{"regionCheckMustBeRecorded", "quotaCheckMustBeRecorded"}` for `dev`/`test` and `+ {"deploymentLocationsMustBeSelected", "primaryLocationMustBeUKSouth"}` for `pilot` (`C15`, `C17`). Adding explicit non-empty quota parameters (`sqlVCores`, `apiMinReplicas`, `chatModel*`, `iotHub*`) to the `.bicepparam` files preserves every assertion in `test_governance.py` and `test_bicep_policy.py`.
* **Contrarian check 3 (`ruff` 0.17.3 default settings vs hosted `src-ci.yml` `--isolated` settings)**:
  * `.github/workflows/src-ci.yml:241-248` runs `ruff==0.17.1` with `--isolated --select E,F,I,B,UP --target-version py312 --line-length 100` on an explicit list of `infra/` files (`C19`). Running bare `python3 -m ruff check infra` in this environment uses Ruff `0.17.3` default settings across all `infra/` files and surfaces 112 pre-existing warnings (`SIM117`, `FURB167`, `EXE001`, etc.) in unrelated scripts/tests (`credential_arm.py`, `setup-entra.py`, etc.). Editing 30+ unrelated `infra/` files would violate minimal-scope rules and create cross-worktree merge conflicts. Instead, every Python file created or touched in this task (`infra/tests/test_environment_quota_parameters.py`, `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, `infra/tests/test_deploy.py`, `infra/tests/test_pipeline.py`) must pass BOTH bare `python3 -m ruff check <files>` (`0` issues under Ruff 0.17.3 defaults) AND `src-ci.yml`'s `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` + `ruff format --isolated --line-length 100 --check`, while the pre-existing untouched `infra/` output of bare `python3 -m ruff check infra` is recorded transparently in validation evidence.
* **Contrarian check 4 (Honesty boundary on Issue `#137`)**:
  * Deterministic parameterization, fail-closed reference/quota guards, recorded read-only check ledger validation (`R1`-`R17`), and architecture documentation deliver the repository-verifiable engineering contract for Criterion 4, but do NOT fabricate live Azure quota reservations, private pilot subscription binding, or named human sign-off (`W1`, `W2`, `C14`). Commit messages and documentation must use `Refs #137` and keep live Azure/human prerequisites explicit.

## Evidence Log

| ID | Source (`path:line` or URL) | Finding |
|----|-----------------------------|---------|
| `W1` | `https://github.com/jmservera/ama/issues/137#issuecomment-6192754703` (retrieved 2026-11-15; posted 2026-10-15) | Owner selected pilot primary region `uksouth` and subscription owner `@jmservera`; did not select `sqlLocation`, availability zones, or SKU/quota sizing. |
| `W2` | `https://github.com/jmservera/ama/issues/137` (retrieved 2026-11-15) | Four of five checklist criteria ticked; `- [ ] Region and quota choices are parameters with recorded checks, not assumptions` remains open; closure audits highlight unauthenticated nonempty reference strings and remaining live subscription/quota unknowns. |
| `C1` | `infra/main.bicep:10-35,95-145,198-235` | Defines region (`location`, `sqlLocation`, `zoneRedundant`), check-reference (`regionCheckReference`, `quotaCheckReference`), and quota/SKU parameters; `sqlVCores` and `monthlyBudget` lack `@minValue`/`@maxValue`; `parameter-guard` uses `!empty(...)` without trimming or placeholder/assumption/UUID rejection. |
| `C2` | `infra/modules/guard.bicep:1-45,130-165` | Enforces `@minLength(1)` fail-closed string checks across all 28 guard parameters before dependent modules deploy. |
| `C3` | `infra/modules/sql.bicep:17-60` | Consumes `location` (`sqlLocation`), `endpointLocation` (`location`), `sqlTier` (`GP_S_Gen5` vs `GP_Gen5`), `sqlVCores` (unbounded `int`), `zoneRedundant`, and backup retention/redundancy. |
| `C4` | `infra/modules/foundry.bicep:14-68` | Loops over `modelDeployments` (`@minLength(1)`) setting `sku.name` and `sku.capacity` per deployment in `location`. |
| `C5` | `infra/modules/iothub.bicep:9-45` | Consumes `iotHubSku` (`B1`), `iotHubUnits` (`1..1`), `retentionDays` (`1..7`), and `location`. |
| `C6` | `infra/modules/containerapps.bicep:35-85,235-245,355-375,565-590` | Consumes `location`, `zoneRedundant`, `apiMinReplicas` (`0..4`), Consumption workload profile, `maxReplicas: enablePublicSimulationLane ? 1 : 4` (API), `0..5` (`agents`), `0..2` (`importJob`). |
| `C7` | `infra/main.bicepparam:1-19` | `dev` parameter set (`uksouth`/`uksouth`, `serverless`, `regionCheckReference = '' // PLACEHOLDER`, `quotaCheckReference = '' // PLACEHOLDER`); omits explicit `sqlVCores`, `apiMinReplicas`, model, and IoT quota parameters. |
| `C8` | `infra/main.test.bicepparam:1-19` | `test` parameter set (`uksouth`/`uksouth`, `production` profile, `serverless`); omits explicit `sqlVCores`, `apiMinReplicas`, model, and IoT quota parameters. |
| `C9` | `infra/main.pilot.example.bicepparam:1-25` | Non-deployable `pilot` example (`location = '' // PLACEHOLDER`, `sqlLocation = '' // PLACEHOLDER`, `sqlTier = 'provisioned'`, `sqlVCores = 2 // PLACEHOLDER`, `apiMinReplicas = 1`, `enableLocks = true`); omits explicit model and IoT quota parameters. |
| `C10` | `infra/scripts/deploy.py:1-215` | Operator CLI enforces `--resource-group ama` and image resolution but does not reject placeholder/assumption/UUID overrides for `regionCheckReference`, `quotaCheckReference`, `location`, or `sqlLocation`. |
| `C11` | `infra/scripts/pipeline.py:125-160` | Hosted pipeline helper checks `OVERRIDES` for empty or uppercase `"PLACEHOLDER"` and `[a-z][a-z0-9]+` locations, but does not reject case-insensitive assumption/placeholder tokens (`assumed`, `tbd`, `todo`, `unverified`, etc.) or embedded UUIDs in check references. |
| `C12` | `infra/README.md:957-1145` | `## Environments` table has stale `Service SKUs` (claiming pilot uses `GP_S_Gen5` instead of `GP_Gen5` from `sqlTier = 'provisioned'`) and stale `modelDeployments` (`gpt-4.1-mini`/`gpt-4.1` capacity `30` instead of `gpt-4.1-nano` capacity `1`); `lines 1044-1145` hold the `R1`-`R17` dated read-only capability/quota ledger. |
| `C13` | `docs/architecture/README.md:1-38` | Architecture index has no document or section specifying the `dev`/`test`/`pilot` environment strategy, region/quota parameter contract, mechanical guards, and recorded check ledger. |
| `C14` | `docs/adrs/0002-pilot-readiness-architecture.md:1092-1114` | Records owner's 2026-10-15 `uksouth`/`@jmservera` selection and the 2026-10-18/19 read-only capability/quota boundary. |
| `C15` | `infra/tests/test_bicep_policy.py:125-169,768,895-947,1190-1230,2385-2455,2720-2750` | Custom ARM `evaluate()` supports fixed function scope and exact `(remaining, digit) => replace(remaining, digit, '')` lambda; locks synthetic check strings (`synthetic-region-check`, `synthetic-quota-check`), `.bicepparam` failing guard sets, and `containerapps` `maxReplicas`. |
| `C16` | `infra/public-edge-existing.bicep:29` | Canonical Bicep `reduce(split('0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f,-', ','), ..., (remaining, digit) => replace(remaining, digit, ''))` pattern already supported by `test_bicep_policy.py`. |
| `C17` | `infra/tests/test_governance.py:44-78` | Asserts `NON-DEPLOYABLE EXAMPLE`, exact `param regionCheckReference = '' // PLACEHOLDER` and `param quotaCheckReference = '' // PLACEHOLDER` lines, and no secret-like parameter names across all three `.bicepparam` files. |
| `C18` | `infra/tests/test_container_hosting_completeness.py:115` | Locks `maxReplicas: enablePublicSimulationLane ? 1 : 4` in `containerapps.bicep`. |
| `C19` | `.github/workflows/src-ci.yml:229-250` | Compiles/lints all `infra/*.bicep` and `infra/modules/*.bicep` with `az bicep`, discovers all `infra/tests`, and runs `ruff --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` on targeted `infra/` Python files. |

## Synthesis and Convergence Recommendation

* **Selected approach**:
  1. **Harden Bicep region/quota bounds and recorded-check guards (`infra/main.bicep`, `infra/modules/sql.bicep`, `infra/modules/guard.bicep`)**:
     * Add `@minValue(1) @maxValue(80)` on `sqlVCores` in `infra/main.bicep` and `infra/modules/sql.bicep`, and `@minValue(1)` on `monthlyBudget` in `infra/main.bicep`.
     * Strengthen `regionCheckMustBeRecorded`, `quotaCheckMustBeRecorded`, and `deploymentLocationsMustBeSelected` in `infra/main.bicep` (using `trim`, `toLower`, `split`, `length`, and the exact `(remaining, digit) => replace(remaining, digit, '')` `reduce` form supported by `test_bicep_policy.evaluate`) so whitespace-only strings, placeholder/assumption tokens (`placeholder`, `todo`, `tbd`, `assumed`, `assumption`, `unverified`, `pending`, `unknown`, `example.invalid`, plus exact `none`, `n/a`, `na`, `skip`), and bare 36-char subscription/tenant UUIDs fail closed in template validation, and clarify `@description` metadata in `infra/modules/guard.bicep`.
  2. **Make quota choices explicit across `dev`, `test`, and `pilot` parameter sets (`infra/main.bicepparam`, `infra/main.test.bicepparam`, `infra/main.pilot.example.bicepparam`)**:
     * Explicitly set `sqlVCores`, `apiMinReplicas`, `chatModelName`, `chatModelVersion`, `chatModelSku`, `chatModelCapacity`, `iotHubSku`, and `iotHubUnits` in `main.bicepparam`, `main.test.bicepparam`, and `main.pilot.example.bicepparam` (preserving existing values and adding `// PLACEHOLDER` annotations to unapproved pilot capacity inputs in `main.pilot.example.bicepparam`), while keeping `regionCheckReference = '' // PLACEHOLDER`, `quotaCheckReference = '' // PLACEHOLDER`, and pilot `location = '' // PLACEHOLDER` / `sqlLocation = '' // PLACEHOLDER` non-deployable by default.
  3. **Align CLI recorded-check & region validation (`infra/scripts/pipeline.py`, `infra/scripts/deploy.py`)**:
     * Add deterministic validation rejecting empty/whitespace values, case-insensitive placeholder/assumption tokens, and embedded UUIDs in `regionCheckReference` / `quotaCheckReference` (plus Azure region slug syntax `[a-z][a-z0-9]+` for `location` / `sqlLocation`) across `pipeline.py` environment overrides and `deploy.py` `--parameter` overrides.
  4. **Author canonical architecture specification in `docs/architecture/` and reconcile `infra/README.md` (`docs/architecture/environment-region-quota-strategy.md`, `docs/architecture/README.md`, `infra/README.md`, `.github/workflows/src-ci.yml` ruff file list if needed — skip workflow edits to stay within Focused tier!)**:
     * Create `docs/architecture/environment-region-quota-strategy.md` documenting the `dev`/`test`/`pilot` parameter matrix, every region parameter (including separate `sqlLocation` and standalone `iot-hub-live.bicep`, `resident-demo.bicep`, `resident-assistant.bicep` `swedencentral` opt-in boundary), every quota-bearing parameter and compile-time bound, mechanical Bicep + CLI recorded-check guards, the recorded `R1`-`R17` read-only check ledger with explicit `Observed` / `Unknown` / `Blocked` honesty states, and the offline vs live acceptance boundary. Index it in `docs/architecture/README.md`.
     * Fix the stale `Service SKUs` (`GP_Gen5` provisioned in pilot example vs `GP_S_Gen5` serverless in `dev`/`test`) and `modelDeployments` (`gpt-4.1-nano` capacity `1` default) rows in `infra/README.md` and link to `docs/architecture/environment-region-quota-strategy.md`.
     * Keep `.github/workflows/` untouched so the change stays strictly within the Focused validation tier per repository instructions.
  5. **Deliver comprehensive deterministic test suite (`infra/tests/test_environment_quota_parameters.py`)**:
     * Compile `main.bicep`, child modules, standalone regional templates, and all three `.bicepparam` files via `az bicep`; verify every region and quota parameter's presence, type, `@allowed`/`@minValue`/`@maxValue`/`@minLength` bounds, module forwarding, and explicit declaration across `dev`/`test`/`pilot`; test `parameter-guard` rejection of empty, whitespace, placeholder, assumption (`assumed`, `assumption`, `tbd`, `todo`, `unverified`, `pending`, `unknown`, `none`, `n/a`, `skip`, `example.invalid`), and UUID check references plus blank/whitespace/placeholder `location`/`sqlLocation`; perform negative ARM template mutation tests verifying guard tamper detection; test `deploy.py` and `pipeline.py` check-reference/location validation; and verify parity between compiled Bicep parameter sets, `docs/architecture/environment-region-quota-strategy.md`, and `infra/README.md` (`## Environments` + `R1`-`R17` recorded-check ledger).
* **Alternatives rejected**:
  * *Hardcoding recorded check IDs inside committed `.bicepparam` files*: Rejected because committed `.bicepparam` files must stay non-deployable (`PLACEHOLDER`) until an authorized operator binds a private subscription copy with fresh region/quota verification (`test_governance.py:66-67`, `test_bicep_policy.py:923-940`).
  * *Editing `.github/workflows/src-ci.yml` or 30+ unrelated `infra/` Python files*: Rejected because workflow edits escalate validation tier rules and sweeping unrelated `infra/` edits create merge conflicts across parallel worktrees.

## Unresolved Decisions, Risks, and Potential Further Research

* Live Azure subscription binding, fresh selected-region SQL/model/Container Apps/IoT quota headroom queries (`R5`, `R7`, `R11`, `R14`-`R17`), availability-zone confirmation, and named human sizing/cost approval remain external operational gates before completing a private pilot `.bicepparam` copy.
* No unresolved codebase uncertainties block `rpi-plan`.

## Artifact Self-Check

* [x] Research brief, parameters, extension registry, participation, direction controls, questions, prior-knowledge gate, three-wave cycle (`Wider`, `Deeper`, `Contrarian`), evidence log (`C1`-`C19`, `W1`-`W2`), and convergence recommendation recorded.
* [x] Zero source edits performed during `rpi-research`.
* [x] Planning Readiness set to `Ready` and Research disposition set to `executed`.
