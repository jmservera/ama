<!-- markdownlint-disable-file -->
# RPI Plan Critique: Rebase Issue #115 Immutable Blob Ledger Digests onto `#1641` (`e282dc327`)

## Metadata

* Task ID: issue-115-c2-rebase-164-0905
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Rebase `feat/demo-115-blob-ledger` (current `HEAD` `1b66fd607`, parent `84cb5608a`, base `fa6f8d1dd`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`e282dc3276992a17507351dd4f75d08a8808f56d`, PR `#1641`) in `/home/azureuser/source/ama-demo-wt/feat-115-blob-ledger` after `git fetch origin feat/demo-164-chat-grounding-provenance-0900`; resolve the conflict in `infra/tests/test_monitoring_alerts.py` preserving both `#146` (PR `#1778`) cost/budget/anomaly/job-rank alert assertions and `#115` immutable Blob ledger digest verification and alerting assertions; run `src-ci.yml`-aligned focused validation (`infra/tests` discovery `test_*.py`, `src/core/tests` discovery `*ledger*`, `ruff check` across `src/core`, `src/api`, and `src-ci.yml` `--isolated` `infra/` flags, `ruff format --isolated --line-length 100 --check infra/tests/test_monitoring_alerts.py`, and `(cd src/core && python3 -m mypy)`); commit updated `.copilot-tracking/` artifacts with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`; do not push; and leave a clean frozen working tree.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-research.md (`C1`-`C8`), .copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-plan.md, .copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-phase-details.md, .copilot-tracking/rpi-sessions/2026-11-15/immutable-blob-ledger-digests-115-rebase-state.json, .copilot-tracking/reviews/logs/2026-11-15/immutable-blob-ledger-digests-115-rebase-review.md, .github/workflows/src-ci.yml, infra/tests/test_monitoring_alerts.py (compared against `e282dc327:infra/tests/test_monitoring_alerts.py`), src/core/pyproject.toml, and .gitignore.
* Decisions, dependencies, and acceptance criteria considered: Research decisions `D1`-`D4`, functional requirements `FR-1`-`FR-3`, non-functional requirements `NFR-1`-`NFR-2`, acceptance criteria `AC-1`-`AC-4`, test ownership lock (`10` merged tests in `infra/tests/test_monitoring_alerts.py`, `0` test removals, `0` new test files), and phase/task units `P01` (`P01-T01`) and `P02` (`P02-T01`, `P02-T02`).
* Assessment boundary: Evaluates plan and phase-detail credibility, conflict-merge completeness, shared-host namespace and cache isolation, `src-ci.yml` command parity, and RPI stage sequencing from read-only repository state prior to executing the rebase. Does not execute mutating git operations, remote pushes, hosted GitHub Actions workflows, or live Azure deployments.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Req 1 (`git fetch` + rebase onto `e282dc327`) | Covered | `FR-1`, `AC-1`, `P01`, and `P01-T01` fetch `origin feat/demo-164-chat-grounding-provenance-0900` (`e282dc3276992a17507351dd4f75d08a8808f56d`), replay `84cb5608a` and `1b66fd607` while keeping untracked `c2-rebase` `.copilot-tracking/` files intact (`git status --short --untracked-files=no` verified empty), and assert `git merge-base --is-ancestor e282dc3276992a17507351dd4f75d08a8808f56d HEAD`. |
| Caller Req 2 (`infra/tests/test_monitoring_alerts.py` merge) | Covered | Read-only diff comparison across `fa6f8d1dd..1b66fd607` (24 files) and `fa6f8d1dd..e282dc327` (54 files) confirms `infra/tests/test_monitoring_alerts.py` is the sole overlapping file (`C1`, `C2`). Retaining `test_ranking_archive_job_failure_alert_routes_to_job_rank_runbook` (`#146`) followed by `test_installed_ledger_alerts_name_owner_resolvable_runbook_and_core_markers` (`#115`) inside `AlertOwnerAndRunbookTests` ahead of all 4 `WorkbookPanelTests` cost/budget/anomaly tests (`C3`) preserves all `10` tests cleanly within 100 columns. |
| Caller Req 3 (`src-ci.yml`-aligned focused validation) | Covered | `FR-2`, `AC-2`, `AC-3`, `P02`, and `P02-T01` cover full `infra/tests` discovery (`test_*.py` under `REQUIRE_AZ_BICEP=1 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1` with `infra/tests` ahead of `src/api/tests` per `C6` and `src/orchestrator/src` included per `C7`, verified at 0 loader errors), `src/core/tests` `-p '*ledger*'` discovery plus `src/orchestrator/tests/test_digest_blob.py` and `#146`/`#189`/doc/dependency suites, `ruff check` on `src/core`, `src/api`, `infra/tests/test_monitoring_alerts.py`, and `--isolated --select E,F,I,B,UP --target-version py312 --line-length 100` `infra/` targets (`C8`), `ruff format --isolated --line-length 100 --check infra/tests/test_monitoring_alerts.py`, `(cd src/core && PYTHONDONTWRITEBYTECODE=1 python3 -m mypy)`, and `az bicep build --stdout >/dev/null` + `lint`. |
| Caller Req 4 (`.copilot-tracking/` commit, trailer, no push, clean tree) | Covered | `FR-3`, `AC-4`, `P02-T02`, and `Handoff` preserve the `rpi-implement` vs `rpi-review` boundary: `P02-T02` verifies `e282dc327..HEAD` diff boundaries and local privacy-safe `user.email` (`8036360+jmservera@users.noreply.github.com`, already configured in `.git/config`) and reconciles `P01`/`P02` markers pre-Review; after one-pass `rpi-review` writes the 7th `c2-rebase` artifact (`review.md`) and the parent persists `Follow-up` state (`state.json`), the parent commits all 7 `immutable-blob-ledger-digests-115-c2-rebase-*` files with `Refs #115` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, re-verifies clean `git status --short`, and does not push. |
| Research `C1`-`C8` and Decisions `D1`-`D4` | Covered | Every research finding (`C1`-`C8`) and convergence decision (`D1`-`D4`) maps directly to `FR-1`-`FR-3`, `NFR-1`-`NFR-2`, and `P01`/`P02` validation commands without contradiction or omitted prerequisite. |
| `NFR-1` & `NFR-2` (Shared-host isolation & RPI history integrity) | Covered | Zero `/tmp` writes, zero `pip` mutations of `~/.local/*.pth`, zero `.pyc` or ARM `.json` debris (`PYTHONDONTWRITEBYTECODE=1`, `az bicep build --stdout >/dev/null`, and ignored `/src/**/.mypy_cache/` + `.ruff_cache/.gitignore`), and zero edits to committed `84cb5608a` or `1b66fd607` RPI records. |
| `P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02` | Covered | Dependencies (`P01-T01` -> `P02-T01` -> `P02-T02`), target files, validation commands, timeout guidance (`initial_wait` >= 300s for full `REQUIRE_AZ_BICEP=1` `infra/tests` discovery), and completion evidence are specific and executable. |

