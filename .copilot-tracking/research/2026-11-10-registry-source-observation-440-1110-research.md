# Research: Registry wave (PR 1393) current-main observation (2026-11-10, Refs #440 #185)

Disposition: executed. Planning Readiness: Ready. Docs-only; no runtime, test, install, image, SQL, browser, cloud, model, live or private-data work.

## Scope and dependency

* New recurring observation of the merged Registry wave. Not the old CSV C6, not a retry, no source-correction pool, no product/test/config fix.
* Worktree `issue-440-registry-source-checkpoint-1110`, branch `docs/demo-registry-source-checkpoint-440-1110`, declared child of `docs/demo-nomination-ux-checkpoint-440-1110` at `6119b7aa3858c35fd4964d4f54dc7f8ef27ca2fa` (published parent PR 1396, observed OPEN, MERGEABLE, head unchanged at observation). No retarget, rebase, merge or parent edit. If PR 1396 merges later, Root owns the dependency transition.
* The local branch source is older than main (topic base `65c2ab9d9`); the Registry adapter does not exist in it. Current-main facts below are read through `git show origin/main:<path>` only.

## Pin (fetched 2026-11-10 ~15:07Z, `origin/main` unmoved)

* `origin/main` `6cc59776666620309fb6b67ad2fdafb343d40998`, tree `eaf44bcdec8bdf5e9dfab2e73b1ded5459d8ff3c` (equals Root prediction). Ancestry: PR 1393 merged 2026-11-10T14:54:22Z, after #1392 (`57d32c0d0`, workspace oracle repair) and #1394 (`15516ff3d`, docs). The merge changes 25 files (2012 insertions, 1 deletion) from `57d32c0d0`: adapter, tests, Core README, `pyproject.toml` and the PR's own `.copilot-tracking` records.
* Blobs at the pin: `src/core/src/zava_forward/core/synthetic/device_registry_azure.py` `5add5e34d4d4` (418 lines), `src/core/tests/test_device_registry_azure.py` `954c8a206c9d` (844 lines), `src/core/README.md` `e4619c34a8f8`, `src/core/pyproject.toml` `1c2d73533df4`. All four equal the reviewed candidate `7085213b969c` blobs in the Root handoff.
* Documents at the pin: BRD Agentic Retrofit Programme 0.21.0 `draft` `34d88395de86` (FR-048, AC-090, OD-43); PRD Zava Forward 0.21.0 `in-review` `c788b917bafa` (FR-050, AC-066 to AC-068, all Not run); ADR 0003 `d60645397b20` (owner-accepted with amendment 2026-10-15, decision 6, implementation status says no live identity or provisioning follows).
* Hosted: reviewed head `7085213b9` all 19 contexts SUCCESS (PR 1393 body, final guard text in Root proof). For main `6cc59776` the observed run list is Capstone Rubric Scorer success (push), Graph Update pip in `/src/core` success, Infrastructure PR what-if skipped; no other push CI run was listed for that commit. Not inferred green for the source.

## Consumed evidence (read, not re-run)

* `handoff-185-main-integration-1110.md`: final head `7085213b969c`, tree `2cd50a62147c`, ordinary `--no-ff` adoption of main `06374dfca` into E1 `105d479ae`; 89 selector tests OK no skips (adapter, identity, provisioning, dependency rule), Root reproductions 2 OK, Ruff check passed and format 237 files, mypy 290 files no issues, own venv `azure-iot-hub` 2.7.0 and `six` 1.17.0; log hash `c1c09185...30d35`, seven records, verify exit 0.
* `checks-185-main-integration-1110/`: raw `.exit`, `.log` for venv, install, selector, root repro, ruff, mypy and provenance.
* `independent-185-main-integration-1433/functional/verdict.json`: approve, 0 findings, no E2, no waiver.
* `pr185-qualified-body-1438.txt` and Root proof 1873 style qualification: main prospective tree `eaf44bcd` equals reviewed candidate for the Core, Agents, Orchestrator, Importer and API product-source subtrees and the API dependency manifest; remaining differences are rubric documentation and the independently reviewed workspace checker helper, two checkers and their tests (component qualification, not full-tree equality).
* Adverse and qualified: an earlier extra full Core discovery timed out and is NOT a pass and was not re-run; no API selector claimed; `__context__` stays programmatically reachable; research-open and plan-done were recorded in one call after one preflight in the source run (disclosed process qualification).
* Root ledger (`demo-run-ledger.md`) records the NomUX/Bicep reviewer verdict for the parent PR; it is not consumed as Registry evidence.

## Source behaviour at the pin (static read)

* Keyless, default off: importing, constructing, dry run and `close()` never import the SDK, acquire a token or connect; auth is an injected Entra token credential or a pre-built client (exactly one); no connection string, key or ambient discovery.
* Inputs: hub host regex `*.azure-devices.net`, finite `EnrollmentSpec` (1 to `MAX_DEVICES`=100 `SYN-` ids), run id, public X.509 thumbprints (40 or 64 hex); timeout 1 to 60 seconds.
* Writes conditional: create `If-None-Match: *` disabled with exact run marker `zava-forward:sim-run:v1:`; delete uses the exact non-wildcard ETag of an ownership snapshot, refusing drift; uncertain writes report a safe readback.
* `list_run` complete or refuses: 1000-device page limit refuses (`LIST_INCOMPLETE`), unmarked entries are confirmed by bounded individual reads (at most 100 per call), unreadable or over-budget refuses, so whole-run teardown refuses before any delete with an incomplete manifest.
* Errors carry fixed codes; `__suppress_context__` hides caller context in formatted tracebacks only.
* Out of scope in source: certificate or key issuance, storage, rotation, activation, Registry-before-credential ordering, authentication update, the command line (`--apply` still refuses), Device Provisioning Service.
* Packaging: `iothub` extra and `dev` extra pin `azure-iot-hub==2.7.0` and `six==1.17.0`; `dependencies` stay empty.

## Boundaries and owners

* #185 OPEN (criteria: approach and credential owner unchecked; mapping checked; credentials issued/stored unchecked; teardown unchecked). Its latest comment records the 1393 merge as a bounded source increment. The issue "Existing delivery" text is not copied as current truth beyond what the pin shows.
* #110 OPEN (live Hub identities and live acceptance unproven), #109 OPEN epic, #184 OPEN (live streaming stage 2), #111 OPEN (analysis and review task), #1288 OPEN. PR 1395 (child of #109 preparation, base `feat/demo-sensor-review-109-1110`, head `2b050647bff5`) is OPEN and unmerged into main; excluded. The local 109 preparation candidate `a3d5e615f` (research and plan only, no implement) is preparation, not implemented integration.
* Credential owner for the exercise is named in ADR 0003 (exercise issue/rotation/revocation owner); device issuance, secure storage, teardown and live Hub/SQL/UI/model acceptance remain unproved.

## Findings

* No new confirmed defect and no confirmed refactoring from this read. Residuals map to existing owners: credential lifecycle, Registry-before-credential and authentication-update (#185), live Hub and ingestion acceptance (#110, #184), integration and review-task work (#109, #111), UI acceptance (#1288). No duplicate issue is warranted.

## Planning readiness

Ready: one dated section in the existing evidence pack, an index paragraph and an append-only log entry; no change to the NomUX or Bicep sections or old CSV records.
