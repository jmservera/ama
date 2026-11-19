<!-- markdownlint-disable-file -->
# RPI Phase Details: Environment Strategy, Region and Quota Parameterization, Recorded Checks, and Architecture Documentation (Issue #137)

## Metadata

* Task ID: issue-137
* Task slug: infra-137-env-quotas
* Related plan: .copilot-tracking/plans/2026-11-15/infra-137-env-quotas-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/infra-137-env-quotas-research.md, docs/adrs/0002-pilot-readiness-architecture.md, infra/README.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Bicep Region/Quota Bounds, Parameter Sets, and Recorded-Check Guards | Complete | P01, P01-T01, P01-T02 |
| P02 | Architecture Documentation and Runbook Parity | Complete | P02, P02-T01 |
| P03 | Deterministic Verification Suite, Focused Validation, and Local Commit | Complete | P03, P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Bicep Region/Quota Bounds, Parameter Sets, and Recorded-Check Guards

### Context

`infra/main.bicep` defines region (`location`, `sqlLocation`, `zoneRedundant`), recorded-check reference (`regionCheckReference`, `quotaCheckReference`), and quota-bearing parameters (`sqlTier`, `sqlVCores`, `sqlAutoPauseDelayMinutes`, `apiMinReplicas`, `chatModel*`, `modelDeployments`, `iotHub*`, `monthlyBudget = 300`), guarded by `infra/modules/guard.bicep` (`parameter-guard`, 29 boolean-equivalent `minLength(1)` parameters). Research (`C1`, `C3`, `C7`-`C11`, `C15`-`C17`) and plan critique (`PC-001`-`PC-004`) identified four actionable gaps:
1. `sqlVCores` (`infra/main.bicep`) / `maxVCores` (`infra/modules/sql.bicep`) and `monthlyBudget` (`infra/main.bicep`) lack numeric bounds (`@minValue`/`@maxValue`).
2. `regionCheckMustBeRecorded` and `quotaCheckMustBeRecorded` only check `!empty(...)`, accepting whitespace-only strings, placeholder/assumption words (`placeholder`, `todo`, `tbd`, `assumed`, `assumption`, `unverified`, `pending`, `unknown`, `none`, `n/a`, `na`, `skip`, `example.invalid`), and bare 36-character `8-4-4-4-12` hex UUIDs; `deploymentLocationsMustBeSelected` accepts whitespace-only, malformed, UUID, or assumption-word `sqlLocation` inputs.
3. While all three `.bicepparam` files already declare `apiMinReplicas = 0`, `infra/main.bicepparam` (`dev`) and `infra/main.test.bicepparam` (`test`) omit explicit `sqlVCores`, `sqlAutoPauseDelayMinutes`, `modelDeployments`, `iotHubSku`, `iotHubUnits`, `iotHubRetentionDays`, `iotHubMonthlyCost`, and `monthlyBudget`, and `infra/main.pilot.example.bicepparam` (`pilot`) omits explicit `modelDeployments`, `iotHubSku`, `iotHubUnits`, `iotHubRetentionDays`, `iotHubMonthlyCost`, and `monthlyBudget` (subject to `test_bicep_policy.py:759-760` forbidding `"chat"` in `dev`/`pilot` and `test_sql_tier.py:48` forbidding `"AutoPause"` in `pilot`).
4. `infra/scripts/pipeline.py` only checks uppercase `"PLACEHOLDER"` on `OVERRIDES` (missing word-bounded assumption tokens, embedded UUIDs, `location == "uksouth"`, and lowercase assumption slugs on `sqlLocation`), and `infra/scripts/deploy.py` performs no check-reference or region validation on `--parameter` overrides.

### Intent

Eliminate implicit quota omissions, unbounded numeric capacity inputs, and assumption/placeholder/UUID bypasses across Bicep templates, environment `.bicepparam` sets, and Python deployment helpers while maintaining 100% compatibility with `test_bicep_policy.py`, `test_governance.py`, and `test_sql_tier.py`.

### Boundaries

