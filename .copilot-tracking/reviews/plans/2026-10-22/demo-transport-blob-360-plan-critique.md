<!-- markdownlint-disable-file -->
# RPI Plan Critique: demo-transport-blob-360

## Metadata

* Task ID: demo-transport-blob-360
* Critique date: 2026-10-22
* Plan: .copilot-tracking/plans/2026-10-22/demo-transport-blob-360-plan.md
* Phase details: .copilot-tracking/details/2026-10-22/demo-transport-blob-360-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: offline-only private-Blob result transport replacing the ARM tag relay for the in-VNet SQL staff job; no Azure changes. Plan User Decisions DN1 to DN5 are authoritative and are not challenged.
* Research and evidence considered: .copilot-tracking/research/2026-10-22/demo-transport-blob-360-research.md; infra/scripts/staff_azure.py; infra/scripts/staff-azure-worker.py; infra/modules/storage.bicep; infra/staff-initializer-rbac.bicep; infra/tests/test_staff_azure.py (existence only); infra/cutover-proof.Dockerfile; infra/.dockerignore; tools/rpi-checks.py; .github/workflows/src-ci.yml.
* Decisions, dependencies, and acceptance criteria considered: DN1 to DN5, FR1 to FR6, NFR1 to NFR3, AC1 to AC5, P01 to P04 tasks.
* Assessment boundary: static reading of the plan, details, research and named code. No code was run and no live Azure state was inspected. Findings concern correctness, security, fail-closed behaviour, import cycles, Bicep index stability, controller reachability and test coverage.

## Coverage Assessment

| ID | Coverage | Evidence or concern |
|---|---|---|
| FR1 / P01-T03 | Partial | Worker write path covered; retry/idempotence and write-failure exit semantics undefined (PC-004, PC-009) |
| FR2, FR3, FR4 / P01-T01 | Partial | Envelope covered; reader bounds, clock skew, size-before-download, MAX_PAGES basis missing (PC-004, PC-005) |
| FR5 / P01-T02 | Partial | Unreachable is an explicit error, but the recovery claim in research is false (PC-001) |
| FR6 / P01-T04 | Partial | Property list stated; URL trust and operator ARM read grant missing (PC-003, PC-006) |
| DN1 private path | Partial | Reader route unproved by design; account-wide Contributor holders can overwrite (PC-006) |
| DN2 completeness | Partial | 64 page ceiling is a silent design limit not tied to measured size (PC-005) |
| DN3 retire old paths | Partial | Relay concept, console remnants and AC2 pattern undefined (PC-008) |
| DN4 roles | Missing | No task or test; research Q6 promised a cheap regression check (PC-011) |
| P02-T01 Bicep | Partial | Append-only noted; no guard test; lifecycle vs versioning unaddressed (PC-007) |
| P02-T02 RBAC | Partial | Default, ordering, operator role, delete power (PC-006) |
| P02-T04 / P04 build and gate | Missing | .dockerignore, rpi-checks and CI file lists omit the new module (PC-002) |
| AC1 tests | Partial | Several fail-closed cases absent (PC-010) |

## Verdict

* Verdict: Revise
* Rationale: the direction is sound and matches DN1 to DN5, but the plan has one false recovery claim, a build/gate inventory gap that would break the image or leave new code unchecked, unvalidated blob-URL trust, an under-specified reader and an unsafe RBAC default. All are planner-correctable offline without a new user decision except PC-005 ceiling choice, which has a recommended default.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Unverified-read recovery claim is false because the run key is ephemeral

* Related IDs: FR5, P01-T02, research Q3, research Risks
* Evidence: infra/scripts/staff_azure.py execute() generates `key` in memory and passes it only in the job secret that the `finally` block deletes; research Q3 says blobs "stay readable by a later private-host read until expiry".
* Concern: after the controller deletes the job, nobody holds the AEAD key. A read refused as unreachable leaves undecryptable ciphertext, so no later read is possible. The SQL job may already have committed.
* Impact: operators may be told to retry the read, or may reapply blindly. DN2 completeness and fail-closed intent are weakened by an unrecoverable outcome with misleading guidance.
* Smallest useful change: correct research and README text; define the unreachable outcome as "SQL/restart outcome unverified, rerun is the recovery, no later read"; reuse the existing "Do not reapply blindly" wording and require an idempotence or verify-first statement for `check` before `apply`. Add a test that unreachable raises StaffJobError, still runs cleanup, and the message contains the unverified wording.
* Action owner: planning parent
* Exact resolving evidence: research Q3 and Risks edited; P01-T02 states the outcome; named test in P02-T03.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: New module is missing from image, ignore, gate and CI inventories

