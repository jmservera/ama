---
title: Infrastructure Issue 137 Environment Region and Quota Parameters Plan Critique
description: Single-pass credibility critique of the Issue 137 candidate RPI plan and phase details against infra Bicep templates, CLI scripts, tests, and architecture documentation
author: GitHub Copilot
ms.date: 2026-11-15
ms.topic: reference
---

## Critique Summary

* Execution status: Complete
* Verdict: Revise
* Plan: .copilot-tracking/plans/2026-11-15/infra-137-env-quotas-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md
* Highest-impact finding: PC-001 (Critical: declaring `chatModel*` parameters in `infra/main.bicepparam` and `infra/main.pilot.example.bicepparam` deterministically fails `infra/tests/test_bicep_policy.py:759-760`, and re-adding `apiMinReplicas` duplicates lines already present in all three `.bicepparam` files)
* Action owner: planning parent
* User response required: no
* Smallest next action: Revise `FR-1`..`FR-4`, `NFR-1`..`NFR-2`, `AC-1`..`AC-5`, `P01`..`P03`, and `P01-T01`..`P03-T01` in place to resolve `PC-001` through `PC-006` before entering implementation.

## Inputs and Criterion Boundary

* Supplied evidence reviewed:
  * `.copilot-tracking/research/2026-11-15/infra-137-env-quotas-research.md` (`C1` through `C19`, `W1` through `W2`)
  * `.copilot-tracking/plans/2026-11-15/infra-137-env-quotas-plan.md` (`FR-1` through `FR-4`, `NFR-1` through `NFR-2`, `AC-1` through `AC-5`, `P01` through `P03`)
  * `.copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md` (`P01-T01`, `P01-T02`, `P02-T01`, `P03-T01`)
  * Bicep templates and parameter sets: `infra/main.bicep`, `infra/modules/guard.bicep`, `infra/modules/sql.bicep`, `infra/modules/foundry.bicep`, `infra/modules/iothub.bicep`, `infra/modules/containerapps.bicep`, `infra/modules/operationalMonitoring.bicep`, `infra/iot-hub-live.bicep`, `infra/resident-demo.bicep`, `infra/resident-assistant.bicep`, `infra/public-edge-existing.bicep`, `infra/main.bicepparam`, `infra/main.test.bicepparam`, `infra/main.pilot.example.bicepparam`
  * CLI scripts and CI workflow: `infra/scripts/pipeline.py`, `infra/scripts/deploy.py`, `.github/workflows/src-ci.yml`
  * Existing infrastructure regression tests: `infra/tests/test_bicep_policy.py`, `infra/tests/test_governance.py`, `infra/tests/test_sql_tier.py`, `infra/tests/test_deploy.py`, `infra/tests/test_pipeline.py`, `infra/tests/test_container_hosting_completeness.py`, `infra/tests/test_iothub_module.py`, `infra/tests/test_monitoring_alerts.py`
  * Documentation and project context: `infra/README.md`, `docs/architecture/README.md`, `docs/architecture/resident-assistant-prototype.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`
* Explicit requirements and decisions:
  * Deliver and prove the remaining unticked Issue `#137` acceptance criterion (`Region and quota choices are parameters with recorded checks, not assumptions`) on stacked branch `feat/infra-137-env-quotas` under the focused validation tier.
  * Keep existing test files in `infra/tests/` untouched (`0` modifications) to avoid stacked-branch merge conflicts (including `infra/tests/test_monitoring_alerts.py`), placing new regression coverage in `infra/tests/test_environment_quota_parameters.py`.
  * Document the environment, region, and quota parameter and check contract in `docs/architecture/` and reconcile `infra/README.md` without fabricating live Azure check outcomes or embedding tenant, subscription, or principal UUIDs.
  * Run `python3 -m unittest infra/tests/test_environment_quota_parameters.py -q`, `python3 -m ruff check infra`, and `python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_environment_quota_parameters.py`, plus existing `infra/tests/` regression suites.
* Acceptance criteria in scope:
  * Issue `#137` unticked criterion (`Region and quota choices are parameters with recorded checks, not assumptions`) and candidate plan `AC-1` through `AC-5`.
* Out-of-scope or unverified areas:
  * Live authenticated Azure subscription capability or quota queries (`az sql db list-editions`, `az cognitiveservices usage list`, `az rest` quota endpoints) are intentionally out of scope; target-subscription values not covered by a committed dated check remain explicitly marked `Unknown`.
  * GitHub workflow edits under `.github/workflows/` are out of scope to preserve focused-tier classification.

## Coverage Assessment

