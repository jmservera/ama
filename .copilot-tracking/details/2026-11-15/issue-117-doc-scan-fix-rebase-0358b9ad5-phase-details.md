<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #117 Document Scan Fix (`test_resident_decisions`) and Rebase onto 0358b9ad5

## Metadata

* Task ID: issue-117-doc-scan-fix-rebase-0358b9ad5
* Task slug: issue-117-doc-scan-fix-rebase-0358b9ad5
* Related plan: .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-research.md (`C1`–`C8`), .copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md, .copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md

## Phase Index

| Phase ID | Name                                                                               | Status   | Detail sections       |
|----------|------------------------------------------------------------------------------------|----------|-----------------------|
| P01      | Rebase onto 0358b9ad5 and Fix Synthetic Evidence Fixture in test_resident_decisions | Complete | P01, P01-T01, P01-T02 |
| P02      | Execute Worktree-Isolated Focused src-ci.yml Validation                            | Complete | P02, P02-T01          |
| P03      | Reconcile Pre-Review #117 and Child Tracking Artifacts                             | Complete | P03, P03-T01          |

<!-- rpi:phase id=P01 -->
## P01: Rebase onto 0358b9ad5 and Fix Synthetic Evidence Fixture in test_resident_decisions.py

### Context

Branch `feat/demo-117-doc-scan` is at `5c5370a4a` (commits `e9c31f7fa` and `5c5370a4a` atop `fa6f8d1dd`). Stacked parent `origin/feat/demo-164-chat-grounding-provenance-0900` advanced 6 commits to `0358b9ad5`. Read-only `git merge-tree --write-tree --messages 0358b9ad5 5c5370a4a` (`C2`) exited `0` with clean auto-merges in `src/core/src/zava_forward/core/doc_controls.py` (`#109` sensor refusal) and `src/core/src/zava_forward/core/assistants.py` (`#146` monitoring status). In `src/core/tests/test_resident_decisions.py`, `test_resident_acceptance_never_clears_technical_or_hazard_gates` fails at line 2526 because its synthetic pre-gate setup builds `dict(id=f"SYN-{kind}", kind=kind, generated=False)` without `scan` metadata (`C3`), whereas `dataset.py:113-115` (`supplied_resident_fixture`) uses `scan=dict(status="clean", scanner="Synthetic metadata fixture")` (`C5`) and `test_technical_evidence_usability.py:29-67` enforces fail-closed quarantine on `generated=False` documents missing `scan` (`C6`).

### Intent

Configure repository-local privacy-safe git email, replay `feat/demo-117-doc-scan` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0358b9ad5`), update the synthetic setup comprehension in `src/core/tests/test_resident_decisions.py` to carry clean synthetic scan metadata without touching `is_available_case_document`, and commit the test fix cleanly.

### Boundaries

* Included: `gh api user` lookup and `git config --local user.email`, `git fetch origin feat/demo-164-chat-grounding-provenance-0900` verification (`0358b9ad5`), `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, editing `src/core/tests/test_resident_decisions.py` (`test_resident_acceptance_never_clears_technical_or_hazard_gates`), and committing `src/core/tests/test_resident_decisions.py` with privacy-safe noreply email and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
* Excluded: Modifying tracked `.copilot-tracking/` files prior to `git rebase`, changing `is_available_case_document` or `scan_status` in `doc_controls.py`, changing `src/api/src/zava_forward/api/server.py`, or pushing to `origin`.

### Likely Targets

* `src/core/tests/test_resident_decisions.py`: Update `c["documents"]` setup comprehension in `test_resident_acceptance_never_clears_technical_or_hazard_gates` to include `scan=dict(status="clean", scanner="Synthetic metadata fixture")`, formatted to <=100 chars per line (`ruff format`) and strict `mypy`.

### Dependencies

* Clean tracked working tree (`git diff --quiet` and `git diff --cached --quiet`).

### Validation Expectations

