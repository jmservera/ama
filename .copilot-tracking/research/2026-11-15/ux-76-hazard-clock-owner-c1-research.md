<!-- markdownlint-disable-file -->

# Task Research: ux-76-hazard-clock-owner-c1

| Field              | Value                                                                          |
|--------------------|--------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                     |
| Researcher / agent | rpi-research (RPI Agent automatic mode)                                        |
| Status             | Complete                                                                       |
| Artifact path      | .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c1-research.md  |
| Planning Readiness | Ready                                                                          |
| Disposition        | executed                                                                       |

## Research Brief

* What to research: Investigate the exact root cause of the `MssqlParity.test_every_view_filter_sort_and_search_matches_the_in_memory_store` failure in GitHub Actions `mssql` job (`132694355150`) on PR #1768 (`5d4c80ee3`), verify the rebase interaction with `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`, after PR #1769 / Issue #83 merged), and verify every staff-roster iteration and queue-fingerprint path in `src/core/src/zava_forward/core/`.
* Why it matters: 325/326 tests passed in `mssql` CI on PR #1768, with 1 parity mismatch between `Store` (in-memory) and `MssqlStore` (SQL Server clustered primary key order on `staff.email`) when `case` has `owner_code="PM-01"` (`Pam Lead`) and `owner="Sam Example"`. In addition, PR #1769 (`#83`) merged into target base `feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`), introducing one 6-line conflict in `store.py` and also bumping `taskqueues.MEMBERSHIP_REVISION` to `4`.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` phases for Issue #76 Correction Cycle 1 (`ux-76-hazard-clock-owner-c1`).
* Scope: `src/core/src/zava_forward/core/taskqueues.py`, `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/sqlstore.py`, `src/core/src/zava_forward/core/mssqlstore.py`, `src/core/README.md`, `src/core/tests/test_sqlreads.py`, `src/core/tests/test_hazard_safeguarding_clock_owner.py`, `src/core/tests/test_hazard_safeguarding_clock_owner_76.py`, and `src/api/tests/test_mssqlstore.py`.
* Non-goals: Pushing to remote, running `tools/rpi-checks.py`, or touching unrelated web/API modules.
* Criteria: `project_safety_clock_and_owner` and `_match_staff` are 100% deterministic and invariant to `staff` sequence ordering; rebase onto `0c1fa1da4` preserves both `#83` (`handoff_view` policy/staff args) and `#76` (`staff=staff_list`) behavior plus queue-fingerprint invalidation; focused unit tests, `test_sqlreads.py`, and `mypy` pass cleanly.
* Requested outputs: Synthesized 3-wave evidence log, rebase conflict & `MEMBERSHIP_REVISION` audit, evaluation of alternatives, convergence recommendation, and planning readiness record.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                               |
|--------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Why did `MssqlParity` diverge from `Store` on `escalation_owner` (`Sam Example` vs `Pam Lead`), how does rebasing onto `0c1fa1da4` interact with `store.py` and `taskqueues.py`, and what changes make staff resolution completely order-independent across all engines? |
| Codebase scope                       | `src/core/`, `src/api/tests/test_mssqlstore.py`, `.copilot-tracking/*/2026-11-15/ux-76-hazard-clock-owner*`                          |
| External scope                       | none (caller-supplied CI failure evidence and local repository code)                                                                |
| Initial internal candidate areas     | `src/core/src/zava_forward/core/taskqueues.py`, `store.py`, `sqlstore.py`, `mssqlstore.py`; `src/core/tests/test_sqlreads.py`, `test_hazard_safeguarding_clock_owner_76.py`; `src/api/tests/test_mssqlstore.py` |
| Initial external candidate areas     | none                                                                                                                                |
| Research posture                     | focused                                                                                                                             |
| Posture provenance                   | default (bounded correction cycle with exact CI traceback and named target modules)                                                 |
| Explicit limits / deadline           | Focused validation tier (`src/core` unit tests + `test_sqlreads.py` + `mypy`); commit locally without pushing or running `rpi-checks.py` |
| Posture-specific completion basis    | Complete root-cause trace, full scan of `staff` iteration sites and rebase touchpoints, and contrarian verification of tests/typing |
| Edits allowed during research?       | no, research-only                                                                                                                   |
| Resolved evidence root               | `.copilot-tracking/` default                                                                                                        |
| Known constraints / excluded sources | Preserve historical `ux-76-hazard-clock-owner-*` cycle-0 artifacts untouched; record Correction Cycle 1 in `-c1` artifacts          |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                         | Match and provenance                                           | Scoped authority or output contract                            | Selected / skipped reason                                                                   |
|---------------------|-----------------------------------|----------------------------------------------------------------|----------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` matches workspace files and tracking artifacts | Validation-tier rules, commit conventions, RPI preservation    | Selected automatically as repository-wide instruction                                       |
| Skill               | `web-design-guidelines`           | Web UI changes only                                            | Pre-edit and review checklist for web files                    | Skipped: Correction Cycle 1 is backend `src/core` and `src/core/tests` only (no web edits) |
| Research specialist | `hve-core-all:rpi-researcher`     | Registered general RPI research lane worker                    | Independent subagent lane artifact                             | Skipped: single tight trace across 5 files fits direct inline inspection cleanly            |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                        | Answers / unanswered | Resulting decision or selected further research       |
|------------------|----------------------------------------------------------------------------------------------|----------------------|-------------------------------------------------------|
| Intake           | Non-interactive session with complete CI failure traceback, rebase target, and validation spec | N/A (non-interactive)| Proceed with `focused` posture and `convergence` mode |
| Convergence      | All questions answered with direct `path:line` evidence                                      | N/A                  | Converge on Option A and advance to `rpi-plan`        |

## Scope and Success Criteria

* Scope: Rebase diff against `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`), staff matching and fallback resolution in `taskqueues.py`, test path expectations in `src/core/tests/`, and `mypy` strictness configuration in `src/core/pyproject.toml`.
* Success criteria:
  * Exact divergence mechanism between `Store`/`SqlStore` (SQLite) and `MssqlStore` (SQL Server) proven with `path:line` evidence.
  * Every `staff` / `roster` iteration site in `taskqueues.py`, `store.py`, and `workflows.py` audited for order sensitivity.
  * Rebase conflicts and semantic overlaps with `#83` (`0c1fa1da4`) identified.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  * Verify rebase conflict in `src/core/src/zava_forward/core/store.py` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`).
  * Confirm root cause in `_match_staff` and `project_safety_clock_and_owner` (`src/core/src/zava_forward/core/taskqueues.py`) causing `MssqlParity.test_every_view_filter_sort_and_search_matches_the_in_memory_store` to fail.
  * Confirm unit-test file layout (`test_hazard_safeguarding_clock_owner.py` vs `test_hazard_safeguarding_clock_owner_76.py`) and `mypy` strict-typing rules in `src/core`.

