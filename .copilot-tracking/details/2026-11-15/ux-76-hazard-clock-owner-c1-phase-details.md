<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #76 Correction Cycle 1 — PR #1768 `mssql` CI Parity Fix and Rebase onto `#1641`

## Metadata

* Task ID: issue-76-c1
* Task slug: ux-76-hazard-clock-owner-c1
* Related plan: .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c1-research.md, .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md

## Phase Index

| Phase ID | Name                                                               | Status   | Detail sections       |
|----------|--------------------------------------------------------------------|----------|-----------------------|
| P01      | Rebase onto `#1641` (`0c1fa1da4`) and Order-Invariant Staff Resolution | Complete | P01, P01-T01, P01-T02 |
| P02      | Permutation Parity Unit Tests, Focused Validation, and Local Commit Preparation | Complete | P02, P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Rebase onto `#1641` (`0c1fa1da4`) and Order-Invariant Staff Resolution

### Context

Research findings `C1`–`C10` confirm two concrete issues:
1. Target branch `origin/feat/demo-164-chat-grounding-provenance-0900` advanced to `0c1fa1da4` after PR #1769 (`#83`) merged, creating a 6-line merge conflict in `Store._work_context` (`src/core/src/zava_forward/core/store.py`) and also claiming `taskqueues.MEMBERSHIP_REVISION = 4`.
2. In `src/core/src/zava_forward/core/taskqueues.py`, `_match_staff` checks `code`, `email`, and `name` inside a single pass over `staff`, and `project_safety_clock_and_owner` scans `roster` in raw input order for role-based escalation fallback. Because SQL Server (`MssqlStore`) stores `staff` in a clustered primary-key index on `email` (`[kim@example.test, pam@example.test, sam@example.test]`) while `Store` and SQLite keep seed insertion order (`[Sam Example, Pam Lead, Kim Builder]`), cases in `test_sqlreads.make_cases` with `owner_code="PM-01"` and default `owner="Sam Example"` resolved `escalation_owner` to `"Sam Example"` in `Store` vs `"Pam Lead"` in `MssqlStore`.

### Intent

Rebase cleanly onto `0c1fa1da4` and make all safety-item staff matching and fallback resolution strictly deterministic and invariant to `staff` ordering.

### Boundaries

* Included: Git rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`); `src/core/src/zava_forward/core/store.py` conflict resolution; `src/core/src/zava_forward/core/taskqueues.py` (`MEMBERSHIP_REVISION`, `_match_staff`, `project_safety_clock_and_owner`); `src/core/README.md`.
* Excluded: Web/API changes, `tools/rpi-checks.py`, or remote pushes.

### Likely Targets

* `src/core/src/zava_forward/core/store.py`: Resolve `Store._work_context` rebase conflict.
* `src/core/src/zava_forward/core/taskqueues.py`: Update `MEMBERSHIP_REVISION`, `_match_staff`, and `project_safety_clock_and_owner`.
* `src/core/README.md`: Sync documented `MEMBERSHIP_REVISION = 5`.

### Dependencies

* Untracked `.copilot-tracking/` `-c1` files do not overlap any paths in `02ab20cac..0c1fa1da4`, allowing `git rebase` to run on a clean tracked tree before source edits.

### Validation Expectations

* Rebase completes with zero remaining conflict markers; `#83` (`test_handoff_escalation_83.py`) and `#76` (`test_hazard_safeguarding_clock_owner_76.py`) both pass.

### Completion Evidence

* `git merge-base --is-ancestor 0c1fa1da4 HEAD` succeeds and `taskqueues.py` contains order-invariant `_match_staff` and sorted role fallback.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Rebase branch onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) and resolve `store.py`

#### Context

`origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) added `as_of`, `policy`, and `staff` arguments to `handoff_view(...)` in `Store._work_context`, while `5d4c80ee3` added `staff=staff_list` to `taskqueues.context(...)` on the same closing line (`C5`).

#### Intent

Replay `5d4c80ee3` onto `0c1fa1da4` preserving both `#83` and `#76` call arguments.

#### Boundaries

* Included:
  * Run `git fetch origin feat/demo-164-chat-grounding-provenance-0900 && git rebase origin/feat/demo-164-chat-grounding-provenance-0900`.
  * Resolve `src/core/src/zava_forward/core/store.py` in `Store._work_context` to keep:
    ```python
            handoff=handoff_view(
                c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff")
            ),
            staff=staff_list,
        )
    ```
  * Stage `src/core/src/zava_forward/core/store.py` and finish rebase via `GIT_EDITOR=true git rebase --continue`.
* Excluded: Rewriting unrelated commits or force-pushing.

#### Likely Targets

* `src/core/src/zava_forward/core/store.py`

#### Dependencies

* Clean tracked working tree prior to `git rebase`.

#### Validation Expectations

* `git status` shows rebase finished cleanly on `feat/ux-76-hazard-clock-owner` with `0c1fa1da4` in ancestry.

#### Completion Evidence

