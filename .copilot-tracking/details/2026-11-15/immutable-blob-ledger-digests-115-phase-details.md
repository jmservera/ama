<!-- markdownlint-disable-file -->
# RPI Phase Details: Immutable Blob Ledger Digests and Scheduled Verification (Issue #115)

## Metadata

* Task ID: issue-115-immutable-blob-ledger-digests
* Task slug: immutable-blob-ledger-digests-115
* Related plan: .copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/immutable-blob-ledger-digests-115-research.md (`C1`–`C18`)

## Phase Index

| Phase ID | Name                                                               | Status      | Detail sections          |
|----------|--------------------------------------------------------------------|-------------|--------------------------|
| P01      | Core Immutable Blob Ledger Digest & Scheduled Alerting Contract    | Ready       | P01, P01-T01, P01-T02    |
| P02      | Bicep Immutability Wiring & Scheduled Mismatch Alert Policy Tests  | Ready       | P02, P02-T01, P02-T02    |
| P03      | Focused Validation, Tracking Reconciliation, Review & Local Commit | Ready       | P03, P03-T01             |

<!-- rpi:phase id=P01 -->
## P01: Core Immutable Blob Ledger Digest & Scheduled Alerting Contract

### Context

`src/core/src/zava_forward/core/ledger.py` (`C2`) implements SHA-256 hash-chain entries (`verify_entries`, `verify_years`, `make_digest`, `make_year_digest`), while remote Blob digest publication/verification was migrated unchanged from `mvp/` into `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py` (`C4`) without strict typing, container retention-lock policy verification, or Blob immutability response-header checks. Meanwhile, `src/core/src/zava_forward/core/ranking_archive_blob.py` (`C5`) and `monitoring_coverage.py` (`C6`) establish the exact `src/core` conventions for strictly typed, secret-redacting HTTPS Blob REST adapters, strict `<EnumerationResults>` XML listing validation, and diagnostic event sanitization while honoring `ALLOWED = {"core"}` (`C16`).

### Intent

Provide a complete, strictly typed (`mypy --strict`), Ruff-clean `zava_forward.core.ledger_digest_blob` contract and unit test suite in `src/core` that enforces immutable container retention-lock policies/headers and deterministic scheduled mismatch alerting (`LEDGER_DIGEST_ALERT` / `LEDGER_DIGEST_OK`).

### Boundaries

* Included: `src/core/src/zava_forward/core/ledger_digest_blob.py`, `src/core/pyproject.toml` (only if a narrow `disallow_untyped_calls = false` entry is needed for legacy `ledger` calls), `src/core/tests/test_ledger_digest_blob.py`, and `src/core/README.md` (if listing the new module).
* Excluded: `src/api`, `src/agents`, `src/importer`, and `src/orchestrator` runtime files.

### Likely Targets

* `src/core/src/zava_forward/core/ledger_digest_blob.py`: New typed module implementing retention-lock verification, create-only Blob digest store, publication/verification, scheduled alert runner, and CLI entrypoint.
* `src/core/pyproject.toml`: Add `zava_forward.core.ledger_digest_blob`, `test_ledger_digest_blob`, and `tests.test_ledger_digest_blob` to `disallow_untyped_calls = false` override so calls into legacy untyped `zava_forward.core.ledger` keep all other `mypy --strict` checks enabled.
* `src/core/tests/test_ledger_digest_blob.py`: Deterministic in-memory unit, fault-injection, retention-lock, mismatch-alert, and secret-redaction tests.
* `src/core/README.md`: Document `ledger_digest_blob` alongside `ledger` and `ranking_archive_blob` if modules are enumerated there.

### Dependencies

* None.

### Validation Expectations

* `cd src/core && python3 -m unittest discover -s tests -v`
* `cd src/core && ruff check . && ruff format --check . && mypy`

### Completion Evidence

* Passing unit tests in `src/core/tests/test_ledger_digest_blob.py`, clean `ruff` and `mypy --strict` runs in `src/core`, and `test_dependency_rule.py` passing.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement `zava_forward.core.ledger_digest_blob` and `pyproject.toml` typing boundary

#### Context

