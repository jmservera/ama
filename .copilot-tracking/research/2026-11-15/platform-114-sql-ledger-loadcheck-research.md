---
description: "Primary evidence artifact for Issue #114 per-year ledger pre-reliance verification and loadcheck cost reporting"
---
<!-- markdownlint-disable-file -->

# Task Research: platform-114-sql-ledger-loadcheck

| Field              | Value                                                                                      |
|--------------------|--------------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                                 |
| Researcher / agent | RPI Agent (`rpi-research`)                                                                 |
| Status             | Complete                                                                                   |
| Artifact path      | .copilot-tracking/research/2026-11-15/platform-114-sql-ledger-loadcheck-research.md        |

## Research Brief

* What to research: Exact contracts, inheritance hierarchy, error handling, and test coverage in `src/core` (`store.py`, `sqlstore.py`, `mssqlstore.py`, `ledger.py`, `synthetic/loadcheck.py`) plus ADR-0001/ADR-0002 and PRD load/latency/cost targets needed to deliver the remaining offline-testable engineering slice for Issue #114.
* Why it matters: Issue #114 requires (1) deterministic pre-reliance per-year audit chain and sealed ledger digest verification proven across multi-year (`2024`, `2025`, `2026`) audit entries before reliance, and (2) structured load-check latency and cost evaluation against PRD targets with honest `Unknown` reporting when Azure meter inputs are absent, without claiming live Azure SQL runs or DH-005 cloud drills.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, `rpi-review`, and coordinator branch review.
* Scope: `src/core/src/zava_forward/core/{store,sqlstore,mssqlstore,ledger}.py`, `src/core/src/zava_forward/core/synthetic/loadcheck.py`, `src/core/tests/{test_recovery,test_sqlstore,test_loadcheck}.py`, `src/core/README.md`, `docs/adrs/{0001-azure-architecture,0002-pilot-readiness-architecture}.md`, and `docs/prds/zava-forward-retrofit-programme-demonstrator.md`.
* Non-goals: Live Azure SQL deployment/load runs, live Azure point-in-time restore drills, claiming Issue #114 full closure (`Refs #114`, not `Closes #114`), UI changes, or running `tools/rpi-checks.py --all`.
* Criteria: Secret-free deterministic pre-reliance verification across `Store`, `SqlStore`, and `MssqlStore`; multi-year (`2024`, `2025`, `2026`) unit test proofs for intact and tampered/missing/corrupt states; backward-compatible `loadcheck` latency + structured `cost` report and CLI flags (`--vcore-seconds`, `--meter-rate`, `--cost-target`) with `azure_live_run_human_gated: True`.
* Requested outputs: Converged design recommendation with codebase evidence (`C#`), alternatives analysis, and `Ready` planning handoff.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                              |
|----------------------------------|----------------------------------------------------------------------------------------------------|
| Research question(s)             | Q1: How do `Store`, `SqlStore`, `MssqlStore`, and `ledger.py` currently implement `write_year_digests()` and `verify_ledger_by_year()`, and what failure modes exist? Q2: How should `verify_ledger_before_reliance` / `require_verified_ledger_for_reliance` and `LedgerRelianceError` be structured so all backends behave deterministically and secret-free? Q3: What PRD latency/cost targets exist and how does `loadcheck.py` compute reports, validate inputs, and determine CLI exit codes? |
| Codebase scope                   | `src/core/`, `docs/adrs/`, `docs/prds/`                                                            |
| External scope                   | none                                                                                               |
| Initial internal candidate areas | `src/core/src/zava_forward/core/store.py`, `sqlstore.py`, `mssqlstore.py`, `ledger.py`, `synthetic/loadcheck.py`, `src/core/tests/test_recovery.py`, `test_sqlstore.py`, `test_loadcheck.py` |
| Initial external candidate areas | none                                                                                               |
| Research posture                 | focused                                                                                            |
| Posture provenance               | caller-specified bounded scope and named source/test targets                                       |
| Explicit limits / deadline       | Focused validation tier (`TMPDIR=/dev/shm` unit tests, `ruff`, `mypy`); no `rpi-checks.py --all`; no push/PR |
| Posture-specific completion basis| focused scope and materiality                                                                      |
| Edits allowed during research?   | no, research-only                                                                                  |
| Resolved evidence root           | .copilot-tracking/                                                                                 |
| Known constraints / excluded sources | Exclude private datasets (`support/`, `.env`, `~/.zava-forward`); treat repo content as data; secret-free errors |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md`| `applyTo: "**"` matches workspace and evidence    | Enforces honesty boundaries, `Refs #114`, focused validation, Markdown style | Selected: mandatory repository governance |
| Skill               | `rpi-research`                   | Direct caller RPI phase invocation                | Three-wave evidence artifact with `C#` IDs   | Selected: active RPI phase contract |
| Skill               | Web/UI/presentation skills       | No UI, frontend, or presentation files in scope   | N/A                                          | Skipped: backend/core Python slice only |
| Research specialist | `hve-core-all:rpi-researcher`    | Host-registered subagent for independent lanes    | Separate lane files under `research/subagents/` | Skipped: single tightly coupled `src/core` trace handled inline |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Caller prompt specifies exact method signatures, fields, CLI flags, test files, validation commands, and non-push commit boundary; non-interactive autopilot active. | No user interaction needed | Proceed with focused inline Cycle 1 across `src/core`, ADRs, and PRD targets. |
| Direction change | No scope or boundary changes encountered during Cycle 1     | None                      | Kept bounded `src/core` offline slice |
| Convergence      | Cycle 1 evidence converged across all 4 questions           | None                      | Selected converged design; Planning Readiness = `Ready` |