* `git merge-base --is-ancestor 0c1fa1da4 HEAD` exits `0` and `store.py` contains no conflict markers.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Make `_match_staff` and `project_safety_clock_and_owner` order-invariant and bump `MEMBERSHIP_REVISION`

#### Context

Research `C6`–`C10` showed `_match_staff` matches `name` on an earlier staff row before checking `code` on a later staff row, `project_safety_clock_and_owner` scans `roster` unsorted for `target_role`, and `MEMBERSHIP_REVISION = 4` now collides with `#83` on `0c1fa1da4`.

#### Intent

Guarantee field-precedence (`code` > `email` > `name`) and canonical tie-break ordering regardless of `staff` row order, and bump `MEMBERSHIP_REVISION` to `5`.

#### Boundaries

* Included:
  * Set `MEMBERSHIP_REVISION = 5` in `src/core/src/zava_forward/core/taskqueues.py` and update `MEMBERSHIP_REVISION = 5` in `src/core/README.md`.
  * Define canonical staff ordering key `(str(m.get("code") or m.get("oid") or "").strip(), str(m.get("email") or "").strip().lower(), str(m.get("name") or "").strip().lower())` in `_match_staff`, then run three separate precedence passes across `ordered_staff`:
    1. If `code`: normalize `code_clean = code.strip()` and match `if code_clean and m_code == code_clean:`.
    2. If `email`: normalize `email_low = email.strip().lower()` and match `if email_low and m_email == email_low:`.
    3. If `name`: normalize `name_low = name.strip().lower()` and match `if name_low and m_name == name_low:`.
  * In `project_safety_clock_and_owner`, iterate `for member in sorted(roster, key=lambda m: str(m.get("code") or m.get("email") or m.get("name") or "")):` inside the `target_role` escalation fallback loop.
* Excluded: Altering clock window rules or `FR-003` receipt-is-not-acceptance owner precedence.

#### Likely Targets

* `src/core/src/zava_forward/core/taskqueues.py`
* `src/core/README.md`

#### Dependencies

* P01-T01 completed.

#### Validation Expectations

* `ruff check`, `ruff format --check`, and `mypy` pass on `taskqueues.py`.

#### Completion Evidence

* `_match_staff` and `project_safety_clock_and_owner` produce identical outputs for any permutation of `staff`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Permutation Parity Unit Tests, Focused Validation, and Local Commit Preparation

### Context

Research `C11` and `C12` plus critique `PC-001` and `PC-002` confirmed that Cycle 0 tests live in `test_hazard_safeguarding_clock_owner_76.py` whereas caller validation explicitly invokes `-p "test_hazard_safeguarding_clock_owner.py"`, `mypy` runs with `strict = true` (`disallow_untyped_calls = true`) across `src` and `tests`, and closeout requires repository-local `gh api user` noreply email configuration plus a clean local `Refs #76` commit after Review without pushing.

### Intent

Add focused, strictly typed unit tests proving staff-order invariance and SQL Server email-order store parity in `src/core/tests/test_hazard_safeguarding_clock_owner.py`, run the full focused validation suite, configure privacy-safe Git author metadata, and reconcile artifacts for `rpi-review` and final clean commit.

### Boundaries

* Included: Creating `src/core/tests/test_hazard_safeguarding_clock_owner.py` (test budget: max 1 new test file, 0 test removals); running `test_hazard_safeguarding_clock_owner.py`, `test_sqlreads.py`, `mypy`, `ruff check`, `ruff format --check`, and `unittest discover -s tests -q` in `src/core`; configuring repository-local `user.email` via `gh api user`; recording `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-changes.md` and post-`rpi-review` clean commit sequencing.
* Excluded: Modifying existing `test_sqlreads.py` to mask mixed `owner_code` / `owner` cases; running `tools/rpi-checks.py`; pushing to remote.

### Likely Targets

* `src/core/tests/test_hazard_safeguarding_clock_owner.py`
* `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-changes.md`

### Dependencies

* P01 completed.

### Validation Expectations

* All four caller validation commands plus `ruff check` / `ruff format --check` exit `0`, and `git diff --name-status` matches the locked test/scope budget.

### Completion Evidence

* Recorded command outputs, configured local Git author email, and reconciled checklist markers ready for `rpi-review` and final clean local commit.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add `src/core/tests/test_hazard_safeguarding_clock_owner.py` and execute focused validation

#### Context

The exact `MssqlParity` failure occurred when `case` had `owner_code="PM-01"`, `owner="Sam Example"`, and an open hazard with `owner="Bea"`, and `staff` was ordered `[Sam, Pam, Kim]` (`Store`) vs `[Kim, Pam, Sam]` (`MssqlStore` clustered `email` PK order). Because `Store`, `SqlStore`, and `test_sqlreads` are untyped under `mypy` `disallow_untyped_calls = true`, tests must invoke them via `Any`-typed bindings (`store_cls: Any = Store`, `sql_store_cls: Any = SqlStore`, `reads_mod: Any = test_sqlreads`).