| Area | Status | Notes |
| --- | --- | --- |
| `FR-1` (Bicep parameter bounds) | Gap | `P01-T01` targets `sqlVCores` inside `infra/modules/sql.bicep`, where the actual parameter is `maxVCores` (`infra/modules/sql.bicep:20`, locked by `infra/tests/test_sql_tier.py:37`); `research.md:89` also misstates `monthlyBudget` default as `150` instead of `300` (`infra/main.bicep:25`). See `PC-002`. |
| `FR-2` (`.bicepparam` parity across `dev`, `test`, `pilot`) | Gap | Adding `chatModel*` to `infra/main.bicepparam` or `infra/main.pilot.example.bicepparam` violates `infra/tests/test_bicep_policy.py:759-760` (`assertNotIn("chat", ...)`). `apiMinReplicas = 0` already exists in all three files (`main.bicepparam:18`, `main.test.bicepparam:18`, `main.pilot.example.bicepparam:23`), `AutoPause` is forbidden in `main.pilot.example.bicepparam` (`infra/tests/test_sql_tier.py:48`), and `modelDeployments` / `monthlyBudget` / `iotHubMonthlyCost` are omitted from the explicit quota-parameter list. See `PC-001`. |
| `FR-3` (Fail-closed guards in Bicep and Python CLI helpers) | Gap | Raw substring stripping/matching produces false positives on valid repo anchors (`spending`, `appending`, `jtbd`); `P01-T01`'s 36-char UUID predicate omits hyphen positions `8-4-4-4-12` and does not match embedded UUIDs; `sqlLocation` accepts invalid slugs in `main.bicep` and accepts lowercase assumption words (`placeholder`, `assumed`, `tbd`, `unknown`) in both `pipeline.py` and `deploy.py`. See `PC-003` and `PC-004`. |
| `FR-4` (Architecture documentation and `infra/README.md` parity) | Gap | `P02-T01` and `P03-T01` do not account for five pre-existing `.copilot-tracking/` links in `docs/architecture/README.md:25,79,355,359,371`, and must explicitly distinguish historical `2026-10-18` `612cbed7` `R4`/`R8`/`R9` queries (`GP_S_Gen5_2`, `gpt-4.1-mini`, `gpt-4.1`) from current unverified template defaults (`GP_Gen5` in pilot example and `gpt-4.1-nano` default). See `PC-006`. |
| `NFR-1` (Backward compatibility with untouched `infra/tests/`) | Gap | `P01-T01` fails `test_bicep_policy.py:759-760` if `chatModel*` is added (`PC-001`), risks `test_bicep_policy.py:2391` if `"Empty means"` is removed from `infra/main.bicep` (`PC-002`), and fails `test_bicep_policy.py:1219,2400` if `sqlLocation` disallows hyphens (`'offline-region'`, `'offline-sql-region'`) (`PC-004`). |
| `NFR-2` (Code quality, `ruff`, `mypy`, and deterministic execution) | Gap | Non-`--isolated` `python3 -m ruff check` exits `1` on untouched lines of `infra/scripts/deploy.py` (`EXE001`) and `infra/scripts/pipeline.py` (`EXE001`, `SIM102`) and reports 112 pre-existing warnings across `infra/`, short-circuiting `python3 -m ruff check infra && python3 -m ruff format ...`; running `test_bicep_policy.py` and `test_pipeline.py` also requires editable `src/*` distributions installed first. See `PC-005`. |
| `AC-1` (Explicit bounded parameters and `az bicep build` / `build-params`) | Gap | Blocked as written by `PC-001` (duplicate `apiMinReplicas` fails `az bicep build-params`; `chatModel*` breaks policy test) and `PC-002` (`maxVCores` vs `sqlVCores` in `infra/modules/sql.bicep`). |
| `AC-2` (Deterministic rejection across `main.bicep`, `pipeline.py`, `deploy.py`) | Gap | Overstates embedded-UUID parity in Bicep (`PC-003`) and leaves `sqlLocation` / `location` assumption-slug bypasses in `main.bicep`, `pipeline.py`, and `deploy.py` (`PC-004`). |
| `AC-3` (Architecture documentation and index discoverability) | Sound with adjustment | Covered once `PC-002` (`monthlyBudget = 300`, `29` existing guards -> `31` after adding 2 guards) and `PC-006` (`2026-10-18` `R4`/`R8`/`R9` provenance honesty) are applied. |
| `AC-4` (New test suite and full `infra/tests/` + `ruff` pass) | Gap | Requires fixes in `PC-001`, `PC-003`, `PC-004`, `PC-005`, and `PC-006` so `test_environment_quota_parameters.py` and existing `infra/tests/` pass deterministically and `ruff format --check` is not skipped behind a short-circuited `&&`. |
| `AC-5` (Honesty, privacy, and no fabricated Azure approvals) | Gap | CLI exception strings in `P01-T02` need an explicit rule not to echo raw rejected parameter values (which could print pasted subscription/tenant UUIDs to CI stderr), and `P02-T01` must keep `GP_Gen5` and `gpt-4.1-nano` marked `Unknown` relative to `2026-10-18` `R4`/`R8`/`R9`. See `PC-004` and `PC-006`. |
| `P01` / `P01-T01` (Bicep bounds, guards, and `.bicepparam` sets) | Gap | Directly affected by `PC-001`, `PC-002`, `PC-003`, and `PC-004`. |
| `P01` / `P01-T02` (`pipeline.py` and `deploy.py` preflight hardening) | Gap | Directly affected by `PC-003` and `PC-004` (including `plan.md:16` falsely stating `deploy.py` validates compiled parameter files on disk, which breaks `infra/tests/test_deploy.py:79`). |
| `P02` / `P02-T01` (`docs/architecture/environment-region-quota-strategy.md`, `docs/architecture/README.md`, `infra/README.md`) | Gap | Directly affected by `PC-001`, `PC-002`, and `PC-006`. |
| `P03` / `P03-T01` (`infra/tests/test_environment_quota_parameters.py` and validation commands) | Gap | Directly affected by `PC-001`, `PC-003`, `PC-004`, `PC-005`, and `PC-006`. |

