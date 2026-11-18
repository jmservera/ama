<!-- markdownlint-disable-file -->
# RPI Plan Critique: Resolve Routed Review Findings RV-001, RV-002, and RV-003 for Issue #137

## Metadata

* Task ID: issue-137-rv-fixes
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/infra-137-env-quotas-rv-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/infra-137-env-quotas-rv-fixes-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Single-pass credibility critique of child plan `issue-137-rv-fixes` (`infra-137-env-quotas-rv-fixes`, parent `issue-137` / `infra-137-env-quotas`) resolving routed review defects `RV-001` (High), `RV-002` (Medium), and `RV-003` (Medium) while preserving parent RPI review history untouched, maintaining the 8-method lock on `infra/tests/test_environment_quota_parameters.py`, running Focused validation, and committing locally without pushing.
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/infra-137-env-quotas-rv-fixes-plan.md, .copilot-tracking/details/2026-11-15/infra-137-env-quotas-rv-fixes-phase-details.md, .copilot-tracking/reviews/logs/2026-11-15/infra-137-env-quotas-review.md, infra/scripts/deploy.py, infra/scripts/pipeline.py, infra/main.bicep, docs/architecture/environment-region-quota-strategy.md, infra/tests/test_environment_quota_parameters.py
* Decisions, dependencies, and acceptance criteria considered: `FR-1`..`FR-3`, `NFR-1`..`NFR-2`, `AC-1`..`AC-3`, test ownership lock (`8` methods in `infra/tests/test_environment_quota_parameters.py`, `0` additions, `0` removals, `infra/tests/test_monitoring_alerts.py` untouched), Focused validation tier, and caller `Do NOT push` boundary.
* Assessment boundary: Evaluates exact code, Bicep, documentation, and test alignment across the supplied plan, phase details, parent review log, and five target workspace files; does not inspect unreferenced modules, execute live Azure subscription queries, or run test commands during read-only critique.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| `RV-001`, `FR-1`, `AC-1` | Covered | `(?<![a-z0-9])...(?![a-z0-9])` on `FORBIDDEN_CHECK_PATTERN` and `(?<![0-9a-f])...(?![0-9a-f])` on `EMBEDDED_UUID_PATTERN` in `infra/scripts/deploy.py` and `infra/scripts/pipeline.py` close underscore-delimited assumption (`assumed_uksouth_2026`, `todo_check`, `tbd_later`, `unverified_quota`) and embedded-UUID (`sub_<uuid>_uksouth`) bypasses while preserving `spending_*`, `jtbd_*`, and 40/64-char hex digests. |
| `RV-002`, `FR-2`, `AC-2`, `P01-T01` | Partial | `@minValue(-1)` on `sqlAutoPauseDelayMinutes` in `infra/main.bicep` and replacing nonexistent `modules/resourceAlerts.bicep` with `modules/operationalMonitoring.bicep` are accurate, but `P01-T01` leaves an inaccurate `enableDemoChat` claim in the `chatModel*` `Downstream resource target` cell and leaves `"word-bounded"` CLI boundary prose ambiguous (`PC-002`). |
| `RV-003`, `FR-3`, `AC-1`..`AC-3`, `P01-T02` | Partial | Preserves the 8-method lock and adds `@minValue(-1)`/`chatModel*` contract assertions, but hyphenated redaction test values (`"ukwest-leaked-region"`, `"placeholder-sql-secret"`) short-circuit on `re.fullmatch(r"[a-z][a-z0-9]+", ...)` before reaching two target error branches, two `AC-1` tokens (`tbd_later`, `unverified_quota`) are omitted from CLI test lists, and whole-file substring checks for defaults `1`, `2`, and `60` pass vacuously (`PC-001`). |
| `NFR-1`, `NFR-2` | Covered | Focused validation commands (`unittest`, `REQUIRE_AZ_BICEP=1` suites, `az bicep lint`, `ruff --isolated`, bare `ruff check` on `test_environment_quota_parameters.py`, `mypy --strict`) and Markdown rules are explicitly specified. |
| `P01` | Partial | Single-phase dependency structure and parent-artifact immutability boundaries are sound pending direct planner refinements in `PC-001` and `PC-002`. |

## Verdict

* Verdict: Revise
* Rationale: The proposed lookaround regexes (`RV-001`), `@minValue(-1)` Bicep bound, and `modules/operationalMonitoring.bicep` catalog correction (`RV-002`) directly resolve the parent review defects, but `P01-T02` has three concrete test-effectiveness gaps (`PC-001`: short-circuited CLI redaction probes, omitted `AC-1` negative tokens, and vacuous whole-document numeric default checks) and `P01-T01` leaves stale `chatModel*` target/boundary prose in `docs/architecture/environment-region-quota-strategy.md` (`PC-002`). Both are bounded planner-owned corrections requiring no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Planned CLI redaction probes, `AC-1` inputs, and compiled-default doc checks in `P01-T02` leave two CLI guard branches masked and numeric defaults vacuously matched