* Included: `infra/main.bicep`, `infra/modules/sql.bicep`, `infra/modules/guard.bicep`, `infra/main.bicepparam`, `infra/main.test.bicepparam`, `infra/main.pilot.example.bicepparam`, `infra/scripts/pipeline.py`, `infra/scripts/deploy.py`.
* Excluded: `infra/modules/containerapps.bicep` replica expressions (`maxReplicas: enablePublicSimulationLane ? 1 : 4` and `maxReplicas: 5`), existing `infra/tests/` files (`0` edits), and `.github/workflows/`.

### Likely Targets

* `infra/main.bicep` and `infra/modules/sql.bicep`: `@minValue(1) @maxValue(80)` on `sqlVCores` (`main.bicep`) and `maxVCores` (`modules/sql.bicep`), `@minValue(1)` on `monthlyBudget` (`main.bicep`), and delimiter-tokenized `validRegionCheck` / `validQuotaCheck` / `validSqlLocation` variables feeding `parameter-guard` while keeping `"Empty means"` in `main.bicep:189`.
* `infra/modules/guard.bicep`: Clarify `@description('... Empty means ...')` strings on `regionCheckMustBeRecorded`, `quotaCheckMustBeRecorded`, and `deploymentLocationsMustBeSelected` across the 29 existing guard parameters (retaining exact `"Empty means"` substring required by `test_bicep_policy.py:2391`).
* `infra/main.bicepparam`, `infra/main.test.bicepparam`, `infra/main.pilot.example.bicepparam`: Retain single `apiMinReplicas = 0` in place and add explicit declarations for `sqlVCores`, `modelDeployments`, `iotHubSku`, `iotHubUnits`, `iotHubRetentionDays`, `iotHubMonthlyCost`, and `monthlyBudget` (plus serverless-only `sqlAutoPauseDelayMinutes = 60` in `dev` and `test`).
* `infra/scripts/pipeline.py` and `infra/scripts/deploy.py`: Fail-closed, value-redacted validation helpers for `regionCheckReference`, `quotaCheckReference`, `location`, and `sqlLocation`.

### Dependencies

* None.

### Validation Expectations

* `az bicep build` and `az bicep lint` pass on `infra/main.bicep`, `infra/modules/sql.bicep`, and `infra/modules/guard.bicep`; `az bicep build-params` passes on all three `.bicepparam` files.
* `test_bicep_policy.py`, `test_governance.py`, `test_sql_tier.py`, `test_deploy.py`, and `test_pipeline.py` pass with zero regressions, and `mypy --strict` passes on `pipeline.py` and `deploy.py`.

### Completion Evidence

* Compiled ARM expressions and Python helper checks reject empty, whitespace, placeholder, assumption, skip-word, and UUID check references and invalid locations while accepting valid synthetic and dated check references.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Harden Bicep quota bounds, `.bicepparam` quota declarations, and `parameter-guard` check-reference/location validation

#### Context

`infra/tests/test_bicep_policy.py:125-169` evaluates `main.bicep` variables and `parameter-guard` expressions via a restricted Python `scope` (`trim`, `toLower`, `empty`, `equals`, `length`, `split`, `take`, `skip`, `replace`, `contains`, `reduce`, etc.) where `reduce` supports ONLY the exact lambda signature `(remaining, digit) => replace(remaining, digit, '')` (note `filter` and `endsWith` are NOT in `scope`) (`C15`, `C16`, `PC-003`, `PC-004`). Designing our guard variables strictly around `replace`, `split`, `contains`, `take`, `skip`, `length`, `trim`, `toLower`, and `(remaining, digit) => replace(remaining, digit, '')` guarantees native evaluation in both Azure ARM and `test_bicep_policy.py`:

* Define `uuidHexCharacters = split('0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f,-', ',')` and `regionSlugCharacters = split('a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,0,1,2,3,4,5,6,7,8,9,-', ',')`.
* Normalize `normalizedRegionCheck = toLower(trim(regionCheckReference))` and `normalizedQuotaCheck = toLower(trim(quotaCheckReference))`.
* Tokenize each check reference into delimited words using nested `replace` + `split(..., ' ')` across `'-'`, `'_'`, `'/'`, `'#'`, `'.'`, `':'`, `','`, `';'`, `'('`, `')'` (`regionCheckWords`, `quotaCheckWords`), avoiding false positives on legitimate repository words such as `'spending'`, `'appending'`, or `'jtbd'` (`PC-003`).
* Require for each check reference (`regionCheckValid`, `quotaCheckValid`):
  1. `!empty(normalizedCheck)`
  2. Substring exclusions: `!contains(normalizedCheck, 'placeholder') && !contains(normalizedCheck, 'example.invalid') && !contains(normalizedCheck, 'n/a') && !contains(normalizedCheck, '00000000-0000-0000-0000-000000000000')`
  3. Delimited-word exclusions: `!contains(checkWords, 'todo') && !contains(checkWords, 'tbd') && !contains(checkWords, 'assumed') && !contains(checkWords, 'assumption') && !contains(checkWords, 'unverified') && !contains(checkWords, 'pending') && !contains(checkWords, 'unknown') && !contains(checkWords, 'none') && !contains(checkWords, 'na') && !contains(checkWords, 'skip')`
  4. Not a bare 36-char `8-4-4-4-12` UUID: `!(length(normalizedCheck) == 36 && length(split(normalizedCheck, '-')) == 5 && take(skip(normalizedCheck, 8), 1) == '-' && take(skip(normalizedCheck, 13), 1) == '-' && take(skip(normalizedCheck, 18), 1) == '-' && take(skip(normalizedCheck, 23), 1) == '-' && empty(reduce(uuidHexCharacters, normalizedCheck, (remaining, digit) => replace(remaining, digit, ''))))`
* Normalize `normalizedLocation = toLower(trim(location))` and `normalizedSqlLocation = toLower(trim(sqlLocation))` with `sqlLocationWords = split(normalizedSqlLocation, '-')`, requiring for `deploymentLocationsMustBeSelected`:
  1. `!empty(normalizedLocation) && location == normalizedLocation`
  2. `!empty(normalizedSqlLocation) && sqlLocation == normalizedSqlLocation && length(normalizedSqlLocation) >= 3`
  3. Leading lowercase ASCII letter and `[a-z0-9-]+` character set without leading, trailing, or double hyphens: `contains('abcdefghijklmnopqrstuvwxyz', take(normalizedSqlLocation, 1)) && !contains(split(normalizedSqlLocation, '-'), '') && empty(reduce(regionSlugCharacters, normalizedSqlLocation, (remaining, digit) => replace(remaining, digit, '')))` (preserving `'uksouth'`, `'ukwest'`, `'offline-region'`, and `'offline-sql-region'`)
  4. Not a bare `8-4-4-4-12` UUID and free of `'placeholder'` or forbidden assumption/skip words (`'todo'`, `'tbd'`, `'assumed'`, `'assumption'`, `'unverified'`, `'pending'`, `'unknown'`, `'none'`, `'na'`, `'skip'`) in `sqlLocationWords`.
* Preserve all `test_governance.py`, `test_bicep_policy.py`, and `test_sql_tier.py` `.bicepparam` invariants (`PC-001`, `PC-002`):
  * Keep exact `param regionCheckReference = '' // PLACEHOLDER` and `param quotaCheckReference = '' // PLACEHOLDER` lines, keep every `= ''` / `example.invalid` / `00000000-` line annotated with `PLACEHOLDER`, and retain the single existing `param apiMinReplicas = 0` in all three files without duplication.
  * Declare `sqlVCores`, `modelDeployments = [{ name: 'standard', model: 'gpt-4.1-nano', version: '2025-04-14', skuName: 'GlobalStandard', capacity: 1 }]`, `iotHubSku = 'B1'`, `iotHubUnits = 1`, `iotHubRetentionDays = 1`, `iotHubMonthlyCost = 60`, and `monthlyBudget = 300` across `main.bicepparam` (`dev`), `main.test.bicepparam` (`test`), and `main.pilot.example.bicepparam` (`pilot`), plus `sqlAutoPauseDelayMinutes = 60` in serverless `dev` and `test` only.
  * Keep zero occurrences of `"chat"` in `main.bicepparam` and `main.pilot.example.bicepparam` and zero occurrences of `"AutoPause"` in `main.pilot.example.bicepparam`.

#### Intent

Make all region and quota choices bounded, explicit across `dev`/`test`/`pilot`, and mechanically guarded against empty/whitespace/placeholder/assumption/UUID/malformed-slug strings in ARM/Bicep validation.

