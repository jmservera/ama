<!-- markdownlint-disable-file -->
# RPI Plan Critique: #360 correction1 (Blob credential binding and operation budget)

## Metadata

* Task ID: demo-transport-blob-360-correction1
* Critique date: 2026-10-22
* Plan: .copilot-tracking/plans/2026-10-22/demo-transport-blob-360-correction1-plan.md
* Phase details: .copilot-tracking/details/2026-10-22/demo-transport-blob-360-correction1-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: single critique of the correction plan for two blocking review findings (ambient Blob credential; unbounded Blob operations blocking cleanup).
* Research and evidence considered: .copilot-tracking/research/2026-10-22/demo-transport-blob-360-correction1-research.md; infra/scripts/staff_azure.py; infra/scripts/staff_blob.py; infra/scripts/setup-entra.py (Azure class 120-200, contexts 323, transport construction ~1095, run flow ~1714); infra/tests/test_staff_azure.py.
* Decisions, dependencies, and acceptance criteria considered: D1-D3, FR1-FR4, AC1-AC3, P01-P03.
* Assessment boundary: static reading only; no code was run and no SDK behaviour was verified. Live behaviour stays unverified, as the plan states.

## Coverage Assessment

| ID | Coverage | Evidence or concern |
|----|----------|---------------------|
| FR1 / P01-T01 | Partial | Adapter bound to cli.call is sound (execute is given a `transport` Azure built from `cli.profile`, setup-entra.py ~1095, so fallback profile flows through). Expiry parsing and error mapping underspecified (PC-003); deadline interaction (PC-001). |
| FR2 / P01-T02 | Covered | Kwargs are plain azure-core client options. Retry arithmetic note in PC-006. |
| FR3 / P02-T01,T02 | Partial | Preflight wording wrong (PC-002); abandoned-thread side effects (PC-001); fake-clock hazard (PC-004). |
| FR4 / P02-T03 | Partial | Zero or negative remaining budget not specified (PC-006). |
| AC1 | Partial | Construction alone does not prove token acquisition uses the profile (PC-005). |
| AC2 | Partial | No time or thread-release mechanism for tests (PC-004). |
| AC3 | Covered | Gate steps and ordering present; test-suite updates missing (PC-004). |

## Verdict

* Verdict: Revise
* Rationale: The design (profile-bound TokenCredential plus thread-bounded calls) is credible and consistent with the code, but the plan has one behavioural regression (preflight wording), one unbounded-time hole in the new credential, and test-design gaps that would break existing tests or leave AC1/AC2 unproven. All are planner-correctable.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Token subprocess is not bound to the operation budget and an abandoned thread can race cleanup

* Related IDs: FR1, FR3, P01-T01, P02-T01, D2
* Evidence: infra/scripts/setup-entra.py:140-160 (`call` uses 120 s when `self.deadline is None`, otherwise `min(120, deadline - now)`); infra/scripts/staff_azure.py:252-254 (preflight runs before `cli.deadline` is set) and ~362 (finally resets `cli.deadline`).
* Concern: In preflight `cli.deadline` is None, so each `az account get-access-token` may run up to 120 s inside a 45 s `_bounded` budget; the abandoned daemon thread keeps the az subprocess alive after the error. In read, the abandoned thread shares mutable `cli.deadline`, which the finally block then resets to now+90, so a stale token call may run concurrently with cleanup az calls against the same profile (token cache).
* Impact: Stall hazard and profile contention during the secret-cleanup path the correction is meant to protect.
* Smallest useful change: Have `ProfileCredential` carry its own absolute deadline (or have `_bounded` set a cancelled flag the credential checks before spawning az) and cap the subprocess timeout to remaining budget; set `cli.deadline` for the preflight window and restore it. State that after expiry the credential refuses new token calls.
* Action owner: planning parent
* Exact resolving evidence: P01-T01/P02-T01 text naming the credential-level deadline/cancel flag; a test where the stalled token call is released after expiry and no further `subprocess.run` happens.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: FR3 applies "unverified wording" to preflight timeouts

* Related IDs: FR3, P02-T02, AC2
* Evidence: infra/scripts/staff_blob.py preflight message "no job was created and no fallback exists"; infra/tests/test_staff_azure.py:566-570 asserts "no job was created".
* Concern: A preflight stall occurs before any job or secret exists; "outcome unverified" would wrongly imply SQL may have changed and would conflict with the existing contract.
* Impact: Misleading operator guidance and a likely failing/weakened test.
* Smallest useful change: Specify distinct wording: preflight expiry reuses the existing "unreachable or unauthorized ... no job was created" message; only read expiry uses the unverified wording.
* Action owner: planning parent
* Exact resolving evidence: FR3/P02-T02 amended; test asserts each wording.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Token adapter parsing and error mapping are underspecified