* Related IDs: P01-T01, P02-T04, P04-T01, AC4
* Evidence: infra/.dockerignore whitelists `scripts/staff_azure.py` and `scripts/staff-azure-worker.py` only; infra/cutover-proof.Dockerfile COPY list; tools/rpi-checks.py RUFF_GROUPS and mypy tuple list staff files; .github/workflows/src-ci.yml lines naming those files for ruff/mypy.
* Concern: P02-T04 mentions only the Dockerfile. Without `.dockerignore` the COPY fails at build; if omitted from the image the worker raises ImportError at job start. If omitted from rpi-checks/CI lists, `staff_blob.py` and any new test file are never linted or type-checked, so AC4 passes without covering the new security code. P02-T04 also sits after P01 though P01 tests may import through those paths.
* Impact: broken worker image or unchecked code that the full gate reports green.
* Smallest useful change: expand P02-T04 to Dockerfile, `.dockerignore`, `tools/rpi-checks.py` (RUFF_GROUPS, mypy list, tools tests that pin the lists), `.github/workflows/src-ci.yml` (keep check names), plus a contract test asserting every staff script imported by the worker is in the COPY and ignore lists.
* Action owner: planning parent
* Exact resolving evidence: task text names all four files; contract test listed; `tools/rpi-checks.py --all` output shows the new files linted.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Blob endpoint is taken from app env and sent to the worker without trust validation

* Related IDs: FR6, P01-T03, P01-T04
* Evidence: plan P01-T04 binds `blob_url` from API env `ZF_BLOB_ACCOUNT_URL`; P01-T03 puts the account URL in the request; worker uses ManagedIdentityCredential.
* Concern: no rule restricts scheme, host or path. A mutated env value, userinfo, query string, alternate host or sovereign/custom domain would make the worker present a managed-identity token and ciphertext to an unintended endpoint, and the controller would validate against a different account than the one ARM verified.
* Impact: token and data exposure to an unexpected endpoint; the FR6 private-account check could be about a different account than the one written.
* Smallest useful change: add a shared strict parser (https only, host exactly `<account>.blob.core.windows.net`, no userinfo, port, path, query or fragment, account name matches the ARM-resolved account in the same subscription and resource group); the worker re-validates the received URL and the fixed container name; add tests for each rejected form.
* Action owner: planning parent
* Exact resolving evidence: P01-T01/T04 name the parser; tests for rejection cases listed.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Reader and writer fail-closed rules are under-specified

* Related IDs: FR2, FR3, FR4, FR5, P01-T01, P01-T02, P01-T03
* Evidence: plan P01-T01 lists constants and function names only; staff_azure.py polls status in a loop and `replicaRetryLimit` is 0; TTL is 900 s while default `seconds` is 600 and callers may pass larger.
* Concern: missing rules for (a) listing: prefix must be `<run>/` with the 32-hex run validated, exact names `page-NNN.json` with bounded index, listing capped at MAX_PAGES + 1 and refusing any extra, including non-current versions if listed; (b) check blob size from properties before download and cap ciphertext length; (c) read only after execution status Succeeded and never when Failed, Stopped, Canceled or Degraded; (d) tolerate bounded clock skew but require not-after to exceed the job deadline (reject `seconds` greater than TTL minus margin) and refuse not-after beyond a maximum; (e) bounded connection timeout and retry count so "unreachable" returns within the deadline instead of SDK default retries; (f) worker must exit non-zero if any write fails, handle ResourceExists from `overwrite=False` as failure (no silent overwrite, no partial success), and write the page that carries `count` consistently so a partial set is detectable; (g) page with `ok` false must surface as failure, as today; (h) credential choice on the controller must be explicit (injected, not silent DefaultAzureCredential fallback through ambient environment or IMDS).
* Impact: ambiguity, resource exhaustion, a long hang, or acceptance of an incomplete or replayed set.
* Smallest useful change: add these as acceptance rules in P01-T01/T02/T03 and map each to a test in PC-010.
* Action owner: planning parent
* Exact resolving evidence: phase details contain items (a) to (h); tests exist for each.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: 64 x 64 KiB ceiling is not derived from a measured size and risks a hidden DN2 conflict

* Related IDs: DN2, FR4, P01-T01, research Q5
* Evidence: research Q5 is synthetic and states the real position count is unknown and not read; MAX_PAGES = 64, PAGE_BYTES = 64 KiB gives a 4 MiB plaintext cap.
* Concern: DN2 forbids silent reduction; refusing at the ceiling is fail-closed, but a real run could then be permanently unusable. The cap is also bounded by the 12 KiB MAX_INPUT and job memory only implicitly.
* Impact: the transport could pass tests and fail on first real use; operators lack a rule to raise the bound safely.
* Smallest useful change: state the cap as a deliberate fail-closed ceiling with arithmetic from the synthetic row size (document rows per run at the cap), make the refusal message explicit, test exact-boundary and boundary-plus-one, and record a live prerequisite to measure real size and re-size under review.
* Action owner: planning parent
* Exact resolving evidence: details give the arithmetic and refusal text; boundary tests; README live prerequisite.
* Decision route: direct planner correction (constants may change after live measurement; no user decision needed now)