#### Boundaries

* Included: `infra/main.bicep`, `infra/modules/sql.bicep`, `infra/modules/guard.bicep`, `infra/main.bicepparam`, `infra/main.test.bicepparam`, `infra/main.pilot.example.bicepparam`.
* Excluded: Changing `guard.bicep` parameter names/count (`29`), changing `maxVCores` parameter name in `infra/modules/sql.bicep`, or removing `"Empty means"` from `infra/main.bicep` or any `guard.bicep` `@description`.

#### Likely Targets

* `infra/main.bicep`: Add `@minValue(1)` to `monthlyBudget`, `@minValue(1) @maxValue(80)` to `sqlVCores`, add normalized/tokenized check and `sqlLocation` guard variables, and wire them into `guard.params`.
* `infra/modules/sql.bicep`: Add `@minValue(1) @maxValue(80)` to `maxVCores`.
* `infra/modules/guard.bicep`: Update `@description` text for `deploymentLocationsMustBeSelected`, `regionCheckMustBeRecorded`, and `quotaCheckMustBeRecorded` while keeping `"Empty means"` intact.
* `infra/main.bicepparam`, `infra/main.test.bicepparam`, `infra/main.pilot.example.bicepparam`: Add explicit quota parameters without `"chat"` in `dev`/`pilot` or `"AutoPause"` in `pilot`.

#### Dependencies

* None.

#### Validation Expectations

* `az bicep build` and `az bicep lint` succeed on `main.bicep`, `modules/sql.bicep`, and `modules/guard.bicep`; `az bicep build-params` succeeds on all three `.bicepparam` files.

#### Completion Evidence

* `test_bicep_policy.py`, `test_governance.py`, and `test_sql_tier.py` pass unchanged, and new guard expressions reject whitespace, placeholder, assumption, skip, malformed-slug, and UUID inputs while accepting valid anchors (`spending`, `jtbd`) and `'offline-sql-region'`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Enforce recorded-check and region-slug validation in `infra/scripts/pipeline.py` and `infra/scripts/deploy.py`

#### Context

In `infra/scripts/pipeline.py`, `parameters()` validates `OVERRIDES` from `DEPLOY_PARAMETERS`. Adding focused `validate_check_reference(key: str, value: str) -> None` and region-override checks (`PC-003`, `PC-004`):
* Rejects `regionCheckReference` and `quotaCheckReference` values matching word-bounded assumption/placeholder regex `r"(?i)(?:placeholder|example\.invalid|n/a|\b(?:todo|tbd|assumed|assumption|unverified|pending|unknown|none|na|skip)\b)"` or containing any bare or embedded UUID `r"(?i)\b[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}\b"`.
* Enforces `overrides["location"] == "uksouth"`, requires `[a-z][a-z0-9]+` on `location` and `sqlLocation`, and rejects `sqlLocation` matching the forbidden placeholder/assumption word set (`placeholder`, `todo`, `tbd`, `assumed`, `assumption`, `unverified`, `pending`, `unknown`, `none`, `na`, `skip`).
* Never echoes the raw rejected parameter `value` in `PipelineError` messages so pasted tenant/subscription UUIDs or tokens cannot leak to CI stderr.

In `infra/scripts/deploy.py`, adding `validate_parameter_overrides(parameters: list[str]) -> None` iterates over every `"NAME=VALUE"` entry in `args.parameter` (without collapsing duplicates via `dict(...)` and without reading `--parameters` from disk so `test_deploy.py:79` mock paths continue to pass) before calling Azure CLI:
* If `name` is `regionCheckReference` or `quotaCheckReference`, enforces non-empty/non-whitespace, no placeholder/word-bounded assumption token, and no bare or embedded UUID (raising `DeploymentError` naming only `name`).
* If `name` is `location`, requires exact `"uksouth"` (raising `DeploymentError` naming only `name`).
* If `name` is `sqlLocation`, requires `[a-z][a-z0-9]+` and not in the forbidden placeholder/assumption word set (raising `DeploymentError` naming only `name`).
Existing `test_deploy.py` calls that omit `regionCheckReference` or pass `"regionCheckReference=reviewed-region-record"` continue to work unchanged.

#### Intent

