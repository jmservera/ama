<!-- markdownlint-disable-file -->

# Task Research: immutable-blob-ledger-digests-115-c2-rebase

| Field              | Value                                                                                              |
|--------------------|----------------------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                                         |
| Researcher / agent | rpi-research (RPI Agent automatic child session)                                                   |
| Status             | Complete                                                                                           |
| Artifact path      | .copilot-tracking/research/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-research.md      |

## Research Brief

* What to research: Commit ancestry, exact file/hunk overlap, cross-feature semantic interactions (`#109`, `#189`, `#146` / PR `#1778`), and `src-ci.yml`-equivalent focused validation mechanics for rebasing `feat/demo-115-blob-ledger` (`1b66fd607`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`e282dc327`, PR `#1641`) for Issue `#115` without pushing.
* Why it matters: `origin/feat/demo-164-chat-grounding-provenance-0900` advanced three commits (`704c6b07a` `#109` PR `#1775`, `6bdcf7f90` `#189` PR `#1777`, and `e282dc327` `#146` PR `#1778`) past `fa6f8d1dd`. Both `#146` (`e282dc327`) and `#115` (`84cb5608a`) append a test method at line 72 of `infra/tests/test_monitoring_alerts.py`, and local `unittest` / `ruff` commands must respect `src-ci.yml` module-discovery and `--isolated` lint contracts on this shared non-sandboxed host while leaving `git status --short` completely clean.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` in this automatic RPI child loop.
* Scope: Git commit ranges `fa6f8d1dd..e282dc327` vs `fa6f8d1dd..1b66fd607`, conflict merge in `infra/tests/test_monitoring_alerts.py`, cross-module compatibility across `monitoring_coverage.py`, `main.bicep`, `operationalMonitoring.bicep`, and `src/core`, focused `unittest` / `ruff` / `mypy` validation matching `.github/workflows/src-ci.yml`, and clean post-Review `.copilot-tracking/` commit preservation.
* Non-goals: Pushing to `origin`, running `tools/rpi-checks.py` (full gate), mutating shared `~/.local` Python site-packages, or altering `#109`, `#189`, or `#146` production behavior.
* Criteria: Answer every research question with workspace-relative `path:line` evidence (`C1`–`C8`), execute all three waves (`Wider`, `Deeper`, `Contrarian`) in order, select one evidence-backed convergence option, and record `Planning Readiness: Ready`.
* Requested outputs: Primary research artifact in convergence mode.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                      |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1: Which files conflict or semantically interact between `fa6f8d1dd..1b66fd607` and `fa6f8d1dd..e282dc327`? Q2: How should `infra/tests/test_monitoring_alerts.py` merge `#146` and `#115` assertions cleanly? Q3: What exact `PYTHONPATH` and `ruff` / `mypy` invocations match `src-ci.yml` without module-name shadowing or legacy `infra/` lint noise? |
| Codebase scope                       | `infra/`, `src/core/`, `src/orchestrator/`, `src/api/`, `.github/workflows/src-ci.yml`, `.copilot-tracking/`                               |
| External scope                       | none                                                                                                                                       |
| Research posture                     | focused                                                                                                                                    |
| Posture provenance                   | default (bounded internal rebase and conflict-resolution task with exact commit SHAs and named validation targets)                         |
| Explicit limits / deadline           | Single automatic RPI child run; focused validation tier; do not push; leave clean frozen working tree                                      |
| Posture-specific completion basis    | focused scope coverage across commit ancestry, hunk-level conflict analysis, semantic cross-checks, and `src-ci.yml` command verification  |
| Edits allowed during research?       | no, research-only                                                                                                                          |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                                       |
| Known constraints / excluded sources | Shared non-sandboxed host environment; preserve prior committed RPI critique/review records (`84cb5608a`, `1b66fd607`); keep `Refs #115`   |

## Extension Registry and Provenance