<!-- rpi:critique id=PC-006 -->
### PC-006 [High]: RBAC design has an unsafe default, missing operator grant, ordering gap and overbroad data role

* Related IDs: DN1, P02-T02, research Q2
* Evidence: infra/staff-initializer-rbac.bicep existing `includeResultRelay` defaults true while its description requires separate explicit approval; research Q2 requires an operator Storage Blob Data Reader at the container; infra/main.bicep grants api and import identities Storage Blob Data Contributor at account scope; no built-in write-only role exists (research Risks).
* Concern: (a) P02-T02 names a new param `includeResultBlob` without a default; it must default false so a plain deployment grants nothing. (b) The operator Reader grant and any ARM read the controller needs for FR6 (storage account and container properties) are in no task. (c) The container role scope uses an `existing` child resource, so the role template needs the account and container to exist first; this is a deployment ordering prerequisite. (d) Contributor at container scope also permits delete and overwrite by the worker identity; api and import identities already hold account-wide Contributor and can overwrite or delete `staff-results` blobs. The plan documents only the worker overwrite risk.
* Impact: accidental grant on deploy, an unrunnable controller, and an undocumented tamper surface.
* Smallest useful change: default `includeResultBlob` false with the same approval wording; add the operator Reader and discovery ARM read as parameterised, default-off, reviewable definitions or as explicit live prerequisites; state the ordering prerequisite; add the account-wide Contributor residual risk (detected by AEAD and exact-set validation but not prevented) to the README trust statement; update text-contract tests for the assignment scope string, default and absence of account-scope grants.
* Action owner: planning parent
* Exact resolving evidence: P02-T02 text and tests; README prerequisite list; Bicep text-contract test asserting default false and container scope.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Bicep index stability and lifecycle details are not guarded

* Related IDs: P02-T01, G3
* Evidence: infra/modules/storage.bicep `blobContainers[4]` (audit-archive) and `[5]` (ledger-digests) are referenced by index; the `containers` array is the only source. No managementPolicies resource exists today.
* Concern: "append at end" is a convention only; any insertion would silently attach immutability policies to the wrong container, and an immutable result container would break lifecycle deletion. The lifecycle rule must also handle versioning (account has versioning and 30-day soft delete): without `version` delete actions, expired blobs leave versions; soft delete keeps ciphertext 30 days regardless. A rule prefix must be container-qualified (`staff-results/`), and only one management policy exists per account.
* Impact: wrong immutability binding, retained ciphertext, a rule that does nothing.
* Smallest useful change: append `staff-results` as the seventh element, add a text-contract test asserting the array order and that indices 4 and 5 resolve to audit-archive and ledger-digests (or replace index parents with name lookups); define the policy with base blob and version delete after one day, container-qualified prefix, and state in README that soft delete retention remains and that expiry delay is up to 24 hours (reader not-after is the control).
* Action owner: planning parent
* Exact resolving evidence: contract test; Bicep text showing version delete; README sentence; `bicep build` or recorded NOT RUN per AC3.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: Retirement scope omits the relay concept and AC2 has no defined pattern

* Related IDs: DN3, G2, AC2, P01-T02, research Q1
* Evidence: staff_azure.py passes `relay` in the payload and env `ZF_STAFF_RELAY`, `discover` gates on relay job capacity, `Management.request` in staff-azure-worker.py special-cases `TAG_VERSION`, cleanup error text refers to "encrypted relay tags", infra/tests/test_setup_entra.py and infra/README.md also reference staff_azure; `decode_result` and `encode_result` serve the console/tag chunk format.
* Concern: the plan retires tags but not explicitly the relay job lookup, relay env/payload fields, the TAG_VERSION branch, chunk codecs, console decode path and messages. `includeResultRelay` in the RBAC template and consumers outside the named test file (test_setup_entra, README) may be left stale. AC2's "tag/console result code" grep has no pattern, so it cannot fail.
* Impact: dead code that preserves rejected paths, stale operator guidance, and a vacuous acceptance check.
* Smallest useful change: list the exact symbols (result_prefix, tags_url, result_tags, read_result, clear_result, chunk codecs, MAX_CHUNKS, TAG_VERSION, ZF_STAFF_RELAY, `relay` field, relay capacity gate, relay messages, `includeResultRelay`) and files to scan; define AC2 as a grep over those names across infra/ and the tests returning no match except the superseded README history.
* Action owner: planning parent
* Exact resolving evidence: AC2 contains the pattern; scan output recorded in the changes log.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-009 -->
### PC-009 [Medium]: StaffJobError move and import graph are unspecified and risk a cycle or a coupling regression