Ensure both the hosted OIDC pipeline (`pipeline.py`) and the operator CLI (`deploy.py`) fail closed on assumed, placeholder, whitespace, or UUID-leaking check references and malformed location overrides before invoking `az deployment group`.

#### Boundaries

* Included: `infra/scripts/pipeline.py`, `infra/scripts/deploy.py`.
* Excluded: Changing CLI flags or breaking existing `test_pipeline.py` / `test_deploy.py` call signatures.

#### Likely Targets

* `infra/scripts/pipeline.py`: Add check-reference token + embedded-UUID validation inside `parameters()`.
* `infra/scripts/deploy.py`: Add `validate_parameter_overrides(args.parameter)` called at the start of `main()`'s `try:` block before `az_json(...)`.

#### Dependencies

* None.

#### Validation Expectations

* `python3 -m unittest infra/tests/test_pipeline.py infra/tests/test_deploy.py -q`, `mypy --strict infra/scripts/pipeline.py infra/scripts/deploy.py`, and `ruff` checks pass with zero errors.

#### Completion Evidence

* Unit tests in `infra/tests/test_environment_quota_parameters.py` verify `PipelineError` and `DeploymentError` (exit code `1`) on placeholder, assumption, whitespace, UUID, and invalid-region inputs.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Architecture Documentation and Runbook Parity

### Context

The prompt requires region and quota choices and their recorded checks to be documented in `docs/architecture/`. Currently `docs/architecture/README.md` has no environment/region/quota specification (`C13`), and `infra/README.md` (`## Environments`, lines 985-1006) contains two stale rows (`Service SKUs` claiming pilot uses serverless `GP_S_Gen5` instead of provisioned `GP_Gen5`, and `modelDeployments` claiming `gpt-4.1-mini`/`gpt-4.1` capacity `30` instead of `gpt-4.1-nano` capacity `1`) (`C12`).

### Intent

Establish a single, truthful, machine-verifiable architecture specification in `docs/architecture/environment-region-quota-strategy.md` (indexed in `docs/architecture/README.md`) and align `infra/README.md` with compiled Bicep templates while preserving all historical `R1`-`R17` observation dates and explicit `Unknown`/`Blocked` governance boundaries.

### Boundaries

* Included: `docs/architecture/environment-region-quota-strategy.md` (new), `docs/architecture/README.md`, `infra/README.md`.
* Excluded: `docs/case_study_48_original.md`, `docs/reference/memory.md`, or placing any `.copilot-tracking/` path in `docs/` or `infra/` files.

### Likely Targets

* `docs/architecture/environment-region-quota-strategy.md`: YAML frontmatter (`title`, `description`, `author`, `ms.date: 2026-11-15`), no H1, `*` unordered lists, ASCII punctuation (no em dashes, no bolded-prefix list items), covering:
  1. Architectural principle: region and quota choices are bounded parameters gated by fail-closed recorded check references, never silent template assumptions.
  2. Environment parameter matrix across `dev` (`infra/main.bicepparam`), `test` (`infra/main.test.bicepparam`), and `pilot` (`infra/main.pilot.example.bicepparam`, non-deployable example), reflecting `apiMinReplicas = 0`, `monthlyBudget = 300`, `iotHubMonthlyCost = 60`, `modelDeployments` (`gpt-4.1-nano`, `2025-04-14`, `GlobalStandard`, capacity `1`), serverless `GP_S_Gen5` (`dev`/`test`, `sqlAutoPauseDelayMinutes = 60`) vs provisioned `GP_Gen5` (`pilot`), and optional `enableDemoChat`-only `chatModel*` parameters.
  3. Complete region parameter and standalone-template boundary catalog (`location`, `sqlLocation` + primary-VNet private endpoint invariant, `zoneRedundant`, plus `iot-hub-live.bicep`, `resident-demo.bicep`, and opt-in `resident-assistant.bicep` `swedencentral` realtime preview boundary).
  4. Complete quota, SKU, and capacity parameter catalog (`sqlTier`, `sqlVCores` / `maxVCores` `1..80`, `sqlAutoPauseDelayMinutes`, `apiMinReplicas` `0..4`, Container Apps fixed replica ceilings, `modelDeployments` / `chatModel*`, `iotHubSku` / `iotHubUnits` / `iotHubRetentionDays` / `iotHubMonthlyCost`, `monthlyBudget >= 1` default `300`).
  5. Mechanical fail-closed guards across the 29 `guard.bicep` controls (`main.bicep`) and Python (`pipeline.py` / `deploy.py`), including word-bounded assumption/skip tokens, `placeholder`/`example.invalid`/`n/a` exclusion, and bare vs embedded subscription/tenant UUID exclusion.
  6. Recorded capability and quota check contract and `R1`-`R17` evidence summary (linking to `infra/README.md` for full REST query paths, attributing the `2026-10-18` snapshot to commit `612cbed7`, keeping `Observed`, `Empty / Unknown`, `Denied`, and `Failed` outcomes honest, and explicitly marking current `GP_Gen5` and `gpt-4.1-nano` defaults as `Unknown` pending fresh `R4`/`R8`/`R9` queries on the target subscription).
  7. Deterministic offline verification (`infra/tests/test_environment_quota_parameters.py`).
