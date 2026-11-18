<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #117 Document Scan Rebase Continuation onto fa6f8d1dd

## Metadata

* Task ID: issue-117-doc-scan-rebase-fa6f8d1dd
* Task slug: issue-117-doc-scan-rebase-fa6f8d1dd
* Related plan: .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-research.md (`C1`–`C8`), .copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md, .copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md

## Phase Index

| Phase ID | Name                                                               | Status | Detail sections |
|----------|--------------------------------------------------------------------|--------|-----------------|
| P01      | Rebase Branch onto fa6f8d1dd and Resolve Store.focus Conflict      | Ready  | P01, P01-T01    |
| P02      | Execute Worktree-Isolated Focused Validation                       | Ready  | P02, P02-T01    |
| P03      | Reconcile Pre-Review #117 and Child Tracking Artifacts             | Ready  | P03, P03-T01    |

<!-- rpi:phase id=P01 -->
## P01: Rebase Branch onto fa6f8d1dd and Resolve Store.focus Conflict

### Context

Branch `feat/demo-117-doc-scan` holds clean candidate commit `4d91dae33` atop `243764945`. Target integration branch `origin/feat/demo-164-chat-grounding-provenance-0900` advanced by three squash-merged commits (`36aeddae3` PR #1773, `f71331d42` PR #1768, and `fa6f8d1dd` PR #1774). Read-only `git merge-tree --write-tree --messages origin/feat/demo-164-chat-grounding-provenance-0900 4d91dae33` (`C2`) confirmed that `chat_case_answers.py`, `projection.py`, and `taskqueues.py` auto-merge cleanly while `src/core/src/zava_forward/core/store.py` has a single 2-line adjacency conflict in `Store.focus`.

### Intent

Configure repository-local privacy-safe git email from `gh api user`, replay `4d91dae33` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`), and resolve `Store.focus` in `src/core/src/zava_forward/core/store.py` so both `#76` safety item owner projection and `#117` fail-closed document availability filtering remain intact.

### Boundaries

* Included: `gh api user` verification and `git config --local user.email`, `git fetch` verification of `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`), `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, conflict resolution in `Store.focus` (`src/core/src/zava_forward/core/store.py`), optional import-order fix in `src/core/src/zava_forward/core/taskqueues.py` if git 3-way auto-merge orders `from .doc_controls` ahead of stdlib imports, and `GIT_EDITOR=true git rebase --continue`.
* Excluded: Modifying any tracked `.copilot-tracking/` file prior to `git rebase --continue`, editing `src/api/src/zava_forward/api/server.py`, or pushing to `origin`.

### Likely Targets

* `src/core/src/zava_forward/core/store.py`: Resolve the single conflict hunk in `Store.focus` (`staff_list = self.data.get("staff") or list(self.staff.values())`, `open_h = self._open_safety_items(c, staff=staff_list)`, `ev = {d["kind"] for d in c["documents"] if is_available_case_document(d)}`).
* `src/core/src/zava_forward/core/taskqueues.py`: Verify top-of-file import block ordering after git auto-merge so `ruff check .` (`I001`) and `ruff format --check .` pass cleanly.

### Dependencies

* Clean tracked working tree (`git diff --quiet` and `git diff --cached --quiet`).

### Validation Expectations

* `git merge-base --is-ancestor fa6f8d1dd HEAD` exits `0`.
* `git diff --check` exits `0` with zero conflict markers.
* `git --no-pager diff fa6f8d1dd..HEAD -- src/api/src/zava_forward/api/server.py` is empty.

### Completion Evidence

* Rebased feature commit SHA recorded directly atop `fa6f8d1dd`.

### Unresolved Items

* none

<!-- rpi:task id=P01-T01 -->
### P01-T01: Configure local privacy-safe git email, rebase onto fa6f8d1dd, and resolve Store.focus in store.py

#### Context

In `Store.focus`, upstream `f71331d42` replaced `open_h = [h for h in c["hazards"] if not h["released"]]` with `staff_list` and `self._open_safety_items(c, staff=staff_list)`, immediately adjacent to `#117`'s `ev = {d["kind"] for d in c["documents"] if is_available_case_document(d)}` (`C3`).

#### Intent

Complete `git rebase origin/feat/demo-164-chat-grounding-provenance-0900` preserving both lines in `Store.focus` and clean Ruff import formatting across auto-merged `src/core` files.

#### Boundaries

* Included: Local noreply `user.email` config, `git rebase`, `edit` of `src/core/src/zava_forward/core/store.py` (and `taskqueues.py` import order if needed before or during rebase continue), `git add`, and `GIT_EDITOR=true git rebase --continue`.
* Excluded: Any remote git operation.

#### Likely Targets

* `src/core/src/zava_forward/core/store.py`
* `src/core/src/zava_forward/core/taskqueues.py` (verification of auto-merged import block)