## Direction Controls

| Control type | Direction or boundary                                                                                      | Source / checkpoint | Effect on active brief, evidence, or revalidation                            |
|--------------|------------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------|
| narrow       | Fix `MssqlParity` staff-ordering sensitivity and rebase `feat/ux-76-hazard-clock-owner` onto `0c1fa1da4`   | Caller intake brief | Scopes changes to `store.py` (conflict resolution), `taskqueues.py`, `README.md`, and `src/core/tests/` |
| exclude      | Do not push and do not run `tools/rpi-checks.py`                                                           | Caller intake brief | Restricts validation to focused local `unittest` + `mypy` commands           |

## Research Questions

|  # | Sub-question                                                                                                                     | Type    | Priority | Status   |
|---:|----------------------------------------------------------------------------------------------------------------------------------|---------|----------|----------|
| Q1 | Why did `MssqlParity` produce `'escalation_owner': 'Pam Lead'` while `Store` and SQLite `Parity` produced `'Sam Example'`?       | depth   | H        | answered |
| Q2 | Are there any other `staff` / `roster` iteration sites in `taskqueues.py`, `workflows.py`, or `store.py` sensitive to row order? | breadth | H        | answered |
| Q3 | What syntactic and semantic overlaps exist when rebasing `5d4c80ee3` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`)? | depth | H | answered |
| Q4 | How are `test_hazard_safeguarding_clock_owner*.py` and `mypy` configured in `src/core`?                                          | contrarian | M     | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/rpi-sessions/2026-11-15/ux-76-hazard-clock-owner-state.json` and `.copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-research.md`, plus `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, and `docs/reference/memory.md`.
* Reused findings: `project_safety_clock_and_owner` in `taskqueues.py` is the single shared projection helper for `work["hazard_clocks"]`, `workflows.hazard_view`, `workflows.safeguarding_view`, and `Store._open_safety_items`.
* Note on branch name: The checked-out branch for PR #1768 at `5d4c80ee3` in worktree `/home/azureuser/source/ama-demo-wt/feat-76-hazard-clock-owner` is `feat/ux-76-hazard-clock-owner` targeting `feat/demo-164-chat-grounding-provenance-0900` (`gh pr view 1768`).

## Cycle 1 Execution (Wider, Deeper, Contrarian)

### Wave 1: Wider (Engine Storage Order and Rebase Surface)

* Engine row-ordering difference (`C1`, `C2`, `C3`, `C4`):
  * `MssqlParity` (`src/api/tests/test_mssqlstore.py:621`) subclasses `reads.Parity` (`src/core/tests/test_sqlreads.py:59`) and substitutes `MssqlStore` for `SqlStore` (`C1`, `C2`).
  * `MssqlStore` creates `staff` with `CREATE TABLE staff (email NVARCHAR(200) COLLATE Latin1_General_100_BIN2 PRIMARY KEY, body NVARCHAR(MAX) NOT NULL)` (`src/core/src/zava_forward/core/mssqlstore.py:31`). In SQL Server, `PRIMARY KEY` defaults to `CLUSTERED`, so `SELECT body FROM staff` in `SqlStore._sync` (`src/core/src/zava_forward/core/sqlstore.py:1028`) returns rows sorted by `email`: `[kim@example.test (CON-1), pam@example.test (PM-01), sam@example.test (RLO-01)]` (`C3`, `C4`).
  * In `Store` (in-memory JSON seed) and SQLite (`rowid` insertion order), `STAFF` (`src/core/tests/test_sqlreads.py:21-23`) is ordered `[Sam Example (RLO-01), Pam Lead (PM-01), Kim Builder (CON-1)]` (`C2`).
* Upstream base diff (`02ab20cac..0c1fa1da4`) (`C5`, `C6`):
  * Target branch `origin/feat/demo-164-chat-grounding-provenance-0900` advanced from `02ab20cac` to `0c1fa1da4`, merging Issue #83 (`PR #1769`) and Issue #164 updates.
  * In `src/core/src/zava_forward/core/store.py:445-456` (`Store._work_context`), `#83` changed `handoff=handoff_view(c)` to `handoff=handoff_view(c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff"))`, while `#76` changed the same line to `handoff=handoff_view(c), staff=staff_list` — producing the single 6-line merge conflict (`C5`).
  * Notice also in `sqlstore.py:796-799` on `0c1fa1da4`, `#83` populates transaction-local `data["staff"]` via `SELECT body FROM staff ORDER BY email`, which sorts by `email` even in SQLite during `_refresh_queue_membership` (`C6`).