* `docs/architecture/README.md`: Add bullet linking `[Environment, region, and quota parameter strategy](environment-region-quota-strategy.md)` without `.copilot-tracking/` references in the added entry.
* `infra/README.md`: Update `Service SKUs` and `Model SKU/quota inputs (modelDeployments)` rows in `## Environments`, note that historical `2026-10-18` (`612cbed7`) `R4`/`R8`/`R9` receipts queried `GP_S_Gen5_2`, `gpt-4.1-mini`, and `gpt-4.1` whereas current pilot `GP_Gen5` and default `gpt-4.1-nano` capacity `1` remain `Unknown` until fresh `R4`/`R8`/`R9` queries are recorded, update the check-reference guard note to reflect rejection of whitespace/placeholder/assumption/UUID values, cross-link `../docs/architecture/environment-region-quota-strategy.md`, and preserve all phrases locked by `test_governance.py:82-84` (`"DoNotEnforce"`, `"until the owner accepts a cost"`) and `test_container_hosting_completeness.py:137-160` (`"Revision rollback:"`, `"not at declared scale"`, `"makes no production"`).

### Dependencies

* P01-T01.

### Validation Expectations

* Markdown links resolve cleanly, style rules (YAML frontmatter, no H1 when `title` present, `*` lists, no em dashes, no bold-prefix list items, no `.copilot-tracking/` references) hold, and `infra/tests/test_environment_quota_parameters.py` verifies parity between the docs and compiled Bicep.

### Completion Evidence

* `docs/architecture/environment-region-quota-strategy.md` created, `docs/architecture/README.md` and `infra/README.md` updated, and automated parity tests green.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Author `docs/architecture/environment-region-quota-strategy.md`, index in `docs/architecture/README.md`, and reconcile `infra/README.md`

#### Context

Repository Markdown conventions forbid H1 headings when YAML frontmatter contains `title`, require `*` for unordered lists in new content, require plain ASCII punctuation without em dashes or bolded-prefix list items, and forbid `.copilot-tracking/` references in production documentation.

#### Intent

Deliver complete, traceable architecture documentation in `docs/architecture/` and fix the two stale rows in `infra/README.md` without altering dated historical query receipts (`R1`-`R17`).

#### Boundaries

* Included: `docs/architecture/environment-region-quota-strategy.md`, `docs/architecture/README.md`, `infra/README.md`.
* Excluded: Rewriting `2026-10-18` historical query receipt outcomes (`R1`-`R17`) in `infra/README.md` (add a current-template note rather than altering historical observations).

#### Likely Targets

* `docs/architecture/environment-region-quota-strategy.md`
* `docs/architecture/README.md`
* `infra/README.md`

#### Dependencies

* P01-T01.

#### Validation Expectations

* Verified by `infra/tests/test_environment_quota_parameters.py` documentation parity and style assertions plus `git diff --check`.

#### Completion Evidence

* All relative Markdown links and parameter/SKU/ledger tables match compiled Bicep templates.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Deterministic Verification Suite, Focused Validation, and Local Commit

### Context

