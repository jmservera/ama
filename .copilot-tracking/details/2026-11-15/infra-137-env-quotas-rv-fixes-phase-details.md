<!-- markdownlint-disable-file -->
# RPI Phase Details: Resolve Routed Review Findings RV-001, RV-002, and RV-003 for Issue #137

## Metadata

* Task ID: issue-137-rv-fixes
* Task slug: infra-137-env-quotas-rv-fixes
* Parent task: issue-137 (`infra-137-env-quotas`)
* Related plan: .copilot-tracking/plans/2026-11-15/infra-137-env-quotas-rv-fixes-plan.md
* Evidence sources: .copilot-tracking/reviews/logs/2026-11-15/infra-137-env-quotas-review.md, .copilot-tracking/research/2026-11-15/infra-137-env-quotas-research.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Fix RV-001..RV-003 Across CLI Scripts, Bicep, Architecture Doc, and Regression Suite | Complete | P01, P01-T01, P01-T02 |

<!-- rpi:phase id=P01 -->
## P01: Fix RV-001..RV-003 Across CLI Scripts, Bicep, Architecture Doc, and Regression Suite

### Context

Parent review `.copilot-tracking/reviews/logs/2026-11-15/infra-137-env-quotas-review.md` identified three bounded defects (`RV-001`, `RV-002`, `RV-003`) before local commit.

### Intent

Fix all three defects cleanly while preserving parent RPI review history untouched.

### Boundaries

* Included: `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, `infra/main.bicep`, `docs/architecture/environment-region-quota-strategy.md`, `infra/tests/test_environment_quota_parameters.py`.
* Excluded: Modifying `infra/tests/test_monitoring_alerts.py` or rewriting `.copilot-tracking/reviews/logs/2026-11-15/infra-137-env-quotas-review.md`.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Update CLI regex lookarounds (`deploy.py`, `pipeline.py`), `sqlAutoPauseDelayMinutes` bound (`main.bicep`), and architecture catalog (`environment-region-quota-strategy.md`)

#### Context

Python `\b` treats `_` as `\w`, permitting `assumed_2026` and `sub_<uuid>_uksouth`. In addition, `infra/main.bicep` omits `@minValue(-1)` on `sqlAutoPauseDelayMinutes`, and `docs/architecture/environment-region-quota-strategy.md` cites `modules/resourceAlerts.bicep` instead of `modules/operationalMonitoring.bicep` and lists `modules/foundry.bicep` in the `Defined in` cell for `chatModel*`.

#### Intent

Close `RV-001` and `RV-002` across all four target files.

#### Likely Targets

* `infra/scripts/deploy.py` and `infra/scripts/pipeline.py`:
  * `FORBIDDEN_CHECK_PATTERN = re.compile(r"(?<![a-z0-9])(?:todo|tbd|assumed|assumption|unverified|pending|unknown|none|na|skip)(?![a-z0-9])|placeholder|example\.invalid|n/a", re.IGNORECASE)`
  * `EMBEDDED_UUID_PATTERN = re.compile(r"(?<![0-9a-f])[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}(?![0-9a-f])", re.IGNORECASE)`
* `infra/main.bicep`: Add `@minValue(-1)` immediately above `param sqlAutoPauseDelayMinutes int = 60`.
* `docs/architecture/environment-region-quota-strategy.md`: Update `chatModel*` `Defined in` to `main.bicep` and update its `Downstream resource target` cell so it states `chatModel*` populate the default `standard` entry of `modelDeployments` forwarded as `deployments` to `modules/foundry.bicep` (separate from `demoDirectIngress` + `chatDemoActivation == 'approved-2026-11-03'` runtime activation in `modules/containerapps.bicep`, removing any `enableDemoChat` reference); update `monthlyBudget` `Defined in` and target description to `main.bicep, modules/operationalMonitoring.bicep`; and document both `(?<![a-z0-9])...(?![a-z0-9])` (treating `_` as a delimiter) and `(?<![0-9a-f])[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}(?![0-9a-f])` in `## Mechanical Fail-Closed Guards`.

