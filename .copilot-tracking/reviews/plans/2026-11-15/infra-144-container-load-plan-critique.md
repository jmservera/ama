<!-- markdownlint-disable-file -->
# Plan Critique: Issue #144 Container Hosting Completeness

## Metadata

* Task ID: issue-144
* Task slug: infra-144-container-load
* Plan under review: .copilot-tracking/plans/2026-11-15/infra-144-container-load-plan.md
* Phase details under review: .copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md
* Evidence sources: .copilot-tracking/research/2026-11-15/infra-144-container-load-research.md (`C1`-`C19`), GitHub Issue #144, `src/check-container.py`, `infra/modules/containerapps.bicep`, `infra/resident-demo.bicep`, `infra/live-receiver-job.bicep`, `infra/live-simulator-job.bicep`, `infra/scripts/pipeline.py`, `infra/scripts/deploy.py`, `infra/README.md`, `infra/tests/*`, `src/*/pyproject.toml`, and target workload entrypoints under `src/`
* Critique execution: Complete
* Verdict: Revise
* Critique date: 2026-11-15

## Inputs and Criterion Boundary

### Assessed Artifacts

* .copilot-tracking/plans/2026-11-15/infra-144-container-load-plan.md
* .copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md
* .copilot-tracking/research/2026-11-15/infra-144-container-load-research.md
* `src/check-container.py`, `src/api/Dockerfile`, `src/agents/Dockerfile`, `src/orchestrator/Dockerfile`, `src/importer/Dockerfile`, `src/api/Dockerfile.resident-demo`, `src/api/live-simulator.Dockerfile`
* `infra/modules/containerapps.bicep`, `infra/resident-demo.bicep`, `infra/live-receiver-job.bicep`, `infra/live-simulator-job.bicep`, `infra/scripts/pipeline.py`, `infra/scripts/deploy.py`, `.github/workflows/src-deploy.yml`, `infra/README.md`
* `infra/tests/test_container_contract.py`, `infra/tests/test_container_hosting_completeness.py`, `infra/tests/test_bicep_policy.py`, `infra/tests/test_pipeline.py`, `infra/tests/test_deploy.py`, `infra/tests/test_resident_demo_deploy.py`
* `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/resident_demo/__main__.py`, `src/api/src/zava_forward/api/live_receiver.py`, `src/api/src/zava_forward/api/live_simulator.py`, `src/agents/src/zava_forward/agents/__main__.py`, `src/agents/src/zava_forward/agents/worker.py`, `src/orchestrator/src/zava_forward/orchestrator/__main__.py`, `src/orchestrator/src/zava_forward/orchestrator/token_store.py`, `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py`, `src/orchestrator/src/zava_forward/orchestrator/ranking_publish.py`, `src/orchestrator/src/zava_forward/orchestrator/source_monitor.py`, `src/orchestrator/src/zava_forward/orchestrator/document_rescan.py`, `src/importer/src/zava_forward/importer/__main__.py`
* `src/api/tests/scale_load.py`, `src/api/tests/test_scale_fixture_load_and_restart.py`, `src/core/src/zava_forward/core/resident_showcase.py`, `src/core/src/zava_forward/core/synthetic/run_plan.py`

### Confirmed Requirements and Decisions

* Execute the full RPI loop (`research`, `plan`, `implement`, `review`) with dated artifacts under `2026-11-15` for Issue #144 on branch `feat/infra-144-container-load` in `/home/azureuser/source/ama-demo-wt/feat-144-container-load`.
* Deliver and prove all four unticked Issue #144 acceptance criteria:
  * Worker and job images are real, versioned, and deployed through the pipeline.
  * Container hardening (non-root, read-only file system, dropped capabilities) is enforced in the deployed app, not only in CI.
  * A load test against the declared scale fixture is run and recorded without claiming production scale.
  * Single-replica and restart behaviour is verified with audit persistence.
