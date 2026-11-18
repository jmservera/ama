<!-- markdownlint-disable-file -->

# Task Research: immutable-blob-ledger-digests-115

| Field              | Value                                                                                   |
|--------------------|-----------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                              |
| Researcher / agent | rpi-research (RPI Agent automatic session)                                              |
| Status             | Complete                                                                                |
| Artifact path      | .copilot-tracking/research/2026-11-15/immutable-blob-ledger-digests-115-research.md     |

## Research Brief

* What to research: Existing ledger digest publication, remote immutable Blob container retention-lock modeling/verification, and scheduled verification mismatch alerting across `src/core` and `infra/` for Issue #115 (`Immutable Blob ledger digests and scheduled verification`), grounded in `docs/adrs/0002-pilot-readiness-architecture.md` (Decision 2, DH-007).
* Why it matters: Issue #115 requires deterministic offline/Bicep enforcement and scheduled verification mismatch alerting so that immutable container retention lock policy and scheduled mismatch alert behavior are explicitly enforced and tested in `src/core/tests/` and/or `infra/tests/`, without overclaiming owner-approved live retention lock irreversibility or live hosted monitoring acceptance.
* Audience or intended use: Planning (`rpi-plan`), independent plan critique (`rpi-plan-critique`), implementation (`rpi-implement`), and review (`rpi-review`) in this automatic RPI loop.
* Scope: `src/core/` (ledger digest publication, verification, CLI/scheduled entrypoints, alerting), `src/core/tests/`, `infra/` (Bicep storage/container immutability policies, scheduled verification job/alert infrastructure, deployment/validation scripts), `infra/tests/`, and `docs/adrs/0002-pilot-readiness-architecture.md`.
* Non-goals: Pushing to remote, running `tools/rpi-checks.py`, claiming `Closes #115` when live hosted acceptance or irreversible owner-locked retention gates remain human-owned, or altering unrelated application modules (`src/api`, `src/agents`, web UI).
* Criteria: Every research question answered with exact `path:line` codebase evidence (`C#`), clear identification of gaps between current `src/core` + `infra/` enforcement and Issue #115's two criteria, evaluated design alternatives with convergence selection, and verified focused test/type/lint commands.
* Requested outputs: Primary research artifact in convergence mode with concrete implementation recommendation and file-level impact for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                               |
|--------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | How do `src/core` and `infra/` currently model, enforce, and test immutable Blob ledger container retention-lock policies and scheduled digest verification mismatch alerts, and what exact gaps can be closed deterministically offline? |
| Codebase scope                       | `src/core/`, `infra/`, `docs/adrs/0002-pilot-readiness-architecture.md`, `docs/architecture/`                                       |
| External scope                       | none (internal repository architecture, Python `src/core`, and Azure Bicep templates/tests in workspace)                            |
| Initial internal candidate areas     | `docs/adrs/0002-pilot-readiness-architecture.md`, `src/core/`, `src/core/tests/`, `infra/`, `infra/tests/`                          |
| Initial external candidate areas     | none                                                                                                                                |
| Research posture                     | balanced                                                                                                                            |
| Posture provenance                   | default (bounded internal task with named targets `src/core` and `infra/`, plus adjacent contract coupling between Bicep and Python) |
| Explicit limits / deadline           | Single continuous non-interactive RPI run; focused validation tier (`src/core` and `infra/tests` unit tests, `ruff`, `mypy`); no `tools/rpi-checks.py`; do not push |
| Posture-specific completion basis    | balanced scope coverage and adequate evidence across `src/core`, `infra/`, ADR-0002, and test suites                                |
| Edits allowed during research?       | no, research-only                                                                                                                   |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                                |
| Known constraints / excluded sources | Do not read private datasets; preserve existing workflow/check names; commit with `Refs #115` (not `Closes #115` unless every live/human criterion is met) |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                      | Match and provenance                                           | Scoped authority or output contract                                         | Selected / skipped reason                                                                 |
|---------------------|------------------------------------------------|----------------------------------------------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` (custom)     | `applyTo: "**"` matches all repository paths and tracking root | Enforces AMA evidence boundaries, focused validation tier, `Refs #115` rule | Selected: mandatory repository governance                                                 |
| Skill               | `rpi-research`                                 | Invoked directly for Research phase                            | Three-wave evidence collection and primary research artifact                | Selected: active phase skill                                                              |
| Skill               | `python-foundational` / `secure-by-design`     | Adjacent Python and security domain skills                     | Optional coding guidance                                                    | Skipped during Research: direct inspection of existing `src/core` and `infra` suffices    |
| Research specialist | `hve-core-all:rpi-researcher`                  | Registered subagent for independent research lanes             | Writes lane artifact under `.copilot-tracking/research/subagents/`          | Skipped (inline fallback): `src/core` and `infra/` digest contracts are tightly coupled and small enough for direct, exact inspection |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                  | Answers / unanswered | Resulting decision or selected further research                                              |
|------------------|------------------------------------------------------------------------------------------------------------------------|----------------------|----------------------------------------------------------------------------------------------|
| Intake           | Caller specified exact target (Issue #115), paths (`src/core`, `infra/`), validation tier (focused), and non-stop flow | N/A (non-interactive) | Proceed in balanced convergence mode with inline three-wave inspection                       |
| Direction change | None: scope remained within `src/core`, `infra/`, and focused test suites after checking `src/orchestrator/digest_blob.py` contract coupling | N/A | Keep dependency-clean contract in `src/core` and Bicep/policy-test enforcement in `infra/` |
| Convergence      | Evidence across `src/core`, `src/orchestrator`, and `infra/` supports a single typed `src/core` Blob ledger digest retention-lock & scheduled alert contract plus tightened Bicep wiring and mutation tests | N/A | Selected Approach A (typed `src/core` retention-lock & scheduled mismatch verifier + Bicep parameter/output/policy hardening) |

## Scope and Success Criteria

* Scope: Inspect `docs/adrs/0002-pilot-readiness-architecture.md`, `src/core` ledger digest/remote verification modules and tests, and `infra/` Bicep/scripts and `infra/tests/` to identify and design deterministic enforcement for immutable container retention lock policy and scheduled mismatch alerting.
* Assumptions:
  * Verified and refined: PR #404 create-only remote digest publication and malformed head/year anchor rejection live in `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py`, not `src/core`, whereas `src/core` only contains local file digest helpers in `ledger.py` (`C2`, `C4`).
  * Verified: Both `src/core` and `infra/` have concrete deterministic gaps around immutable retention-lock policy verification and scheduled mismatch alert enforcement/mutation testing (`C4`, `C5`, `C7`, `C8`, `C11`, `C12`, `C13`).
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and one recommendation is selected in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  1. Inspect existing ledger digest publication and verification in `src/core` and `infra/` for Issue #115 (`Digests land in an immutable container with a retention lock` and `Scheduled verification alerts on mismatch`).
  2. Determine how to strengthen deterministic offline/Bicep verification and scheduled mismatch alerting so both policies/behaviors are explicitly enforced and tested in `src/core/tests/` and/or `infra/tests/`.
* Inferred research questions:
  * Q1: What does ADR-0002 Decision 2 and DH-007 specify for immutable Blob ledger digests, retention locks, and scheduled verification alerts?
  * Q2: How does `src/core` currently implement ledger digest publication, container immutability/retention-lock verification, scheduled verification execution, and mismatch alerting?
  * Q3: How does `infra/` (Bicep modules, scripts, parameters, alerts, scheduled jobs) currently provision the ledger digest Blob container, immutability policy / retention lock, scheduled verification job, and mismatch alert rules?
  * Q4: What tests currently exist in `src/core/tests/` and `infra/tests/`, and what exact gaps exist in enforcing retention-lock state and scheduled mismatch alerting?
* Caller constraints and non-goals: Focused validation tier only (`src/core` tests, `infra/tests`, `ruff`, `mypy`); do not run `tools/rpi-checks.py`; do not push; use `Refs #115`.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                 | Source / checkpoint | Effect on active brief, evidence, or revalidation                         |
|----------------------------------------------------------|---------------------------------------------------------------------------------------|---------------------|---------------------------------------------------------------------------|
| narrow                                                   | Restrict scope to `src/core`, `infra/`, and tests for Issue #115                      | Caller intake       | Focus waves on ledger digest code, Bicep/infra definitions, and test suites |
| exclude                                                  | Do not run `tools/rpi-checks.py` and do not push to remote                            | Caller intake       | Validation planning uses focused unit tests, `mypy`, and `ruff` only      |

## Research Questions

|  # | Sub-question                                                                                                                      | Type            | Priority | Status   |
|---:|-----------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | What architectural contracts do ADR-0002 (Decision 2, DH-007) and related docs define for immutable ledger digests and alerting?  | straightforward | H        | answered |
| Q2 | How does `src/core` implement remote ledger digest publication, container retention-lock checks, and scheduled mismatch alerting? | depth           | H        | answered |
| Q3 | How does `infra/` provision the immutable Blob container, retention-lock policy, scheduled verifier, and mismatch monitor/alert?  | depth           | H        | answered |
| Q4 | What offline assertions exist in `src/core/tests/` and `infra/tests/`, and what concrete gaps should Issue #115 close now?        | breadth         | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: Issue #115 body, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`.
* Reused (verified) findings: Issue #115 notes that PR #404 added create-only digest publication/verification and malformed remote anchor rejection with explicit alerts and nonzero exit, while owner-approved retention duration/irreversible lock evidence and live hosted acceptance remain open.
* Superseded / stale: Legacy `mvp/` label description (`Part of this exists in mvp/`) predates the 2026-10-27 cut-over to `src/`; post-cut-over remote digest code lives in `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py` (`C4`) and has not yet been elevated into a typed `src/core` contract (`C2`, `C6`).

## Research Cycle Log

### Cycle 1

* **Wave 1 — Wider (inline)**:
  * Surveyed ADR-0002 Decision 2 and DH-007 (`C1`), `src/core` modules (`ledger.py`, `documents.py`, `ranking_archive_blob.py`, `monitoring_coverage.py`) (`C2`, `C3`, `C5`, `C6`), `src/orchestrator` (`digest_blob.py` and `test_digest_blob.py`) (`C4`), and `infra/` Bicep modules (`main.bicep`, `modules/storage.bicep`, `modules/containerapps.bicep`, `modules/guard.bicep`, `modules/operationalMonitoring.bicep`, `monitoring-runbooks.md`) (`C7`–`C11`).
  * Established how the sister immutable archive (`ranking_archive_blob.py`, Issue #1258) bridges `src/core` provider constants, in-memory Blob REST testing (`ranking_blob_fixture.py`), and `infra/tests/test_bicep_policy.py` (`C5`, `C14`, `C17`).
* **Wave 2 — Deeper (inline)**:
  * Inspected `src/core/src/zava_forward/core/ledger.py` (`C2`) and `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py` (`C4`) line by line:
    * `src/core` has zero Blob ledger digest publication, container retention-lock policy verification, blob immutability response-header enforcement (`x-ms-immutability-policy-mode`, `x-ms-immutability-policy-until-date`), or scheduled verification mismatch alert evaluation.
    * `digest_blob.py` (`src/orchestrator`, excluded from strict `mypy`) writes `If-None-Match: *` blobs and checks hash chains/anchors, yet never inspects container immutability policy lock state (`Locked` vs `Unlocked`, retention days, `allowProtectedAppendWrites`, `allowProtectedAppendWritesAll`) or blob-level immutability headers.
  * Inspected `infra/modules/storage.bicep`, `infra/main.bicep`, `infra/modules/containerapps.bicep`, and `infra/tests/test_bicep_policy.py` (`C7`–`C15`):
    * `storage.bicep` declares `digestRetention` on `blobContainers[5]` (`ledger-digests`) with `immutabilityPeriodSinceCreationInDays: ledgerDigestImmutabilityDays` (`@minValue(1)`, default `365`) and `allowProtectedAppendWrites: false` (`C7`), without explicitly setting `allowProtectedAppendWritesAll: false` or exporting `ledgerDigestContainer` (`C7`).
    * `main.bicep` never exposes `ledgerDigestImmutabilityDays` or passes it to `modules/storage.bicep` (`C8`), nor does it wire `storage.outputs.ledgerDigestContainer` into `modules/containerapps.bicep` (which hardcodes `'ledger-digests'` at line 453, unlike `rankingArchiveContainer` which comes from `storage.outputs`) (`C8`, `C9`).
    * `test_bicep_policy.py` checks only basic `immutabilityPolicies` presence and KQL marker substrings (`LEDGER_DIGEST_ALERT`, `LEDGER_DIGEST_OK`), without checking scheduled alert operators/thresholds/severities/windows/scopes/actions, `ledgerVerify` cron/retry/container/command contracts, or mutating append-write overrides and ledger mismatch alert rules (`C12`, `C13`, `C15`).
* **Wave 3 — Contrarian (inline)**:
  * Tested the hypothesis of setting `state: 'Locked'` directly in `storage.bicep` `immutabilityPolicies`: rejected by contrarian evidence in `infra/tests/test_bicep_policy.py:2032` (`self.assertNotIn("state", policy["properties"])`) and `infra/modules/storage.bicep:6` (`C7`, `C14`). In Azure Storage ARM (`Microsoft.Storage/storageAccounts/blobServices/containers/immutabilityPolicies@2024-01-01`), `state` is read-only on `PUT` (`Unlocked` at creation; irreversible locking requires the post-deployment `lockImmutabilityPolicy` action with `If-Match` ETag after Legal approves retention duration). Setting `state: 'Locked'` in Bicep would misrepresent ARM semantics and violate repository governance (`C1`, `C7`, `C14`).
  * Checked dependency rules (`src/core/tests/test_dependency_rule.py`, `C16`), live Markdown link rules (`src/core/tests/test_live_doc_links.py`, `C18`), `src/core/pyproject.toml` strict `mypy`/`ruff` rules, and `tools/rpi-checks.py` `RUFF_GROUPS`/`TYPE_GROUPS` flags (`--select E,F,I,B,UP --target-version py312 --line-length 100`) so changes remain zero-regression across CI workflows (`C16`, `C18`).
* **Parent Synthesis & Re-entry Decision**:
  * All four research questions (Q1–Q4) are answered with primary `path:line` evidence (`C1`–`C18`); contrarian wave prevented an invalid ARM `state` property design and confirmed clean boundaries between offline deterministic contracts and human/live operational gates. No second cycle needed.

## Evidence Log

| ID  | Location                                                                 | Summary of verified evidence                                                                                                                                      |
|-----|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| C1  | `docs/adrs/0002-pilot-readiness-architecture.md:83`                      | Decision 2 & DH-007 require periodic ledger chain digests in a separate immutable Blob container with time-based retention (`allowProtectedAppendWrites: false`), irreversible lock only after Legal sets duration, and scheduled verification alerting on mismatch or missing run. |
| C2  | `src/core/src/zava_forward/core/ledger.py:1`                             | `src/core` implements local SHA-256 hash-chain entries, `verify_entries`, `verify_years`, `make_digest`, and `make_year_digest`, with no Blob immutability or scheduled verification contract. |
| C3  | `src/core/src/zava_forward/core/documents.py:155`                        | `AzureBlobDocumentStore` implements HTTPS Blob REST transport (`API_VERSION = "2021-08-06"`), Entra MI bearer tokens, and `If-None-Match: *` create-only uploads, without inspecting container/blob immutability headers. |
| C4  | `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py:21`       | `digest_blob.py` defines `ALERT_MARKER = "LEDGER_DIGEST_ALERT"`, `OK_MARKER = "LEDGER_DIGEST_OK"`, `BlobDigestStore`, `publish`, `verify`, and `reconcile`, without verifying container retention-lock policy state or blob immutability headers. |
| C5  | `src/core/src/zava_forward/core/ranking_archive_blob.py:1`               | Sister `src/core` immutable Blob adapter showing strict `mypy` typing, secret-redacted `BlobArchiveError`, strict `<EnumerationResults>` XML validation, and shared Bicep provider constants. |
| C6  | `src/core/src/zava_forward/core/monitoring_coverage.py:42`               | Canonical alert coverage register includes `ledger-digest-mismatch` and `ledger-verify-missing` (`INSTALLED`, criterion `ledger`, source `main.bicep`) plus `sanitise_diagnostic_event`. |
| C7  | `infra/modules/storage.bicep:6`                                          | Declares `ledger-digests` (`blobContainers[5]`) and `digestRetention` (`immutabilityPeriodSinceCreationInDays: ledgerDigestImmutabilityDays`, `allowProtectedAppendWrites: false`), notes locking is an irreversible owner action, omits `allowProtectedAppendWritesAll: false` and `ledgerDigestContainer` output, and scopes `staffResultsLifecycle` deletion to `staff-results/`. |
| C8  | `infra/main.bicep:275`                                                   | `main.bicep` wires `storage` without exposing or forwarding `ledgerDigestImmutabilityDays` and passes `apps` without wiring a `storage.outputs.ledgerDigestContainer` output. |
| C9  | `infra/modules/containerapps.bicep:422`                                  | `ledgerVerify` scheduled Container Apps job runs cron `'0 2 * * *'`, `replicaRetryLimit: 0`, `command: ['python', '-m', 'zava_forward.orchestrator.digest_blob', '--publish']`, with hardcoded `ZF_DIGEST_CONTAINER: 'ledger-digests'` at line 453. |
| C10 | `infra/main.bicep:593`                                                   | Defines `ledgerDigestMismatch` (Sev 1, `PT5M`/`PT15M`, `GreaterThan 0` on `ContainerAppConsoleLogs` `LEDGER_DIGEST_ALERT`) and `ledgerVerifyMissing` (Sev 2, `PT1H`/`P1D`, `LessThan 1` on `LEDGER_DIGEST_OK`). |
| C11 | `infra/monitoring-runbooks.md:107`                                       | Runbooks `ledger-digest-mismatch` and `ledger-verify-missing` specify `Proposed owner: Digital service owner`, SQL vs immutable Blob reconciliation, and immediate incident handling. |
| C12 | `infra/tests/test_bicep_policy.py:1143`                                  | Checks only that two `ledger-` `scheduledQueryRules` use `ContainerAppConsoleLogs` and match `ALERT_MARKER`/`OK_MARKER`, without asserting thresholds, operators, severities, windows, action groups, or `ledgerVerify` job wiring. |
| C13 | `infra/tests/test_bicep_policy.py:1966`                                  | `assert_retention_controls` checks `audit-archive` and `ledger-digests` immutability policies, while `test_mutations_reject_missing_wrong_or_zero_retention` (line 2660) never mutates `allowProtectedAppendWrites`, `allowProtectedAppendWritesAll`, `main.bicep` forwarding, or lifecycle rules. |
| C14 | `infra/tests/test_bicep_policy.py:1990`                                  | `test_ranking_archive_blob_wiring_is_opt_in_private_and_matches_the_provider` asserts `self.assertNotIn("state", policy["properties"])` and verifies Bicep-to-`src/core` constant/output alignment. |
| C15 | `infra/tests/test_alert_runbook_signal_matrix.py:25`                     | Maps `alert-${applicationPrefix}-ledger-digest-mismatch` and `alert-${applicationPrefix}-ledger-verify-missing` to runbook anchors and verifies alert Inventory/runbook alignment. |
| C16 | `src/core/tests/test_dependency_rule.py:8`                               | Enforces `ALLOWED = {"core"}`: `src/core` must never import `zava_forward.orchestrator` or any other workload package. |
| C17 | `src/core/tests/ranking_blob_fixture.py:22`                              | Provides deterministic in-memory HTTPS Blob REST mock pattern (`PUT` `If-None-Match: *`, `GET`, paginated `comp=list`, fault injection, secret-redaction checks). |
| C18 | `src/core/tests/test_live_doc_links.py:16`                               | Validates relative Markdown links across live repository documentation (`docs/`, `src/`, `infra/`), skipping `.copilot-tracking/`. |

## Findings Mapped to Questions and Evidence

* **Q1 (ADR-0002 & governance contract)**: ADR-0002 Decision 2 and DH-007 require periodic ledger chain digests in a separate private Blob container (`ledger-digests`) protected by a time-based WORM immutability policy with `allowProtectedAppendWrites: false` (unlike `audit-archive`, digests are create-only JSON blobs, never append blobs), an owner-executed irreversible retention lock once Legal sets the retention period, and a daily scheduled verifier job whose console markers trigger Azure Monitor alerts on any chain/anchor mismatch (`LEDGER_DIGEST_ALERT`, Sev 1) or missing clean verification (`LEDGER_DIGEST_OK` absent over 24h, Sev 2) (`C1`, `C7`, `C10`, `C11`).
* **Q2 (`src/core` gaps)**: `src/core` currently has only local JSONL digest/hash-chain primitives in `ledger.py` (`C2`) and static register entries in `monitoring_coverage.py` (`C6`). It lacks a typed (`mypy --strict`) Blob ledger digest module enforcing: (a) container/ARM retention-lock policy verification (`state == "Locked"`, `immutabilityPeriodSinceCreationInDays >= min_retention_days`, `allowProtectedAppendWrites is False`, `allowProtectedAppendWritesAll` not `True`, container public access disabled, no lifecycle deletion rule targeting `ledger-digests`), (b) Blob REST response immutability-lock header verification (`x-ms-immutability-policy-mode: locked` and valid future `x-ms-immutability-policy-until-date` when lock enforcement is required), and (c) create-only remote digest publication, full chain + remote head/year anchor verification, and deterministic scheduled verification evaluation emitting sanitized `LEDGER_DIGEST_ALERT` vs `LEDGER_DIGEST_OK` outcomes with runbook/owner attribution (`C2`–`C6`, `C16`).
* **Q3 (`infra/` Bicep gaps)**: `infra/modules/storage.bicep` declares `digestRetention` (`allowProtectedAppendWrites: false`), yet omits explicit `allowProtectedAppendWritesAll: false` and does not export `output ledgerDigestContainer string = blobContainers[5].name` (`C7`). `infra/main.bicep` omits `@minValue(1) param ledgerDigestImmutabilityDays int = 365`, never forwards it to `modules/storage.bicep`, and does not wire `storage.outputs.ledgerDigestContainer` into `modules/containerapps.bicep` (`C8`, `C9`).
* **Q4 (`src/core/tests/` & `infra/tests/` gaps)**: `src/core/tests/` has zero unit tests for immutable Blob ledger digest retention-lock verification or scheduled mismatch alerting (`C2`, `C17`). `infra/tests/test_bicep_policy.py` lacks full contract assertions and mutation rejection tests for: (a) `digestRetention` append-write mutations (`allowProtectedAppendWrites: true`, `allowProtectedAppendWritesAll: true`), `main.bicep` -> `storage.bicep` `ledgerDigestImmutabilityDays` wiring, `storage.bicep` -> `containerapps.bicep` `ledgerDigestContainer` (`ZF_DIGEST_CONTAINER`) wiring, and `staffResultsLifecycle` prefix isolation; and (b) `ledgerDigestMismatch` / `ledgerVerifyMissing` alert operators, thresholds, severities, windows, scopes, action groups, and `ledgerVerify` scheduled job cron/retry/command mutations (`C12`, `C13`, `C14`).

## Key Discoveries

1. **ARM `immutabilityPolicies.properties.state` cannot and must not be set in Bicep (`C7`, `C14`)**: Azure ARM creates `immutabilityPolicies/default` in `Unlocked` state and requires a separate irreversible `lockImmutabilityPolicy` POST action with `If-Match` ETag; `test_bicep_policy.py:2032` explicitly enforces `assertNotIn("state", policy["properties"])`. Deterministic offline enforcement therefore belongs in two complementary layers:
   * **Bicep template + policy/mutation tests (`infra/`)**: enforce private `ledger-digests` container, `immutabilityPeriodSinceCreationInDays >= 1` wired from `main.bicep` to `storage.bicep`, `allowProtectedAppendWrites: false`, `allowProtectedAppendWritesAll: false`, no lifecycle deletion rule touching `ledger-digests` or `digests/`, output `ledgerDigestContainer` wired to `containerapps.bicep` `ZF_DIGEST_CONTAINER`, and complete `ledgerVerify` + `ledgerDigestMismatch` / `ledgerVerifyMissing` alert contracts with mutation rejection.
   * **Core runtime/offline verifier (`src/core`)**: enforce both ARM/policy retention-lock verification (requiring `state == "Locked"`, `immutabilityPeriodSinceCreationInDays >= required_days`, `allowProtectedAppendWrites is False`, `allowProtectedAppendWritesAll is not True`) and Blob REST response header verification (`x-ms-immutability-policy-mode == "locked"` and `x-ms-immutability-policy-until-date` > `as_of` when `require_retention_lock=True`), emitting structured, secret-sanitized `LEDGER_DIGEST_ALERT` records on any retention-lock failure, chain tamper, truncation, anchor mismatch, malformed listing/anchor, or transport error!
2. **Dependency direction requires canonical constants & verifier in `src/core` (`C4`, `C12`, `C16`)**: Placing `ledger_digest_blob.py` in `src/core/src/zava_forward/core/` respects `ALLOWED = {"core"}` (`C16`), enjoys full `mypy --strict` and `ruff` checking, and lets `infra/tests/test_bicep_policy.py` verify Bicep markers, env-var names, and container wiring directly against `zava_forward.core.ledger_digest_blob` (matching `ranking_archive_blob.py`, `C5`, `C14`) while keeping `ALERT_MARKER` and `OK_MARKER` identical (`LEDGER_DIGEST_ALERT`, `LEDGER_DIGEST_OK`).

## Alternatives and Decision State

| Option | Summary | Pros | Cons | Disposition |
|--------|---------|------|------|-------------|
| **Option A (Selected)** | Add strictly typed `zava_forward.core.ledger_digest_blob` in `src/core` (create-only Blob digest store, ARM + Blob-header immutable retention-lock policy verifier, scheduled verification runner with sanitized `LEDGER_DIGEST_ALERT`/`LEDGER_DIGEST_OK` emission and runbook/owner metadata) + comprehensive `src/core/tests/test_ledger_digest_blob.py`; harden `infra/main.bicep`, `infra/modules/storage.bicep`, and `infra/modules/containerapps.bicep` wiring (`ledgerDigestImmutabilityDays`, `allowProtectedAppendWritesAll: false`, `ledgerDigestContainer` output -> `ZF_DIGEST_CONTAINER`) + comprehensive policy & mutation tests in `infra/tests/test_bicep_policy.py` and `infra/tests/test_monitoring_alerts.py`. | Directly closes every deterministic gap in `src/core` and `infra/` within caller scope; 100% `mypy --strict` and `ruff` checked; honors ARM `state` read-only semantics (`C14`) and `core` dependency rule (`C16`); proves both Issue #115 criteria offline with positive and negative/mutation tests. | Does not execute live Azure `lockImmutabilityPolicy` (which remains human/Legal gated per ADR-0002). | **Selected** |
| Option B | Modify only `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py` and `infra/tests/test_bicep_policy.py`. | Smaller diff in `src/core`. | Violates caller target (`src/core` and `infra/`, focused `src/core` + `infra/tests` validation); leaves `src/core` with no typed Blob ledger contract and bypasses `mypy --strict` (`orchestrator` has weak typing). | Rejected |
| Option C | Set `state: 'Locked'` on `digestRetention` in `infra/modules/storage.bicep` and assert it in `test_bicep_policy.py`. | Superficially mentions `"Locked"` in Bicep. | Invalid Azure Storage ARM template semantics (`state` is read-only on `PUT`; locking is a separate POST action after Legal retention sign-off) and contradicts `storage.bicep:6` & `test_bicep_policy.py:2032` (`C7`, `C14`). | Rejected |

## Open Questions, Risks, and Residual Uncertainty

* **Human / live operational gates (intentionally preserved, never fabricated)**:
  1. Legal approval of exact pilot retention duration (currently parameterized with default `365` days; Legal sign-off under #121 / ADR-0002 Decision 2 precedes running the irreversible Azure `lockImmutabilityPolicy` operation).
  2. Live hosted execution of `ledgerVerify` in Azure Container Apps, live Azure Monitor alert delivery (`alert-*-ledger-digest-mismatch` and `alert-*-ledger-verify-missing`), and second-person initial-publication reconciliation.
  * Consequence: Commit message and tracking artifacts must use `Refs #115` and explicitly document these remaining human/live criteria rather than `Closes #115`.
* **Mypy interaction with legacy untyped `src/core` modules**:
  * `ledger.py`, `documents.py`, and `store.py` are in the legacy `ignore_errors = true` list in `src/core/pyproject.toml`. A new strictly typed `zava_forward.core.ledger_digest_blob` module calling `ledger` or `documents` functions either needs narrow typed adapters or a targeted `disallow_untyped_calls = false` override in `src/core/pyproject.toml` (matching `ranking_publication_runner` and `heldout_eval`). We will inspect `src/core/pyproject.toml` in planning and keep full `mypy --strict` typing on all public and internal signatures.

## Current Decisions

* **D1**: Implement `src/core/src/zava_forward/core/ledger_digest_blob.py` with strict typing (`mypy --strict`), secret-safe error handling, deterministic retention-lock verification (both container/ARM immutability policy evaluation requiring `Locked` state, `allowProtectedAppendWrites: False`, `allowProtectedAppendWritesAll: False`, and minimum retention days, and Blob REST response header verification for `x-ms-immutability-policy-mode: locked` and future `x-ms-immutability-policy-until-date`), create-only digest publication, chain/head/year anchor verification, and scheduled verification alert emission (`LEDGER_DIGEST_ALERT` / `LEDGER_DIGEST_OK`) (`C1`–`C6`, `C16`, `C17`).
* **D2**: Harden `infra/modules/storage.bicep`, `infra/main.bicep`, and `infra/modules/containerapps.bicep` by explicitly setting `allowProtectedAppendWritesAll: false` on `digestRetention`, exposing `@minValue(1) param ledgerDigestImmutabilityDays int = 365` in `main.bicep` and forwarding it to `storage.bicep`, exporting `output ledgerDigestContainer string = blobContainers[5].name` from `storage.bicep` and wiring it through `main.bicep` into `containerapps.bicep` (`ZF_DIGEST_CONTAINER`), without fabricating a read-only ARM `state` property (`C7`–`C10`, `C14`).
* **D3**: Expand `infra/tests/test_bicep_policy.py` and `infra/tests/test_monitoring_alerts.py` with comprehensive contract and mutation-rejection tests covering `digestRetention` (`allowProtectedAppendWrites`, `allowProtectedAppendWritesAll`, `main.bicep` parameter forwarding, container wiring, lifecycle isolation, provider constant alignment with `src/core`) and scheduled mismatch alerting (`ledgerVerify` schedule/retry/command/env + `ledgerDigestMismatch` and `ledgerVerifyMissing` operators, thresholds, severities, windows, scopes, and action groups) (`C12`–`C15`).
* **D4**: Validate with focused checks (`src/core` unit tests, `infra/tests` unit tests with `REQUIRE_AZ_BICEP=1`, `az bicep build` + `az bicep lint`, `mypy`, and `ruff check` / `ruff format --check`) and commit with `Refs #115`.

## Unresolved Decisions

* None for offline/Bicep implementation scope. Live retention-period Legal approval and irreversible live lock execution remain external human gates recorded under Issue #115.

## Potential Next Research

* Post-pilot operational verification procedure once Legal confirms retention days and an Azure environment is provisioned (out of scope for offline Issue #115 hardening).

## Planning Readiness

* **Planning Readiness**: `Ready`
* **Research disposition**: `executed`
* **Rationale**: Every codebase contract in `src/core` and `infra/` has been verified with exact file/line citations (`C1`–`C18`), contrarian checks confirmed ARM schema rules and `src/core` dependency/typing boundaries, and a concrete file-by-file design is ready for `rpi-plan`.

## Closeout Record

* Research execution status: `Complete`
* Output mode: `convergence` (supports planning)
* Research-only constraint status: Preserved — zero production or test files modified during `rpi-research`.
* Active continuation owner: Confirmed automatic RPI Agent session (`immutable-blob-ledger-digests-115`), advancing directly to `Plan` (`rpi-plan`).

## Advisory Next Step

* Advance automatic RPI session from `Research` to `Plan` (`rpi-plan`) using this artifact.

## Sources

* Internal codebase files cited in Evidence Log `C1`–`C18`.

## Artifact Self-Check

* [x] Research Brief, Parameters, Extension Registry, Participation, Direction Controls, Questions, and Prior Knowledge Gate populated.
* [x] Cycle 1 completed Wider, Deeper, and Contrarian waves in order before synthesis.
* [x] Every question Q1–Q4 is `answered` and mapped to `path:line` `C#` evidence IDs (`C1`–`C18`).
* [x] Alternatives compared with explicit rejection rationale and Option A selected.
* [x] No source files were modified during Research; no secrets or `.copilot-tracking/` leaks prepared for production code.