* Related IDs: `RV-003`, `FR-3`, `AC-1`, `AC-2`, `P01`, `P01-T02`
* Evidence: .copilot-tracking/details/2026-11-15/infra-137-env-quotas-rv-fixes-phase-details.md (`P01-T02`), .copilot-tracking/plans/2026-11-15/infra-137-env-quotas-rv-fixes-plan.md (`FR-3`, `AC-1`), infra/scripts/pipeline.py (`parameters` lines 155-165), infra/scripts/deploy.py (`validate_parameter_overrides` lines 171-184), infra/tests/test_environment_quota_parameters.py (lines 438-615), docs/architecture/environment-region-quota-strategy.md (lines 78-89)
* Concern: First, `P01-T02` proposes `"ukwest-leaked-region"` (`location`) and `"placeholder-sql-secret"` (`sqlLocation`) as `>= 8`-char redaction probes, but both strings contain `-` and therefore fail `re.fullmatch(r"[a-z][a-z0-9]+", ...)` first; in `pipeline.py`, `location="ukwest-leaked-region"` raises at line 162 (`Invalid region parameter: location`) and never reaches line 164 (`if overrides["location"] != "uksouth":`), while in both `pipeline.py` and `deploy.py`, `sqlLocation="placeholder-sql-secret"` short-circuits before `"placeholder" in ...` is evaluated (and existing line 490 of `test_environment_quota_parameters.py` explicitly skips `"ukwest"`). Second, `AC-1` requires CLI rejection of `assumed_uksouth_2026`, `todo_check`, `tbd_later`, `unverified_quota`, and `sub_<uuid>_uksouth` plus acceptance of `spending_review_2026` and `jtbd_notes_2026`, whereas `P01-T02` omits `"tbd_later"` and `"unverified_quota"` from the CLI test cases and substitutes shorter positive tokens. Third, checking only that compiled defaults from `self.main["parameters"]` (`1` for `chatModelCapacity`, `2` for `sqlVCores`, `60` for `iotHubMonthlyCost` and `sqlAutoPauseDelayMinutes`) appear somewhere in `ARCH_DOC` passes vacuously because `"1"`, `"2"`, and `"60"` already appear in dates and prose across the file.
* Impact: Literal execution of `P01-T02` would leave `pipeline.py`'s `location != "uksouth"` error branch and both scripts' `"placeholder" in sqlLocation` branch untested for raw-value redaction, leave two `AC-1` tokens unverified at the CLI layer, and fail to detect numeric default drift on `sqlVCores` or `chatModelCapacity` in `docs/architecture/environment-region-quota-strategy.md`.
* Smallest useful change: Revise `P01-T02` in `.copilot-tracking/details/2026-11-15/infra-137-env-quotas-rv-fixes-phase-details.md` to: (1) include lowercase alphanumeric non-hyphenated probes (`location="ukwestleakedregion"` and `sqlLocation="placeholdersqlsecret"`) alongside hyphenated invalid slugs and `SYNTHETIC_UUID`, asserting neither raw rejected values nor `SYNTHETIC_UUID` appear across all four keys (`location`, `sqlLocation`, `regionCheckReference`, `quotaCheckReference`) in both `PipelineError` and `deploy.py` `stderr` (removing the `stripped != "ukwest"` exemption); (2) test all five `AC-1` rejected inputs (`"assumed_uksouth_2026"`, `"todo_check"`, `"tbd_later"`, `"unverified_quota"`, `f"sub_{SYNTHETIC_UUID}_uksouth"`) and both `AC-1` accepted inputs (`spending_review_2026`, `jtbd_notes_2026`, plus 40-char SHA anchors) in both CLI tests and the Bicep guard test; and (3) match each parameter's catalog table row (`| \`<param>\` ... |`) in `ARCH_DOC` before asserting its compiled `defaultValue` (and verify both `infra/*.bicep` and `modules/*.bicep` backticked paths exist on disk).
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T02` in `.copilot-tracking/details/2026-11-15/infra-137-env-quotas-rv-fixes-phase-details.md` capturing non-hyphenated `location`/`sqlLocation` redaction probes, complete `AC-1` positive/negative CLI vectors, and row-scoped compiled-default plus `infra/`/`modules/` path assertions.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Low]: `P01-T01` updates `chatModel*` `Defined in` without correcting its inaccurate `enableDemoChat` target description or clarifying the assumption-token lookaround in `environment-region-quota-strategy.md`

* Related IDs: `RV-001`, `RV-002`, `FR-1`, `FR-2`, `AC-2`, `P01`, `P01-T01`
* Evidence: docs/architecture/environment-region-quota-strategy.md (line 86 and lines 107-108), infra/main.bicep (lines 120-137, 154, 330-343, 407), .copilot-tracking/details/2026-11-15/infra-137-env-quotas-rv-fixes-phase-details.md (`P01-T01`)
* Concern: Line 86 of `docs/architecture/environment-region-quota-strategy.md` states in `Downstream resource target` that `chatModelName` / `chatModelVersion` / `chatModelSku` / `chatModelCapacity` are `"Demo-chat deployment inputs active only when demoDirectIngress && chatDemoActivation == 'approved-2026-11-03' (enableDemoChat), plus fallback defaults for modelDeployments"`. In `infra/main.bicep`, `enableDemoChat` does not exist and `chatModel*` are never passed to `modules/containerapps.bicep`; they solely populate the default `standard` element of `modelDeployments`, which `main.bicep` forwards unconditionally as `deployments: modelDeployments` to `modules/foundry.bicep` (while `demoDirectIngress` and `chatDemoActivation == 'approved-2026-11-03'` gate employee demo-chat runtime activation in `modules/containerapps.bicep`). In addition, line 108 of `docs/architecture/environment-region-quota-strategy.md` still says `"word-bounded assumption/placeholder rejection"` without noting the ASCII non-alphanumeric lookaround `(?<![a-z0-9])...(?![a-z0-9])` that treats `_` as a delimiter.
* Impact: Updating only the `Defined in` column for `chatModel*` and only the UUID regex in `P01-T01` leaves an inaccurate wiring statement for `chatModel*` and obscures the underscore boundary rule introduced for `RV-001`.
* Smallest useful change: Expand `P01-T01` in `.copilot-tracking/details/2026-11-15/infra-137-env-quotas-rv-fixes-phase-details.md` to update the `chatModel*` `Downstream resource target` cell in `docs/architecture/environment-region-quota-strategy.md` (stating `chatModel*` populate the default `standard` entry of `modelDeployments` forwarded as `deployments` to `modules/foundry.bicep`, separate from `demoDirectIngress` + `chatDemoActivation == 'approved-2026-11-03'` runtime activation in `modules/containerapps.bicep`) and document `(?<![a-z0-9])...(?![a-z0-9])` alongside `(?<![0-9a-f])...(?![0-9a-f])` in `## Mechanical Fail-Closed Guards` (with `P01-T02` asserting `\b[0-9a-f]{8}` is absent from `ARCH_DOC`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` (and matching stale-regex absence check in `P01-T02`) in `.copilot-tracking/details/2026-11-15/infra-137-env-quotas-rv-fixes-phase-details.md`.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Strengths: Preserves `.copilot-tracking/reviews/logs/2026-11-15/infra-137-env-quotas-review.md` as immutable historical RPI evidence, respects the `8`-method test ownership lock on `infra/tests/test_environment_quota_parameters.py` without touching `infra/tests/test_monitoring_alerts.py`, and uses exact ASCII non-alphanumeric and non-hex lookarounds that match `infra/main.bicep` delimiter semantics without false positives on `spending_*`, `jtbd_*`, or commit/image SHA digests.
* Accepted residual risk: Live target-subscription capability and quota checks (`R4`, `R5`, `R7`, `R8`, `R9`, `R11`, `R14`-`R17`, including `GP_Gen5` and `gpt-4.1-nano`) and named human pilot approval remain tracked under `## Follow-Up Items` (`Refs #137`), and branch-level complete local RPI gate / hosted CI remain deferred per explicit caller direction (`Focused` tier for this child iteration, `Do NOT push`).

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Critique is read-only and strictly bounded to the caller-supplied planning, review, Bicep, Python, documentation, and test files; child module `.bicep` files outside `infra/main.bicep` were not re-read beyond compiled/documented contracts already verified in parent review evidence, and validation suites were not executed during critique.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Directly revise `P01-T01` and `P01-T02` in `.copilot-tracking/details/2026-11-15/infra-137-env-quotas-rv-fixes-phase-details.md` (and finalize `.copilot-tracking/plans/2026-11-15/infra-137-env-quotas-rv-fixes-plan.md`) to incorporate `PC-001` and `PC-002`, then proceed to implementation without another critique pass.
* User response required: no