* Add dedicated test module `infra/tests/test_container_hosting_144.py` and evidence documentation.
* Validate under the user-confirmed Focused tier (`PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests:infra/tests python3 -m unittest infra/tests/test_container_hosting_144.py -q` and `python3 -m ruff check infra && python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_container_hosting_144.py`, plus targeted regression suites).
* Commit locally with the required `Co-authored-by` trailer and do not push.

### Out-of-Scope or Unavailable Evidence

* Live Azure subscription deployment receipts, live ACR pushes, live Azure Queue runs, and hosted multi-replica/autoscaling measurements are outside this local non-push scope and must remain explicitly distinguished from local compiled/runtime/benchmark verification.
* External full-gate receipt workflows (`tools/rpi-checks.py --all`) are out of scope per the confirmed Focused validation tier decision.

## Verdict Summary

Critique execution is Complete and the verdict is Revise. The candidate plan and phase details correctly solve the core Azure Container Apps `2025-07-01` `securityContext` schema constraint (`C14`) and `ENTRYPOINT` prohibition (`C10`) by combining Bicep `ZF_CONTAINER_HARDENING=enforced` + `EmptyDir` scratch mounts with a stdlib `zava_forward.core.container_hardening` guard, `pipeline.py` `rank-publish` digest verification, and fresh 60,000-home scale/restart runs. However, five concrete codebase hazards in `P01`-`P04` would cause swallowed hardening failures, import-time `SystemExit`, `test_bicep_policy.py` failures, host-UID subprocess crashes, or residual `infra/README.md` contradictions if not corrected before `rpi-implement`. All five findings are direct planner corrections requiring no user input.

## Severity Summary

| Severity | Count |
|----------|-------|
| Critical | 0     |
| High     | 3     |
| Medium   | 2     |
| Low      | 0     |

## Findings

### PC-001: Entrypoint broad exception blocks, missing `main()`, and unguarded module-level `sys.exit(...)` will swallow `ContainerHardeningError` or abort tests on import

* Severity: High
* Related IDs: FR-3, P01, P01-T01, P01-T02, P04-T01, C10, C11
* Evidence: `.copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md:72,113-155`; `src/orchestrator/src/zava_forward/orchestrator/token_store.py:55`; `src/api/src/zava_forward/api/resident_demo/__main__.py:52`; `src/api/src/zava_forward/api/live_receiver.py:155`; `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py:242`; `src/orchestrator/src/zava_forward/orchestrator/ranking_publish.py:101`; `src/api/src/zava_forward/api/live_simulator.py:497-516`; `src/orchestrator/src/zava_forward/orchestrator/__main__.py:1-3`; `src/importer/src/zava_forward/importer/__main__.py:217`; `src/agents/src/zava_forward/agents/__main__.py:5`; `src/core/pyproject.toml`; `src/api/pyproject.toml`; `src/orchestrator/pyproject.toml`
* Concern: `P01-T01` defines `ContainerHardeningError(RuntimeError)` and `P01-T02` wires `enforce_from_env(...)` into 12 entrypoints without accounting for existing broad `except` blocks, missing `main()` functions, top-level `sys.exit(...)` calls, and per-package lint/type rules:
  * `token_store.py:55` catches `(KeyVaultError, TokenStoreError, RuntimeError)` and prints `{"status": "token-store-renewal-failed", ...}` (`return 1`); because `ContainerHardeningError` subclasses `RuntimeError`, placing `enforce_from_env()` inside that `try:` block swallows hardening failures as identity/Key Vault errors.
  * `resident_demo/__main__.py:52` (`except Exception:` printing `"Refusing to start: SQL read failed (ContainerHardeningError)."`), `live_receiver.py:155` (`except Exception:` printing `"Cannot run: RECEIVER_FAILED"`), `digest_blob.py:242` (`except Exception:` printing `"LEDGER_DIGEST_ALERT"`), and `ranking_publish.py:101` (`except Exception:` printing `"RANKING_PUBLISH_ALERT"`) will misreport startup hardening refusal if `enforce_from_env(env)` runs inside their domain `try:` blocks, while `live_simulator.py:497-516` parses `ZF_SIM_SEED` and `argparse` before startup guards.
  * `orchestrator/__main__.py:1-3` has no `main()` function at all, and `importer/__main__.py:217` (plus `agents/__main__.py:5`) executes `sys.exit(main(...))` unconditionally at import time with no `if __name__ == "__main__":` guard. Importing `zava_forward.importer.__main__` in `infra/tests/test_container_hosting_144.py` (`P04-T01`) will raise `SystemExit` at import time.
  * `src/core/pyproject.toml` enforces `mypy` (`strict = true`) and `ruff` (`E`, `F`, `I`, `B`, `UP`, line length 100) on `container_hardening.py`, whereas `src/api/pyproject.toml` and `src/orchestrator/pyproject.toml` explicitly exclude `server.py`, `digest_blob.py`, and `token_store.py` from `ruff format` and `I001`.