| Kind                | Candidate                                  | Match and provenance                        | Scoped authority or output contract                            | Selected / skipped reason                                                        |
|---------------------|--------------------------------------------|---------------------------------------------|----------------------------------------------------------------|----------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`          | `applyTo: "**"`                             | AMA branch, email privacy, focused validation, RPI retention   | Selected: mandatory repository rules                                             |
| Skill               | `rpi-research`                             | Active Research phase skill                 | Three-wave research artifact and `Planning Readiness` contract | Selected: active phase skill                                                     |
| Research specialist | `hve-core-all:rpi-researcher`              | Registered lane worker                      | Independent subagent research lane                             | Skipped (inline fallback): single tightly coupled git-rebase boundary (<5 probes)|

## User Participation and Research Decisions

| Checkpoint  | Questions or no-interaction rationale                                                                                              | Answers / unanswered | Resulting decision                                                                                              |
|-------------|------------------------------------------------------------------------------------------------------------------------------------|----------------------|-----------------------------------------------------------------------------------------------------------------|
| Intake      | Caller supplied exact parent ref `origin/feat/demo-164-chat-grounding-provenance-0900` (`e282dc327`), branch `feat/demo-115-blob-ledger` (`1b66fd607`), conflict target, validation list, and no-push rule | N/A | Execute focused inline three-wave research without prompting                                                    |
| Convergence | Only `infra/tests/test_monitoring_alerts.py` overlaps; keeping both `#146` and `#115` methods in `AlertOwnerAndRunbookTests` plus `WorkbookPanelTests` preserves all assertions; child `c2-rebase` tracking commit preserves prior committed RPI records | N/A | Select Option A (rebase `84cb5608a` + `1b66fd607` onto `e282dc327`, keep both methods in `test_monitoring_alerts.py`, run `src-ci.yml`-aligned validation, commit `c2-rebase` RPI artifacts locally) |

## Cycle 1 Waves

### Wave 1: Wider (Upstream Commit Lineage and Overlap Surface)

* Verified fetched `origin/feat/demo-164-chat-grounding-provenance-0900` resolves to `e282dc3276992a17507351dd4f75d08a8808f56d` with three commits added after `fa6f8d1dd`: `704c6b07a` (`#109` sensor non-authority invariant, PR `#1775`), `6bdcf7f90` (`#189` simulator run controls and `verify_bicep_run_controls`, PR `#1777`), and `e282dc327` (`#146` job-rank alert parity and 13-task harm declarations, PR `#1778`).
* Compared `git diff --name-only fa6f8d1dd..1b66fd607` (24 files across `84cb5608a` and `1b66fd607`) against `git diff --name-only fa6f8d1dd..e282dc327` (54 files): `infra/tests/test_monitoring_alerts.py` is the **only** overlapping path (`C1`, `C2`), with zero file overlap on `src/core/README.md`, `src/core/pyproject.toml`, `infra/main.bicep`, `infra/modules/storage.bicep`, `infra/modules/containerapps.bicep`, `infra/tests/test_bicep_policy.py`, or `.copilot-tracking/`.

### Wave 2: Deeper (Conflict Seam in `test_monitoring_alerts.py` and Cross-Module Semantic Contracts)

