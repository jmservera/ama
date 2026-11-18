<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #76 C1 Rebase Continuation onto `#1641` (`08c36e4dc`)

## Metadata

* Task ID: issue-76-c1-rebase
* Task slug: ux-76-hazard-clock-owner-c1-rebase
* Related plan: .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-research.md, .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md

## Phase Index

| Phase ID | Name                                                                                             | Status   | Detail sections |
|----------|--------------------------------------------------------------------------------------------------|----------|-----------------|
| P01      | Rebase `feat/ux-76-hazard-clock-owner` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`08c36e4dc`) | Complete | P01, P01-T01    |
| P02      | Focused Validation and Local Tracking Commit Closeout                                            | Complete | P02, P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Rebase `feat/ux-76-hazard-clock-owner` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`08c36e4dc`)

### Context

Research `C1`–`C5` verified that `origin/feat/demo-164-chat-grounding-provenance-0900` advanced from `0c1fa1da4` to `08c36e4dc` via `#1770` (`d8cb35d25`, Issue #133) and `#1771` (`08c36e4dc`, Issue #108). Replaying `8bd8a4f4d` and `c98e58bf4` onto `08c36e4dc` conflicts only in `src/api/README.md` and `src/core/README.md` where both `#108` and `#76` prepended dated `2026-11-15` `##` sections right below YAML frontmatter.

### Intent

Rebase both `#76` commits cleanly onto `08c36e4dc` while keeping both READMEs' reverse-chronological section ordering and all `#76`, `#108`, and `#133` documentation intact.

### Boundaries

* Included: `git fetch origin feat/demo-164-chat-grounding-provenance-0900`; `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`; conflict resolution in `src/api/README.md` and `src/core/README.md`.
* Excluded: Editing `.py` or `.js` files, squashing commits, or pushing to `origin`.

### Likely Targets

* `src/api/README.md`
* `src/core/README.md`

### Dependencies

* Clean tracked working tree prior to `git rebase` (untracked `ux-76-hazard-clock-owner-c1-rebase-*` paths under `.copilot-tracking/` do not overlap any tracked paths in `0c1fa1da4..08c36e4dc`).

### Validation Expectations

* Rebase completes cleanly; `git merge-base --is-ancestor 08c36e4dc HEAD` exits `0`; zero conflict markers remain.

### Completion Evidence

* `git log --oneline 08c36e4dc..HEAD` shows the two rebased `#76` commits (`feat(queues)` and `fix(queues)`) with clean README diffs.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Fetch target branch, rebase `feat/ux-76-hazard-clock-owner`, and resolve `src/api/README.md` and `src/core/README.md`

#### Context

During Commit 1 (`8bd8a4f4d`) replay onto `08c36e4dc`, Git stops with content conflicts at the top of `src/api/README.md` and `src/core/README.md`. Placing `#76`'s `## Hazard and safeguarding clock and named owner ... (2026-11-15, Refs #76)` section immediately after frontmatter followed by `#108`'s `## Offline RAI held-out evaluation ... (2026-11-15, Refs #108)` section preserves the READMEs' reverse-chronological (newest-at-top) structure and allows Commit 2 (`c98e58bf4`, updating `MEMBERSHIP_REVISION = 5` in `src/core/README.md`) to apply cleanly without a second conflict.

#### Intent

Complete the 2-commit rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`08c36e4dc`) with lossless README conflict resolution.

#### Boundaries