* Impact: Hardening violations in five entrypoints will be misclassified as SQL, Key Vault, or Blob failures; `test_container_hosting_144.py` will crash with `SystemExit` or `AttributeError` when importing `importer.__main__` or `orchestrator.__main__`; and running `ruff format` across excluded legacy files or omitting strict annotations in `container_hardening.py` will break package CI checks (`src-ci.yml`).
* Smallest useful change: Specify in `P01-T01` and `P01-T02` that: (1) every entrypoint executes `enforce_from_env(env)` at the top of `main()` before `argparse`, `ZF_SIM_SEED` parsing, or domain `try:` blocks, catching `ContainerHardeningError` explicitly to write a fixed sanitized hardening refusal to `sys.stderr` and return/exit non-zero (`2`); (2) `orchestrator/__main__.py` defines `main(argv=None, env=None) -> int` guarded by `if __name__ == "__main__":` (preserving no-arg `zava-forward-orchestrator 0.1.0` output for `src/check-container.py:67-71`) and `importer/__main__.py:217` wraps `sys.exit(main(sys.argv[1:]))` under `if __name__ == "__main__":`; and (3) `container_hardening.py` satisfies `mypy --strict`, while edits to `server.py`, `digest_blob.py`, and `token_store.py` stay surgical without whole-file `ruff format`.
* Action owner: planner
* Resolving evidence: Updated `P01-T01` and `P01-T02` task specifications in `.copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md` and `P01` checklist summary in `.copilot-tracking/plans/2026-11-15/infra-144-container-load-plan.md`.
* Decision route: Direct planner correction.

### PC-002: `enablePublicSimulationLane` command override in `containerapps.bicep` writes `/state` before `zava_forward.api` starts and is constrained by `test_bicep_policy.py` forbidden-substring rules