### Wave 2: Deeper (Exact Divergence Trace in `taskqueues.py`)

* `make_cases` mixed `owner` / `owner_code` fixture (`C2`, `C7`, `C8`):
  * `make_cases` (`src/core/tests/test_sqlreads.py:29-40`) creates cases with `fixtures.case(f"ZF-{i:05d}", owner_code=rnd.choice(["RLO-01", "PM-01"]), ...)`, where `c["owner"]` remains the default `"Sam Example"` and `c["owner_role"]` remains `"Resident Liaison Officer"` even when `c["owner_code"] == "PM-01"`, and attaches `c["hazards"] = [dict(category="Damp", priority="P1", ..., owner="Bea")]` to ~5% of cases (`C2`).
  * For those hazard items, `project_safety_clock_and_owner` (`src/core/src/zava_forward/core/taskqueues.py:338-344`) resolves `escalation` from `case_map.get("owner")` (`"Sam Example"`) with `explicit_code=case_map.get("owner_code")` (`"PM-01"`), calling `_resolve_person` -> `_match_staff(code="PM-01", email=None, name="Sam Example", staff=staff)` (`C7`, `C8`).
  * `_match_staff` (`src/core/src/zava_forward/core/taskqueues.py:224-243`) loops once `for member in staff:` checking `code`, `email`, and `name` per member (`C7`):
    * Under `[Sam (RLO-01), Pam (PM-01), Kim (CON-1)]`, member 0 (`Sam`) fails `m_code == "PM-01"` but matches `m_name == "sam example"`, returning `Sam Example`!
    * Under `[Kim (CON-1), Pam (PM-01), Sam (RLO-01)]` (SQL Server clustered PK `email` order), member 1 (`Pam`) matches `m_code == "PM-01"`, returning `Pam Lead`!