#### Intent

Lock in permanent regression coverage for both `_match_staff` precedence (`code` > `email` > `name`) and `target_role` roster sorting across all permutations of `staff`, plus end-to-end `Store` vs email-seeded `SqlStore` `page_cases` and `detail` parity.

#### Boundaries

* Included:
  * Create `src/core/tests/test_hazard_safeguarding_clock_owner.py` with strict `mypy` annotations (zero `type: ignore` comments) testing:
    1. Every `itertools.permutations` ordering of `[Sam Example (RLO-01), Pam Lead (PM-01), Kim Builder (CON-1)]` when `case` has `owner_code="PM-01"` and `owner="Sam Example"` (verifying `escalation_owner == "Pam Lead"`, `escalation_owner_id == "PM-01"`, and identical `named_owner` whether direct hazard `owner="Bea"` is present or unallocated, plus whitespace-padded `code=" PM-01 "` normalization in `_match_staff`).
    2. Unallocated escalation role-scan fallback when multiple `Building Safety Liaison` / `Retrofit Programme Manager` staff members exist in reversed orders (`[BS-2, BS-1]` vs `[BS-1, BS-2]`).
    3. End-to-end `Store` vs `SqlStore` parity using `Any`-typed bindings (`store_cls: Any = Store`, `sql_store_cls: Any = SqlStore`, `reads_mod: Any = test_sqlreads`) where `Store` is seeded with `STAFF` in `[Sam, Pam, Kim]` order and `SqlStore` is seeded from a `sql_seed.json` whose `staff` array is sorted by `email` (`[kim@example.test, pam@example.test, sam@example.test]`), asserting `[m["email"] for m in sstore.data["staff"]]` is in `email` order and comparing `page_cases` (`all` and `mine`, including `queue` and `flag="hazard"` filters) and `detail` on `make_cases` data.
  * Run in `src/core`:
    * `python3 -m unittest discover -s tests -p "test_hazard_safeguarding_clock_owner.py" -v`
    * `python3 -m unittest discover -s tests -p "test_sqlreads.py" -v`
    * `mypy`
    * `ruff check src/zava_forward/core/taskqueues.py src/zava_forward/core/store.py tests/test_hazard_safeguarding_clock_owner.py && ruff format --check src/zava_forward/core/taskqueues.py tests/test_hazard_safeguarding_clock_owner.py`
    * `python3 -m unittest discover -s tests -q`
* Excluded: Adding `mypy` ignore overrides in `pyproject.toml`.

#### Likely Targets

* `src/core/tests/test_hazard_safeguarding_clock_owner.py`

#### Dependencies

* P01-T01 and P01-T02.

#### Validation Expectations

* All targeted and package-wide `src/core` tests, `mypy`, and `ruff` checks exit `0`.

#### Completion Evidence

* Green test, `mypy`, and `ruff` results recorded in `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-changes.md`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Verify diff boundaries, configure privacy-safe Git author, and reconcile changes for Review and local commit

#### Context

Repository governance (`.github/copilot-instructions.md`) and `NFR-3`/`AC-5` require configuring repository-local `user.email` from `gh api user` (`{id}+{login}@users.noreply.github.com`) and committing all code and `c1` RPI tracking artifacts (`research`, `plans`, `details`, `critique`, `changes`, `reviews`, and `state.json`) locally with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leaving `git status --short` empty without pushing or running `tools/rpi-checks.py`.

#### Intent

Ensure implementation handoff to `rpi-review` has verified scope boundaries, configured privacy-safe Git identity, and complete changes documentation so the post-`rpi-review` local commit captures every code and tracking artifact cleanly.

#### Boundaries

* Included:
  * Check `git diff origin/feat/demo-164-chat-grounding-provenance-0900 --name-status` to confirm zero `src/api/` changes beyond Cycle 0, zero test removals, and exactly one new test file (`src/core/tests/test_hazard_safeguarding_clock_owner.py`).
  * Resolve `gh api user` (`id` and `login`) and configure `git config --local user.email "{id}+{login}@users.noreply.github.com"`.
  * Persist `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-changes.md` and reconcile `[x]` checklist markers in `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md` before `rpi-review`.
  * After `rpi-review` writes `.copilot-tracking/reviews/logs/2026-11-15/ux-76-hazard-clock-owner-c1-review.md` and updates `ux-76-hazard-clock-owner-c1-state.json` to `Follow-up` (`completed`), stage all modified/created files and create one local commit with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, then verify `git status --short` is empty.
* Excluded: `git push` or `tools/rpi-checks.py`.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-changes.md`
* `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md`

#### Dependencies

* P02-T01 completed.

#### Validation Expectations

* `git config --local user.email` matches `{id}+{login}@users.noreply.github.com`; post-Review commit succeeds and `git status --short` is empty.

#### Completion Evidence

* Reconciled `changes.md`, `plan.md`, `review.md`, `state.json`, and clean `git status --short` on `feat/ux-76-hazard-clock-owner`.

#### Unresolved Items

* None.