* Related IDs: FR1, P01-T01, AC2
* Evidence: infra/scripts/setup-entra.py `call` raises `AzureError`/`SetupError`, may return None or non-dict.
* Concern: `expiresOn` from az is a naive local-time string; accepting it without a defined parse risks wrong expiry (token reuse past expiry or constant refresh). Plan does not say what happens when `accessToken` is missing/non-string, `expires_on` absent, or output is not a dict, nor that AzureError and SetupError both map to the generic error without chaining (`from None`).
* Impact: Wrong expiry or leaked detail through exception chaining; AC2 "failing token acquisition" is not fully defined.
* Smallest useful change: Require `expires_on` (int epoch); if absent, fail closed with the generic error rather than guessing local time (or define explicit local-time parsing). Validate types; catch Exception and raise `StaffJobError(...) from None`.
* Action owner: planning parent
* Exact resolving evidence: P01-T01 rewritten with these rules; tests for missing expiry, non-dict, AzureError, and a token canary absent from raised message and `__cause__`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Existing tests and the fake-clock harness are not accounted for

* Related IDs: P02-T01, P03-T01, AC2, AC3
* Evidence: infra/tests/test_staff_azure.py:758 patches `default_container` with `lambda url:`; :525-533 `run_with_clock` patches `JOB.time.monotonic`/`sleep` on the shared `time` module, advancing 250 s per sleep.
* Concern: (1) New `default_container(url, cli)` signature breaks the existing lambda and any similar patches. (2) `_bounded` computes remaining time from `time.monotonic`; under the fake clock the remaining time can be zero/negative or huge while `Thread.join` uses real time, causing spurious timeouts in existing tests. (3) AC2 tests need small injectable budgets (the module constants must be patchable) and an Event to release stalled threads, otherwise tests take 45 s or leak threads.
* Impact: Regressions across the existing suite and slow or flaky new tests.
* Smallest useful change: Add a P03-T01 item to update the patches/signature; make `_bounded` use a captured real-time source consistent with the caller deadline (or take a remaining-seconds value computed once), and specify patchable PREFLIGHT_BUDGET/READ_BUDGET plus Event-released stubs.
* Action owner: planning parent
* Exact resolving evidence: plan text naming these changes; full infra test run green with no new runtime beyond a few seconds.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: AC1 does not prove token acquisition uses the selected profile

* Related IDs: FR1, AC1, P03-T01
* Evidence: infra/scripts/setup-entra.py:323-335 (fallback swaps `operator` to the isolated profile); ~1095 (`transport = Azure(cli.profile, ...)`); research D3.
* Concern: Constructing a `ContainerClient` never calls `get_token`. Asserting "credential is the profile adapter" is structural only; it does not show the az subprocess runs with `AZURE_CONFIG_DIR` set to the fallback profile, nor that `DefaultAzureCredential` is never reached, nor that `execute` hands the transport (not another Azure) to `default_container`.
* Impact: A regression back to ambient auth, or use of the wrong profile object, would pass.
* Smallest useful change: Extend AC1: call `credential.get_token("https://storage.azure.com/.default")` through patched `subprocess.run`, assert args and `env["AZURE_CONFIG_DIR"]` equal the fallback profile; patch `azure.identity.DefaultAzureCredential` to raise; assert `execute` passes its `cli` argument to `default_container`.
* Action owner: planning parent
* Exact resolving evidence: named tests with those assertions in P03-T01.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: Budget arithmetic and edge cases unstated

* Related IDs: FR2, FR4, P02-T02, P02-T03
* Evidence: plan P01-T02 (5 s connect, 15 s read, retry_total 2) versus 45 s budgets.
* Concern: Worst-case SDK time per request (about 3 x 20 s plus backoff) exceeds the 45 s budget, so the budget, not the retry policy, is the real bound; remaining budget at or below zero (job deadline nearly reached) is not specified; repeated read polls each abandon a thread on stall but the first stall already aborts, which should be stated.
* Impact: Ambiguity only; low risk.
* Smallest useful change: One sentence in P02: budget supersedes retries; non-positive remaining budget raises immediately without starting a thread; a read timeout is terminal for the run.
* Action owner: planning parent
* Exact resolving evidence: P02 details amended; a test for zero remaining budget.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Correct source of operator context: transport Azure is built from `cli.profile`, so ARM and Blob share the fallback profile.
* Alternatives (AzureCliCredential, signal.alarm, socket-only timeouts) were considered and rejected with reasons; read-only abandoned threads are an accepted, documented residual risk.
* Live storage data-plane token and role remain unverified, correctly listed as follow-up.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Static review only; azure-core retry/credential behaviour, `az` output fields (`expires_on` availability by CLI version) and test runtime were not executed.

## Recommended Next Action

* Highest-impact finding: PC-001 (with PC-004 equal in test-regression risk)
* Action owner: planning parent
* Smallest next action: revise P01-T01, P02-T01/T02 and P03-T01 as above, then finalize without another critique.
* User response required: no

## Next Steps

No user action is required; the planning parent revises directly (all findings are direct corrections).
