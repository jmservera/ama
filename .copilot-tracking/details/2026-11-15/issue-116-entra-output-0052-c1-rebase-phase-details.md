<!-- markdownlint-disable-file -->
# RPI Phase Details: Cycle 1 Rebase Continuation (`c1-rebase`) Onto Merged Parent Tip `0c1fa1da4` (`PR #1769`)

## Metadata

* Task ID: issue-116-entra-output-0052-c1-rebase
* Task slug: issue-116-entra-output-0052-c1-rebase
* Related plan: .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-rebase-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-c1-rebase-research.md

## Phase Index

| Phase ID | Name                                                                        | Status  | Detail sections |
|----------|-----------------------------------------------------------------------------|---------|-----------------|
| P01      | Fetch Parent Branch and Rebase `7b882614d..e7d05fab4` Onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4` -> `d8cb35d25`) | Complete | P01, P01-T01    |
| P02      | Focused Validation, C1 Tracking Updates, and Pre-Review Reconciliation      | Complete | P02, P02-T01    |

<!-- rpi:phase id=P01 -->
## P01: Fetch Parent Branch and Rebase `7b882614d..e7d05fab4` Onto `0c1fa1da4`

### Context

Research (`C1`-`C4`) established that `origin/feat/demo-164-chat-grounding-provenance-0900` advanced by 1 commit from `7f83f4749` (`PR #1761`) to `0c1fa1da4` (`PR #1769`, `Refs #83`). When replaying `7b882614d` (`feat(core,api): recheck AI output role visibility and gate document derivatives`) and `e7d05fab4` (`fix(core): preserve reviewer-authored notes in _record_view and fix docstring`) onto `0c1fa1da4`, `src/api/src/zava_forward/api/server.py` and `src/api/tests/test_role_endpoint_inventory.py` auto-merge cleanly, `src/core/src/zava_forward/core/store.py` has 2 conflict blocks (`_queue_candidates` and `_work_context`), and `e7d05fab4` replays with zero conflicts afterward.

### Intent

Rebase `feat/ai-116-entra-output-0052` (`7b882614d..e7d05fab4`) cleanly onto `0c1fa1da4` while preserving 100% of `#83` (`0c1fa1da4`), `#164` (`7f83f4749`), and `#116` (`7b882614d..e7d05fab4`).

### Boundaries

