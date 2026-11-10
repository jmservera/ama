<!-- markdownlint-disable-file -->
# Research: #185 keyless Registry adapter, extension E1 (inventory completeness and traceback context)

Written 2026-11-10T13:54Z (`date -u` readback 13:53:18Z at the preceding step). Task `185-iot-registry-azure-e1`, parent task `185-iot-registry-azure-initial`, branch `feat/demo-iot-registry-185-1110`, frozen starting head `c7cfb463d5d9bd57e9f72e457cf0073b6b7c7e76` (clean). Refs #185. Research disposition: executed (narrow; the SDK and contract research of the initial increment is reused, not repeated). Planning Readiness: Ready.

## Authority and budget (durable record)

* Owner, 2026-11-09T08:00:39Z: repository default of up to five total review-correction cycles per issue (no reset of spent cycles). Owner, 2026-11-09T08:02:51Z: "add 5 additional cycles to exhausted issues" (one-time, issues exhausted at that time).
* Root reconciliation 2026-11-10 (`185-extension-e1-authority-1352.txt`, `handoff-185-dated-budget-audit-1344.md`): #185 had at least 7 certain historical correction debits by 2026-11-06 (strict reading 14 to 15) against the five-total default, so it was exhausted before the grant. The grant covers it by dated eligibility; no named list is required. No post-grant correction debit exists: the 2026-11-10 Registry increment was an explicit initial increment and later work was read-only.
* Extension before this work: 5. Root authorizes ONLY E1 now. After E1 is consumed the extension remaining is 4. Further batches need a Root selection. This is not a fresh default five, a reset, a retroactive approval of historical overage, or a new extension. Historical spent cycles and the earlier "balance UNKNOWN" statements stay as original records.
* Dated chronology table (from the 1344 audit, preserved, not rewritten): 2026-11-01 #647 rounds 1 to 4 (`67043a15a`, `3cdd3eab7`, `509abde04`, `eaa2a8f0e`) and `4a2a21834` (certain corrections), seven further source-bearing #647 fixes (charging undefined); 2026-11-03 #849 `e34b8678e` (certain) and `2b0b6ffd2`; 2026-11-06 #1205 `a7d4e956d` (certain forward cycle). Certain floor 7; strict 14 to 15. 2026-11-10 `c7cfb463` initial, independent review REQUEST_CHANGES (not a debit by itself).
* E1 debit: this single correction batch (the repair of the two findings below) consumes E1. Extension remaining after E1: 4. Recorded again in the changes record.

## Findings under repair (independent review, exact head c7cfb463)

Source: `independent-185-registry-initial-1110/functional-findings.json`, `reproduce_functional_findings.py` (read), issue comment 6757594821 (read). Root reproduced both as failing on the frozen head; the original 85 unit tests, lint, format and mypy (286 files) passed and do not waive them.

* F1, High, incomplete inventory. `list_run` confirms an entry that omits `statusReason` by a bounded read only when its ID is enrolled; every other such entry is silently skipped. A run-marked, non-enrolled identity behind an omitting list payload is therefore missing from a successful inventory. Consequence: `device_identity._teardown_locked` full-run precheck `set(list_run) - owned` misses it, so teardown can report success while it remains; provision's active-run check can also pass. The existing test `test_payload_that_omits_the_marker_is_confirmed_by_a_bounded_read` encodes this omission (expects only SYN-A1 although SYN-B1 carries the exact marker). The original critique recorded it as a documented residual; the independent review rates it High and not acceptable.
* F2, Medium, traceback context leak. `raise RegistryError(code)` outside the adapter's own `except` does not clear an exception that the CALLER is currently handling. Python sets `__context__` to that exception, and `traceback.format_exception` prints it, disclosing the caller's secret-bearing exception. The sanitisation test never calls the adapter inside a caller `except` block. Existing `device_identity` tests do exercise this boundary for its own errors.

## Verified facts (read at head, no network)