#### Dependencies

* none

#### Validation Expectations

* `git --no-pager log -n 2 --oneline` shows the rebased `#117` feature commit directly atop `fa6f8d1dd`.

#### Completion Evidence

* Rebased commit SHA and clean `git diff --check` exit `0`.

#### Unresolved Items

* none

<!-- rpi:phase id=P02 -->
## P02: Execute Worktree-Isolated Focused Validation

### Context

On this shared host, `~/.local` editable installs for `zava-forward-{core,agents,api}` point to another worktree (`feat-164-chat-revocation-0042`) (`C8`). Prepending worktree-local `PYTHONPATH` (and `MYPYPATH` where needed) ensures all static checks and unit tests evaluate the rebased `feat-117-doc-scan` HEAD without disturbing concurrent worktrees.

### Intent

Prove zero lint, format, type, quarantine-gate, safety-projection, endpoint-inventory, or rename-guard regressions on the rebased HEAD.

### Boundaries

* Included:
  * Asserting `zava_forward.core.__file__`, `zava_forward.agents.__file__`, and `zava_forward.api.__file__` all resolve inside `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan/`.
  * Running `ruff check .`, `ruff format --check .`, and `mypy` in `src/core`.
  * Running `ruff check .`, `ruff format --check .`, and `mypy` in `src/api`.
  * Running `#117` document malware scan quarantine tests and `#76` `Store.focus` regression tests in `src/core` (`tests/test_document_rescan.py`, `tests/test_resident_documents.py`, `tests/test_technical_evidence_usability.py`, `tests/test_documents.py`, `tests/test_hazard_safeguarding_clock_owner.py`).
  * Running `#117` document controls and route inventory tests in `src/api` (`tests/test_document_controls.py`, `tests/test_role_endpoint_inventory.py`).
  * Running `python3 tools/rename-zava-tests.py` from repository root.
* Excluded: `tools/rpi-checks.py` and global `pip install -e`.

### Likely Targets

* Read-only CLI validation across `src/core`, `src/api`, and `tools/rename-zava-tests.py`.

### Dependencies

* P01

### Validation Expectations

* Ephemeral `PYTHONNOUSERSITE=1` venv (`pip install -e src/core -e src/agents -e "src/api[dev]"`, matching `src-ci.yml` without touching `~/.local`) verifies PEP 420 namespace `zava_forward.{core,agents,api}.__path__` entries all resolve inside `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan/`.
* `cd src/core && "$TMPVENV/bin/python" -m ruff check . && "$TMPVENV/bin/python" -m ruff format --check . && "$TMPVENV/bin/python" -m mypy` exits `0`.
* `cd src/api && "$TMPVENV/bin/python" -m ruff check . && "$TMPVENV/bin/python" -m ruff format --check . && "$TMPVENV/bin/python" -m mypy` exits `0`.
* `cd src/core && PYTHONPATH=src:tests python3 -m unittest tests/test_document_rescan.py tests/test_resident_documents.py tests/test_technical_evidence_usability.py tests/test_documents.py tests/test_hazard_safeguarding_clock_owner.py -v` exits `0`.
* `cd src/api && PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m unittest tests/test_document_controls.py tests/test_role_endpoint_inventory.py -v` exits `0`.
* `python3 tools/rename-zava-tests.py` exits `0`.

### Completion Evidence

* Exact pass counts and exit `0` status recorded in `.copilot-tracking/` changes artifacts.

### Unresolved Items

* none

<!-- rpi:task id=P02-T01 -->
### P02-T01: Assert worktree module resolution and run ruff, mypy, and focused #117/#76/inventory unit tests

#### Context

Caller Step 2 requires `ruff check .`, `ruff format --check .`, `mypy`, and the `#117` document malware scan quarantine tests in `src/core` and `src/api` on the rebased HEAD. Including `test_hazard_safeguarding_clock_owner.py` and `test_role_endpoint_inventory.py` also verifies the `Store.focus` conflict resolution and unchanged route inventory.

#### Intent

Execute all focused validation commands with verified worktree module isolation and capture exact outputs.

#### Boundaries

* Included: Worktree path check, `ruff`, `mypy`, `unittest`, and `rename-zava-tests.py`.
* Excluded: Unrelated test edits or shared environment package installation.

#### Likely Targets

* `src/core/tests/test_document_rescan.py`
* `src/core/tests/test_resident_documents.py`
* `src/core/tests/test_technical_evidence_usability.py`
* `src/core/tests/test_documents.py`
* `src/core/tests/test_hazard_safeguarding_clock_owner.py`
* `src/api/tests/test_document_controls.py`
* `src/api/tests/test_role_endpoint_inventory.py`
* `tools/rename-zava-tests.py`

#### Dependencies

* P01-T01

#### Validation Expectations

* Every command exits `0`.

#### Completion Evidence