The caller requested deterministic checks in `infra/tests/test_environment_quota_parameters.py` (new file to avoid conflicts with `test_monitoring_alerts.py`), Focused validation (`python3 -m unittest infra/tests/test_environment_quota_parameters.py -q` and `python3 -m ruff check infra && python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_environment_quota_parameters.py`), and a local commit with the Copilot trailer without pushing. Note that `test_bicep_policy.py` imports `zava_forward.orchestrator` / `zava_forward.core`; if those distributions are not installed in system `python3`, we can run `test_environment_quota_parameters.py` directly on system `python3` (zero `zava_forward` runtime dependency needed!) AND verify `test_bicep_policy.py` using a temporary workspace-local `.venv-137-tmp` cleaned up before `git status` and commit.

### Intent

Prove every region/quota parameter, `.bicepparam` set, fail-closed Bicep + CLI check-reference guard, negative template mutation, and architecture/runbook parity invariant deterministically, run single-pass `rpi-review`, and commit cleanly without pushing.

### Boundaries

* Included: `infra/tests/test_environment_quota_parameters.py`, Focused validation commands, `.copilot-tracking/` `2026-11-15` artifacts, and local git commit.
* Excluded: Editing `test_monitoring_alerts.py`, running `tools/rpi-checks.py --all`, or running `git push`.

### Likely Targets

* `infra/tests/test_environment_quota_parameters.py`: Self-contained stdlib `unittest` suite (no `#!/usr/bin/env python3` shebang, zero `zava_forward` imports) compiling Bicep via `az bicep build` / `az bicep build-params` so it runs cleanly under standalone `python3 -m unittest infra/tests/test_environment_quota_parameters.py -q` and bare `python3 -m ruff check infra/tests/test_environment_quota_parameters.py`.

### Dependencies

* P01, P02.

### Validation Expectations

* `python3 -m unittest infra/tests/test_environment_quota_parameters.py -q` exits `0` under system `python3`.
* Full `REQUIRE_AZ_BICEP=1` `infra/tests` discovery (`test_bicep_policy.py`, `test_governance.py`, `test_sql_tier.py`, `test_deploy.py`, `test_pipeline.py`, `test_container_hosting_completeness.py`, `test_iothub_module.py`, `test_monitoring_alerts.py`, and `test_environment_quota_parameters.py`) exits `0` in a workspace-external/cleaned-up Python virtual environment with editable `src/*` (`core`, `agents`, `api`, `orchestrator`, `importer`), `PyYAML==6.0.3`, and `src/api/requirements.txt` installed, removed before `git status` verification (`PC-005`).
* `az bicep build` and `az bicep lint` across `infra/*.bicep` and `infra/modules/*.bicep` exit `0`.
* Bare `python3 -m ruff check infra/tests/test_environment_quota_parameters.py` exits `0`; hosted CI `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_environment_quota_parameters.py infra/scripts/deploy.py infra/scripts/pipeline.py` exits `0`; explicit (unchained) `python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_environment_quota_parameters.py infra/scripts/deploy.py infra/scripts/pipeline.py` exits `0`; `mypy --strict infra/scripts/pipeline.py infra/scripts/deploy.py infra/tests/test_environment_quota_parameters.py` exits `0`; and bare `python3 -m ruff check infra` output is inspected to verify `0` diagnostics on `test_environment_quota_parameters.py` and `0` new diagnostics on modified lines of `deploy.py` and `pipeline.py`.

### Completion Evidence

* Validation table recorded in `.copilot-tracking/changes/2026-11-15/infra-137-env-quotas-changes.md`, post-implementation review recorded in `.copilot-tracking/reviews/logs/2026-11-15/infra-137-env-quotas-review.md`, and clean `git status --short` after local commit.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Create `infra/tests/test_environment_quota_parameters.py` and run Focused validation (`unittest`, `az bicep`, `ruff`, `mypy`)

#### Context

`infra/tests/test_environment_quota_parameters.py` must run deterministically offline under `python3 -m unittest infra/tests/test_environment_quota_parameters.py -q` without network calls, cloud credentials, `zava_forward` imports, or mutating existing test files.

#### Intent