## Actionable Findings

### PC-001: `.bicepparam` `chatModel*` and `apiMinReplicas` edits deterministically fail `test_bicep_policy.py` and `az bicep build-params`

* Severity: Critical
* Related IDs: `FR-2`, `NFR-1`, `AC-1`, `AC-4`, `P01`, `P01-T01`, `P02-T01`, `P03-T01`, `C3`, `C4`, `C13`
* Action owner: planning parent
* Decision route: direct planner correction
* Evidence:
  * `.copilot-tracking/plans/2026-11-15/infra-137-env-quotas-plan.md:14,22,63,115` and `.copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md:27,63-67` instruct declaring `chatModelName`, `chatModelVersion`, `chatModelSku`, `chatModelCapacity`, `apiMinReplicas`, and `sqlVCores` across `infra/main.bicepparam`, `infra/main.test.bicepparam`, and `infra/main.pilot.example.bicepparam`, while keeping existing `infra/tests/*.py` unmodified (`0` edits).
  * `infra/tests/test_bicep_policy.py:759-760` (`test_test_parameters_record_demo_chat_privacy_refs`) asserts `self.assertNotIn("chat", (INFRA / name).read_text().lower())` for both `main.bicepparam` and `main.pilot.example.bicepparam`.
  * `infra/main.bicepparam:18`, `infra/main.test.bicepparam:18`, and `infra/main.pilot.example.bicepparam:23` already declare `param apiMinReplicas = 0`, and `infra/tests/test_bicep_policy.py:699` asserts `apiMinReplicas == 0` across all three files (disproving `.copilot-tracking/research/2026-11-15/infra-137-env-quotas-research.md:72,82,150`, which claimed `dev`/`test` omit `apiMinReplicas` and `pilot` sets `apiMinReplicas = 1`).
  * `infra/tests/test_sql_tier.py:48` asserts `self.assertNotIn("AutoPause", PILOT)` on `infra/main.pilot.example.bicepparam`.
  * `infra/main.bicep:25-26,79-95,306` also routes Foundry deployments, budget quota guards, and serverless SQL pause behavior through `modelDeployments`, `monthlyBudget` (`300`), `iotHubMonthlyCost` (`60`), and `sqlAutoPauseDelayMinutes` (`60`).
* Concern:
  Adding any `chatModel*` identifier or comment containing `"chat"` to `infra/main.bicepparam` or `infra/main.pilot.example.bicepparam` causes an immediate failure in `test_bicep_policy.py:759-760`. Appending `param apiMinReplicas` creates a duplicate parameter assignment rejected by `az bicep build-params`, and changing `pilot` to `1` fails `test_bicep_policy.py:699`. Similarly, adding `sqlAutoPauseDelayMinutes` or `"AutoPause"` in a comment to `infra/main.pilot.example.bicepparam` fails `test_sql_tier.py:48`. Meanwhile, omitting `modelDeployments`, `monthlyBudget`, and `iotHubMonthlyCost` leaves active quota- and cost-bearing parameters implicit despite `FR-2`'s completeness claim.
* Impact:
  `P01-T01` cannot compile or pass the locked regression gate (`test_bicep_policy.py` and `az bicep build-params`), blocking `AC-1`, `AC-4`, and `NFR-1`.
* Smallest useful change:
  Revise `Executive Summary`, `Scope`, `FR-2`, `P01`, `P01-T01`, `P02-T01`, and `P03-T01` so that:
  1. All three `.bicepparam` files declare Foundry model SKU and TPM quota capacity via `param modelDeployments = [{ name: 'standard', model: 'gpt-4.1-nano', version: '2025-04-14', skuName: 'GlobalStandard', capacity: 1 }]` (alongside `param sqlVCores = 2`, `param monthlyBudget = 300`, and `param iotHubMonthlyCost = 60`), keeping zero occurrences of substring `"chat"` in `infra/main.bicepparam` and `infra/main.pilot.example.bicepparam` (optional `chatModel*` parameters in `infra/main.bicep` remain documented as `enableDemoChat`-only overrides permissible solely in `infra/main.test.bicepparam` when `enableDemoChat` is evaluated).
  2. `sqlAutoPauseDelayMinutes = 60` is declared only in serverless `infra/main.bicepparam` and `infra/main.test.bicepparam`, with zero occurrences of `"AutoPause"` in `infra/main.pilot.example.bicepparam`.
  3. Existing `param apiMinReplicas = 0` lines in all three `.bicepparam` files are retained in place without duplication, and `P02-T01` / `P03-T01` record `apiMinReplicas = 0` across all three files.