* Severity: High
* Related IDs: FR-2, FR-3, P01-T02, P02-T01, P04-T01, C1, C13
* Evidence: `infra/modules/containerapps.bicep:136-149,313-325`; `infra/tests/test_bicep_policy.py:2324-2358`; `.copilot-tracking/research/2026-11-15/infra-144-container-load-research.md:107,172`; `.copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md:126,180-238`
* Concern: When `enablePublicSimulationLane` is `true`, `infra/modules/containerapps.bicep:136-149` overrides the `api` container `command` with `['python', '-c', publicSimulationRecipe]`, which creates `/state/public-simulation`, checks symlink state, and writes `/state/public-simulation/hmac.key` before calling `os.execv(sys.executable, [sys.executable, "-m", "zava_forward.api"])`. Without calling `enforce_from_env()` at the start of `publicSimulationRecipe`, the container performs `/state` writes before hardening is checked. Meanwhile, `infra/tests/test_bicep_policy.py:2331-2358` asserts both `len(on_container["env"]) == len(off_container["env"]) + 2` and that none of `("os.environ", "getenv", "urandom", "token_bytes", "secrets", "observe", "request")` appear in `publicSimulationRecipe`. Also, `tokenRenewal` (`containerapps.bicep:313-325`) defines an inline `env: [...]` array rather than `concat(commonEnv, [...])`, and research lines `107,172` mention checking hardening on `/healthz` whereas `P01-T02` excludes changing `/healthz` (`infra/tests/test_container_hosting_completeness.py:118`).
* Impact: Either the public-simulation API lane mutates `/state` prior to hardening validation, `tokenRenewal` misses `commonEnv` hardening variables, or introducing `os.environ`/`getenv` in `publicSimulationRecipe` (or touching `/healthz` in `server.py`) breaks `test_bicep_policy.py` or `test_container_hosting_completeness.py`.
* Smallest useful change: Update `P02-T01` to: (1) add `ZF_CONTAINER_HARDENING`, `PYTHONDONTWRITEBYTECODE`, `TMPDIR`, and `ZF_STATE` to `commonEnv` (preserving `len(on_container["env"]) == len(off_container["env"]) + 2`) AND explicitly add them to `tokenRenewal`'s inline `env` block; (2) prepend `from zava_forward.core.container_hardening import enforce_from_env; enforce_from_env()` at the start of `publicSimulationRecipe` before `os.makedirs` while explicitly prohibiting `os.environ` / `getenv` literals inside `publicSimulationRecipe`; and (3) note in `P01-T02` that startup-time enforcement (including `publicSimulationRecipe`) intentionally supersedes the research `/healthz` remark so `server.py`'s `/healthz` handler remains unchanged.
* Action owner: planner
* Resolving evidence: Updated `P01-T02` and `P02-T01` boundaries and target notes in `.copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md`.
* Decision route: Direct planner correction.

### PC-003: Host-UID subprocess conflict in `SIGKILL` restart / load execution, irreversible in-process `prctl` / `umask` side effects, and PEP 420 `sys.path` setup in `test_container_hosting_144.py`

* Severity: High
* Related IDs: FR-3, FR-4, FR-5, P01-T01, P03-T01, P04-T01, C16, C17
* Evidence: `.copilot-tracking/plans/2026-11-15/infra-144-container-load-plan.md:21`; `.copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md:75-78,278-329,373-399`; `src/api/tests/test_scale_fixture_load_and_restart.py:57-83`
* Concern: Three runtime/test interaction pitfalls exist across `P01-T01`, `P03-T01`, and `P04-T01`:
  * `P04-T01` item 4 (`details:394-398`) calls for running live separate-process API `SIGKILL` restart over SQLite `SqlStore` *"with `ZF_CONTAINER_HARDENING=enforced` (via mocked/compliant check or subprocess verification)"*, and `plan:21` refers to running `P03` benchmarks with the hardened runtime path in place. However, `ApiProcess` (`test_scale_fixture_load_and_restart.py:66-71`) spawns a real child OS process (`[sys.executable, "-m", "zava_forward.api.server"]`) on the Linux host where `UID != 10001` and `/app` is absent; parent-process `unittest.mock.patch` cannot cross `subprocess.Popen`, so passing `ZF_CONTAINER_HARDENING=enforced` to `ApiProcess` on the host will cause `server.main()` to exit non-zero before `/healthz` comes up.
  * In `P01-T01` (`details:75-78`), calling `os.umask(0o077)` and `libc.prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)` directly inside the in-process `unittest` runner mutates process-global `umask` and irreversibly sets `NoNewPrivs=1` on the test runner process itself.
  * In this workspace, none of the five `zava_forward.*` packages are installed into site-packages, and `zava_forward` is an implicit PEP 420 namespace package (no `__init__.py`). While `P04-T01` (`details:373-381`) notes adding `src/orchestrator/src` and `src/importer/src` to subprocess `PYTHONPATH`, any in-process imports of `zava_forward.orchestrator.*` or `zava_forward.importer.*` inside `test_container_hosting_144.py` under the caller's exact `PYTHONPATH` (`src/core/src:src/agents/src:src/api/src:...`) will fail with `ModuleNotFoundError` unless `test_container_hosting_144.py` also appends those two paths to `sys.path` and calls `importlib.invalidate_caches()`.