ADR-0002 Decision 2 (`C1`) and `infra/modules/storage.bicep` (`C7`) require `ledger-digests` to use time-based immutability with `allowProtectedAppendWrites: false` (create-only JSON block blobs, never append blobs) and an owner-applied retention lock (`state == "Locked"` in ARM control plane; `x-ms-immutability-policy-mode: locked` and `x-ms-immutability-policy-until-date` on Azure Blob REST responses), plus daily scheduled verification emitting `LEDGER_DIGEST_ALERT` (Sev 1) on mismatch and `LEDGER_DIGEST_OK` on verified intact state (`C4`, `C10`, `C11`).

#### Intent

Create `src/core/src/zava_forward/core/ledger_digest_blob.py` with zero external runtime dependencies beyond the Python 3.12 standard library and `zava_forward.core.{ledger,monitoring_coverage}`.

#### Boundaries

* Included:
  * Canonical constants matching `containerapps.bicep` and `digest_blob.py`: `ACCOUNT_URL_VAR = "ZF_DIGEST_ACCOUNT_URL"`, `CONTAINER_VAR = "ZF_DIGEST_CONTAINER"`, `CLIENT_ID_VAR = "ZF_DIGEST_CLIENT_ID"`, `SAS_VAR = "ZF_DIGEST_SAS"`, `DIGEST_DIR_VAR = "ZF_DIGEST_DIR"`, `REQUIRE_LOCK_VAR = "ZF_DIGEST_REQUIRE_RETENTION_LOCK"`, `MIN_RETENTION_DAYS_VAR = "ZF_DIGEST_MIN_RETENTION_DAYS"`, `DEFAULT_CONTAINER = "ledger-digests"`, `DEFAULT_MIN_RETENTION_DAYS = 365`, `ALERT_MARKER = "LEDGER_DIGEST_ALERT"`, `OK_MARKER = "LEDGER_DIGEST_OK"`, `RECONCILE_OK_MARKER = "LEDGER_DIGEST_RECONCILE_OK"`, `RECONCILE_ALERT_MARKER = "LEDGER_DIGEST_RECONCILE_ALERT"`, `MISMATCH_RUNBOOK = "ledger-digest-mismatch"`, `MISSING_RUNBOOK = "ledger-verify-missing"`, `PROPOSED_OWNER = "Digital service owner"`.
  * `LedgerDigestBlobError(RuntimeError)` with guaranteed secret/URL/SAS omission.
  * `verify_container_retention_lock(policy, *, container_properties=None, lifecycle_prefixes=(), container_name=DEFAULT_CONTAINER, require_locked=True, min_retention_days=DEFAULT_MIN_RETENTION_DAYS)`: checks container `publicAccess` (`None`/absent), policy presence, `state == "Locked"` when `require_locked=True` (recording `locked: bool` accurately and rejecting `"Unlocked"` when `require_locked=True`), strict `int` (not `bool`) `immutabilityPeriodSinceCreationInDays >= max(1, min_retention_days)`, `allowProtectedAppendWrites is False`, `"allowProtectedAppendWritesAll" not in policy` (rejecting both ARM-invalid simultaneous presence with `allowProtectedAppendWrites` and any truthy/non-absent `allowProtectedAppendWritesAll`), and absence of any storage-account lifecycle deletion rule prefix overlapping `container_name`, `f"{container_name}/"`, or empty account-wide prefix `""`.
  * `verify_blob_retention_headers(headers, *, as_of=None, created_at=None, min_retention_days=None)`: case-insensitively inspects `x-ms-immutability-policy-mode` (must equal `"locked"`) and `x-ms-immutability-policy-until-date` (RFC 1123 or ISO-8601 UTC timestamp strictly greater than `as_of` UTC, and `>= created_at + timedelta(days=min_retention_days)` when both are provided).
  * `BlobLedgerDigestStore`: HTTPS-only account URL validation, DNS-safe container name validation, canonical root anchor name validation (`digest-{count:010d}.json` and `year-{YYYY}.json`, rejecting traversal `..`, slashes, or non-canonical names), Entra Managed Identity token acquisition (`ZF_DIGEST_CLIENT_ID`) or SAS credential (`ZF_DIGEST_SAS`) support, `create_anchor(name, payload)` using `PUT` with `If-None-Match: *` and `x-ms-blob-type: BlockBlob` (returning `True` on `200`/`201`, `False` on `409 BlobAlreadyExists`/`412` only after reading back and confirming identical logical immutable anchor fields — `chain`, `algorithm`, `count`, `head`, plus `year` and `first_prev` for year anchors, ignoring volatile `"at"` — or raising mismatch/error, never overwriting or deleting), `read_anchor_with_headers(name)` / `read_anchor(name)`, strict `<EnumerationResults>` paginated XML `list_names(prefix="")` (rejecting structurally invalid XML or non-200 responses with `LedgerDigestBlobError`), and `open_ledger_digest_store(env, transport=None)`.
  * `publish_ledger_digests(entries, years, blob, *, published_at=None)`: validates local chain (`ledger.verify_entries`, `ledger.verify_years`) before writing `digest-{count:010d}.json` and sealed `year-{year}.json` anchors; refuses divergent pre-existing remote anchors.
  * `verify_ledger_digests(entries, years, blob, *, require_retention_lock=False, require_current_head=False, retention_policy=None, container_properties=None, lifecycle_prefixes=(), min_retention_days=DEFAULT_MIN_RETENTION_DAYS, as_of=None)` and `reconcile_ledger_digests(blob, record, *, require_retention_lock=False, as_of=None)`: verifies optional ARM/container policy lock, local chain and year digests, remote `digest-{count:010d}.json` and `year-{YYYY}.json` anchors (rejecting missing anchors on non-empty ledger, malformed names/JSON/fields, remote count ahead of local store [truncation], hash mismatch at any anchored count, stale remote head when `require_current_head=True`, missing/mismatched year digest, and missing/unlocked/expired blob retention headers on every inspected remote anchor when `require_retention_lock=True`).
  * `run_scheduled_verification(entries, years, blob, *, publish=False, require_retention_lock=False, retention_policy=None, container_properties=None, lifecycle_prefixes=(), min_retention_days=DEFAULT_MIN_RETENTION_DAYS, as_of=None, out=None)` and `main(argv=None, ...)`: orchestrates scheduled `--publish` + verify (and `--reconcile`), emits sanitized `LEDGER_DIGEST_ALERT` (`exit_code=1`) when scheduled `ZF_DIGEST_*` configuration is missing or invalid, catches transport/policy/chain failures without leaking secrets, sanitizes diagnostic payload via `monitoring_coverage.sanitize_diagnostic`, emits `LEDGER_DIGEST_OK` (`exit_code=0`) only when intact and lock-compliant, and emits `LEDGER_DIGEST_ALERT` (`exit_code=1`, `runbook="ledger-digest-mismatch"`, `proposed_owner="Digital service owner"`) on any violation while suppressing `LEDGER_DIGEST_OK`.