* Resolving evidence:
  Updated `FR-2`, `P01`, `P01-T01`, `P02-T01`, and `P03-T01` specifying `modelDeployments`, `sqlVCores`, `monthlyBudget`, `iotHubMonthlyCost`, serverless-only `sqlAutoPauseDelayMinutes`, single in-place `apiMinReplicas = 0`, and explicit preservation of `test_bicep_policy.py:699,759-760` and `test_sql_tier.py:48`.

### PC-002: `FR-1` / `P01-T01` references nonexistent parameter `sqlVCores` in `infra/modules/sql.bicep`, and research baseline misstates `monthlyBudget` (`150` vs `300`) and guard count (`28` vs `29`)

* Severity: High
* Related IDs: `FR-1`, `AC-1`, `AC-3`, `P01`, `P01-T01`, `P02-T01`, `P03-T01`, `C2`, `C4`
* Action owner: planning parent
* Decision route: direct planner correction
* Evidence:
  * `.copilot-tracking/plans/2026-11-15/infra-137-env-quotas-plan.md:22,62,115` and `.copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md:26,41` instruct adding `@minValue(1) @maxValue(80)` to `sqlVCores` in both `infra/main.bicep` and `infra/modules/sql.bicep`.
  * `infra/modules/sql.bicep:20` declares `param maxVCores int = 2` (not `sqlVCores`), `infra/main.bicep:341` passes `maxVCores: sqlVCores`, and `infra/tests/test_sql_tier.py:37` asserts `self.assertIn("maxVCores: sqlVCores", MAIN)`.
  * `.copilot-tracking/research/2026-11-15/infra-137-env-quotas-research.md:89` records `monthlyBudget (int = 150)` and line `146` (`C2`) records `28 guard parameters`, whereas `infra/main.bicep:25` defines `param monthlyBudget int = 300` and `infra/modules/guard.bicep:11-39` / `infra/main.bicep:199-231` define `29` guard parameters.
  * `infra/tests/test_bicep_policy.py:2391` asserts `self.assertIn("Empty means", MAIN)`, matching `infra/main.bicep:189` (`Empty means the prerequisite was not reviewed, not that Azure approved it.`).
* Concern:
  Renaming `maxVCores` to `sqlVCores` in `infra/modules/sql.bicep` breaks `infra/main.bicep:341` and `infra/tests/test_sql_tier.py:37`, while searching for `sqlVCores` in `infra/modules/sql.bicep` misses the parameter altogether. Propagating `monthlyBudget = 150` or `28` baseline guards into `P02-T01` architecture tables and `P03-T01` documentation-parity tests would either fail against `infra/main.bicep` or codify false template defaults, and editing `infra/main.bicep:189` without keeping `"Empty means"` breaks `test_bicep_policy.py:2391`.
* Impact:
  Module compilation or `test_sql_tier.py` / `test_bicep_policy.py` regressions fail during `P01`, or `P02`/`P03` publish inaccurate parameter and guard counts.
* Smallest useful change:
  Update `Scope`, `FR-1`, `P01`, and `P01-T01` to decorate `param sqlVCores int = 2` in `infra/main.bicep:111` and `param maxVCores int = 2` in `infra/modules/sql.bicep:20` with `@minValue(1) @maxValue(80)` (preserving the `maxVCores` parameter name and `"Empty means"` in `infra/main.bicep:189`), and record `monthlyBudget = 300` and `29` existing `guard.bicep` parameters (`31` total after adding the two new guards) in `P01-T01`, `P02-T01`, and `P03-T01`.
* Resolving evidence:
  Updated `FR-1`, `P01`, `P01-T01`, `P02-T01`, and `P03-T01` naming `maxVCores` in `infra/modules/sql.bicep:20`, `monthlyBudget = 300`, `29 -> 31` `guard.bicep` boolean parameters, and preservation of `"Empty means"` in `infra/main.bicep`.

### PC-003: Raw substring token stripping causes false positives on valid repository anchors (`spending`, `appending`, `jtbd`), `P01-T01` omits UUID hyphen positions `8-4-4-4-12`, and `FR-3` / `AC-2` overstate Bicep embedded-UUID detection