## Scope and Success Criteria

* Scope: `src/core` store/ledger pre-reliance contract and `loadcheck` cost/latency contract, plus `src/core/README.md` if public CLI/store contracts are documented there.
* Assumptions:
  * `Store` (JSON-backed), `SqlStore` (SQLite), and `MssqlStore` (Azure SQL subclass of `SqlStore`) already share or override `write_year_digests` and `verify_ledger_by_year` — to be verified in Wave 1/2.
  * PRD defines NFR latency and database cost targets — to be verified in Wave 1/2.
* Success criteria:
  * Every research question is answered with `path:line` `C#` evidence.
  * Three waves (Wider, Deeper, Contrarian) completed in order.
  * Converged design handles edge cases (current vs past year determination, empty ledger, unsealed past year when `require_sealed_past_years=True` vs `False`, corrupt JSON/digest rows, tampered chain, negative/NaN/partial cost CLI arguments, CLI exit codes).

## Task Research Requests

* Explicit requests: Deliver pre-reliance per-year ledger verification (`verify_ledger_before_reliance`, `require_verified_ledger_for_reliance`, `LedgerRelianceError`) in `store.py` / `sqlstore.py` (inherited by `mssqlstore.py`) with multi-year tests in `test_recovery.py` and `test_sqlstore.py`; extend `loadcheck.py` (`evaluate_cost`, `run`, `main` with `--vcore-seconds`, `--meter-rate`, `--cost-target`) and `test_loadcheck.py`.
* Inferred research questions: How is "completed past year" determined deterministically in tests and runtime? How does `loadcheck` treat `within_target: False` vs `status: "Unknown"` for overall pass/exit code? Are any other callers in `src/` importing `verify_ledger_by_year` or `loadcheck.run`?
* Caller constraints and non-goals: Offline-testable slice only; preserve existing `test_loadcheck.py` assertions and CLI exit-code semantics; `Refs #114`; local commit only.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Scope code edits to `src/core` (`store.py`, `sqlstore.py`, `synthetic/loadcheck.py`, tests, and directly related `src/core/README.md`) | User intake prompt   | Constrains all waves to `src/core` and upstream callers/docs |
| exclude                                                  | Do not run `tools/rpi-checks.py --all`, do not push or open PR, do not claim live Azure run | User intake prompt   | Focused validation tier and `azure_live_run_human_gated: True` |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status |
|---:|------------------|------------------------------------------|-----------|--------|
| Q1 | How do `Store`, `SqlStore`, `MssqlStore`, and `ledger.py` implement `write_year_digests()`, `verify_ledger_by_year()`, and audit storage? | depth | H | answered |
| Q2 | What edge cases and exception/problem contracts are needed for `verify_ledger_before_reliance`, `require_verified_ledger_for_reliance`, and `LedgerRelianceError` across multi-year (`2024`, `2025`, `2026`) audit logs? | depth | H | answered |
| Q3 | What are the exact PRD load, latency, and cost targets, and how should `evaluate_cost`, `run`, and `main` in `loadcheck.py` integrate cost reporting while preserving existing CLI exit-code semantics? | depth | H | answered |
| Q4 | Do any downstream callers in `src/core`, `src/api`, `src/orchestrator`, or `src/importer` call `verify_ledger_by_year`, `write_year_digests`, or `loadcheck` in ways that could break or benefit from alignment? | breadth | M | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-10-15/issue-114-azure-sql-ledger-research.md`, `.copilot-tracking/research/2026-10-18/issue-114-loadcheck-evidence-research.md`, `.copilot-tracking/reviews/2026-11-04/issue-114-r1-review.md`
* Reused (verified) findings: Issue #114 has three acceptance criteria; live Azure SQL load/cost and DH-005 restore drills remain human/Azure-gated (`Refs #114`), while PR #403 hardened `loadcheck.py` against empty-sample and worker-error false positives.
* Superseded / stale: `2026-10-15` references to `mvp/zavaforward_mvp/` are superseded by `src/core/src/zava_forward/core/` after the 2026-10-27 cut-over.

