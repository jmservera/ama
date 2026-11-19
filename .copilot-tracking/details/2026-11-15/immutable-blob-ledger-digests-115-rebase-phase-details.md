<!-- markdownlint-disable-file -->
# RPI Phase Details: Rebase Issue #115 Immutable Blob Ledger Digests onto `#164` (`fa6f8d1dd`)

## Metadata

* Task ID: issue-115-rebase-164-0820
* Task slug: immutable-blob-ledger-digests-115-rebase
* Related plan: .copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-rebase-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/immutable-blob-ledger-digests-115-rebase-research.md (`C1`–`C8`)

## Phase Index

| Phase ID | Name                                                                                             | Status   | Detail sections       |
|----------|--------------------------------------------------------------------------------------------------|----------|-----------------------|
| P01      | Fetch & Rebase `feat/demo-115-blob-ledger` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`) | Complete | P01, P01-T01          |
| P02      | Focused Validation and Pre-Review Reconciliation                                                 | Complete | P02, P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Fetch & Rebase `feat/demo-115-blob-ledger` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`)

### Context

`feat/demo-115-blob-ledger` currently has one clean commit (`681903493`, 17 files) on `243764945`. Fetched `origin/feat/demo-164-chat-grounding-provenance-0900` sits at `fa6f8d1dd0493342718a70c134dd9fcb3305cd6c` (`243764945` + `36aeddae3` `#215` + `f71331d42` `#76` + `fa6f8d1dd` `#216`). Research (`C1`, `C2`) verified `src/core/README.md` is the sole overlapping file across the 17 `#115` files and 300 upstream files.

### Intent

Replay `681903493` cleanly atop `fa6f8d1dd` while preserving untracked child RPI files, resolving `src/core/README.md` in newest-first reverse-chronological order without data loss, and confirming exact diff boundaries.

### Boundaries

* Included: Git rebase of `feat/demo-115-blob-ledger` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`) and conflict merge in `src/core/README.md`.
* Excluded: Modifying any source, test, or Bicep file unless a concrete post-rebase test/type check reveals an incompatibility, or pushing to `origin`.

### Likely Targets

* `src/core/README.md`: Keep `## Immutable Blob ledger digests and scheduled verification (2026-11-15, Refs #115)` immediately above `## Hazard and safeguarding clock and named owner projection (2026-11-15, Refs #76)` right after YAML frontmatter, preserving `#108`, `#133`, and `#216` sections verbatim.

### Dependencies

* `origin/feat/demo-164-chat-grounding-provenance-0900` fetched at `fa6f8d1dd0493342718a70c134dd9fcb3305cd6c`.

### Validation Expectations

* `git merge-base --is-ancestor fa6f8d1dd0493342718a70c134dd9fcb3305cd6c HEAD` exits `0`.
* Conflict-marker grep (`^(<{7}|={7}|>{7})`) in `src/core/README.md` returns zero matches.
* `git diff --name-only fa6f8d1dd..HEAD` lists exactly the 17 paths from `681903493`.

### Completion Evidence

* Rebased commit SHA recorded in changes log, `fa6f8d1dd` confirmed as parent commit, and `src/core/README.md` conflict-free.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Rebase `681903493` onto `fa6f8d1dd` and resolve `src/core/README.md`

#### Context

During `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, untracked child RPI files under `.copilot-tracking/*/*/immutable-blob-ledger-digests-115-rebase-*` do not overlap with any tracked upstream path (`243764945..fa6f8d1dd`) and remain intact in place when `git status --short --untracked-files=no` is empty (`PC-001`). When `681903493` replays onto `fa6f8d1dd`, Git flags a single conflict at the top of `src/core/README.md` between `#76` (`HEAD`) and `#115` (`681903493`).

#### Intent

Complete the rebase cleanly with original commit message and trailers preserved (`GIT_EDITOR=true git rebase --continue`).

#### Boundaries