* Impact: `test_container_hosting_144.py` (or `P03-T01` if `ZF_CONTAINER_HARDENING=enforced` is exported in the host environment) will fail with child API startup refusal, `ModuleNotFoundError` on `zava_forward.orchestrator` / `zava_forward.importer`, or cross-test `umask`/`NoNewPrivs` contamination.
* Smallest useful change: Clarify in `P01-T01`, `P03-T01`, and `P04-T01` that: (1) `enforce_container_hardening(...)` accepts injectable `umask_fn` / `prctl_fn` / `status_text` / path parameters for side-effect-free in-process unit tests, while real kernel `prctl(PR_SET_NO_NEW_PRIVS, 1)` + `/proc/self/status` `NoNewPrivs == 1` + `os.umask(0o077)` execution is verified inside an isolated child `python3 -c` subprocess; (2) host-level `scale_load.py`, `test_scale_fixture_load_and_restart.py` (`P03-T01`), and `ApiProcess` `SIGKILL` restart tests run with `ZF_CONTAINER_HARDENING` unset (matching plain host/developer mode), paired with dedicated child-subprocess tests with `ZF_CONTAINER_HARDENING=enforced` on the non-10001 host proving real OS-process fail-closed startup refusal across all four packages; and (3) `infra/tests/test_container_hosting_144.py` registers `ROOT / "src/orchestrator/src"` and `ROOT / "src/importer/src"` in both `sys.path` (followed by `importlib.invalidate_caches()`) and child subprocess `PYTHONPATH`.
* Action owner: planner
* Resolving evidence: Updated `P01-T01`, `P03-T01`, and `P04-T01` details in `.copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md` and `Executive Summary` / `P04-T01` text in `.copilot-tracking/plans/2026-11-15/infra-144-container-load-plan.md`.
* Decision route: Direct planner correction.

### PC-004: Criterion 1 gap on `orchestrator` scheduled job entrypoint ("still only prints a version") and `infra/scripts/deploy.py` `rank-publish` parity

* Severity: Medium
* Related IDs: FR-1, P01-T02, P02-T01, P02-T02, P04-T01, P04-T02, C4, C7, C8
* Evidence: `infra/README.md:1338`; `src/orchestrator/src/zava_forward/orchestrator/__main__.py:1-3`; `infra/modules/containerapps.bicep:385-428,477-518`; `infra/scripts/deploy.py:37-39`; `infra/tests/test_deploy.py`; `infra/tests/test_bicep_policy.py:421-452`; `src/check-container.py:67-71`
* Concern: `infra/README.md:1338` explicitly identifies *"The orchestrator entrypoint still only prints a version"* as part of Criterion 1 (`Worker and job images real, versioned, deployed through the pipeline`). Under the current candidate plan (`P01-T02`), `orchestrator/__main__.py` still only prints `zava-forward-orchestrator 0.1.0`, so `job-${prefix}-orchestrator` (`containerapps.bicep:385-428`, running every 5 minutes) remains a version-printing stub rather than a bounded standby/diagnostic job entrypoint like `agents` (`python -m zava_forward.agents serve`, which enters clean standby when live dispatch is not enabled). Additionally, `infra/scripts/deploy.py:37-39` discovers existing `orchestratorImage` jobs via `("orchestrator", "auth-renewal", "ledger-verify")`, omitting `"rank-publish"` whereas `P02-T02` updates only `infra/scripts/pipeline.py`.
* Impact: Leaving `orchestrator/__main__.py` as a version-only stub and omitting `"rank-publish"` from `deploy.py:37-39` leaves an explicit Criterion 1 defect documented in `infra/README.md:1338` unresolved and creates image-discovery drift between `pipeline.py` and `deploy.py`.
* Smallest useful change: Expand `P01-T02`, `P02-T01`, and `P02-T02` minimally so that: (1) `zava_forward.orchestrator.__main__.main` preserves exact `zava-forward-orchestrator 0.1.0` stdout when invoked with no arguments (satisfying `src/check-container.py:67-71`) and supports a bounded `run` subcommand (`command: ['python', '-m', 'zava_forward.orchestrator']`, `args: ['run']` on `orchestrator` in `infra/modules/containerapps.bicep`, compatible with `test_bicep_policy.py:421-452`) that enforces hardening, validates required environment shape (`QUEUE_ENDPOINT`, `TASK_QUEUE`, `API_BASE_URL`), and exits `0` with a structured standby report when live dispatch is not active (or non-zero on invalid configuration); and (2) `P02-T02` also adds `"rank-publish"` to `targets` in `infra/scripts/deploy.py:37-39` and verifies `infra/tests/test_deploy.py` remains green.
* Action owner: planner
* Resolving evidence: Updated `P01-T02`, `P02-T01`, and `P02-T02` specifications in `.copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md` and `FR-1` / `Scope` in `.copilot-tracking/plans/2026-11-15/infra-144-container-load-plan.md`.
* Decision route: Direct planner correction.