* Second order-sensitive loop in `project_safety_clock_and_owner` (`C9`):
  * Lines `345-361` of `src/core/src/zava_forward/core/taskqueues.py` fall back to scanning `for member in roster:` for `target_role` when `destination` and `case["owner"]` are both unrecorded. If two staff members hold the same `target_role`, raw `roster` iteration order would depend on SQL Server `email` order vs JSON insertion order unless `roster` is sorted deterministically (`sorted(roster, key=lambda m: str(m.get("code") or m.get("email") or m.get("name") or ""))`) (`C9`).

### Wave 3: Contrarian (Semantic Overlaps, Duplicate-Key Edge Cases, and Test/Mypy Discovery)

* Contrarian check 1 — `MEMBERSHIP_REVISION` collision with `#83` (`C6`, `C10`):
  * Both `#83` (`0c1fa1da4`) and `#76` (`5d4c80ee3`) incremented `MEMBERSHIP_REVISION` from `3` to `4` (`src/core/src/zava_forward/core/taskqueues.py:8`). Git rebase auto-merges identical changes to `4`, meaning a SQL database already migrated under `#83` (`MEMBERSHIP_REVISION = 4`) would share the same revision number unless bumped to `5`. Grepping both branches confirms no test pins `MEMBERSHIP_REVISION == 4` (`test_hazard_safeguarding_clock_owner_76.py:293` writes `'stale-revision-3'` and asserts rebuild). Bumping `MEMBERSHIP_REVISION = 5` (and updating `src/core/README.md:12`) guarantees deterministic queue-flag rebuild on top of `#83` (`C6`, `C10`).
* Contrarian check 2 — Duplicate name/email tie-breaking in `_match_staff` (`C7`):
  * Checking `code` across all `staff` first, then `email` across all `staff`, then `name` across all `staff` eliminates cross-field order sensitivity (`code` always beats `email`, which always beats `name`). Furthermore, iterating over `ordered_staff = sorted(staff, key=lambda m: (str(m.get("code") or m.get("oid") or "").strip(), str(m.get("email") or "").strip().lower(), str(m.get("name") or "").strip().lower()))` inside `_match_staff` ensures even contrived duplicate-name fixtures with distinct codes/emails cannot vary by input list permutation (`C7`). Roster size is tiny (~3-15 entries) and only runs on open safety items, adding negligible overhead to 60,000-case benchmarks.