* Included: `git fetch origin feat/demo-164-chat-grounding-provenance-0900`, `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, resolving `src/core/README.md` (`#115` H2 followed by `#76` H2 followed by `#108` H2), `git add src/core/README.md`, and `GIT_EDITOR=true git rebase --continue`.
* Excluded: Rewriting `fa6f8d1dd` history or force-pushing.

#### Likely Targets

* `src/core/README.md`

#### Dependencies

* Clean tracked working tree before rebase (`git status --short --untracked-files=no` empty).

#### Validation Expectations

* `git log -n 2 --oneline` shows rebased `feat(core,infra): enforce immutable blob ledger digests and mismatch alerts` directly on `fa6f8d1dd`.
* Both `## Immutable Blob ledger digests and scheduled verification (2026-11-15, Refs #115)` and `## Hazard and safeguarding clock and named owner projection (2026-11-15, Refs #76)` plus `### Owned citation/refusal evaluation gates and rule-card ship comparator (#216)` exist in `src/core/README.md`.

#### Completion Evidence

* Clean rebase exit 0 and verified `git diff --stat fa6f8d1dd..HEAD`.

<!-- rpi:phase id=P02 -->
## P02: Focused Validation and Pre-Review Reconciliation

### Context

`infra/tests/test_bicep_policy.py` imports `zava_forward.core.ledger_digest_blob` and `zava_forward.orchestrator.digest_blob` (`C5`) and compiles Bicep modules via `az bicep` when `REQUIRE_AZ_BICEP=1` (`C6`), while global Python user site-packages point to another worktree. Passing `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1` with explicit worktree `PYTHONPATH` disables `USER_SITE` `.pth` shadowing across parent and child processes while retaining system `PyYAML` (`PC-001`), and passing `--stdout >/dev/null` to `az bicep build` prevents untracked ARM `.json` files in `infra/` (`PC-003`). Per `PC-002`, `P02` completes pre-Review reconciliation for `rpi-review`, while final `Follow-up` state persistence, the local `docs(rpi)` tracking commit, and final `HEAD` / empty `git status --short` verification execute immediately after `rpi-review`.

### Intent

Validate all lint, format, strict type, Blob ledger, doc-link, dependency-rule, Bicep build/lint (`--stdout`), and Bicep policy/alert tests under verified worktree-only `zava_forward.__path__` resolution, and reconcile all `P01`/`P02` plan, phase-details, and changes-record markers ahead of `rpi-review`.

### Boundaries

* Included: Worktree-isolated `PYTHONNOUSERSITE=1` + `PYTHONDONTWRITEBYTECODE=1` validation across `src/core`, `src/orchestrator`, and `infra/tests`, diff-boundary and privacy-safe `user.email` checks, and pre-Review `.copilot-tracking/` marker reconciliation.
* Excluded: `/tmp` virtualenvs, `tools/rpi-checks.py`, mutating global `~/.local` Python installs, authoring the review log inside `rpi-implement`, or `git push`.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-rebase-changes.md`
* `.copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-rebase-plan.md`
* `.copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-rebase-phase-details.md`

### Dependencies

* `P01` complete.

### Validation Expectations

* `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=src/core/src:src/orchestrator/src python3 -c "import zava_forward, yaml; ..."` confirms `zava_forward.__path__` points exclusively into `/home/azureuser/source/ama-demo-wt/feat-115-blob-ledger`.
* `(cd src/core && ruff check . && ruff format --check . && PYTHONPATH=src:tests mypy)` (`strict = true` on `zava_forward.core.ledger_digest_blob` and combined `#76`/`#216`/`#115` `src` + `tests`).
* `(cd src/orchestrator && ruff check . && ruff format --check . && mypy)` (note: `src/orchestrator/pyproject.toml` skips `digest_blob` and `zava_forward.core.*` by override; runtime parity is enforced by `test_digest_blob.py` and `test_bicep_policy.py`).
* `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_bicep_policy.py infra/tests/test_monitoring_alerts.py` and `ruff format --isolated --line-length 100 --check infra/tests/test_bicep_policy.py infra/tests/test_monitoring_alerts.py`
* `(cd src/core && PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=src:tests python3 -m unittest tests/test_ledger_digest_blob.py tests/test_dependency_rule.py tests/test_live_doc_links.py -v)`
* `(cd src/orchestrator && PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest tests/test_digest_blob.py -v)`
* `for f in infra/main.bicep infra/modules/storage.bicep infra/modules/containerapps.bicep; do az bicep build --file "$f" --stdout >/dev/null && az bicep lint --file "$f"; done`
* `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 REQUIRE_AZ_BICEP=1 PYTHONPATH=src/core/src:src/orchestrator/src python3 -m unittest infra/tests/test_bicep_policy.py infra/tests/test_monitoring_alerts.py -v`