#### Validation Expectations

* `az bicep lint --file infra/main.bicep`, `ruff`, and `mypy --strict` exit `0`.

#### Completion Evidence

* Compiled `main.bicep` `sqlAutoPauseDelayMinutes.minValue == -1`, `deploy.py`/`pipeline.py` lookaround regexes updated, and `docs/architecture/environment-region-quota-strategy.md` reconciled.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Harden `infra/tests/test_environment_quota_parameters.py` assertions and run Focused validation

#### Context

`RV-003` identified missing underscore-delimited negative cases, incomplete per-branch value/UUID redaction checks, omitted `sqlAutoPauseDelayMinutes` / `chatModel*` bound assertions, and static substring checks in the documentation parity test.

#### Intent

Strengthen the existing 8 test methods in `infra/tests/test_environment_quota_parameters.py` so any regression of `RV-001` or `RV-002` fails immediately.

#### Likely Targets

* `infra/tests/test_environment_quota_parameters.py`:
  * `_assert_contract`: Assert `params["sqlAutoPauseDelayMinutes"]["minValue"] == -1`, `params["chatModelCapacity"]["minValue"] == 1`, and `params["chatModelSku"]["allowedValues"] == ["GlobalStandard", "Standard"]`.
  * `test_bicep_recorded_check_and_location_guards_reject_assumptions_and_uuids`: Include `"assumed_uksouth_2026"`, `"todo_check"`, `"tbd_later"`, `"unverified_quota"`, and positive `"docs/reference/research/spending_review_2026.md#jtbd_notes_2026"`.
  * `test_negative_mutations_are_caught_by_contract_assertions`: Add mutation deleting `sqlAutoPauseDelayMinutes.minValue`.
  * `test_pipeline_parameters_enforce_recorded_checks_and_redact_values` and `test_deploy_cli_rejects_invalid_check_and_region_overrides_before_az`: Include all five `AC-1` rejected inputs (`"assumed_uksouth_2026"`, `"todo_check"`, `"tbd_later"`, `"unverified_quota"`, `f"sub_{SYNTHETIC_UUID}_uksouth"`), both `AC-1` accepted inputs (`"infra/README.md#spending_review_2026"`, `"docs/reference/research/jtbd_notes_2026"`, plus 40-char commit SHA anchors), and lowercase alphanumeric non-hyphenated redaction probes (`location="ukwestleakedregion"`, `sqlLocation="placeholdersqlsecret"`) alongside hyphenated invalid slugs, asserting neither raw rejected values (`>= 8` chars, removing the `"ukwest"` exemption) nor `SYNTHETIC_UUID` appear across all four keys (`location`, `sqlLocation`, `regionCheckReference`, `quotaCheckReference`) in `PipelineError` or `deploy.py` `stderr`.
  * `test_architecture_doc_and_infra_readme_match_compiled_templates_and_r1_r17`: Verify every backticked `infra/*.bicep` and `modules/*.bicep` path in `ARCH_DOC` exists on disk, assert `\b[0-9a-f]{8}` and `enableDemoChat` are absent from `ARCH_DOC`, and match each parameter's catalog table row (`| \`<param>\` ... |`) before verifying its compiled `defaultValue` from `self.main["parameters"]` (`sqlVCores`, `monthlyBudget`, `iotHubMonthlyCost`, `chatModelName`, `chatModelVersion`, `chatModelSku`, `chatModelCapacity`, `sqlAutoPauseDelayMinutes`).

#### Validation Expectations

* Standalone `python3 -m unittest infra/tests/test_environment_quota_parameters.py -q`, `REQUIRE_AZ_BICEP=1` `test_bicep_policy.py` + `test_pipeline.py` + `test_sql_tier.py` + `test_deploy.py` + `test_governance.py`, `az bicep lint`, `ruff`, and `mypy --strict` pass cleanly.

#### Completion Evidence

* All Focused validation checks recorded with exit `0`.

#### Unresolved Items

* None.