* In `infra/tests/test_monitoring_alerts.py`:
  * Upstream `e282dc327` (`#146` / PR `#1778`) appends `test_ranking_archive_job_failure_alert_routes_to_job_rank_runbook(self) -> None` (`C2`) at the end of `AlertOwnerAndRunbookTests` right above `WorkbookPanelTests` (which asserts `#146`'s cost-vs-budget `ConfiguredMonthlyBudget` / `Unreconciled`, AI usage capability/period beside `AzureCostRecord`, `AI_LIMIT_BREACH` owner/runbook holds, and `Insufficient` missing-data messages, `C3`).
  * Branch commit `84cb5608a` (`#115`) appends `test_installed_ledger_alerts_name_owner_resolvable_runbook_and_core_markers(self) -> None` (`C1`) at the exact same insertion point right above `WorkbookPanelTests`.
  * Retaining `test_ranking_archive_job_failure_alert_routes_to_job_rank_runbook` followed immediately by `test_installed_ledger_alerts_name_owner_resolvable_runbook_and_core_markers` inside `AlertOwnerAndRunbookTests` (preserving all 4 upstream `AlertOwnerAndRunbookTests` methods + all 4 `WorkbookPanelTests` cost/budget/anomaly methods intact) preserves 100% of both `#146` and `#115` coverage within 100-column `ruff format` style.
* Cross-feature semantic checks across `fa6f8d1dd..e282dc327`:
  * `e282dc327` adds `job-rank` (`CANDIDATE`) to `monitoring_coverage.ALERTS` while keeping `ledger-digest-mismatch` and `ledger-verify-missing` at `INSTALLED` (`C4`), and `infra/tests/test_ai_alert_runbook_ownership.py` keeps `test_ledger_digest_alerts_name_owner_and_anchor` expecting `Proposed owner: Digital service owner` (`C5`), matching `ledger_digest_blob.PROPOSED_OWNER`.
  * `6bdcf7f90` (`#189`) inspects `infra/main.bicep` via `verify_bicep_run_controls` (`src/core/tests/test_simulator_run_controls_189.py`) without colliding with `#115`'s `ledgerDigestImmutabilityDays` parameter or `ledgerVerify` wiring, and `704c6b07a` (`#109`) + `6bdcf7f90` (`#189`) + `e282dc327` (`#146`) keep `src/core` `mypy` (`strict = true`) clean.

### Wave 3: Contrarian (`unittest` Path Shadowing, `ruff` Config Resolution, and RPI History Preservation)

* Challenge 1: Why does literal `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests:infra/tests python3 -m unittest discover -s infra/tests -p 'test_*.py' -q` fail on this codebase?
  * Counter-evidence found by direct probe: Both `src/api/tests/test_diagnostic_log_privacy.py` and `infra/tests/test_diagnostic_log_privacy.py` exist (`C6`), AND `infra/tests/test_bicep_policy.py` imports `zava_forward.orchestrator.digest_blob` (`C7`). When `src/api/tests` precedes `infra/tests` on `PYTHONPATH`, `unittest.loader._find_test_path` raises `ImportError: 'test_diagnostic_log_privacy' module incorrectly imported from '.../src/api/tests'`. In `.github/workflows/src-ci.yml:215,239` (`C8`), `infra/tests` runs with all five `src/*/src` distributions installed (`core`, `agents`, `api`, `orchestrator`, `importer`) and **no** `src/*/tests` ahead of `infra/tests`. Placing `infra/tests` first and including `src/orchestrator/src` (`REQUIRE_AZ_BICEP=1 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=infra/tests:src/core/src:src/agents/src:src/api/src:src/orchestrator/src:src/importer/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest discover -s infra/tests -p 'test_*.py' -q`) resolves `infra/tests` cleanly under `src-ci.yml` semantics while keeping all five worktree distributions isolated from shared host `~/.local` `.pth` files.
* Challenge 2: Why does bare `python3 -m ruff check src/core src/api infra` fail on untouched `infra/` files?
  * Counter-evidence found by direct probe: `src/core/pyproject.toml` and `src/api/pyproject.toml` configure `select = ["E", "F", "I", "B", "UP"]` and `line-length = 100`, whereas `infra/` has **no** `pyproject.toml`, causing bare `ruff check infra` on Ruff `0.17.3` to apply unconfigured default/preview lint rules (`FURB162`, `ISC004`, `RUF100`) producing 114 pre-existing errors on untouched `infra/scripts/` and `infra/tests/` files. In `.github/workflows/src-ci.yml:241-249` (`C8`), `infra/` files are always checked with `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`. Running `python3 -m ruff check src/core src/api infra/tests/test_monitoring_alerts.py` (which passes even under Ruff `0.17.3` defaults!) **plus** `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` across `infra/tests/test_monitoring_alerts.py`, `infra/tests/test_bicep_policy.py`, and the `src-ci.yml` `infra/` targets verifies both strictness levels without falsely failing on unrelated legacy `infra/` scripts.
* Challenge 3: Why does `(cd src/core && PYTHONNOUSERSITE=1 python3 -m mypy)` fail while `(cd src/core && PYTHONDONTWRITEBYTECODE=1 python3 -m mypy)` succeeds?
  * Counter-evidence: `mypy 2.4.1` is installed in `/home/azureuser/.local/lib/python3.12/site-packages`, while `src/core/pyproject.toml` pins `mypy_path = ["src", "tests"]` and `files = ["src", "tests"]`, so `(cd src/core && PYTHONDONTWRITEBYTECODE=1 python3 -m mypy)` resolves all `zava_forward.core` modules from the local worktree without touching sibling worktrees.
* Challenge 4: Should we overwrite `1b66fd607`'s committed `immutable-blob-ledger-digests-115-rebase-*` files or record a child `immutable-blob-ledger-digests-115-c2-rebase-*` set?
  * Counter-evidence: Repository policy (`.github/copilot-instructions.md`, tracking retention policy) and RPI Agent one-pass Critique/Review rules forbid overwriting committed critique/review outcomes. Recording this loop in `.copilot-tracking/*/*/immutable-blob-ledger-digests-115-c2-rebase-*` (`parent_task = issue-115-rebase-164-0820`, matching `ux-76-hazard-clock-owner-c2-rebase`) preserves both `84cb5608a` and `1b66fd607` verbatim across the rebase and commits the new RPI set cleanly on top.

## Evidence Log

* `C1`: `infra/tests/test_monitoring_alerts.py:72-89` (on `84cb5608a` / `1b66fd607`) — Adds `test_installed_ledger_alerts_name_owner_resolvable_runbook_and_core_markers` at the end of `AlertOwnerAndRunbookTests`.
* `C2`: `origin/feat/demo-164-chat-grounding-provenance-0900:infra/tests/test_monitoring_alerts.py:72-95` (`e282dc327`) — Adds `test_ranking_archive_job_failure_alert_routes_to_job_rank_runbook` at line 72 of `AlertOwnerAndRunbookTests`; sole overlapping file between `fa6f8d1dd..1b66fd607` and `fa6f8d1dd..e282dc327`.
* `C3`: `infra/tests/test_monitoring_alerts.py:92-120` (and `98-126` on `e282dc327`) — `WorkbookPanelTests` asserts `#146` cost-vs-budget (`ConfiguredMonthlyBudget`, `AzureActualCost='Unknown'`, `Unreconciled`), AI capability/period cost variance, `AI_LIMIT_BREACH` owner/runbook holds, and `Insufficient` missing-data messages.
* `C4`: `origin/feat/demo-164-chat-grounding-provenance-0900:src/core/src/zava_forward/core/monitoring_coverage.py:60-115` (`e282dc327`) — Adds `job-rank` (`CANDIDATE`) to `ALERTS` while retaining `ledger-digest-mismatch` and `ledger-verify-missing` as `INSTALLED`.
* `C5`: `origin/feat/demo-164-chat-grounding-provenance-0900:infra/tests/test_ai_alert_runbook_ownership.py:68-73` (`e282dc327`) — Asserts `Proposed owner: Digital service owner` on `ledger-digest-mismatch` and `ledger-verify-missing` runbook sections.
* `C6`: `src/api/tests/test_diagnostic_log_privacy.py:1` and `infra/tests/test_diagnostic_log_privacy.py:1` — Duplicate module basename requiring `infra/tests` to precede `src/api/tests` (or omit `src/api/tests`) on `PYTHONPATH` during `unittest discover -s infra/tests`.
* `C7`: `infra/tests/test_bicep_policy.py:1196-1238,2126` — Imports `zava_forward.core.ledger_digest_blob` and `zava_forward.orchestrator.digest_blob`, requiring `src/orchestrator/src` alongside `src/core/src` on `PYTHONPATH`.
* `C8`: `.github/workflows/src-ci.yml:95-115,215-249` — Defines hosted CI execution: editable installs of all 5 `src/*` distributions, `REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -v`, per-project `ruff check . && ruff format --check .` + `mypy`, and `ruff check/format --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` on `infra/` files.

## Alternatives and Convergence Selection

* **Option A (Selected)**: Rebase `feat/demo-115-blob-ledger` (`84cb5608a` + `1b66fd607`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`e282dc327`), resolve `infra/tests/test_monitoring_alerts.py` by preserving both `test_ranking_archive_job_failure_alert_routes_to_job_rank_runbook` (`#146`) and `test_installed_ledger_alerts_name_owner_resolvable_runbook_and_core_markers` (`#115`) inside `AlertOwnerAndRunbookTests` ahead of `WorkbookPanelTests`, run `src-ci.yml`-aligned focused validation (`infra/tests` full discovery with `infra/tests` first + `src/orchestrator/src` + `REQUIRE_AZ_BICEP=1`, `src/core/tests -p '*ledger*'`, `src/orchestrator/tests/test_digest_blob.py`, `ruff check` on `src/core`, `src/api`, and `--isolated --select E,F,I,B,UP` `infra/` targets, `ruff format --isolated --line-length 100 --check infra/tests/test_monitoring_alerts.py`, and `(cd src/core && python3 -m mypy)`), complete `rpi-review`, and commit the 7 `immutable-blob-ledger-digests-115-c2-rebase-*` RPI artifacts locally (`Refs #115`, `Co-authored-by` trailer, no push) leaving a clean frozen working tree.
* **Option B (Rejected — Overwrite `1b66fd607` `immutable-blob-ledger-digests-115-rebase-*` files in place)**: Violates repository RPI history-preservation rules and RPI Agent one-pass Critique/Review invariants.
* **Option C (Rejected — Modify unrelated legacy `infra/scripts/` files to satisfy unconfigured Ruff `0.17.3` `FURB`/`ISC` rules)**: Violates surgical-change boundaries by touching unrelated files outside `#115` scope when `src-ci.yml` explicitly scopes `infra/` Ruff checks with `--isolated --select E,F,I,B,UP --target-version py312 --line-length 100`.

## Current Decisions, Risks, and Readiness

* Current decisions:
  * D1: Preserve `84cb5608a` and `1b66fd607` RPI artifacts intact and record this full RPI loop in `.copilot-tracking/*/*/immutable-blob-ledger-digests-115-c2-rebase-*` (`parent_task = issue-115-rebase-164-0820`).
  * D2: Merge `infra/tests/test_monitoring_alerts.py` keeping `test_ranking_archive_job_failure_alert_routes_to_job_rank_runbook` (`#146`) followed by `test_installed_ledger_alerts_name_owner_resolvable_runbook_and_core_markers` (`#115`) inside `AlertOwnerAndRunbookTests`, with all `WorkbookPanelTests` cost/budget/anomaly assertions preserved (`C1`, `C2`, `C3`).
  * D3: Run `infra/tests` discovery with `REQUIRE_AZ_BICEP=1 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1` and `infra/tests` ahead of `src/*/tests` plus `src/orchestrator/src` (`C6`, `C7`, `C8`), run `*ledger*` discovery in `src/core/tests` (plus `src/orchestrator/tests/test_digest_blob.py`), run `ruff check` across `src/core`, `src/api`, `infra/tests/test_monitoring_alerts.py`, and `--isolated --select E,F,I,B,UP --target-version py312 --line-length 100` `src-ci.yml` `infra/` targets, run `ruff format --isolated --line-length 100 --check infra/tests/test_monitoring_alerts.py`, and run `(cd src/core && PYTHONDONTWRITEBYTECODE=1 python3 -m mypy)`.
  * D4: Commit the 7 `immutable-blob-ledger-digests-115-c2-rebase-*` tracking artifacts locally after `rpi-review` and `Follow-up` state persistence (`Refs #115`, privacy-safe `user.email`, `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`), re-verify focused validation and empty `git status --short`, and do not push.
* Unresolved decisions or risks: None blocking planning or execution; remote branch push / hosted CI and live Azure WORM lock (`#121`) + Monitor alert delivery remain open follow-ups (`Refs #115`).
* Research disposition: `executed`
* Planning Readiness: `Ready`
* Self-check: Passed (`Wider` -> `Deeper` -> `Contrarian` completed in order; all claims backed by `C1`–`C8`; zero production source edits during Research).