* `git merge-base --is-ancestor 0358b9ad5 HEAD` exits `0`.
* `git diff --check` exits `0`.
* `git --no-pager diff 0358b9ad5..HEAD -- src/api/src/zava_forward/api/server.py` outputs empty string.
* `git --no-pager show HEAD --stat` shows the clean test-fix commit modifying `src/core/tests/test_resident_decisions.py` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` and zero `.copilot-tracking/` path mentions in the commit message.

### Completion Evidence

* Rebased commits and new fix commit SHA atop `0358b9ad5`.

### Unresolved Items

* none

<!-- rpi:task id=P01-T01 -->
### P01-T01: Configure local privacy-safe git email and rebase feat/demo-117-doc-scan onto 0358b9ad5

#### Context

Repository rules require setting repository-local `user.email` to `{id}+{login}@users.noreply.github.com` via `gh api user` before committing or rebasing, and rebasing `feat/demo-117-doc-scan` onto the latest `origin/feat/demo-164-chat-grounding-provenance-0900` (`0358b9ad5`).

#### Intent

Set repository-local privacy-safe git identity, fetch `origin/feat/demo-164-chat-grounding-provenance-0900` (`0358b9ad5`), and rebase `feat/demo-117-doc-scan` cleanly onto `0358b9ad5`.

#### Boundaries

* Included: `gh api user`, `git config --local user.email`, `git fetch origin feat/demo-164-chat-grounding-provenance-0900`, `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, and verifying clean auto-merge of `doc_controls.py` and `assistants.py`.
* Excluded: Remote writes or modifying tracked files prior to rebase completion.

#### Likely Targets

* Git branch `feat/demo-117-doc-scan` (`doc_controls.py` and `assistants.py` auto-merged by git).

#### Dependencies

* none

#### Validation Expectations

* `git merge-base --is-ancestor 0358b9ad5 HEAD` exits `0` and `git diff --check` exits `0`.

#### Completion Evidence

* Rebased commit SHAs atop `0358b9ad5`.

#### Unresolved Items

* none

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add clean synthetic scan metadata in test_resident_decisions.py and commit fix cleanly

#### Context

In `src/core/tests/test_resident_decisions.py` (`test_resident_acceptance_never_clears_technical_or_hazard_gates`), lines 2522-2524 construct `dict(id=f"SYN-{kind}", kind=kind, generated=False)` without `scan` metadata solely to clear the technical gate in pre-state setup before returning a technical sign-off and proving resident acceptance never clears technical or hazard gates (`C3`). Adding `scan=dict(status="clean", scanner="Synthetic metadata fixture")` matches `dataset.py:113-115` (`C5`) and preserves `#117` fail-closed missing-scan quarantine (`C4`, `C6`).

#### Intent

Update `c["documents"]` in `test_resident_acceptance_never_clears_technical_or_hazard_gates` (`src/core/tests/test_resident_decisions.py`) with `scan=dict(status="clean", scanner="Synthetic metadata fixture")` formatted cleanly for `ruff format` and `mypy --strict`, verify quick test pass, and commit `src/core/tests/test_resident_decisions.py` cleanly.

#### Boundaries

* Included: Single list-comprehension update in `src/core/tests/test_resident_decisions.py` and local `git commit` with `Refs #117` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
* Excluded: Any edit to `src/core/src/zava_forward/core/doc_controls.py` or unrelated tests; any `.copilot-tracking/` mention in commit messages.

#### Likely Targets

* `src/core/tests/test_resident_decisions.py`

#### Dependencies

* P01-T01

#### Validation Expectations

* `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_resident_decisions.JsonResidentDecisions.test_resident_acceptance_never_clears_technical_or_hazard_gates test_resident_decisions.SqlResidentDecisions.test_resident_acceptance_never_clears_technical_or_hazard_gates -q` exits `0`.
* `git show HEAD --stat` shows only `src/core/tests/test_resident_decisions.py` committed cleanly with noreply author and `Co-authored-by` trailer.

#### Completion Evidence

* Committed fix SHA and passing targeted test output.

#### Unresolved Items

* none

<!-- rpi:phase id=P02 -->
## P02: Execute Worktree-Isolated Focused src-ci.yml Validation

### Context

Shared `~/.local` editable installs on this non-sandboxed host can point to sibling worktrees. Verifying PEP 420 namespace paths (`zava_forward.{core,agents,api}.__path__`) under the worktree-prepended `PYTHONPATH` and executing both the caller's exact `src-ci.yml` commands and full `src/core` unit discovery guarantees 100% `src-core` and `src-api` CI parity on the rebased HEAD.