* All public refusals are `raise RegistryError(...)` sites in `device_registry_azure.py` (configuration, enrollment, `create`, `run_of`, `delete`, `list_run`, `_run`, `_device`, `_models`, `_devices`). SDK exceptions are already caught in `_invoke`, `_prepare` and `_load`, which keep only the integer HTTP status; no SDK text reaches an error.
* `_read` does not require enrolment, so a bounded confirmation read of a listed non-enrolled ID needs no new SDK surface (`get_identity` is already used). `delete`/`create`/`run_of` still refuse non-enrolled IDs, so no destructive path widens.
* `device_identity.MAX_DEVICES` is 100: the existing bound for enrolled confirmation reads. `device_identity` teardown with a returned uncovered ID refuses with `TEARDOWN_MANIFEST_INCOMPLETE:n` before any delete or revoke, which is the truthful outcome when a non-enrolled marked identity exists.
* A real hub lists many devices without a `statusReason` (foreign, unmarked). Refusing every such non-enrolled entry would make the adapter unusable on a shared hub; the review's own alternative is a bounded internal ownership read refusing when the budget is exhausted. That alternative is adopted.
* `raise exc` without `from` never resets `__suppress_context__`; `from None` sets it. `traceback.format_exception` honours it. The context object itself remains reachable (the review notes this). Clearing `__context__` altogether is not possible for a raise inside a caller's handler without catching and replacing it in the caller, which is outside this boundary.

## Current origin/main (fetched 2026-11-10T13:52Z)

`origin/main` is `c9e15acbf5c0893358818e562d034d62321ea6d4`, 20 commits ahead of the topic base `2bfd5e07545db18380f48a9854654c8393d0e9bc`. The diff to the owned files is limited to `src/core/README.md` and `src/core/pyproject.toml` (main changed them; the topic adds to them). Main does not change `device_identity.py`, `device_provision.py`, or the topic's two new files. No material intent conflict. Main adoption is not needed for this repair, is left for the owner/Root publication step and will be reconciled there; no rebase, reset or amend is done. A conflict in the two shared files is expected to be mechanical and is not claimed resolved.

## Design (smallest correct patch)

* F1: in `list_run`, any listed entry whose `statusReason` is not a string is confirmed by one bounded `get_identity` read regardless of enrolment, with a total confirmation budget of `device_identity.MAX_DEVICES` reads per call. Present and exactly marked: include (enrolled or not). Present and not marked: exclude. Absent (404): exclude. Denied or unreadable: refuse `ACCESS_DENIED` or `UNAVAILABLE`. Budget exceeded: refuse `LIST_INCOMPLETE`. Complete or explicit refusal; no first-page, truncated or duplicate-as-complete path. Max calls per `list_run` are 1 + 100.
* F2: `RegistryError.__init__` sets `__suppress_context__ = True`, so every public fixed-code refusal, including future ones and constructor/dataclass refusals, hides the caller's ambient context without touching `__cause__` semantics. Existing `raise ... ` statements stay as is.
* No new codes, providers, permission policy or manifest policy. No change to `device_identity`, `device_provision`, CLI, README guarantees except the residual note that the critique documented.

## Test plan (red then green)

* F1 old-fail/new-pass: omitting payload with an exact-marked non-enrolled SYN-B1 must be listed (and the Root repro passes); an unmarked non-enrolled entry is excluded; budget exhaustion refuses `LIST_INCOMPLETE`; an unreadable confirmation refuses; whole-run teardown through the real SDK path refuses with `TEARDOWN_MANIFEST_INCOMPLETE` and deletes nothing.
* F2 old-fail/new-pass: for every public refusal path, raise inside a caller `except RuntimeError(SECRET)` handler; `traceback.format_exception` must not contain the sentinel and `__suppress_context__` must be true.
* Existing 85 Registry/identity/provision/dependency tests unchanged except the one fixture expectation that encoded the omission. Impacted Core selectors, Ruff check and format, and Core mypy including both files.
* Not run: full or `--changed` gate, cloud, SQL, browser, scanners. No live Registry, identity, credential or token operation; the SDK transport is the local simulator.

## Boundaries

No live calls, credentials, provisioning, token acquisition, secret export or spend. No CredentialStore or lifecycle decision. Registry-before-credential and auth-update pair contracts stay open. Aside from the two owned source files, only the narrow README residual note may change. No 111, 131, 132, 1360, parent 184, schema, UI or unrelated Core change.