* Excluded: Modifying `ledger.py` or `documents.py` legacy files.

#### Likely Targets

* `src/core/src/zava_forward/core/ledger_digest_blob.py`
* `src/core/pyproject.toml`

#### Dependencies

* `zava_forward.core.ledger` and `zava_forward.core.monitoring_coverage`.

#### Validation Expectations

* `mypy` and `ruff check . && ruff format --check .` in `src/core` exit 0.

#### Completion Evidence

* Module created and cleanly typed/linted.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add unit, fault-injection, retention-lock, and mismatch-alert tests in `src/core/tests/test_ledger_digest_blob.py`

#### Context

`src/core/tests/test_ranking_archive_blob.py` (`C17`) demonstrates the repository's gold-standard offline Blob test harness: an in-memory HTTPS REST fake transport modeling conditional `PUT` (`If-None-Match: *`), `GET` headers, paginated `<EnumerationResults>` XML, injected HTTP/transport faults, mixed-case headers, and sentinel-secret non-leakage assertions.

#### Intent

Create `src/core/tests/test_ledger_digest_blob.py` proving every retention-lock rule, create-only publication/verification path, scheduled mismatch alert scenario, CLI exit code, and secret-redaction invariant.

#### Boundaries

* Included:
  * `verify_container_retention_lock` positive/negative matrix (`Locked` vs `Unlocked`/missing/deleted, retention days `< min_retention_days` / `0` / `bool`, `allowProtectedAppendWrites=True`, `allowProtectedAppendWritesAll=True`, `publicAccess="Blob"`, lifecycle deletion prefix overlapping `digests/`, and `require_locked=False` pre-lock honesty).
  * `verify_blob_retention_headers` positive/negative matrix (RFC 1123 and ISO-8601 `x-ms-immutability-policy-until-date`, mixed-case headers, `locked` vs `unlocked`/missing mode, expired `until-date <= as_of`, shortened retention window vs `created_at + min_retention_days`).
  * `BlobLedgerDigestStore` create-only `If-None-Match: *` behavior, no `put`/`delete`/`overwrite` methods, path-traversal and HTTP URL refusal, Entra MI bearer token usage without logging secrets, paginated listing, and malformed 200 XML rejection.
  * `publish_ledger_digests`, `verify_ledger_digests`, and `run_scheduled_verification` / `main`:
    * Clean `--publish` and verify -> `LEDGER_DIGEST_OK`, `exit_code == 0`, no `LEDGER_DIGEST_ALERT`.
    * Tampered entry payload/hash, truncated local chain behind remote head, divergent pre-existing remote head or year digest, missing remote head/year anchor on non-empty chain, malformed remote anchor filename/JSON/schema, stale remote head when `require_current_head=True`, unlocked/missing/expired Blob immutability headers when `require_retention_lock=True`, unlocked ARM retention policy snapshot, and Blob 500/timeout/auth failures -> `LEDGER_DIGEST_ALERT`, `exit_code == 1`, `runbook == "ledger-digest-mismatch"`, `proposed_owner == "Digital service owner"`, zero `LEDGER_DIGEST_OK`, and zero sentinel secret leakage (`SENTINEL-SAS-SECRET`, `SENTINEL-TOKEN`, `acct.blob.core.windows.net`).
  * Concise update to `src/core/README.md` if core modules are listed there.