* Contrarian check 3 — Unit-test filename and `mypy --strict` coverage (`C11`, `C12`):
  * Cycle 0 created `src/core/tests/test_hazard_safeguarding_clock_owner_76.py` (`C11`), whereas the caller validation script runs `python3 -m unittest discover -s tests -p "test_hazard_safeguarding_clock_owner.py" -v` as well as full `unittest discover -s tests -q`. Without `src/core/tests/test_hazard_safeguarding_clock_owner.py`, `unittest discover -p "test_hazard_safeguarding_clock_owner.py"` would execute `0` tests! Creating `src/core/tests/test_hazard_safeguarding_clock_owner.py` with full type annotations (since `pyproject.toml:34-39` runs `mypy` with `strict = true` across `files = ["src", "tests"]` unless overridden) ensures both the targeted `-p "test_hazard_safeguarding_clock_owner.py"` run and `mypy` validate the new regression suite (`C11`, `C12`).

## Evidence Log

| ID  | Source (`path:line`)                                                          | Finding                                                                                                                               |
|-----|-------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| C1  | `src/api/tests/test_mssqlstore.py:621`                                        | `MssqlParity` inherits `reads.Parity` (`test_sqlreads.py`) and swaps `reads.SqlStore` to `MssqlStore`.                                |
| C2  | `src/core/tests/test_sqlreads.py:21`                                          | `STAFF` is ordered `[Sam (RLO-01), Pam (PM-01), Kim (CON-1)]`; `make_cases` (`line 29`) sets `owner_code="PM-01"` while keeping default `owner="Sam Example"`. |
| C3  | `src/core/src/zava_forward/core/mssqlstore.py:31`                             | `staff` table has `email ... PRIMARY KEY` (clustered PK in SQL Server), ordering un-ordered scans by `email` (`kim`, `pam`, `sam`).    |
| C4  | `src/core/src/zava_forward/core/sqlstore.py:1028`                             | `SqlStore._sync` loads `self.data["staff"]` via `SELECT body FROM staff`, yielding insertion order in SQLite vs `email` order in SQL Server. |
| C5  | `src/core/src/zava_forward/core/store.py:445`                                 | `Store._work_context` conflicts on `handoff=handoff_view(...)` (`#83`) vs `handoff=handoff_view(c), staff=staff_list` (`#76`).        |
| C6  | `src/core/src/zava_forward/core/sqlstore.py:761`                              | On `0c1fa1da4`, `#83` also bumped `taskqueues.MEMBERSHIP_REVISION` to `4` and added `handoff_policy` to `_queue_fingerprint`.         |
| C7  | `src/core/src/zava_forward/core/taskqueues.py:224`                            | `_match_staff` checks `code`, `email`, and `name` per member in a single loop over `staff`, making mixed `code`+`name` resolution depend on `staff` row order. |
| C8  | `src/core/src/zava_forward/core/taskqueues.py:338`                            | `project_safety_clock_and_owner` passes `case_map.get("owner")` with `explicit_code=case_map.get("owner_code")` to `_resolve_person`. |
| C9  | `src/core/src/zava_forward/core/taskqueues.py:345`                            | Role-based escalation fallback iterates `for member in roster:` in raw input order rather than deterministic sorted key order.        |
| C10 | `src/core/README.md:12`                                                       | Documents `MEMBERSHIP_REVISION` for `#76` safety clock/owner queue projection.                                                        |
| C11 | `src/core/tests/test_hazard_safeguarding_clock_owner_76.py:1`                 | Existing `#76` core tests live in `test_hazard_safeguarding_clock_owner_76.py`; `test_hazard_safeguarding_clock_owner.py` does not yet exist. |
| C12 | `src/core/pyproject.toml:34`                                                  | `mypy` runs with `strict = true` on `files = ["src", "tests"]`, requiring complete type annotations on new test modules not listed in `ignore_errors`. |

## Synthesis and Evaluation of Alternatives

### Alternatives Compared