* Included: Repository-local privacy-safe `git config --local user.email` setup via `gh api user`, path-preserving `find` + `tar` archive/restore of untracked `c1-rebase` `.copilot-tracking/` files at `/home/azureuser/.copilot/session-state/f0c59e3e-4b74-4f53-a238-646f1d96d6c1/files/c1-rebase-backup.tar`, `git fetch origin feat/demo-164-chat-grounding-provenance-0900`, `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, and 2-hunk conflict resolution in `src/core/src/zava_forward/core/store.py`.
* Excluded: Modifying any source logic outside mechanical conflict resolution in `store.py`, amending commit messages of `7b882614d` or `e7d05fab4`, or pushing to `origin`.

### Likely Targets

* `src/core/src/zava_forward/core/store.py`: `_queue_candidates` (`key` tuple with `json.dumps(self.data.get("handoff_policy"), sort_keys=True)`) and `_work_context` (`handoff=handoff_view(c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff"))`), plus verification that `detail` (`d["handoff"] = handoff_view(...)`) and lines `1016..2075` role-visibility changes remain intact.

### Dependencies

* None.

### Validation Expectations

* `git merge-base --is-ancestor 0c1fa1da4 HEAD` exits `0`, `git grep -n '<<<<<<<'` returns empty, and `git diff 0c1fa1da4..HEAD -- src/core/src/zava_forward/core/taskqueues.py src/core/src/zava_forward/core/sqlstore.py` is empty (proving `0c1fa1da4`'s `MEMBERSHIP_REVISION = 4` and `_queue_fingerprint` are preserved untouched).

### Completion Evidence

* Clean rebased commit pair `fc44a697c` (`7b882614d'`) and `41091c2a0` (`e7d05fab4'`) atop `d8cb35d25` (`PR #1770`, direct child of `0c1fa1da4` / `PR #1769`).

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Fetch `origin feat/demo-164-chat-grounding-provenance-0900`, rebase `7b882614d..e7d05fab4` onto `0c1fa1da4`, and resolve `store.py` conflict

#### Context

In `src/core/src/zava_forward/core/store.py`:
* Conflict hunk 1 (`_queue_candidates`): `0c1fa1da4` added `json.dumps(self.data.get("handoff_policy"), sort_keys=True)` to `key`, whereas `7b882614d` formatted `key` across multiple lines.
* Conflict hunk 2 (`_work_context`): `0c1fa1da4` updated `handoff=handoff_view(c)` to `handoff=handoff_view(c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff"))`, whereas `7b882614d` split `resident_reasons=resident_gate(c), technical_missing=missing_items(c), handoff=handoff_view(c)` onto separate lines.

#### Intent

1. Resolve `{id}+{login}@users.noreply.github.com` from `gh api user` and set `git config --local user.email`.
2. Archive all untracked `c1-rebase` tracking files with full relative paths via `find .copilot-tracking -name 'issue-116-entra-output-0052-c1-rebase-*' -print0 | tar --null -cf /home/azureuser/.copilot/session-state/f0c59e3e-4b74-4f53-a238-646f1d96d6c1/files/c1-rebase-backup.tar -T -`, remove those matched untracked files (`find .copilot-tracking -name 'issue-116-entra-output-0052-c1-rebase-*' -delete`), and confirm `git status --short` is empty.
3. Run `git fetch origin feat/demo-164-chat-grounding-provenance-0900` and verify `git rev-parse origin/feat/demo-164-chat-grounding-provenance-0900` equals `0c1fa1da474b541eece7b8ac61760a919fe0f756`.
4. Run `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`.
5. Edit `src/core/src/zava_forward/core/store.py` to resolve `_queue_candidates` with:
   ```python
        key = (
            self.version,
            self.as_of,
            controls.today(),
            json.dumps(ranking.CURRENT, sort_keys=True),
            json.dumps(self.data.get("handoff_policy"), sort_keys=True),
        )
   ```
   and `_work_context` with:
   ```python
            building_reasons=buildings.blockers(data, cases, c),
            resident_reasons=resident_gate(c),
            technical_missing=missing_items(c),
            handoff=handoff_view(
                c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff")
            ),
        )
   ```
6. Stage `src/core/src/zava_forward/core/store.py`, run `GIT_EDITOR=true git rebase --continue`, verify both `7b882614d'` and `e7d05fab4'` completed cleanly atop `0c1fa1da4`, and restore the `c1-rebase` `.copilot-tracking/` files via `tar -xf /home/azureuser/.copilot/session-state/f0c59e3e-4b74-4f53-a238-646f1d96d6c1/files/c1-rebase-backup.tar && rm -f /home/azureuser/.copilot/session-state/f0c59e3e-4b74-4f53-a238-646f1d96d6c1/files/c1-rebase-backup.tar`.

#### Boundaries

* Included: `src/core/src/zava_forward/core/store.py`.
* Excluded: Touching `taskqueues.py`, `sqlstore.py`, `workflows.py`, or any other file in `0c1fa1da4`.

#### Likely Targets

* `src/core/src/zava_forward/core/store.py`

#### Dependencies

* None.

#### Validation Expectations

* `git merge-base --is-ancestor 0c1fa1da4 HEAD` exits `0`; `git log --oneline 0c1fa1da4..HEAD` shows the 2 rebased commits (`7b882614d'` and `e7d05fab4'`); zero conflict markers remain.

#### Completion Evidence

* Recorded new commit SHAs `fc44a697c` (`7b882614d'`) and `41091c2a0` (`e7d05fab4'`) atop `d8cb35d25` (`PR #1770`, parent `0c1fa1da4` / `PR #1769`).

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Focused Validation, C1 Tracking Updates, and Pre-Review Reconciliation

### Context

Caller Scope items #3-#4 require updating `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md` and `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md` to record the rebase onto `0c1fa1da4`, running the Focused validation commands (mapping non-existent `src/api/tests/test_design_system_source_contract.py` to canonical `src/api/tests/test_design_system.py` per `PC-001`, and including `src/api` on `PYTHONPATH` for `test_handoff_escalation_api_83.py` per `PC-002`), and reconciling `c1-rebase` implementation artifacts before read-only `rpi-review` (with Scope item #5's clean local tracking commit executed by the automatic RPI parent immediately after `rpi-review` completes per `PC-003`).

### Intent

Execute all Focused validation checks on the rebased code, update `c1-changes.md` and `c1-review.md` (preserving `c1`'s original `Conformant` verdict while recording the `0c1fa1da4` rebase, module-name disclosure, and validation), and reconcile `c1-rebase` RPI artifacts ready for single-pass `rpi-review`.

### Boundaries

* Included: Focused validation execution, `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md`, and `c1-rebase` `.copilot-tracking/` reconciliation (`c1-rebase-changes.md`, `c1-rebase-plan.md`, `c1-rebase-phase-details.md`).
* Excluded: Source or test code modifications, Docker/`rpi-checks.py --all`, `git push`, and `ask_user` (final post-review `git commit` runs in the automatic RPI parent closeout after `rpi-review` writes `c1-rebase-review.md` and `c1-rebase-state.json`).

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md`
* `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md`
* `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-rebase-changes.md`

### Dependencies

* P01.

### Validation Expectations

* Every command below exits `0`:
  1. `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api/src:src/api/tests python3 -m unittest src/api/tests/test_ai_tasks.py src/api/tests/test_design_system.py src/core/tests/test_data_protection.py -q`
  2. `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api:src/api/src:src/api/tests python3 -m unittest src/core/tests/test_handoff_escalation_83.py src/api/tests/test_handoff_escalation_api_83.py src/api/tests/test_role_endpoint_inventory.py src/api/tests/test_content_standard.py src/core/tests/test_human_review_effectiveness_223.py -q`
  3. `cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy`
  4. `cd src/api && python3 -m ruff check . && python3 -m ruff format --check .`
  5. `python3 tools/rename-zava-tests.py`

### Completion Evidence

* Passing Focused validation outputs recorded in both `c1-changes.md` and `c1-rebase-changes.md`, `c1-review.md` updated with original `Conformant` verdict preserved, and `c1-rebase` plan/details/changes reconciled with zero dirty `src/` or `tools/` files.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run Focused validation suites, update `c1-changes.md` and `c1-review.md` for `0c1fa1da4`, and reconcile `c1-rebase` artifacts for `rpi-review`

#### Context

Per repository governance ("Preserve original critique/Review outcomes"), `issue-116-entra-output-0052-c1-review.md` retains its original `Outcome: Conformant` and original `7f83f4749` assessment sections while adding a dated `Rebase Continuation Record (0c1fa1da4 / PR #1769)` note (and updating `Residual Work` to note completion via `issue-116-entra-output-0052-c1-rebase`), and `issue-116-entra-output-0052-c1-changes.md` adds a dated `Rebase Continuation Onto 0c1fa1da4 (PR #1769)` subsection and validation row with the new rebased SHAs and explicit `test_design_system_source_contract.py` -> `test_design_system.py` disclosure.

#### Intent

Run all 5 Focused validation commands (`4` caller-requested checks with `test_design_system.py` + `1` cross-feature `#83`/`#116` regression command with `src/api` on `PYTHONPATH`), update `c1-changes.md` and `c1-review.md`, and write/reconcile `c1-rebase-changes.md`, `c1-rebase-plan.md`, and `c1-rebase-phase-details.md` ready for single-pass `rpi-review` (after which the automatic RPI parent records `Follow-up` / `completed` in `c1-rebase-state.json` and creates the single clean local tracking commit with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`).

#### Boundaries

* Included: `.copilot-tracking/` updates and Focused validation commands.
* Excluded: Any edit to `src/` or `tools/`, any `git push`, or any `ask_user` call.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md`
* `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md`
* `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-rebase-changes.md`

#### Dependencies

* P01-T01.

#### Validation Expectations

* All 5 validation commands exit `0`; Markdown relative links resolve; `git status --short` shows only `.copilot-tracking/` files prior to `rpi-review`.

#### Completion Evidence

* Passing Focused validation results and reconciled `c1` + `c1-rebase` `.copilot-tracking/` artifacts ready for `rpi-review`.

#### Unresolved Items

* None.