### PC-005: `P04-T02` `infra/README.md` target section range omits the immediately preceding `#118` startup-guard paragraph (`lines 1317-1333`) that would contradict the new runtime guard

* Severity: Medium
* Related IDs: FR-1, FR-2, FR-4, FR-5, P04-T02, C8, C9
* Evidence: `.copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md:426-445`; `infra/README.md:1317-1404`; `infra/tests/test_container_hosting_completeness.py:124-133,152-161`
* Concern: `P04-T02` cites `infra/README.md` lines `1298-1365`, whereas the actual Issue #144 table and benchmark narrative span `infra/README.md:1334-1404`, immediately preceded at lines `1317-1333` by `## Hardened source image rollout (#118)` stating *"Images remain non-root but no longer carry a fail-closed startup guard that would prevent Container Apps startup."* Updating the Issue #144 status table without reconciling lines `1323-1332` will leave an internal factual contradiction in `infra/README.md`; conversely, editing lines `1344-1404` carelessly could drop phrases pinned by `infra/tests/test_container_hosting_completeness.py` (`Revision rollback:`, `activeRevisionsMode: Single`, `pipeline.py`, `src-deploy.yml`, `"not at declared scale"`, and `"makes no production"`).
* Impact: `infra/README.md` would either contradict the newly implemented `zava_forward.core.container_hardening` fail-closed startup guard, fail `test_container_hosting_completeness.py`, or blur local contract/benchmark proof with live Azure deployment receipts.
* Smallest useful change: Update `P04-T02` to target `infra/README.md:1317-1404`, reconciling the `#118` hosted-hardening note (explaining that ACA `2025-07-01` still lacks ARM `securityContext`, while deployed Bicep templates now set `ZF_CONTAINER_HARDENING=enforced` + `EmptyDir` scratch volumes enforced at process startup by `zava_forward.core.container_hardening` without `ST_RDONLY`/`CapBnd` assumptions), updating the `#144` hosting status table and adding the dated `2026-11-15` 60,000-home benchmark evidence alongside preserved `2026-11-01`/`2026-11-13` records, keeping all `test_container_hosting_completeness.py` pinned phrases intact, and stating explicitly that no live Azure deployment receipt was executed in this local run.
* Action owner: planner
* Resolving evidence: Updated `P04-T02` context, intent, and validation notes in `.copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md`.
* Decision route: Direct planner correction.

## Coverage Assessment