* Related IDs: P01-T01, P01-T03
* Evidence: staff-azure-worker.py imports from staff_azure; plan says define StaffJobError in staff_blob and re-export from staff_azure; scripts rely on the script directory being on sys.path (worker in /app/scripts).
* Concern: the direction is acceptable only if staff_blob imports nothing from staff_azure or the worker, and the worker switches to staff_blob so the controller module (and its ARM helpers) is not loaded in the job. No test pins this; a later late-import fix could reintroduce a cycle, and `isinstance` identity across the re-export must hold for existing tests.
* Impact: import-time failure in the image, or two distinct exception classes.
* Smallest useful change: state that staff_blob has no intra-repo imports, the worker imports only staff_blob and staff_roster, and add tests: `staff_azure.StaffJobError is staff_blob.StaffJobError`, and importing staff_blob alone in a clean interpreter succeeds.
* Action owner: planning parent
* Exact resolving evidence: details text and the two tests.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-010 -->
### PC-010 [Medium]: AC1 test list omits several fail-closed and security cases

* Related IDs: AC1, P02-T03, FR2 to FR6, NFR1
* Evidence: AC1 names boundary, tamper, replay, expiry, extra-blob, missing-page, unreachable and size tests only; no worker test is planned although the worker is rewired.
* Concern: not covered: each FR6 property failing independently (public access Enabled, shared key on, anonymous on, container publicAccess not None, container missing, no private endpoint); URL rejection forms (PC-003); run-prefix confusion (another run with a shared prefix); non-matching or oversized names; blob larger than the cap checked before download; status Failed/Stopped skips the read and still cleans up; `ok: false` page; worker write failure exits non-zero, ResourceExists refused, nothing logged (NFR1 assert no key, payload or URL in output); cross-run page substitution, reordered or duplicate index; not-after beyond maximum; credential injection (no ambient fallback); bounded timeout; cleanup-not-confirmed message updated; unreachable path still deletes the job.
* Impact: security-critical branches can regress unseen while the gate reports green.
* Smallest useful change: replace AC1 with an enumerated test matrix in P02-T03 mapping each rule from PC-001, PC-003, PC-004 and this list to a named test, including a worker test module added to the PC-002 lists.
* Action owner: planning parent
* Exact resolving evidence: matrix in phase details; test names present and passing; coverage shown in the gate receipt.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-011 -->
### PC-011 [Low]: DN4 has no implementation or verification task

* Related IDs: DN4, research Q6, P03-T01
* Evidence: research Q6 promises "design text only, plus a regression check where cheap"; phase details contain only README wording in P03-T01.
* Concern: DN4 constraints (never directory-admin roles, admin-prefixed account stays ProgrammeManager, immutable bindings not overwritten, no names/UPNs/object IDs collected) are asserted without pointing to existing evidence or a test.
* Impact: an unverified claim in the evidence pack; reviewers cannot confirm the statement.
* Smallest useful change: cite the existing setup-entra tests and #363 behaviour by file and test name in P03-T01, or add one text-level check; state that production assignment code is unchanged.
* Action owner: planning parent
* Exact resolving evidence: README statement carries the cited test names; those tests run in P04.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Strengths: owner decisions are encoded as controls; AEAD with associated data binds run, operation and digests; the ARM restart path is preserved; the offline-only boundary and live prerequisites are explicit; no disclosure of names, UPNs or object IDs.
* Residual risks to accept explicitly: controller reachability and Entra data-plane roles are unproved live; soft delete and versions retain ciphertext for 30 days; account-wide Contributor holders can overwrite or delete blobs (detected, not prevented); lifecycle expiry latency of up to 24 hours.

## Questions or Blocking Evidence Gaps

* None blocking. PC-005 ceiling choice has a recommended default; no user decision is required.

## Limitations

* Static review only; the test file and Bicep were not executed; hosted and live behaviour unverified; the contents of test_staff_azure.py and test_setup_entra.py were not read in detail.

## Recommended Next Action

* The planning parent applies PC-001 to PC-011 directly to the plan and phase details, then finalises without another critique.

## Related Artifacts

| Path | Description |
|---|---|
| .copilot-tracking/plans/2026-10-22/demo-transport-blob-360-plan.md | Plan under critique |
| .copilot-tracking/details/2026-10-22/demo-transport-blob-360-phase-details.md | Phase details |
| .copilot-tracking/research/2026-10-22/demo-transport-blob-360-research.md | Research |

## Next Steps

* Return to the planning parent (`/rpi-plan` if standalone) to revise; no user response is required.