## Verdict

* Verdict: Pass
* Rationale: The plan and phase details are complete, internally consistent, and directly grounded in verified repository and CI evidence (`C1`-`C8`). Read-only verification confirms `infra/tests/test_monitoring_alerts.py` is the sole overlapping path between `fa6f8d1dd..1b66fd607` and `fa6f8d1dd..e282dc327`, the two-method merge inside `AlertOwnerAndRunbookTests` preserves all 10 `#146` and `#115` alert and workbook assertions within 100-column Ruff formatting, the `PYTHONNOUSERSITE=1` `PYTHONPATH` ordering loads `infra/tests` cleanly with zero module-shadowing or loader errors, `src/core/pyproject.toml` pins `mypy_path = ["src", "tests"]` under `strict = true`, local `user.email` is already set to `8036360+jmservera@users.noreply.github.com`, and separating `P02-T02` pre-Review reconciliation from the parent post-Review `Follow-up` commit preserves one-pass `rpi-review` integrity while ending with an empty `git status --short` and no push.

## Findings

* None. Zero actionable `Critical`, `High`, `Medium`, or `Low` planning defects or evidence gaps were identified across the supplied boundary.

## Strengths and Residual Risk

* Accurate hunk-level conflict scoping (`C1`-`C3`): Both `#146` (`e282dc327`) and `#115` (`84cb5608a`) append one method at line 72 of `AlertOwnerAndRunbookTests` above `WorkbookPanelTests`, making sequential retention deterministic and side-effect-free.
* Verified `src-ci.yml` parity on a shared host (`C6`-`C8`): Placing `infra/tests` before `src/api/tests` prevents `test_diagnostic_log_privacy` basename shadowing, including `src/orchestrator/src` satisfies `test_bicep_policy.py` imports, setting `REQUIRE_AZ_BICEP=1` prevents silent Bicep test skips, and using `--isolated --select E,F,I,B,UP --target-version py312 --line-length 100` matches `.github/workflows/src-ci.yml:241-252` without touching unrelated legacy `infra/` files.
* Clean RPI lifecycle and retention adherence (`FR-3`, `NFR-2`): Recording a distinct 7-file `immutable-blob-ledger-digests-115-c2-rebase-*` artifact set preserves prior committed `84cb5608a` and `1b66fd607` critique/review outcomes verbatim and commits the complete post-Review record in one clean local `docs(rpi)` commit (`Refs #115`).
* Accepted residual risk 1 (concurrent upstream ref movement before `git fetch`): `origin/feat/demo-164-chat-grounding-provenance-0900` currently resolves to `e282dc3276992a17507351dd4f75d08a8808f56d`; if another stacked PR merges into `feat/demo-164-chat-grounding-provenance-0900` before `P01-T01` fetches, `P01` and `P02-T02`'s `git diff --name-only e282dc327..HEAD` boundary check will surface the upstream delta immediately rather than silently masking unreviewed changes.
* Accepted residual risk 2 (deferred remote push and live Azure operational gates): Remote branch push/hosted CI execution (`Do NOT push`) and Legal retention sign-off (`#121`) + irreversible Azure `lockImmutabilityPolicy` and live Azure Monitor alert delivery remain explicitly tracked in `Follow-Up Items` under `Refs #115`.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* This critique operated strictly read-only against pre-rebase git state (`HEAD` `1b66fd607`, fetched `origin/feat/demo-164-chat-grounding-provenance-0900` `e282dc327`) and did not execute `git rebase` or post-rebase runtime test runs reserved for `rpi-implement`.
* Hosted GitHub Actions execution and live Azure storage/Monitor verification are outside the caller's local no-push boundary.

## Recommended Next Action

* Highest-impact finding: none
* Action owner: none
* Smallest next action: Mark the plan `Planning status: Ready` and `Critique Disposition: Pass` in the active parent RPI workflow and proceed directly to `rpi-implement` (`P01`, `P02`).
* User response required: no