* Excluded: Live Azure Storage network calls.

#### Likely Targets

* `src/core/tests/test_ledger_digest_blob.py`
* `src/core/README.md` (only if module table/list exists)

#### Dependencies

* P01-T01.

#### Validation Expectations

* `cd src/core && python3 -m unittest discover -s tests -p "test_ledger_digest_blob.py" -v`
* `cd src/core && python3 -m unittest discover -s tests -v`

#### Completion Evidence

* All tests in `src/core/tests/` pass, including `test_ledger_digest_blob.py`, `test_dependency_rule.py`, `test_monitoring_coverage.py`, and `test_live_doc_links.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Bicep Immutability Wiring & Scheduled Mismatch Alert Policy/Mutation Tests

### Context

`infra/modules/storage.bicep` (`C7`) defines `digestRetention` on `blobContainers[5]` (`ledger-digests`) with `allowProtectedAppendWrites: false` and `ledgerDigestImmutabilityDays` (`@minValue(1)`, default `365`), yet omits `allowProtectedAppendWritesAll: false` and does not export `ledgerDigestContainer`. `infra/main.bicep` (`C8`) neither exposes `ledgerDigestImmutabilityDays` nor wires `storage.outputs.ledgerDigestContainer` into `infra/modules/containerapps.bicep` (`C9`), which currently hardcodes `ZF_DIGEST_CONTAINER: 'ledger-digests'`. Finally, `infra/tests/test_bicep_policy.py` (`C12`, `C13`, `C14`) lacks comprehensive contract assertions and mutation-rejection coverage for `digestRetention` append-write flags, `main.bicep` retention/container wiring, `staffResultsLifecycle` prefix isolation, and `ledgerVerify` / `ledgerDigestMismatch` / `ledgerVerifyMissing` scheduled verification alerting.

### Intent

Align Bicep immutability and scheduled-job container wiring across `storage.bicep`, `main.bicep`, and `containerapps.bicep`, and prove via policy and mutation tests in `infra/tests/` that weakening any retention-lock or scheduled mismatch alert control fails compilation/policy validation.

### Boundaries

* Included: `infra/modules/storage.bicep`, `infra/main.bicep`, `infra/modules/containerapps.bicep`, `infra/README.md` (if documenting `ledgerDigestImmutabilityDays`), `infra/tests/test_bicep_policy.py`, and `infra/tests/test_monitoring_alerts.py`.
* Excluded: `.github/workflows/*.yml`, `infra/main*.bicepparam` (default `365` keeps all existing parameter files valid without churn), and `ledgerVerify` Python module command (`zava_forward.orchestrator.digest_blob --publish` remains unchanged per `test_bicep_policy.py:444`).

### Likely Targets

* `infra/modules/storage.bicep`: Keep `allowProtectedAppendWrites: false` on `digestRetention` (without mutually-exclusive `allowProtectedAppendWritesAll`) and add `output ledgerDigestContainer string = blobContainers[5].name`.
* `infra/modules/containerapps.bicep`: Add `param ledgerDigestContainer string = 'ledger-digests'` and bind `ZF_DIGEST_CONTAINER` on `ledgerVerify` to `ledgerDigestContainer`.
* `infra/main.bicep`: Expose `@minValue(1) param ledgerDigestImmutabilityDays int = 365` (with clear `@description` noting ARM creates an unlocked time-based WORM policy and irreversible locking is an owner action after Legal sets duration), pass `ledgerDigestImmutabilityDays` to `storage`, and pass `ledgerDigestContainer: storage.outputs.ledgerDigestContainer` to `apps`.
* `infra/tests/test_bicep_policy.py` & `infra/tests/test_monitoring_alerts.py`: Add full contract + mutation-rejection tests and cross-check Bicep constants against `zava_forward.core.ledger_digest_blob`.
* `infra/README.md`: Document `ledgerDigestImmutabilityDays` if parameters are listed there.

### Dependencies

* P01.

### Validation Expectations

* `az bicep build --file infra/main.bicep --stdout > /dev/null && az bicep lint --file infra/main.bicep`
* `az bicep build --file infra/modules/storage.bicep --stdout > /dev/null && az bicep lint --file infra/modules/storage.bicep`
* `az bicep build --file infra/modules/containerapps.bicep --stdout > /dev/null && az bicep lint --file infra/modules/containerapps.bicep`
* `REQUIRE_AZ_BICEP=1 python3 -m unittest discover -s infra/tests -v`
* `ruff` checks on `infra/tests/test_bicep_policy.py` and `infra/tests/test_monitoring_alerts.py`.

### Completion Evidence

* Clean Bicep build/lint across all modified `.bicep` files and passing `infra/tests` discovery including new retention-lock and scheduled-mismatch-alert mutation tests.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Harden `storage.bicep`, `main.bicep`, and `containerapps.bicep` ledger digest immutability and container wiring

#### Context

In Azure Storage ARM `2024-01-01`, `immutabilityPolicies` treats `allowProtectedAppendWrites` and `allowProtectedAppendWritesAll` as mutually exclusive on `PUT`, while `state` is read-only (`C7`, `C14`, `PC-001`). Keeping `allowProtectedAppendWrites: false` without `allowProtectedAppendWritesAll` prevents append-blob mutations on `ledger-digests` while staying ARM-valid, and wiring `ledgerDigestImmutabilityDays` and `storage.outputs.ledgerDigestContainer` removes hardcoded drift between `main.bicep`, `storage.bicep`, and `containerapps.bicep` (`C8`, `C9`).

#### Intent

Tighten the Bicep templates cleanly while keeping default parameter behavior (`ledgerDigestImmutabilityDays = 365`, `ledgerDigestContainer = 'ledger-digests'`) 100% backward-compatible with `main.bicepparam`, `main.test.bicepparam`, and `main.pilot.example.bicepparam`.

#### Boundaries

* Included: `infra/modules/storage.bicep`, `infra/modules/containerapps.bicep`, `infra/main.bicep`, and `infra/README.md` (if needed).
* Excluded: Adding `state` to ARM `immutabilityPolicies` or changing `ledgerVerify` image/command.

#### Likely Targets

* `infra/modules/storage.bicep`
* `infra/modules/containerapps.bicep`
* `infra/main.bicep`
* `infra/README.md`

#### Dependencies

* P01-T01.

#### Validation Expectations

* `az bicep build` and `az bicep lint` succeed with zero warnings on `infra/main.bicep`, `infra/modules/storage.bicep`, and `infra/modules/containerapps.bicep`.

#### Completion Evidence

* Compiled ARM JSON reflects `ledgerDigestImmutabilityDays` parameter forwarding, `allowProtectedAppendWrites: false`, `allowProtectedAppendWritesAll: false`, and `storage.outputs.ledgerDigestContainer` wiring into `ledgerVerify`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Expand `infra/tests/test_bicep_policy.py` and `infra/tests/test_monitoring_alerts.py` with retention-lock and scheduled mismatch alert mutation tests

#### Context

Currently `assert_retention_controls` and `test_mutations_reject_missing_wrong_or_zero_retention` in `infra/tests/test_bicep_policy.py` (`C13`) do not check `allowProtectedAppendWritesAll`, `state` absence on `digestRetention`, `main.bicep` `ledgerDigestImmutabilityDays` forwarding, `storage.outputs.ledgerDigestContainer` -> `containerapps` `ZF_DIGEST_CONTAINER` wiring, `staffResultsLifecycle` exclusion of `digests/`, or `verify_container_retention_lock(..., require_locked=False)` compatibility. Likewise, `test_ledger_alerts_use_azure_monitor_resource_specific_console_schema` and `test_ledger_alert_queries_match_the_verifier_markers` (`C12`) have no helper assertion method or mutation tests rejecting weakened thresholds, operators, severities, windows, disabled states, missing action groups, or broken `ledgerVerify` schedule/retry/env wiring.

#### Intent

Add `assert_ledger_verification_controls(template)` and comprehensive mutation tests in `infra/tests/test_bicep_policy.py` (plus source-level schedule/mismatch checks in `infra/tests/test_monitoring_alerts.py`), cross-checking constants against `zava_forward.core.ledger_digest_blob` (`ALERT_MARKER`, `OK_MARKER`, `ACCOUNT_URL_VAR`, `CONTAINER_VAR`, `DEFAULT_CONTAINER`).

#### Boundaries

* Included:
  * Extend `assert_retention_controls` in `infra/tests/test_bicep_policy.py` to assert `allowProtectedAppendWrites is False` and `"allowProtectedAppendWritesAll" not in props` on `ledger-digests`, `"state" not in props`, `main.bicep` `ledgerDigestImmutabilityDays` (`minValue >= 1`, `defaultValue == 365`) forwarded to `storage`, `storage.outputs.ledgerDigestContainer` forwarded to `containerapps` `ledgerDigestContainer`, `staffResultsLifecycle` prefix list disjoint from `ledger-digests/` and empty prefix, and evaluation of `props` through `evaluate(...)` + `zava_forward.core.ledger_digest_blob.verify_container_retention_lock(..., require_locked=False)`.
  * Extend `test_mutations_reject_missing_wrong_or_zero_retention` to reject mutating `allowProtectedAppendWrites = True`, adding `"allowProtectedAppendWritesAll": False` or `True`, adding `"state": "Locked"`, removing `main.bicep` `ledgerDigestImmutabilityDays` forwarding or `minValue`, or adding `"ledger-digests/"` to `staffResultsLifecycle`.
  * Add `assert_ledger_verification_controls(template)` and `test_mutations_reject_weakened_ledger_verification_and_mismatch_alerts` in `infra/tests/test_bicep_policy.py` verifying:
    * `ledgerVerify` job in `containerapps`: `triggerType == "Schedule"`, `cronExpression == "0 2 * * *"`, `replicaRetryLimit == 0`, evaluated `concat(...)` `env` wiring `ZF_DIGEST_ACCOUNT_URL` to `blobEndpoint` and `ZF_DIGEST_CONTAINER` to `ledgerDigestContainer`, and command `['python', '-m', 'zava_forward.orchestrator.digest_blob', '--publish']`.
    * `ledgerDigestMismatch` (`alert-*-ledger-digest-mismatch`): `enabled is True`, `severity == 1`, `evaluationFrequency == "PT1H"`, `windowSize == "PT1H"`, `operator == "GreaterThan"`, `threshold == 0`, `scopes` referencing `monitoring` `workspaceId`, `actionGroups` referencing `monitoring` `actionGroupId`, query referencing `ledgerJobName` and `LEDGER_DIGEST_ALERT`, and alignment between `zava_forward.core.ledger_digest_blob.ALERT_MARKER` and `zava_forward.orchestrator.digest_blob.ALERT_MARKER`.
    * `ledgerVerifyMissing` (`alert-*-ledger-verify-missing`): `enabled is True`, `severity == 1`, `evaluationFrequency == "PT1H"`, `windowSize == "P1D"`, `overrideQueryTimeRange == "PT26H"`, `operator == "LessThan"`, `threshold == 1`, `scopes` and `actionGroups` wired to `monitoring`, query referencing `ledgerJobName` and `LEDGER_DIGEST_OK`, and marker alignment with `zava_forward.core.ledger_digest_blob.OK_MARKER`.
    * Mutation rejection for disabling either alert, changing mismatch threshold to `1` or operator to `LessThan`, removing `actionGroups`, removing `LEDGER_DIGEST_ALERT` / `LEDGER_DIGEST_OK`, changing `ledgerVerify` `replicaRetryLimit` to `1` or `triggerType` to `"Manual"`, or breaking `ledgerDigestContainer` forwarding.
  * Extend `infra/tests/test_monitoring_alerts.py` to assert `main.bicep` ledger alert runbook descriptions/severity/window/action-group parity alongside `operationalMonitoring.bicep`.
* Excluded: Requiring Azure cloud connectivity.

#### Likely Targets

* `infra/tests/test_bicep_policy.py`
* `infra/tests/test_monitoring_alerts.py`

#### Dependencies

* P01-T01, P02-T01.

#### Validation Expectations

* `REQUIRE_AZ_BICEP=1 python3 -m unittest discover -s infra/tests -v`
* `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_bicep_policy.py infra/tests/test_monitoring_alerts.py`
* `ruff format --isolated --line-length 100 --check infra/tests/test_bicep_policy.py infra/tests/test_monitoring_alerts.py`

#### Completion Evidence

* All `infra/tests` unit and mutation tests, `ruff`, and `mypy` pass.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Validation, Tracking Reconciliation, Review & Local Commit

### Context

Repository instructions require focused validation (`src/core` tests, `infra/tests`, `ruff`, `mypy`, Bicep build/lint, plus live doc link validation via `test_live_doc_links.py`), full reconciliation of plan checkboxes, phase details, and `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-changes.md`, one post-implementation `rpi-review` pass, and a local commit using privacy-safe GitHub noreply author/committer email, `Refs #115`, and the `Co-authored-by` trailer without pushing.

### Intent

Verify zero regressions across all focused suites, reconcile tracking artifacts, execute `rpi-review`, and create a clean local commit on `feat/demo-115-blob-ledger`.

### Boundaries

* Included: Focused test/lint/type execution, tracking artifact updates, `rpi-review` artifact under `.copilot-tracking/reviews/2026-11-15/`, local `git config --local user.email` from `gh api user`, and `git commit`.
* Excluded: Running `tools/rpi-checks.py` and `git push`.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-changes.md`
* `.copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-plan.md`
* `.copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-phase-details.md`
* `.copilot-tracking/reviews/2026-11-15/immutable-blob-ledger-digests-115-review.md`
* `.copilot-tracking/rpi-sessions/2026-11-15/immutable-blob-ledger-digests-115-state.json`

### Dependencies

* P01, P02.

### Validation Expectations

* `src/core` unit tests, `infra/tests` (`REQUIRE_AZ_BICEP=1`), `az bicep build` + `az bicep lint`, `mypy`, `ruff check`, and `ruff format --check` all exit 0; `git status --short` clean after commit; `git log -1` shows `Refs #115` and `Co-authored-by` trailer with zero `.copilot-tracking/` references in commit message or production code.

### Completion Evidence

* Clean test/lint/type outputs recorded in changes and review artifacts, clean git working tree, and verified HEAD commit on `feat/demo-115-blob-ledger`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Execute focused validation suite and reconcile implementation evidence

#### Context

All planned checks in the focused tier must execute against editable workspace packages (`src/core` and `src/orchestrator`) with `REQUIRE_AZ_BICEP=1` enabled for `infra/tests`.

#### Intent

Run and record every focused validation check, reconcile P01–P03 checkboxes and `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-changes.md`, then hand off cleanly to `rpi-review` and commit.

#### Boundaries

* Included: Focused validation runs, changes artifact authoring, and plan/details status reconciliation.
* Excluded: `tools/rpi-checks.py` and remote push.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-changes.md`
* `.copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-plan.md`
* `.copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-phase-details.md`

#### Dependencies

* P01-T02, P02-T02.

#### Validation Expectations

* Zero test failures, zero mypy errors, zero ruff check/format violations, zero Bicep build/lint diagnostics.

#### Completion Evidence

* Recorded command exit codes and test counts in `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-changes.md`.

#### Unresolved Items

* None.