* Severity: High
* Related IDs: `FR-3`, `AC-2`, `AC-4`, `P01`, `P01-T01`, `P01-T02`, `P03-T01`, `C2`, `C5`, `C6`, `C7`
* Action owner: planning parent
* Decision route: direct planner correction
* Evidence:
  * `.copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md:45-56` (`P01-T01`) defines `var forbiddenCheckSubstrings = ['placeholder', 'todo', 'tbd', 'assumed', 'assumption', 'unverified', 'pending', 'unknown', 'example.invalid']` and tests `reduce(forbiddenCheckSubstrings, normalizedCheck, (cur, token) => replace(cur, token, '')) == normalizedCheck`, while lines `107-108` (`P01-T02`) apply case-insensitive substring matching for those tokens plus `n/a`, `none`, and `skip`.
  * Although zero of the 74 standard Azure region slugs match `forbiddenCheckSubstrings`, raw substring matching on check references collides with existing repository section anchors and English words: `"pending"` matches `"spending"` (`infra/README.md:332` `#cost-proposal-not-a-quote-or-spending-approval`) and `"appending"` (`docs/architecture/cutover-evidence-pack.md:21` `#statements-of-the-section-above-reconciled-by-appending`), `"tbd"` matches `"jtbd"` (`docs/reference/research/ux/resident-demo-redesign-2026-11-04.md:45` `#jobs-to-be-done-jtbd-analysis`), and naive substring matching of `"none"`, `"na"`, or `"skip"` collides with normal words (`"governance"`, `"canary"`, `"snapshot"`).
  * `.copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md:54-56` checks `length(normalizedCheck) == 36 && length(split(normalizedCheck, '-')) == 5 && empty(reduce(uuidHexCharacters, ...))` without checking exact hyphen indices, unlike `infra/public-edge-existing.bicep:30` (`take(skip(..., 8), 1) == '-' && take(skip(..., 13), 1) == '-' && take(skip(..., 18), 1) == '-' && take(skip(..., 23), 1) == '-'`). Any 36-character dated hex string with four hyphens at other positions (for example `'2026-11-15-01-a1b2c3d4e5f60123456789'`) is falsely rejected as a UUID.
  * `.copilot-tracking/plans/2026-11-15/infra-137-env-quotas-plan.md:64,72` (`FR-3`, `AC-2`) state that `infra/main.bicep`, `pipeline.py`, and `deploy.py` all reject "UUID-bearing" check references, whereas Bicep in `P01-T01` has no regex engine (`infra/tests/test_bicep_policy.py:125-166`) and only detects bare 36-character UUIDs (plus embedded `'00000000-0000-0000-0000-000000000000'` if checked with `contains`), while Python `re.search` detects both bare and prose-embedded UUIDs.
* Concern:
  Valid repo-tracked check references pointing to anchors containing `spending`, `appending`, `jtbd`, or 36-character dated commit-prefix slugs will fail deployment preflight, while `P03-T01` tests written directly from `AC-2` ("UUID-bearing" in `main.bicep`) will fail when passing an embedded non-zero UUID to `evaluate()` in `infra/main.bicep`.
* Impact:
  False-positive deployment blockages on legitimate check anchors and self-contradictory `P03-T01` assertions between `FR-3`/`AC-2` and `P01-T01`.
* Smallest useful change:
  1. In `P01-T01` (`infra/main.bicep`), replace punctuation delimiters (`'-'`, `'_'`, `'/'`, `'#'`, `'.'`, `':'`, `','`, `';'`, `'('`, `')'`) in `normalizedRegionCheck` / `normalizedQuotaCheck` with `' '` via `reduce(['-', '_', '/', '#', '.', ':', ',', ';', '(', ')'], normalizedCheck, (cur, ch) => replace(cur, ch, ' '))`, `split(..., ' ')` into delimited word tokens, and require `empty(filter(forbiddenCheckWords, word => contains(checkWords, word)))` for word-bounded markers (`['todo', 'tbd', 'assumed', 'assumption', 'unverified', 'pending', 'unknown', 'none', 'na', 'skip']`) combined with substring checks `!contains(normalizedCheck, 'placeholder') && !contains(normalizedCheck, 'example.invalid') && !contains(normalizedCheck, 'n/a') && !contains(normalizedCheck, '00000000-0000-0000-0000-000000000000')` (note `filter`, `reduce`, `replace`, `split`, `contains`, `take`, `skip`, `empty`, `length`, `toLower`, and `trim` are all supported by `infra/tests/test_bicep_policy.py:125-166`).
  2. Add the four exact hyphen-position checks `take(skip(normalizedCheck, 8), 1) == '-' && take(skip(normalizedCheck, 13), 1) == '-' && take(skip(normalizedCheck, 18), 1) == '-' && take(skip(normalizedCheck, 23), 1) == '-'` from `infra/public-edge-existing.bicep:30` to the 36-character Bicep UUID guard.
  3. In `P01-T02` (`pipeline.py` and `deploy.py`), use word-bounded regex `r"(?i)(?:placeholder|example\.invalid|n/a|\b(?:todo|tbd|assumed|assumption|unverified|pending|unknown|none|na|skip)\b)"` and UUID regex `r"(?i)\b[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}\b"`, and clarify in `FR-3`, `AC-2`, and `P03-T01` that Bicep rejects bare 36-character UUIDs and embedded all-zero GUIDs while `pipeline.py` and `deploy.py` reject all bare and embedded UUIDs. (Include positive regression cases in `P03-T01` for anchors containing `spending` and `jtbd`.)
* Resolving evidence:
  Updated `FR-3`, `AC-2`, `P01-T01`, `P01-T02`, and `P03-T01` specifying word-tokenized Bicep checks, `8-4-4-4-12` UUID hyphen-index checks, word-bounded Python regexes, and accurate Bicep vs Python UUID scope.

### PC-004: `sqlLocation` and `location` validation bypasses across `main.bicep`, `pipeline.py`, and `deploy.py`, duplicate `--parameter` shadowing, and CLI error/file contract defects

