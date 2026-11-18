<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #76 Correction Cycle 1 (PR #1768 `mssql` CI Parity Fix and Rebase onto `#1641`)

## Metadata

* Task ID: issue-76-c1
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Execute Correction Cycle 1 (`issue-76-c1` / `ux-76-hazard-clock-owner-c1`) on `feat/ux-76-hazard-clock-owner` (`5d4c80ee3`) targeting `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`, PR #1641 after PR #1769 / Issue #83 merged): (1) Step 0 rebase onto `0c1fa1da4` keeping both `#83`'s `handoff=handoff_view(c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff"))` and `#76`'s `staff=staff_list` in `Store._work_context`; (2) fix the `MssqlParity.test_every_view_filter_sort_and_search_matches_the_in_memory_store` failure on PR #1768 by updating `_match_staff` (`code` pass -> `email` pass -> `name` pass) and `project_safety_clock_and_owner` (`sorted(roster, ...)` for `target_role`) in `src/core/src/zava_forward/core/taskqueues.py`, plus `MEMBERSHIP_REVISION = 5`; (3) add strictly typed unit tests in `src/core/tests/test_hazard_safeguarding_clock_owner.py` verifying identical `named_owner` and `escalation_owner` across `staff` orderings (including `owner_code="PM-01"` and `owner="Sam Example"` under `[Sam, Pam, Kim]` vs `[Kim, Pam, Sam]`); (4) run focused-tier validation (`test_hazard_safeguarding_clock_owner.py`, `test_sqlreads.py`, `mypy`, and full `unittest discover -s tests -q` in `src/core`), commit locally with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leave `git status --short` empty, and do not push or run `tools/rpi-checks.py`.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c1-research.md, .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md, .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md, .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md, src/core/src/zava_forward/core/taskqueues.py, src/core/src/zava_forward/core/store.py, src/core/src/zava_forward/core/sqlstore.py, src/core/src/zava_forward/core/mssqlstore.py, src/core/src/zava_forward/core/workflows.py, src/core/pyproject.toml, src/core/README.md, src/core/tests/dataset.py, src/core/tests/test_sqlreads.py, src/core/tests/test_hazard_safeguarding_clock_owner_76.py, and read-only Git 3-way merge inspection against `0c1fa1da4` (`store.py`, `sqlstore.py`, `taskqueues.py`, `workflows.py`, `test_handoff_escalation_83.py`).
* Decisions, dependencies, and acceptance criteria considered: FR-1 through FR-4, NFR-1 through NFR-3, AC-1 through AC-5, research citations C1 through C12, repository commit-author rules in .github/copilot-instructions.md, and focused validation tier rules (`D4` / `#1294`).
* Assessment boundary: Evaluates completeness, rebase safety, codebase contract compatibility, static-typing rules, and closeout sequencing across `P01` (`P01-T01`, `P01-T02`) and `P02` (`P02-T01`) from supplied repository evidence without mutating tracked files or running hosted SQL Server containers.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1, AC-1 / C5, C6, C10 | Covered | Read-only 3-way merge check confirms `src/core/src/zava_forward/core/store.py` (`Store._work_context`) is the sole conflict replaying `5d4c80ee3` onto `0c1fa1da4`, and no test on `0c1fa1da4` or `HEAD` pins `MEMBERSHIP_REVISION == 4`. Note `AC-1` should also be listed in `P01-T01` / `P01-T02` task headers (`PC-002`). |
| FR-2, AC-2 / C7, C8 | Partial | Three-pass precedence (`code` -> `email` -> `name`) over canonically sorted `staff` fixes the `MssqlParity` mismatch, but `P01-T02` compares `m_code == code` without `.strip()` on `code` when `_match_staff` is called directly (`PC-003`). |
| FR-3, AC-2 / C9 | Covered | Sorting `roster` by `str(m.get("code") or m.get("email") or m.get("name") or "")` in `project_safety_clock_and_owner` satisfies caller requirement #2 and removes fallback scan order sensitivity across duplicate-role rosters. |
| FR-4, NFR-1, NFR-2, AC-3, AC-4 / C1-C4, C11, C12 | Partial | `P02-T01` creates `src/core/tests/test_hazard_safeguarding_clock_owner.py` without `pyproject.toml` overrides, but omits required `Any`-typed call bindings for untyped `Store`, `SqlStore`, and `test_sqlreads.make_cases`/`dataset` under `mypy` `disallow_untyped_calls = true`, and describes post-init `SqlStore.data["staff"]` reordering instead of seeding `SqlStore` with email-ordered `staff` so `_seed`/`_refresh_queue_membership` and `_sync` both mirror `MssqlStore` (`PC-001`). |
| NFR-3, AC-5 | Partial | Requirements define local privacy-safe Git commit and clean-worktree closeout across all `c1` artifacts, but neither `Phase Checklist` nor `Phase Details` includes a task or stage-ordered closeout step mapping `NFR-3` and `AC-5` (`PC-002`). |
| P01 / P01-T01 | Covered | Clean single-commit rebase onto `0c1fa1da4` and exact `Store._work_context` conflict resolution preserving `#83` and `#76` arguments. |
| P01 / P01-T02 | Partial | Needs `code.strip()` normalization in `_match_staff` Pass 1 (`PC-003`) and `AC-1`/`AC-2` traceability in the plan task checklist (`PC-002`). |
| P02 / P02-T01 | Partial | Needs `Any`-typed wrapper guidance for untyped `Store`, `SqlStore`, and `test_sqlreads` helpers under strict `mypy` plus email-ordered `sql_seed` initialization (`PC-001`), and a closeout commit task/step covering `NFR-3` and `AC-5` (`PC-002`). |