* Included:
  * Run `git fetch origin feat/demo-164-chat-grounding-provenance-0900` and confirm `git rev-parse --short origin/feat/demo-164-chat-grounding-provenance-0900` (if remote advanced again, inspect before rebasing; expected `08c36e4dc`).
  * Run `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`.
  * Resolve `src/api/README.md` keeping `ms.date: 2026-11-15`, `## Hazard and safeguarding clock and named owner in queues and case cards (2026-11-15, Refs #76)` first, then `## Offline RAI held-out evaluation and candidate comparison API (2026-11-15, Refs #108)`, followed by `## Handoff waiting times screen (2026-11-11, Refs #83)`.
  * Resolve `src/core/README.md` keeping `ms.date: 2026-11-15`, `## Hazard and safeguarding clock and named owner projection (2026-11-15, Refs #76)` first, then `## Offline RAI held-out evaluation and tokenomics candidate comparison (2026-11-15, Refs #108)`, followed by `## Retained sensor readings for employees and Quality evidence (Refs #1288, #107)` (and retaining `#133`'s auto-merged `aftercare` section update).
  * Stage both READMEs and finish rebase with `GIT_EDITOR=true git rebase --continue`, verifying Commit 2 (`fix(queues)`) updates `MEMBERSHIP_REVISION = 5` in `src/core/README.md` and zero `<<<<<<<` / `=======` / `>>>>>>>` markers exist.
* Excluded: Modifying source/test code or force-pushing.

#### Likely Targets

* `src/api/README.md`
* `src/core/README.md`

#### Dependencies

* Clean tracked working tree.

#### Validation Expectations

* `git merge-base --is-ancestor origin/feat/demo-164-chat-grounding-provenance-0900 HEAD` exits `0` and conflict-marker grep returns zero matches.

#### Completion Evidence

* Clean rebased commit history above `08c36e4dc` and verified `src/api/README.md` / `src/core/README.md` sections.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Focused Validation and Local Tracking Commit Closeout

### Context

Caller Step 4 specifies three focused validation commands covering `#76` unit tests (`core` + `api`), `src/core` `ruff` + `mypy`, and `src/api` `ruff`. Step 5 requires committing tracking artifacts locally with `Refs #76` and the Copilot trailer, leaving a clean `git status --short` without pushing.

### Intent

Prove zero regression on the rebased tree and leave a clean committed branch after `rpi-review`.

### Boundaries

* Included: Executing the three focused validation commands; verifying diff boundaries (`0` test removals, `0` new test files in this rebase continuation) and privacy-safe `git config --local user.email`; recording `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-changes.md`; committing all `ux-76-hazard-clock-owner-c1-rebase-*` tracking artifacts after `rpi-review` writes `review.md` and updates `state.json`.
* Excluded: `tools/rpi-checks.py` and `git push`.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-changes.md`
* `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-plan.md`

### Dependencies

* P01 completed.

### Validation Expectations

* All three focused validation commands exit `0`; post-Review commit leaves `git status --short` empty.

### Completion Evidence

* Recorded validation outputs in `changes.md`, completed `review.md` and `state.json`, and clean `git status --short`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run focused `#76` unit tests, `ruff`, and `mypy` across `src/core` and `src/api`

#### Context

Rebasing onto `08c36e4dc` brings in `#1770` (`aftercare`) and `#1771` (`heldout_eval` / `tokenomics_comparison` / `server.py`). Running the caller's focused test, lint, format, and typecheck commands verifies full compatibility on the merged codebase.

#### Intent

Confirm all focused unit, lint, format, and type checks pass on the rebased tree.

#### Boundaries

* Included:
  * `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api/src:src/api/tests python3 -m unittest src/core/tests/test_hazard_safeguarding_clock_owner.py src/core/tests/test_hazard_safeguarding_clock_owner_76.py src/api/tests/test_hazard_safeguarding_clock_owner_api_76.py -q`
  * `(cd src/core && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy)`
  * `(cd src/api && python3 -m ruff check src tests && python3 -m ruff format --check src tests)`
* Excluded: Editing tests or adding `pyproject.toml` suppressions.

#### Likely Targets

* Read-only validation across `src/core` and `src/api`.

#### Dependencies

* P01-T01 completed.

#### Validation Expectations

* Every command exits `0`.

#### Completion Evidence

* Exact pass counts and exit codes recorded in `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-changes.md`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile changes, run `rpi-review` closeout commit with `Refs #76` and Copilot trailer, and verify clean `git status --short`

#### Context

Repository commit conventions require `{id}+{login}@users.noreply.github.com` in repository-local `user.email`, `Refs #76` (non-closing keyword since not every human/hosted criterion of `#76` is closed locally), and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, with `git status --short` empty at exit and zero `git push`.

#### Intent

Reconcile `Implement` artifacts cleanly for `rpi-review` and capture all `ux-76-hazard-clock-owner-c1-rebase-*` tracking artifacts in a single local commit immediately after `rpi-review` completes.

#### Boundaries

* Included:
  * Verify `git diff origin/feat/demo-164-chat-grounding-provenance-0900 --name-status` matches the expected `#76` code/doc/test set plus `.copilot-tracking/` artifacts.
  * Verify `git config --local user.email` matches `{id}+{login}@users.noreply.github.com` via `gh api user` (setting locally if absent).
  * Persist `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-changes.md` and mark `[x]` on `P01`/`P02` in `plan.md` and `Complete` in `phase-details.md` prior to `rpi-review`.
  * After `rpi-review` persists `.copilot-tracking/reviews/logs/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-review.md` and updates `.copilot-tracking/rpi-sessions/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-state.json` to `active_phase: "Follow-up"`, `status: "completed"`, stage all `ux-76-hazard-clock-owner-c1-rebase-*` tracking files and commit locally with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, then verify `git status --short` is empty.
* Excluded: Pushing to `origin`.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-changes.md`
* `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-plan.md`
* `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-phase-details.md`

#### Dependencies

* P02-T01 completed.

#### Validation Expectations

* Local commit succeeds; `git status --short` outputs empty; `git log -n 4 --oneline` shows `08c36e4dc` followed by the two rebased `#76` commits and the `docs(tracking)` commit.

#### Completion Evidence

* Clean `git status --short` and verified local commit metadata.

#### Unresolved Items

* None.