* Test counts, `ruff` file counts, and `mypy` file counts recorded in the changes artifact.

#### Unresolved Items

* none

<!-- rpi:phase id=P03 -->
## P03: Reconcile Pre-Review #117 and Child Tracking Artifacts

### Context

Because `.copilot-tracking/` is git-tracked in this repository (`C7`), `rpi-implement` (`P03-T01`) reconciles the pre-Review tracking set while preserving original `#117` `Residual work` (`RV-001`) Review outcomes, and parent `RPI Agent` post-Review closeout commits all 10 updated parent and child `.copilot-tracking/` artifacts (including `-review.md` and the `Follow-up` `-state.json`) so `git status --short` is empty without pushing.

### Intent

During `rpi-implement` (`P03-T01`), append post-rebase base (`fa6f8d1dd`), rebased feature commit SHA, and focused validation results to parent `#117` changes, review, and state records (without overwriting original `Residual work` / `RV-001` outcomes), author `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-changes.md`, and reconcile `P01`–`P03` plan markers ahead of `rpi-review`. At parent `RPI Agent` post-Review closeout, stage and commit all 10 `.copilot-tracking/` files cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.

### Boundaries

* Included (`P03-T01` pre-Review `rpi-implement`): Appending post-rebase metadata/validation to parent `#117` changes/review/state files (preserving original `Residual work` / `RV-001`), writing child `-changes.md`, reconciling child plan checkboxes, and running `python3 -m json.tool` and `git diff --check`.
* Included (Parent `RPI Agent` post-Review closeout): Final local `git commit` across all 10 updated parent and child `.copilot-tracking/` files after `-review.md` and `Follow-up` `-state.json` are written, without referencing internal `.copilot-tracking/` paths in the commit message.
* Excluded: `git push`, unrequested `git commit --amend` on the rebased feature commit, overwriting original `#117` Review outcomes, or touching production/test code in `P03`.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md` (updated in `P03-T01`)
* `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md` (appended post-rebase note in `P03-T01` preserving original `Residual work` / `RV-001` outcome)
* `.copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-state.json` (updated in `P03-T01`)
* `.copilot-tracking/research/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-research.md` (committed at post-Review closeout)
* `.copilot-tracking/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan.md` (markers reconciled in `P03-T01`, committed at post-Review closeout)
* `.copilot-tracking/details/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-phase-details.md` (committed at post-Review closeout)
* `.copilot-tracking/reviews/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan-critique.md` (committed at post-Review closeout)
* `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-changes.md` (created/reconciled in `P03-T01`, committed at post-Review closeout)
* `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-review.md` (created by `rpi-review`, committed at post-Review closeout)
* `.copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-state.json` (updated across phases, finalized in `Follow-up` and committed at post-Review closeout)

### Dependencies

* P02

### Validation Expectations

* Pre-Review (`P03-T01`): `python3 -m json.tool` exits `0` on both `.copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan*.json` files, `git diff --check` exits `0`, and zero non-`.copilot-tracking/` paths appear in `git status --short`.
* Post-Review parent closeout: `git status --short` outputs empty string and `git log -1` shows noreply author plus `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.

### Completion Evidence

* Pre-Review (`P03-T01`): Reconciled parent/child tracking artifacts and clean `json.tool` + `git diff --check` ready for `rpi-review`.
* Post-Review parent closeout: Empty `git status --short` and verified commit log atop `fa6f8d1dd`.

### Unresolved Items

* none

<!-- rpi:task id=P03-T01 -->
### P03-T01: Append post-rebase lineage to parent #117 records and reconcile child pre-Review RPI artifacts

#### Context

Parent `#117` tracking records currently reflect the pre-rebase `243764945` base and original `Residual work` (`RV-001`) Review outcome. Appending the `fa6f8d1dd` rebase and post-rebase validation results while keeping `RV-001` intact preserves full auditability ahead of `rpi-review`.

#### Intent

Reconcile all pre-Review parent and child `.copilot-tracking/` records so `rpi-review` can assess the complete `P01`–`P03` implementation boundary cleanly before parent `RPI Agent` executes the final 10-file tracking commit.

#### Boundaries

* Included: Pre-Review `.copilot-tracking/` Markdown and JSON updates listed in `P03` Likely Targets.
* Excluded: Production/test files, overwriting original `#117` Review outcomes, and remote git refs.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md`
* `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md`
* `.copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-state.json`
* `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-changes.md`
* `.copilot-tracking/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan.md`

#### Dependencies

* P02-T01

#### Validation Expectations

* `python3 -m json.tool` passes on both state JSON files; `git diff --check` exits `0`; `git status --short` shows only `.copilot-tracking/` entries prior to `rpi-review`.

#### Completion Evidence

* Reconciled pre-Review `.copilot-tracking/` artifacts ready for single-pass `rpi-review`.

#### Unresolved Items

* none