## Verdict

* Verdict: Revise
* Rationale: Root-cause analysis, rebase conflict resolution onto `0c1fa1da4`, `MEMBERSHIP_REVISION = 5` separation from `#83`, and the multi-pass `_match_staff` / sorted-`roster` algorithm are accurate and verified against the codebase. Two Medium findings (`PC-001`, `PC-002`) and one Low finding (`PC-003`) warrant a direct one-pass planner revision before implementation: `P02-T01` must account for `mypy` `disallow_untyped_calls = true` when invoking untyped `Store`, `SqlStore`, and `test_sqlreads` helpers (and seed `SqlStore` with email-ordered `staff` so `_seed`, `_refresh_queue_membership`, and `_sync` all execute in SQL Server PK order), `P02` needs an explicit closeout task/step mapping `NFR-3`, `AC-1`, and `AC-5` (including `gh api user` noreply email setup and post-review final commit sequencing), and `_match_staff` Pass 1 should normalize `code.strip()` consistently with `email` and `name`. All findings are direct planner corrections requiring no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: P02-T01 omits strict-mypy untyped-call handling for Store, SqlStore, and test_sqlreads helpers and only reorders SqlStore.data["staff"] after initialization

* Related IDs: FR-4, NFR-1, AC-3, AC-4, P02, P02-T01, C3, C4, C6, C11, C12
* Evidence: src/core/pyproject.toml lines 34-61; src/core/tests/test_sqlreads.py lines 29, 48; src/core/tests/test_hazard_safeguarding_clock_owner_76.py lines 256-259; src/core/src/zava_forward/core/sqlstore.py lines 206-210, 796-799, 869-880, 1028-1031; .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md (`P02-T01`)
* Concern:
  1. `src/core/pyproject.toml` sets `strict = true` (which enables `disallow_untyped_calls = true` and `warn_return_any = true`) across `files = ["src", "tests"]`. Because `zava_forward.core.store`, `zava_forward.core.sqlstore`, and `test_sqlreads` are untyped modules listed under `ignore_errors = true`, while `test_hazard_safeguarding_clock_owner.py` has no `[[tool.mypy.overrides]]` entry (`P02-T01` excludes editing `pyproject.toml`), calling `Store(...)`, `SqlStore(...)`, `test_sqlreads.make_cases(...)`, or `test_sqlreads.dataset(...)` directly in `test_hazard_safeguarding_clock_owner.py` fails `mypy` with `[no-untyped-call]` unless invoked via `Any`-typed bindings (`store_cls: Any = Store`, `sql_store_cls: Any = SqlStore`, `reads_mod: Any = test_sqlreads`), as done in `src/core/tests/test_hazard_safeguarding_clock_owner_76.py` lines 256-259.
  2. `P02-T01` item 3 specifies parity *"when `SqlStore.data["staff"]` is reordered into SQL Server clustered PK `email` order"*, whereas `SqlStore._initialize` runs `_seed(data_path)` -> `_refresh_queue_membership()` and `_sync()` (populating both `self.staff` and `self.data["staff"]`) during `__init__`. Seeding `SqlStore` from a `sql_seed.json` whose `staff` array is sorted by `email` (`[kim@example.test, pam@example.test, sam@example.test]`) while `Store` seeds `[Sam, Pam, Kim]` exercises SQL Server's clustered-PK `email` row order across initial seeding, queue-membership computation, `_sync()`, and `page_cases` (`all` and `mine`, including `focus` and queue filters), rather than mutating `sstore.data["staff"]` only after construction.