## Executed Research Cycles

### Cycle 1

* Wave 1 — Wider:
  * Investigated ADR-0001 (`C1`), ADR-0002 (`C2`), PRD NFR-002 and cost governance (`C3`, `C4`), `src/core/README.md` (`C5`), and all repository callers of `write_year_digests`, `verify_ledger_by_year`, and `loadcheck` (`C6`).
  * Established that `MssqlStore` (`mssqlstore.py:217`) subclasses `SqlStore` (`sqlstore.py:171`), which subclasses `Store` (`store.py:67`), and that `orchestrator/digest_blob.py` and `core/ledger_digest_blob.py` invoke `store.write_year_digests()` with zero arguments.
* Wave 2 — Deeper:
  * Traced `ledger.py` (`make_year_digest`, `year_digests`, `verify_years`, `write_year_digest`, `read_year_digests`, `read_digests`) (`C7`), `Store` audit and digest methods (`C8`), `SqlStore` `_audit_rows`, `audit_head`, `_audit_evidence`, and `_SyncLock` (`C9`), `MssqlStore` SQL adapter and lazy `dberror` property (`C10`), and `synthetic/loadcheck.py` (`LIMITS`, `run`, `main`) plus `test_loadcheck.py` (`C11`, `C12`).
  * Confirmed PRD NFR-002 core workload limits (`list <= 1.0s`, `detail <= 1.0s`, `write <= 2.0s` at 5 sessions, 2 writers) match `loadcheck.LIMITS`, and confirmed PRD/BRD OD-51 cost honesty rules (`tokenomics.py`, `scale-load-2026-11-15.json`): unpriced or unmetered runs must report `"Unknown"` rather than fabricating zero cost.
* Wave 3 — Contrarian:
  * Tested three failure hypotheses against a naive implementation:
    1. *Hypothesis A (sealing tampered past years)*: Calling `write_year_digests()` unconditionally *before* checking chain integrity would seal tampered unsealed past-year entries into write-once `year-YYYY.json` files. Counter-design: verify audit readability, chain integrity, root digests, `audit_head` (on `SqlStore`/`MssqlStore`), and existing year digests *before* sealing completed past years, then seal completed past years and re-verify `verify_ledger_by_year()`.
    2. *Hypothesis B (`SqlStore` unsealed tail deletion & filename/schema swap)*: Deleting all rows of the current unsealed year (`2026`) in SQL without updating `audit_head` leaves `verify_ledger_by_year()` reporting `intact=True` unless `audit_head` (`count`, `hash`) and root digests (`digest-*.json`) are also verified; swapping `year-2024.json` to contain `{"year": "2025", ...}` or `"algorithm": "md5"` bypasses `DIGEST_KEYS` presence-only checks unless filename-to-year binding and digest types/hashes are validated; accessing `MssqlStore.dberror` when `mssql_python` is absent raises `ModuleNotFoundError` unless guarded against `ImportError`.
    3. *Hypothesis C (`loadcheck.main` backward-compatible exit codes & zero meter rate)*: Making `status == "Unknown"` exit non-zero in `loadcheck.main` would break existing `test_cli_exit_status_tracks_real_run_evidence` (`--data ... --homes 1 --seconds 1` expects exit `0` when latency passes without cost flags), and allowing `--meter-rate 0` would violate OD-51 no-fake-zero rules. Counter-design: require `meter_rate_per_vcore_second > 0`, `vcore_seconds >= 0`, `target_cost >= 0`, compute exact `Decimal` product, set `within_target: None` when inputs are absent, and fail CLI exit code (`1`) on cost only when `within_target is False` (while invalid CLI values exit `2` via `ap.error` before `open_store`).