| Area | Assessment | Notes |
|------|------------|-------|
| Requirements and acceptance criteria | Needs planner revision | All four unticked Issue #144 criteria are mapped (`FR-1`..`FR-5`), subject to closing the `orchestrator` stub + `deploy.py` `rank-publish` parity gap (`PC-004`). |
| Research and evidence grounding | Sound with minor alignment fix | Grounded in verified codebase facts `C1`-`C19`; `P01-T02` must explicitly supersede research's `/healthz` remark so `server.py` `/healthz` remains untouched (`PC-002`). |
| Phase ordering and dependencies | Credible | `P01` (runtime guard + entrypoints) -> `P02` (Bicep + pipeline/deploy scripts) -> `P03` (60,000-home scale and restart runs) -> `P04` (`test_container_hosting_144.py`, `infra/README.md`, validation) is properly ordered. |
| Task boundaries and likely targets | Needs planner revision | Add `infra/scripts/deploy.py` (`PC-004`), `publicSimulationRecipe` + `tokenRenewal` inline `env` handling (`PC-002`), and exact entrypoint guard placement + `if __name__ == "__main__":` fixes (`PC-001`). |
| Test ownership and coverage lock | Needs planner revision | Single canonical module `infra/tests/test_container_hosting_144.py` respects test-file budget, once `sys.path` PEP 420 cache invalidation, subprocess `prctl`/`umask` isolation, and host-UID vs `ApiProcess` separation are specified (`PC-003`). |
| Decisions, trade-offs, and constraints | Credible | Preserves user-confirmed Focused validation tier, non-production-scale framing, `ENTRYPOINT` ban, `resident_showcase` `FORBIDDEN_ENV_PREFIXES`, `main.bicep` empty `orchestratorImage` fallback, and local-only commit constraint. |
| Risks, failure modes, and missed concerns | Addressed by `PC-001`..`PC-005` | Surfaces `RuntimeError` subclass swallowing in `token_store.py`, `test_bicep_policy.py` forbidden substrings on `publicSimulationRecipe`, `mypy --strict` / `ruff format` exclusions, and `infra/README.md` contradiction risk. |
| Validation sufficiency | Credible | Matches the user-confirmed Focused validation commands plus existing `infra/tests` and affected `src/` unit suites (`az bicep v0.48.1`, `ruff 0.17.3`, and `mypy 2.4.1` verified installed locally). |
| Implementation readiness | Ready after planner revision | Ready for `rpi-implement` immediately once `PC-001`..`PC-005` are folded into the plan and phase details. |

## Residual Risks and Limitations

* Azure Container Apps `2025-07-01` does not expose kernel-level `securityContext.readOnlyRootFilesystem` in ARM/Bicep (`C14`), and this task runs locally without pushing or mutating Azure resources; therefore, deployed-app hardening is enforced and proven at the compiled ARM resource specification layer (`ZF_CONTAINER_HARDENING=enforced` + `EmptyDir` scratch volumes) and in-process Python startup layer (`UID/GID 10001:10001`, `prctl(PR_SET_NO_NEW_PRIVS, 1)`, zero active/permitted/inheritable/ambient capabilities, `/` and `/app` write refusal, writable scratch check), while live hosted rollout remains deployment-time scope and must be documented honestly in `infra/README.md`.
* The 60,000-home scale and `SIGKILL` restart benchmarks (`scale_load.py` and `test_scale_fixture_load_and_restart.py`) measure a single local OS process over SQLite `SqlStore` for a 60 s window (`53,821` events) rather than the 1,800 s / 600,000-event hosted workload, and intentionally record `meets_declared_workload: false` without claiming production scale.

## Handoff

* Highest-impact finding: `PC-001` (High — entrypoint `RuntimeError`/`Exception` swallowing, missing `orchestrator/__main__.py:main()`, and unguarded `importer/__main__.py:217` `sys.exit(...)` on import).
* Action owner: `planner`
* Smallest next action: Revise `.copilot-tracking/plans/2026-11-15/infra-144-container-load-plan.md` and `.copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md` directly to incorporate `PC-001` through `PC-005`, record the critique disposition table, and finalize the plan for `rpi-implement` without re-running critique.
* User response required: No.
* Next step: Return to the active `rpi-plan` parent to apply `PC-001`..`PC-005` directly and proceed to implementation.