### Intent

Assert worktree module isolation and execute all focused `src/core` and `src/api` test, lint, format, type, endpoint-inventory, and rename-guard checks.

### Boundaries

* Included:
  * Explicit `python3 -c` assertion verifying `zava_forward.core.__path__`, `zava_forward.agents.__path__`, and `zava_forward.api.__path__` resolve inside `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan/`.
  * Caller's `src/core` validation command (`test_resident_decisions`, `test_technical_evidence_usability`, `test_document_rescan`, `test_resident_documents`, `ruff check src tests`, `ruff format --check src tests`, `mypy`).
  * Full `src/core` `unittest discover -s tests -q` plus `ruff check . && ruff format --check .` matching `.github/workflows/src-ci.yml`.
  * Caller's `src/api` validation command (`tests/test_document_controls.py`, `ruff check src tests`, `ruff format --check src tests`, `mypy`) plus `ruff check . && ruff format --check .` and `tests/test_role_endpoint_inventory.py`.
  * `python3 tools/rename-zava-tests.py` from repository root.
* Excluded: `tools/rpi-checks.py` and global `pip install -e`.

### Likely Targets

* Read-only CLI validation across `src/core`, `src/api`, and `tools/rename-zava-tests.py`.

### Dependencies

* P01

### Validation Expectations

* `PYTHONPATH=src/core/src:src/agents/src:src/api/src python3 -c 'import zava_forward.core as c, zava_forward.agents as ag, zava_forward.api as ap; wt="/home/azureuser/source/ama-demo-wt/feat-117-doc-scan/"; assert all(any(p.startswith(wt) for p in m.__path__) and m.__path__[0].startswith(wt) for m in (c, ag, ap)), (list(c.__path__), list(ag.__path__), list(ap.__path__))'` exits `0`.
* `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_resident_decisions test_technical_evidence_usability test_document_rescan test_resident_documents -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy` exits `0`.
* `cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -q && python3 -m ruff check . && python3 -m ruff format --check .` exits `0`.
* `cd src/api && PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_document_controls.py tests/test_role_endpoint_inventory.py -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=src:../core/src:../agents/src python3 -m mypy` exits `0`.
* `python3 tools/rename-zava-tests.py` exits `0`.

### Completion Evidence

* Exact pass counts and exit `0` status recorded in `.copilot-tracking/` changes artifacts.

### Unresolved Items

* none

<!-- rpi:task id=P02-T01 -->
### P02-T01: Assert worktree module resolution and execute src/core and src/api validation suites

#### Context

Caller Step 3 specifies the exact `src/core` and `src/api` commands matching `src-ci.yml`; adding full `src/core` `unittest discover -s tests -q` also confirms zero regressions across the 6 newly rebased upstream PRs (`#1775`–`#1782`).

#### Intent

Run worktree isolation check and all `src/core`, `src/api`, and rename-guard validation commands to exit `0`.

#### Boundaries

* Included: Worktree path check, `unittest`, `ruff`, `mypy`, and `rename-zava-tests.py`.
* Excluded: Mutating shared user-site installs.

#### Likely Targets

* `src/core/tests/test_resident_decisions.py`
* `src/core/tests/test_technical_evidence_usability.py`
* `src/core/tests/test_document_rescan.py`
* `src/core/tests/test_resident_documents.py`
* `src/api/tests/test_document_controls.py`
* `src/api/tests/test_role_endpoint_inventory.py`

#### Dependencies

* P01-T02

#### Validation Expectations

* All 5 validation commands in `P02` Validation Expectations exit `0`.

#### Completion Evidence

* Recorded command exit codes and test counts in `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-changes.md`.

#### Unresolved Items

* none

<!-- rpi:phase id=P03 -->
## P03: Reconcile Pre-Review #117 and Child Tracking Artifacts

### Context

Repository rules require preserving original critique/Review outcomes (`Residual work` / `RV-001` on `issue-117-doc-scan-review.md`) while keeping `.copilot-tracking/` records reconciled ahead of single-pass `rpi-review`, and leaving a clean committed worktree (`git status --short` empty, no push) at parent `RPI Agent` post-Review closeout.

### Intent