* Parent Synthesis:
  * Accepted: Pre-verify chain + `audit_head` + existing anchors before `write_year_digests()`, support optional keyword-only `current_year: int | None = None` and `seal_past_years: bool = True` alongside `require_sealed_past_years: bool = True`, sanitize all problems/errors to fixed codes without paths or connection strings, and implement `evaluate_cost` + `run` + `main` in `loadcheck.py` with `Decimal` arithmetic and `azure_live_run_human_gated: True`.
  * Rejected: Failing `loadcheck.main` when meter flags are omitted (`status: "Unknown"`), because existing CLI contract tests require exit `0` for offline latency checks.
  * Deferred: Live Azure SQL serverless load execution and witnessed DH-005 point-in-time restore drill (remain tracked on Issue #114 as human/cloud-gated).
* Re-entry Evaluation: No further cycle required; all questions (`Q1`–`Q4`) are answered with direct `path:line` codebase evidence and contrarian edge cases are resolved.

## Evidence Log

| ID   | Source (`path:line`) | Summary | Supports |
|------|----------------------|---------|----------|
| `C1` | `docs/adrs/0001-azure-architecture.md:145` | Selects Azure SQL serverless (`GP_S_Gen5`) with append-only ledger tables and periodic digest export to immutable Blob storage, requiring cost/latency measurement before production scale claims. | Q1, Q3 |
| `C2` | `docs/adrs/0002-pilot-readiness-architecture.md:174` | Requires per-year audit verification and independent immutable ledger digest anchors before operational reliance. | Q1, Q2 |
| `C3` | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1899` | Defines `NFR-002` core workload targets: warm p95 `<= 1.0s` for case list/detail and `<= 2.0s` for controlled writes at 5 concurrent sessions (2 writers). | Q3 |
| `C4` | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:167` | Clarifies historical EXA-012 cost figures are non-authoritative and unpriced/unmetered costs must remain `Unknown` rather than fabricated (`BRD OD-51`, echoed in `src/core/src/zava_forward/core/tokenomics.py:6`). | Q3 |
| `C5` | `src/core/README.md:4671` | Documents Issue #114 per-year ledger digests (`--seal-years`, `--by-year`), `loadcheck` NFR-002 runner, and explicit unverified Azure SQL / cost / DH-005 boundaries. | Q1, Q3, Q4 |
| `C6` | `src/core/src/zava_forward/core/ledger_digest_blob.py:894` | Downstream callers (`ledger_digest_blob.py:894,1518` and `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py:183`) call `store.write_year_digests()` with zero positional args; zero-arg compatibility must be preserved. | Q4 |
| `C7` | `src/core/src/zava_forward/core/ledger.py:64` | Implements `make_year_digest`, `year_digests`, `verify_years` (`lines 78-104`), `write_year_digest` (`lines 118-126`), `read_year_digests` (`lines 129-139`), and `read_digests` (`lines 142-149`); `read_year_digests` drops filename binding if JSON `year` was swapped and `read_digests` raises raw `ValueError`/`OSError` on corrupt root digests. | Q1, Q2 |
| `C8` | `src/core/src/zava_forward/core/store.py:190` | `Store` defines `audit_entries()`, `verify_ledger()`, `verify_ledger_by_year()`, and `write_year_digests()`; `audit_entries()` raises `json.JSONDecodeError`/`OSError` on corrupt JSONL lines. | Q1, Q2 |
| `C9` | `src/core/src/zava_forward/core/sqlstore.py:414` | `SqlStore` subclasses `Store`, maintains `audit_head (id=1, count, hash)` (`lines 97, 414-424, 486-496`), and uses `self.dblock` for atomic `(rows, head)` snapshots via `_audit_rows(0)`. | Q1, Q2 |
| `C10` | `src/core/src/zava_forward/core/mssqlstore.py:217` | `MssqlStore` subclasses `SqlStore` and reuses `SqlStore`'s `audit` and `audit_head` SQL queries via `_Conn`; `MssqlStore.dberror` (`line 221`) imports `mssql_python` lazily and raises `ImportError` when the driver extra is absent. | Q1, Q2 |
| `C11` | `src/core/src/zava_forward/core/synthetic/loadcheck.py:20` | Defines `LIMITS = {"list": 1.0, "detail": 1.0, "write": 2.0}`, `pct`, `grow`, `run`, and `main`; validates parameters before touching `store.cases` or calling `open_store`. | Q3 |
| `C12` | `src/core/tests/test_loadcheck.py:274` | Enforces strict `mypy` and `ruff format` checks (`src/core/pyproject.toml:42-62`), verifies CLI invalid args exit `2` before `open_store`, verifies `set(env) == {"ZF_DATA", "ZF_STATE", "ZF_STORE"}`, and asserts CLI exit `0` on good latency runs without cost flags. | Q3, Q4 |

## Synthesized Findings

1. **Unified Inheritance & Pre-Reliance Ledger Contract (`Q1`, `Q2`, `Q4`)**:
   * Placing `LedgerRelianceError`, `verify_ledger_before_reliance(self, *, require_sealed_past_years: bool = True, current_year: int | None = None, seal_past_years: bool = True) -> dict[str, Any]`, and `require_verified_ledger_for_reliance(self, *, require_sealed_past_years: bool = True, current_year: int | None = None, seal_past_years: bool = True) -> dict[str, Any]` on `Store` (`store.py`), with an internal `_reliance_audit_snapshot()` hook overridden on `SqlStore` (`sqlstore.py`) and `LedgerRelianceError` re-exported from `sqlstore.py`, automatically delivers identical pre-reliance semantics across `Store`, `SqlStore`, and `MssqlStore` (`C8`, `C9`, `C10`).
   * Pre-reliance verification must: (a) read audit entries and optional SQL `audit_head` atomically while catching `OSError`, `ValueError`, `TypeError`, `KeyError`, `RuntimeError`, and driver `dberror` (guarded for `ImportError` on `MssqlStore`) into secret-free machine-readable `problems`; (b) validate root digests (`digest-*.json`), `year-*.json` filename-to-payload `year` and schema invariants, full chain links, and `audit_head` parity *before* sealing so tampered history is never sealed into write-once digest files; (c) invoke `write_year_digests()` for completed past years (`< effective_year`) when `seal_past_years=True` and pre-checks pass; (d) execute `verify_ledger_by_year()` and verify that every past year (`< effective_year`) with audit entries has an intact matching sealed digest when `require_sealed_past_years=True`; and (e) return `reliance_allowed: False` with secret-free `problems` (or raise secret-free `LedgerRelianceError` in `require_verified_ledger_for_reliance`) whenever any year chain, `audit_head`, root digest, or sealed year digest is tampered, missing, dropped, or unreadable (`C7`, `C8`, `C9`).
2. **Structured Load, Latency, and Cost Evaluation Against PRD Targets (`Q3`, `Q4`)**:
   * `evaluate_cost(vcore_seconds=None, meter_rate_per_vcore_second=None, target_cost=None)` in `loadcheck.py` validates finite numeric bounds (`vcore_seconds >= 0`, `meter_rate_per_vcore_second > 0` so zero never fabricates a free run, `target_cost >= 0`, rejecting `bool`/`NaN`/`Inf`), computes exact `Decimal` `measured_cost` when both `vcore_seconds` and `meter_rate_per_vcore_second` are supplied (`status: "measured"`), evaluates `within_target: bool` when `target_cost` is also supplied (`None` otherwise), and returns `status: "Unknown"` with ordered `missing_inputs` (`vcore_seconds`, `meter_rate_per_vcore_second`, `target_cost`) and `azure_live_run_human_gated: True` when meter inputs are absent (`C3`, `C4`, `C11`).
   * `loadcheck.run(...)` validates cost inputs up front (preserving `Mock(spec=[])` pre-store rejection) and attaches both `load` (`sessions`, `writers`, `seconds`, `total_requests`, `achieved_rps`) and `cost` alongside per-class `classes` (`n`, `p50`, `p95`, `max`, `limit`, `within`). `loadcheck.main(...)` adds `--vcore-seconds`, `--meter-rate`, and `--cost-target`, validates them via `ap.error(...)` before `open_store(env)` without altering `env` keys, and exits `0` iff `errors == 0`, all `classes[*]["within"]` are `True`, and `cost["within_target"] is not False` (`C11`, `C12`).

## Alternatives Considered

| Option | Summary | Disposition | Rationale |
|--------|---------|-------------|-----------|
| Option A: Shared `Store` contract + `SqlStore` `audit_head` snapshot hook + pre-seal integrity gate | Implement `LedgerRelianceError`, `verify_ledger_before_reliance`, and `require_verified_ledger_for_reliance` on `Store`, override atomic snapshot/`audit_head` validation on `SqlStore` (inherited by `MssqlStore`), and extend `loadcheck.py` with `Decimal`-backed `evaluate_cost`. | **Selected** | Avoids code duplication across 3 stores, prevents sealing tampered past years, catches SQL `audit_head` truncation, and preserves all existing signatures and CLI exit codes (`C6`–`C12`). |
| Option B: Duplicate standalone methods in `store.py`, `sqlstore.py`, and `mssqlstore.py` | Maintain three separate verification implementations per backend. | Rejected | Violates DRY and risks drift between `SqlStore` and `MssqlStore`, which share identical `audit` and `audit_head` SQL schemas (`C9`, `C10`). |
| Option C: Fail `loadcheck.main` (exit `1`) whenever `cost["status"] == "Unknown"` | Require meter inputs on every CLI invocation for exit `0`. | Rejected | Breaks existing `test_loadcheck.py:299` CLI exit-code contract for local synthetic latency checks (`C12`) and contradicts caller requirement to preserve existing CLI exit-code semantics. |

## Selected Recommendation and Decisions

* Selected recommendation: **Option A** as detailed in Synthesized Findings 1 and 2.
* Confirmed decisions:
  * Preserve `Refs #114` (never `Closes #114`) and `azure_live_run_human_gated: True` because live Azure SQL serverless runs and DH-005 restore drills remain external human/cloud gates (`C1`, `C5`).
  * Keep `LedgerRelianceError` messages and `problems` entries strictly secret-free and filesystem-path-free (fixed reason/code strings and basenames only).
  * Validate `test_loadcheck.py` against both `ruff format --check` and strict `mypy` (`src/core/pyproject.toml`), and run all `ruff check`, `ruff format --check`, `mypy`, and `TMPDIR=/dev/shm` targeted unit tests in `src/core`.
* Open / unresolved decisions: None for this bounded offline slice.

## Risks and Potential Further Research

* Risks:
  * `pyproject.toml` excludes `store.py`, `sqlstore.py`, `loadcheck.py`, `test_recovery.py`, and `test_sqlstore.py` from `ruff format` and `mypy`, while including `test_loadcheck.py` in both strict `mypy` and `ruff format`. Running `python3 -m ruff check`, `python3 -m ruff format --check`, and `python3 -m mypy` from `src/core` verifies exact CI parity.
* Further research (out of scope for this offline task):
  * Live Azure SQL `GP_S_Gen5` metered `loadcheck` run and witnessed DH-005 point-in-time restore drill once target Azure subscription credentials and human approval are available.

## Readiness and Handoff

| Field                | Value                                                                                      |
|----------------------|--------------------------------------------------------------------------------------------|
| Research disposition | executed                                                                                   |
| Planning Readiness   | Ready                                                                                      |
| Blocking items       | None                                                                                       |
| Next phase           | `rpi-plan` (parent-owned automatic continuation)                                           |

## Artifact Self-Check

* [x] Three waves (`Wider`, `Deeper`, `Contrarian`) executed in order and synthesized by parent.
* [x] Every material claim grounded in `C1`–`C12` with workspace-relative `path:line` citations.
* [x] Research remained strictly read-only on source files; zero secrets or private data written.
* [x] Research disposition (`executed`) and Planning Readiness (`Ready`) recorded.