* Severity: High
* Related IDs: `FR-3`, `AC-2`, `AC-4`, `AC-5`, `P01`, `P01-T01`, `P01-T02`, `P03-T01`, `C2`, `C5`, `C6`, `C7`, `C11`, `C12`
* Action owner: planning parent
* Decision route: direct planner correction
* Evidence:
  * `.copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md:57-59` (`P01-T01`) checks `normalizedSqlLocation` only for non-empty and forbidden substrings; malformed inputs such as `'has spaces'`, `'UPPERCASE'`, `'12345'`, `'uksouth/bad'`, or a bare UUID `'12345678-1234-1234-1234-123456789abc'` still satisfy `deploymentLocationsMustBeSelected`. Meanwhile, `infra/tests/test_bicep_policy.py:1219,2400` passes synthetic `'offline-region'` and `'offline-sql-region'`, so Bicep must continue to accept hyphenated lowercase region slugs.
  * In `infra/scripts/pipeline.py:135-146` and `.copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md:105-115` (`P01-T02`), lowercase placeholder and assumption words (`"placeholder"`, `"todo"`, `"tbd"`, `"assumed"`, `"assumption"`, `"unverified"`, `"pending"`, `"unknown"`, `"none"`, `"na"`, `"skip"`) all match `r"^[a-z][a-z0-9]+$"`. Because `pipeline.py:135` checks uppercase `"PLACEHOLDER"` only and `P01-T02` applies `validate_check_reference` only to `regionCheckReference`/`quotaCheckReference`, `"sqlLocation": "placeholder"` or `"assumed"` passes both `pipeline.parameters()` and `deploy.py --parameter sqlLocation=placeholder`, and `pipeline.parameters()` never checks `location == "uksouth"`.
  * `.copilot-tracking/plans/2026-11-15/infra-137-env-quotas-plan.md:16` ("Executive Summary" item 3) states `deploy.py` validates "compiled parameter sets", whereas `infra/tests/test_deploy.py:79` passes `--parameters private.bicepparam` without creating `private.bicepparam` on disk; reading `--parameters` in `deploy.py` breaks `test_deploy.py`. Also `args.parameter` in `infra/scripts/deploy.py:187` is `list[tuple[str, str]]`, so converting to `dict` before validation silently skips duplicate earlier invalid `--parameter` flags.
  * `infra/scripts/pipeline.py:2,127-148,373` prints `PipelineError` messages to `sys.stderr` under a strict no-identifier-leakage contract ("Never publish resource IDs, names, deltas, parameters or Azure messages").
* Concern:
  `FR-3` and `AC-2` explicitly require `main.bicep`, `pipeline.py`, and `deploy.py` to reject placeholder, assumption-word, and invalid-slug `location` / `sqlLocation` inputs, yet all three layers currently leave concrete bypasses; reading `--parameters` in `deploy.py` breaks `test_deploy.py:79`; and interpolating raw parameter values into `PipelineError` or `DeploymentError` messages leaks pasted subscription/tenant UUIDs to stderr.
* Impact:
  Placeholder/assumed regions (`sqlLocation=placeholder`, `sqlLocation=assumed`) or malformed Bicep `sqlLocation` strings slip past preflight guards, `test_deploy.py` breaks if `deploy.py` inspects `--parameters`, or rejected UUIDs leak to logs.
* Smallest useful change:
  1. In `P01-T01` (`infra/main.bicep`), require `sqlLocation == normalizedSqlLocation` (rejecting uppercase and leading/trailing whitespace), `length(normalizedSqlLocation) >= 3`, leading lowercase ASCII letter (`contains('abcdefghijklmnopqrstuvwxyz', take(normalizedSqlLocation, 1))`), allowed characters `'abcdefghijklmnopqrstuvwxyz0123456789-'` (`empty(reduce(regionSlugChars, normalizedSqlLocation, (cur, ch) => replace(cur, ch, '')))`), `!contains(normalizedSqlLocation, '--')`, `!endsWith(normalizedSqlLocation, '-')`, non-UUID, and exclusion of forbidden placeholder/assumption words (`placeholder`, `todo`, `tbd`, `assumed`, `assumption`, `unverified`, `pending`, `unknown`, `none`, `na`, `skip`). This preserves `'uksouth'`, `'ukwest'`, `'offline-region'`, and `'offline-sql-region'` while rejecting spaces, uppercase, digits-only, punctuation, UUIDs, and assumption words.
  2. In `P01-T02` (`pipeline.py` and `deploy.py`), enforce `location == "uksouth"`, `sqlLocation` matching `^[a-z][a-z0-9]+$`, and explicit rejection of the forbidden placeholder/assumption word set on `sqlLocation` (and `location`).
  3. In `deploy.py`, iterate over every `(name, value)` pair in `args.parameter` without collapsing duplicates via `dict(...)` and without reading `--parameters` from disk; remove "compiled parameter sets" from `deploy.py`'s description in `plan.md:16`.
  4. Require `PipelineError` and `DeploymentError` messages in `P01-T02` to include only the offending parameter key, never echoing the raw `value`.