* Impact: Without `Any`-typed call bindings for untyped test/store collaborators, `mypy` fails `NFR-1`/`AC-4` during implementation; without email-ordered seed initialization, `SqlStore._seed` and `SqlStore.staff` remain in `[Sam, Pam, Kim]` order during initial queue indexing.
* Smallest useful change: Update `P02-T01` in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md to specify calling untyped `Store`, `SqlStore`, and `test_sqlreads` (`make_cases`, `dataset`) through `Any`-typed bindings (`store_cls: Any = Store`, `sql_store_cls: Any = SqlStore`, `reads_mod: Any = test_sqlreads`) without `type: ignore` or `pyproject.toml` edits, and seeding `SqlStore` with `staff` sorted by `email` (`[Kim, Pam, Sam]`) while `Store` uses `[Sam, Pam, Kim]` (asserting `sstore.data["staff"]` is in `email` order and comparing `page_cases` across `all` and `mine` views, including `queue` and `flag="hazard"` filters, plus `detail`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `P02-T01` detail section in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md specifying `Any`-typed call wrappers for untyped collaborators and email-ordered `sql_seed` parity testing.
* Decision route: Direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Phase Checklist and Phase Details omit a closeout task mapping NFR-3, AC-1, and AC-5 for local Git commit and post-review clean worktree state

* Related IDs: NFR-3, AC-1, AC-5, P01-T01, P01-T02, P02
* Evidence: .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md (`NFR-3`, `AC-1`, `AC-5`, `Phase Checklist`); .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md (`P01-T01`, `P01-T02`, `P02-T01`); .github/copilot-instructions.md (`Branch and Pull Request Workflow`)
* Concern: `NFR-3` and `AC-5` require configuring repository-local `user.email` as `{id}+{login}@users.noreply.github.com` from `gh api user`, committing all Correction Cycle 1 code and `.copilot-tracking/` artifacts (`research`, `plans`, `details`, `critique`, `changes`, `reviews`, and session `state.json`) locally with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leaving `git status --short` empty, and not pushing to `origin`. However, `P02` ends at `P02-T01` (running unit tests, `mypy`, and `ruff`), leaving `NFR-3`, `AC-1`, and `AC-5` unreferenced in task headers and providing no task for diff-boundary verification, commit-author setup, or commit coordination with `rpi-review` (which writes the `reviews` log and final `state.json` after `rpi-implement`).
* Impact: Executing `P01-T01` through `P02-T01` literally stops before configuring local Git author metadata or committing changes, or creates ambiguity between `rpi-implement` closeout and `rpi-review` artifact persistence required by `AC-5`.
* Smallest useful change: Map `AC-1` to `P01-T01`/`P01-T02` and add `P02-T02` in .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md and .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md covering `NFR-3` and `AC-5`: verify `git diff --name-status` (0 test removals, 1 new test file `src/core/tests/test_hazard_safeguarding_clock_owner.py`, no `src/api/` edits), configure repository-local `user.email` via `gh api user` (`{id}+{login}@users.noreply.github.com`), record `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-changes.md`, and define commit sequencing so implementation + tracking artifacts (and final post-`rpi-review` review/state artifacts) are committed locally with `Refs #76` and the Copilot trailer, leaving `git status --short` empty with zero `git push` or `tools/rpi-checks.py` execution.
* Action owner: planning_parent
* Exact resolving evidence: `AC-1` added to `P01-T01`/`P01-T02` and `P02-T02` added to .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md and .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md mapping `NFR-3` and `AC-5`.
* Decision route: Direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: _match_staff Pass 1 in P01-T02 does not strip whitespace on the input code parameter

* Related IDs: FR-2, AC-2, P01-T02, C7
* Evidence: .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md (`P01-T02` Boundaries); src/core/src/zava_forward/core/taskqueues.py lines 200-220
* Concern: `P01-T02` strips `m_code` (`str(m.get("code") or m.get("oid") or "").strip()`), `email` (`email.strip().lower()`), and `name` (`name.strip().lower()`), but specifies Pass 1 as `If code: match m_code == code` without stripping `code`. While `_resolve_person` strips `raw_code` via `_clean_name`, `FR-2` explicitly specifies direct `_match_staff` calls in acceptance criteria and unit tests, where surrounding whitespace (e.g., `code=" PM-01 "`) or whitespace-only `code="   "` would fail to match Pass 1 if unstripped.
* Impact: Direct callers of `_match_staff(code=..., ...)` with incidental leading/trailing whitespace miss the `code` precedence pass.
* Smallest useful change: Specify `code_clean = code.strip() if code else None` in `P01-T02` (`.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md`) and match `if code_clean and m_code == code_clean:` on Pass 1, mirroring `email_low` and `name_low`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T02` Pass 1 rule in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md normalizing `code.strip()`.
* Decision route: Direct planner correction

## Strengths and Residual Risk

* Exact root-cause and rebase verification: Read-only 3-way merge inspection against `0c1fa1da4` confirms `5d4c80ee3` is the single commit above merge-base `02ab20cac`, `src/core/src/zava_forward/core/store.py` (`Store._work_context`) is the sole merge conflict across all touched files, `#83` (`test_handoff_escalation_83.py`) does not pin `MEMBERSHIP_REVISION == 4`, and every `#76` safety projection call site (`taskqueues.context`, `Store._open_safety_items`, `Store.focus`, `Store.detail`, `workflows.hazard_view`, `workflows.safeguarding_view`, `WorkflowMixin.hazard_states`) delegates through `project_safety_clock_and_owner`.
* Complete staff-order invariance: Combining canonical `(code/oid, email, name)` ordering with three field-precedence passes (`code` -> `email` -> `name`) in `_match_staff` plus sorted `roster` iteration in `project_safety_clock_and_owner` eliminates both cross-field conflict sensitivity (`owner_code="PM-01"` with `owner="Sam Example"`) and duplicate-role/duplicate-name ordering ties.
* Accepted residual risk: Hosted SQL Server container execution (`MssqlParity` with `ZF_TEST_MSSQL=1`) runs in GitHub Actions after owner-authorized push rather than in local focused-tier `src/core` validation; testing all `itertools.permutations` of `STAFF` plus email-ordered `SqlStore` vs seed-ordered `Store` on `make_cases` deterministically reproduces the exact clustered-PK row-order mechanism locally.

## Questions or Blocking Evidence Gaps

* None. All three findings (`PC-001` through `PC-003`) are resolved directly from caller instructions and repository contracts without user input.

## Limitations

* Critique performed via read-only inspection of tracking artifacts, `src/core` source/test modules, and Git commit/merge-tree objects (`02ab20cac`, `5d4c80ee3`, `0c1fa1da4`) without modifying source files or executing mutating Git commands.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply direct planner revisions for `PC-001`, `PC-002`, and `PC-003` to .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md and .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md, finalize planning status without a second critique pass, and advance to `rpi-implement`.
* User response required: No