| Option | Summary | Pros | Cons | Disposition |
|--------|---------|------|------|-------------|
| Option A (Selected) | Rebase onto `0c1fa1da4` keeping both `#83` and `#76` arguments in `store.py`; rewrite `_match_staff` to run precedence passes (`code` across all staff, then `email`, then `name`) over canonically sorted `staff` and sort `roster` in `project_safety_clock_and_owner` role fallback; bump `MEMBERSHIP_REVISION = 5`; add strictly typed unit tests in `src/core/tests/test_hazard_safeguarding_clock_owner.py` | Fixes `MssqlParity` root cause in the domain logic regardless of caller/store; preserves `#83` + `#76` rebase semantics and DB migration; satisfies exact `-p "test_hazard_safeguarding_clock_owner.py"` selector and `mypy --strict` | Touching `MEMBERSHIP_REVISION` requires one-line doc sync in `src/core/README.md` | Selected (`C1`–`C12`) |
| Option B | Add `ORDER BY` only in `SqlStore._sync` (`SELECT body FROM staff ORDER BY email`) without fixing `_match_staff` | One-line SQL change | Leaves `Store` (JSON insertion order) diverging from `SqlStore`/`MssqlStore` (`email` order), breaking SQLite `Parity` too! | Rejected (`C2`, `C4`, `C7`) |
| Option C | Change `make_cases` in `test_sqlreads.py` so `owner` matches `owner_code` | Masks test failure | Masks real production non-determinism when a legacy case's display `owner` name lags `owner_code` or when two staff share a fallback role | Rejected (`C7`, `C9`) |

### Selected Convergence Recommendation

Proceed with **Option A**:
1. Rebase `feat/ux-76-hazard-clock-owner` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`), resolving `src/core/src/zava_forward/core/store.py` (`_work_context`) to pass both `handoff=handoff_view(c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff"))` and `staff=staff_list`.
2. In `src/core/src/zava_forward/core/taskqueues.py`:
   * Update `_match_staff` to check `code` across all `staff` first, then `email` across all `staff`, then `name` across all `staff` (iterating over `staff` sorted by `(code/oid, email, name)` so even duplicate-name ties are permutation-invariant).
   * In `project_safety_clock_and_owner`, iterate over `sorted(roster, key=lambda m: str(m.get("code") or m.get("email") or m.get("name") or ""))` in the `target_role` escalation fallback loop.
   * Bump `MEMBERSHIP_REVISION = 5` (and sync `src/core/README.md`) so databases already at `#83`'s `MEMBERSHIP_REVISION = 4` rebuild `#76` queue flags.
3. Add `src/core/tests/test_hazard_safeguarding_clock_owner.py` (strictly typed for `mypy`) testing permutation invariance of `project_safety_clock_and_owner`, `_match_staff`, `Store.page_cases`, and `SqlStore.page_cases` across all permutations of `STAFF` (including `owner_code="PM-01"` + `owner="Sam Example"` and duplicate-role rosters).

## Risks, Open Questions, and Potential Further Research

* Open questions: None (`Q1`–`Q4` answered).
* Residual risks:
  * Local validation runs SQLite `test_sqlreads.py` and permutation parity tests; real SQL Server container (`MssqlParity` with `ZF_TEST_MSSQL=1`) runs in hosted GitHub Actions `mssql` CI after push. Because the exact `MssqlStore` difference was `self.data["staff"]` ordered `[Kim, Pam, Sam]` vs `[Sam, Pam, Kim]`, explicitly testing both orders (and all `itertools.permutations`) in `test_hazard_safeguarding_clock_owner.py` directly reproduces and verifies the exact `MssqlParity` scenario locally.

## Planning Readiness and Handoff

* Research execution status: Complete (1 full Wider -> Deeper -> Contrarian cycle).
* Research disposition: `executed`
* Planning Readiness: `Ready`
* Self-check:
  * All questions `Q1`–`Q4` answered with `C1`–`C12` `path:line` evidence: pass.
  * Research-only constraint honored (zero tracked source files modified during Research): pass.
  * Ready for parent RPI Agent automatic transition to `rpi-plan`.