* Resolving evidence:
  Updated `plan.md:16`, `P01-T01`, `P01-T02`, and `P03-T01` covering Bicep `sqlLocation` slug/token validation (compatible with `'offline-region'`), CLI `location == "uksouth"` and forbidden-region-word rejection, full `args.parameter` list iteration in `deploy.py`, and value-free exception messages.

### PC-005: `P03` / `P03-T01` misstates non-`--isolated` `ruff check` exit status, short-circuits `ruff format --check` behind `&&`, and omits required `src/*` package installation before `infra/tests/` discovery

* Severity: High
* Related IDs: `NFR-1`, `NFR-2`, `AC-4`, `P03`, `P03-T01`, `C18`
* Action owner: planning parent
* Decision route: direct planner correction
* Evidence:
  * `.copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md:263` asserts that bare `python3 -m ruff check infra/tests/test_environment_quota_parameters.py infra/scripts/deploy.py infra/scripts/pipeline.py` exits `0`. Empirical check in this workspace shows non-`--isolated` `python3 -m ruff check infra/scripts/deploy.py infra/scripts/pipeline.py` exits `1` with 3 pre-existing errors on untouched lines (`EXE001` on `infra/scripts/deploy.py:1` and `infra/scripts/pipeline.py:1` due to `0644` permissions with shebangs, and `SIM102` on `infra/scripts/pipeline.py:251`), while `python3 -m ruff check infra` exits `1` with 112 pre-existing errors across `infra/`.
  * `.github/workflows/src-ci.yml:226-228` invokes Ruff with `--isolated --select E,F,I,B,UP --target-version py312 --line-length 100`, which exits `0` on `deploy.py` and `pipeline.py`.
  * Chaining `python3 -m ruff check infra && python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_environment_quota_parameters.py` as a single `&&` shell command stops after `ruff check infra` exits `1` and never executes `ruff format --check`.
  * `.copilot-tracking/plans/2026-11-15/infra-137-env-quotas-plan.md:57` claims "`src/*` distributions check needed only if `test_bicep_policy.py` imports `zava_forward`", and `phase-details.md:258` runs `REQUIRE_AZ_BICEP=1 python3 -m unittest discover -s infra/tests -q` directly. Under system `python3` without `src/*` installed, both `infra/tests/test_bicep_policy.py:1159` (`from zava_forward.orchestrator import digest_blob`) and `infra/tests/test_pipeline.py:905` (`subprocess.Popen([sys.executable, "-m", "zava_forward.api"])`) fail (`ModuleNotFoundError` and local API smoke startup failure), matching `.github/workflows/src-ci.yml:206,222-224` and repository instructions requiring pip installation of `src/<project>` distributions before running infra suites.
* Concern:
  Following `P03-T01` verbatim causes false red gates during implementation verification (`ruff check` on `deploy.py`/`pipeline.py`, skipped `ruff format --check`, and `ModuleNotFoundError` in `test_bicep_policy.py` and `test_pipeline.py`) or tempts an implementer to make out-of-scope file-mode/refactor edits across `infra/`.
* Impact:
  `P03` validation fails or leaves `ruff format --check` unexecuted.
* Smallest useful change:
  Revise `Dependencies`, `NFR-2`, `AC-4`, `P03`, and `P03-T01` so that:
  1. `infra/tests/test_environment_quota_parameters.py` is authored without a `#!/usr/bin/env python3` shebang and without importing `zava_forward`, ensuring standalone `python3 -m unittest infra/tests/test_environment_quota_parameters.py -q`, bare `python3 -m ruff check infra/tests/test_environment_quota_parameters.py`, and `python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_environment_quota_parameters.py` all exit `0` under system `python3`.
  2. `ruff format --isolated --line-length 100 --check` and `src-ci.yml`'s `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` are run explicitly (not gated behind `python3 -m ruff check infra && ...`) across `infra/tests/test_environment_quota_parameters.py`, `infra/scripts/deploy.py`, and `infra/scripts/pipeline.py` (all exiting `0`), while bare `python3 -m ruff check infra` is also executed and inspected to verify zero diagnostics on `test_environment_quota_parameters.py` and zero new diagnostics on modified lines of `deploy.py` and `pipeline.py`.
  3. Before running full `REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -q`, ensure an isolated/external Python virtual environment (not inside `/tmp` and not committed to Git) has `pip install -e src/core -e src/agents -e src/api -e src/orchestrator -e src/importer` plus `PyYAML==6.0.3` and `src/api/requirements.txt` installed per `.github/workflows/src-ci.yml:206,222-223`, and remove any transient venv or `.ruff_cache` before `git status` verification.
* Resolving evidence:
  Updated `Dependencies`, `NFR-2`, `AC-4`, `P03`, and `P03-T01` documenting the exact `ruff` command separation, no-shebang/stdlib-only rule for `test_environment_quota_parameters.py`, and `src/*` editable pip prerequisite for full `infra/tests` discovery.

### PC-006: `P02-T01` and `P03-T01` risk false test failure on existing `.copilot-tracking/` links in `docs/architecture/README.md` and honesty drift against historical `2026-10-18` `R4`/`R8`/`R9` SKU checks