### Completion Evidence

* Zero failures across all commands above on the rebased tree, verified `git diff fa6f8d1dd..HEAD --name-only` (17 `#115` paths only) and privacy-safe `user.email`, and all `P01`/`P02` markers checked `[x]` with `Ready for rpi-review`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Execute worktree-isolated focused validation suite on rebased tree

#### Context

Running Python test suites under `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1` with explicit worktree `PYTHONPATH` disables `USER_SITE` `.pth` entries across both parent and spawned child Python processes while keeping system `PyYAML` available, and `az bicep build --file ... --stdout >/dev/null` compiles ARM templates in memory without writing untracked `.json` files into `infra/` (`PC-001`, `PC-003`).

#### Intent

Prove `ruff check .`, `ruff format --check .`, `mypy`, `#115` Blob ledger tests, Bicep lint/build (`--stdout`), and `test_bicep_policy.py` + `test_monitoring_alerts.py` all pass cleanly on the rebased `#115` commit atop `fa6f8d1dd`.

#### Boundaries

* Included: Module-origin check and all focused validation commands listed in `P02` Validation Expectations.
* Excluded: Running `tools/rpi-checks.py` or modifying unrelated files.

#### Likely Targets

* Read-only verification across `src/core`, `src/orchestrator`, and `infra/`.

#### Dependencies

* `P01-T01` complete.

#### Validation Expectations

* Every command exits `0` with exact test/file counts captured in the changes record.

#### Completion Evidence

* Captured pass counts and exit codes in `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-rebase-changes.md`.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Verify diff/identity invariants and reconcile `P01`/`P02` markers for `rpi-review`

#### Context

Per `PC-002`, `rpi-implement` completes pre-Review reconciliation before handing off to `rpi-review`; after `rpi-review` creates the review log and the parent RPI agent persists final `Follow-up` state, the parent executes the `docs(rpi)` commit (`Refs #115`) and re-verifies focused checks + empty `git status --short` on the final `HEAD`.

#### Intent

Reconcile plan markers (`[x]`), phase details (`Complete`), diff boundaries (`fa6f8d1dd..HEAD`), privacy-safe `user.email`, and `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-rebase-changes.md` so `rpi-review` receives a complete, clean artifact set.

#### Boundaries

* Included: `git diff fa6f8d1dd..HEAD --name-only` verification, `git config --local user.email` verification via `gh api user`, checking `[x]` on `P01`/`P02` markers, and marking `Ready for rpi-review` in the changes record.
* Excluded: Authoring the review log inside `rpi-implement` or running `git push`.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-rebase-changes.md`
* `.copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-rebase-plan.md`
* `.copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-rebase-phase-details.md`

#### Dependencies

* `P02-T01` complete.

#### Validation Expectations

* `git status --short --untracked-files=no` is empty (only untracked child `.copilot-tracking/` files exist prior to Review closeout), `git diff fa6f8d1dd..HEAD --name-only` lists the exact 17 `#115` paths, and `user.email` matches `{id}+{login}@users.noreply.github.com`.

#### Completion Evidence

* Reconciled `[x]` markers in plan, `Complete` status in phase details and changes record, and `Review readiness: Ready for rpi-review`.