During `rpi-implement` (`P03-T01`), append the `0358b9ad5` rebase base, fix commit SHA, and validation results to parent `#117` records without overwriting original `Residual work` (`RV-001`) Review outcomes, author `issue-117-doc-scan-fix-rebase-0358b9ad5-changes.md`, and reconcile `P01`–`P03` markers `[x]` for `rpi-review`. Immediately after `rpi-review` writes `-review.md` and parent `RPI Agent` transitions state to `Follow-up`, parent `RPI Agent` commits all 10 updated parent and child `.copilot-tracking/` artifacts locally so `git status --short` is empty.

### Boundaries

* Included:
  * Pre-Review (`P03-T01` in `rpi-implement`):
    1. `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md` (append `0358b9ad5` rebase + `test_resident_decisions.py` fix section)
    2. `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md` (append `0358b9ad5` rebase/fix verification note while preserving original `Residual work` / `RV-001` outcome)
    3. `.copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-state.json` (append confirmed child rebase/fix continuation decision)
    4. `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-changes.md` (create complete implementation changes record)
    5. `.copilot-tracking/plans/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-plan.md` (reconcile `P01`–`P03` markers to `[x]`)
    6. `.copilot-tracking/details/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-phase-details.md` (reconcile Phase Index statuses to `Complete`)
  * Post-Review (`RPI Agent` parent closeout):
    7. `.copilot-tracking/research/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-research.md`
    8. `.copilot-tracking/reviews/plans/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-plan-critique.md`
    9. `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-review.md` and `.copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-state.json` (total 10 `.copilot-tracking/` paths committed cleanly with noreply email and `Co-authored-by` trailer, leaving `git status --short` empty).
* Excluded: Overwriting earlier review verdicts, referencing `.copilot-tracking/` paths in git commit messages, or executing `git push`.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md`
* `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md`
* `.copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-state.json`
* `.copilot-tracking/research/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-research.md`
* `.copilot-tracking/plans/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-plan.md`
* `.copilot-tracking/details/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-phase-details.md`
* `.copilot-tracking/reviews/plans/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-plan-critique.md`
* `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-changes.md`
* `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-review.md`
* `.copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-state.json`

### Dependencies

* P02

### Validation Expectations

* Pre-Review (`P03-T01`): `python3 -m json.tool .copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-state.json >/dev/null && python3 -m json.tool .copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-state.json >/dev/null` and `git diff --check` exit `0`; `git status --short | grep -v '\.copilot-tracking/'` is empty.
* Post-Review (`RPI Agent` closeout): `git status --short` outputs empty string.

### Completion Evidence

* Reconciled pre-Review artifacts for `rpi-review`, followed by clean local tracking commit SHA at parent closeout.

### Unresolved Items

* none

<!-- rpi:task id=P03-T01 -->
### P03-T01: Append 0358b9ad5 rebase/fix lineage to parent #117 records and reconcile child pre-Review RPI artifacts

#### Context

Keeping parent `#117` artifacts and child `issue-117-doc-scan-fix-rebase-0358b9ad5` artifacts synchronized before `rpi-review` ensures complete traceability across the initial implementation, the `fa6f8d1dd` rebase, and the `0358b9ad5` rebase + `test_resident_decisions.py` fix.

#### Intent

Append the `0358b9ad5` rebase and `test_resident_decisions.py` fix evidence to parent `#117` records (preserving original `Residual work` / `RV-001` outcomes), author child `-changes.md`, and mark `P01`–`P03` `[x]` cleanly ahead of `rpi-review`.

#### Boundaries

* Included: Pre-Review `.copilot-tracking/` updates and JSON/diff hygiene checks.
* Excluded: Source edits, overwriting original Review verdicts, or remote pushes.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md`
* `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md`
* `.copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-state.json`
* `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-changes.md`
* `.copilot-tracking/plans/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-plan.md`
* `.copilot-tracking/details/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-phase-details.md`

#### Dependencies

* P02-T01

#### Validation Expectations

* `python3 -m json.tool` passes on both state JSON files, `git diff --check` exits `0`, and zero non-`.copilot-tracking/` files appear in `git status --short`.

#### Completion Evidence

* Reconciled pre-Review tracking files ready for `rpi-review`.

#### Unresolved Items

* none