* Severity: Medium
* Related IDs: `FR-4`, `AC-3`, `AC-5`, `P02`, `P02-T01`, `P03-T01`, `C16`, `C17`
* Action owner: planning parent
* Decision route: direct planner correction
* Evidence:
  * `.copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md:223` (`P03-T01`) specifies asserting "absence of `.copilot-tracking/` leaks" across documentation, whereas `docs/architecture/README.md:25,79,355,359,371` already contains five committed historical `.copilot-tracking/` references.
  * `infra/README.md:1044-1058` (`### Read-only pilot capability and quota evidence (2026-10-18, Refs #137)`) is anchored to historical commit `612cbed78a35a4ab426571aa7d2aeb0ae6d691dd` and `main.bicep` SHA-256 `daea1e37adc95f704fba7673883e0b4b6c7b654ab00179b59d8473654ab71f42a`, where `R4` queried `GP_S_Gen5_2` (serverless SQL) and `R8`/`R9` queried `gpt-4.1-mini` and `gpt-4.1` (`capacity = 30`). Neither `GP_Gen5` (provisioned SQL in `infra/main.pilot.example.bicepparam:19`) nor `gpt-4.1-nano` (`capacity = 1` in `infra/main.bicep:92-93`) was queried in that `2026-10-18` snapshot.
  * Existing tests lock specific substrings in `infra/README.md`: `infra/tests/test_governance.py:82-84` asserts `"DoNotEnforce"` and `"until the owner accepts a cost"`, and `infra/tests/test_container_hosting_completeness.py:137-160` asserts `"Revision rollback:"`, `"not at declared scale"`, and `"makes no production"`.
* Concern:
  A blanket `".copilot-tracking/" not in text` assertion on `docs/architecture/README.md` fails immediately on pre-existing lines, rewriting the `2026-10-18` SHA-256 paragraph or implying `2026-10-18` `R4`/`R8`/`R9` verified `GP_Gen5` or `gpt-4.1-nano` violates `AC-5` honesty rules, and accidentally editing locked phrases in `infra/README.md` breaks `test_governance.py` or `test_container_hosting_completeness.py`.
* Impact:
  `test_environment_quota_parameters.py` or `test_governance.py` / `test_container_hosting_completeness.py` fails, or architecture docs overstate what the `2026-10-18` `R1`..`R17` snapshot proved.
* Smallest useful change:
  1. Scope `P03-T01`'s `.copilot-tracking/` leak assertion to `docs/architecture/environment-region-quota-strategy.md`, the `## Environments` section of `infra/README.md`, and the newly added index bullet in `docs/architecture/README.md` (not pre-existing historical lines in `docs/architecture/README.md`).
  2. Specify in `P02-T01` that `infra/README.md:1044-1058` remains explicitly attributed to historical commit `612cbed7` (`2026-10-18`), while both `docs/architecture/environment-region-quota-strategy.md` and `infra/README.md` state clearly that `GP_Gen5` (pilot example provisioned SQL) and `gpt-4.1-nano` (current default model) post-date the `2026-10-18` `R4`/`R8`/`R9` checks and remain `Unknown` until fresh `R4`/`R8`/`R9` queries are recorded for the target subscription.
  3. Explicitly preserve `infra/README.md` phrases checked by `test_governance.py:82-84` and `test_container_hosting_completeness.py:137-160`.
* Resolving evidence:
  Updated `P02-T01` and `P03-T01` scoping the `.copilot-tracking/` check, preserving historical `612cbed7` provenance while marking `GP_Gen5` and `gpt-4.1-nano` as `Unknown` pending fresh `R4`/`R8`/`R9` runs, and listing the locked `infra/README.md` phrases.

## Residual Risks and Limitations

* Offline Bicep expressions cannot resolve whether a path#anchor string inside `regionCheckReference` or `quotaCheckReference` exists on disk or whether its contents were freshly executed against the target Azure subscription; human review and CI/operator verification remain mandatory alongside mechanical guards (`infra/README.md:1027-1033`).
* No live Azure CLI capability or quota queries were executed during this critique; subscription-specific regional quota availability for `uksouth`, `ukwest`, `GP_Gen5`, and `gpt-4.1-nano` remains `Unknown` outside the historical `2026-10-18` (`612cbed7`) receipt scope.
* Existing `infra/tests/*.py` files remain locked against modification (`NFR-1`) to prevent merge conflicts across stacked branches (`origin/feat/demo-164-chat-grounding-provenance-0900`, PR `#1641`).

## Handoff

* Verdict returned to `planning parent`: Revise (`Complete` single-pass critique; `1` Critical, `4` High, `1` Medium, `0` Low findings; user response required: `no`).
* All six findings (`PC-001` through `PC-006`) are deterministic `direct planner correction` items resolvable from repository evidence without user escalation.
* Once the planning parent updates `.copilot-tracking/plans/2026-11-15/infra-137-env-quotas-plan.md` and `.copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md` against the resolving evidence for `PC-001` through `PC-006`, planning can finalize directly without another critique pass and proceed to `rpi-implement`.