Cover all semantic and negative-mutation checks for Issue `#137` Criterion 4 in `<= 14` focused test methods:
1. Region parameters (`location`, `sqlLocation`, `zoneRedundant`), standalone regional template boundaries (`iot-hub-live.bicep`, `resident-demo.bicep`, `resident-assistant.bicep`), and SQL Private Endpoint primary-region invariant (`endpointLocation: location`).
2. Quota/capacity/SKU parameter definitions, compile-time bounds (`sqlTier`, `sqlVCores` / `maxVCores` `1..80`, `sqlAutoPauseDelayMinutes`, `apiMinReplicas` `0..4`, `chatModel*`, `modelDeployments` `minLength 1`, `iotHubSku`, `iotHubUnits` `1..1`, `iotHubRetentionDays` `1..7`, `iotHubMonthlyCost` `1..700`, `monthlyBudget >= 1` default `300`), 29 `guard.bicep` controls, and child-module forwarding (`sql`, `foundry`, `iothub`, `containerapps`, `monitoring`).
3. Explicit region and quota declarations across `main.bicepparam` (`dev`), `main.test.bicepparam` (`test`), and `main.pilot.example.bicepparam` (`pilot`), including `modelDeployments`, `sqlVCores`, `monthlyBudget`, `iotHub*`, serverless-only `sqlAutoPauseDelayMinutes`, single `apiMinReplicas = 0`, zero `"chat"` in `dev`/`pilot`, zero `"AutoPause"` in `pilot`, plus exact fail-closed guard sets when compiled as committed.
4. Mechanical `parameter-guard` rejection of blank, whitespace-only, `placeholder`/`example.invalid`/`n/a`/`00000000-0000-0000-0000-000000000000` substrings, word-bounded assumption/skip words (`assumed`, `assumption`, `tbd`, `todo`, `unverified`, `pending`, `unknown`, `none`, `na`, `skip`), and bare 36-char `8-4-4-4-12` UUID strings in `regionCheckReference` and `quotaCheckReference`, positive acceptance of valid anchors containing `spending` and `jtbd`, and rejection of blank, whitespace, uppercase, digits-only, malformed, UUID, or assumption-word strings in `location` and `sqlLocation` (while accepting `'uksouth'`, `'ukwest'`, `'offline-region'`, and `'offline-sql-region'`).
5. Negative ARM template mutation tests proving that hardcoding `'ok'` on `regionCheckMustBeRecorded`, `quotaCheckMustBeRecorded`, `deploymentLocationsMustBeSelected`, or `primaryLocationMustBeUKSouth`, or removing `sqlVCores` bounds / forwarding, is caught by the policy assertions.
6. CLI helper enforcement in `pipeline.parameters()` and `deploy.main()` rejecting whitespace, placeholder/word-bounded assumption tokens, bare and embedded subscription/tenant UUIDs, duplicate earlier invalid `--parameter` flags, `location != "uksouth"`, and assumption-word/non-slug `sqlLocation` overrides without echoing raw rejected values in error messages, while accepting valid dated/reviewed check references (including `spending` and `jtbd` anchors).
7. Documentation and check-ledger parity across `docs/architecture/environment-region-quota-strategy.md`, `docs/architecture/README.md`, and `infra/README.md` (`## Environments` table SKUs/models, all 17 `R1`-`R17` check rows, explicit `Unknown` classification for `GP_Gen5` and `gpt-4.1-nano` relative to `2026-10-18` `612cbed7`, Markdown conventions, and absence of `.copilot-tracking/` leaks in `docs/architecture/environment-region-quota-strategy.md`, the `## Environments` section of `infra/README.md`, and the newly added bullet in `docs/architecture/README.md`).

#### Boundaries

* Included: `infra/tests/test_environment_quota_parameters.py` and Focused validation execution.
* Excluded: Modifying `infra/tests/test_monitoring_alerts.py` or running `tools/rpi-checks.py`.

#### Likely Targets

* `infra/tests/test_environment_quota_parameters.py`

#### Dependencies

* P01-T01, P01-T02, P02-T01.

#### Validation Expectations

* Zero test failures, zero `az bicep lint` diagnostics, zero `ruff` check/format issues on touched files, and zero `mypy --strict` errors on `pipeline.py`, `deploy.py`, and `test_environment_quota_parameters.py`.

#### Completion Evidence

* Recorded command exit codes and counts in `.copilot-tracking/changes/2026-11-15/infra-137-env-quotas-changes.md`.

#### Unresolved Items

* None.
