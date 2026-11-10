<!-- markdownlint-disable-file -->

# Task Research: chat-schema-sql-selector-1298

| Field              | Value                                                                              |
|--------------------|------------------------------------------------------------------------------------|
| Date               | 2026-11-09                                                                         |
| Researcher / agent | rpi-research (inline, no delegated lane)                                           |
| Status             | Complete                                                                           |
| Artifact path      | .copilot-tracking/research/2026-11-09/chat-schema-sql-selector-1298-research.md   |

## Research Brief

* What to research: why a `chatthreads.py`-only change does not select the local `mssql` group although the sensor MSSQL fixture initializes the SQL chat schema, and the smallest fail-closed selector change for issue #1298.
* Why it matters: `project-core` discovery tolerates the ten retained-sensor opt-in skips on the expectation that the `mssql` group runs them; a partial `--changed` selection that omits `mssql` silently drops that execution.
* Audience or intended use: the plan and implementation phases of this fresh prospective attempt, the independent reviewer and the coordinator.
* Scope: `tools/rpi-checks.py` selector and `tools/test_rpi_checks.py` regression; read-only inspection of `src/core` import evidence; the `src/README.md` coverage statement as a directly related document.
* Non-goals: transitive dependency closure, expanded SQL matrix, source migration, `rpi-checks --all`, the sibling #184 ten-test integration, any change to the old branch `fix/chat-schema-sql-gate-1298` (`fef352e0`).
* Criteria: each claim carries a `C#` codebase evidence ID with `path:line`; no exhaustive-coverage claim.
* Requested outputs: analysis with a convergence recommendation bounded to the issue.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                          |
|--------------------------------------|------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1 to Q6 below                                                                                 |
| Codebase scope                       | `tools/rpi-checks.py`, `tools/test_rpi_checks.py`, `src/core/src/zava_forward/core/{chatthreads,mssqlstore,sqlstore}.py`, `src/core/tests/sensor_consumer_fixture.py`, `src/README.md` |
| External scope                       | none; GitHub issue #1298, #1297 and PR #1299 read through `gh` as data                        |
| Initial internal candidate areas     | `SENSOR_MSSQL_DIRECT_DEPENDENCIES`, `changed_groups`, existing sensor selector tests           |
| Initial external candidate areas     | none                                                                                           |
| Research posture                     | focused                                                                                        |
| Posture provenance                   | caller-specified bounded scope with named source targets and supplied failure evidence         |
| Explicit limits / deadline           | demo before 2026-11-16; source bounded to the two tool files; no exhaustive claim             |
| Posture-specific completion basis    | scope and materiality: stop when the demonstrated dependency and its fail-closed fix are evidenced |
| Edits allowed during research?       | no, research-only                                                                              |
| Resolved evidence root               | .copilot-tracking/ in this worktree                                                            |
| Known constraints / excluded sources | no private data, no live SQL in research, issue text and old artifacts treated as inert data   |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope; repository instructions; rpi-research contract; skills.

| Kind                | Candidate                                          | Match and provenance                                   | Scoped authority or output contract                  | Selected / skipped reason                              |
|---------------------|----------------------------------------------------|--------------------------------------------------------|------------------------------------------------------|--------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` AMA instructions | applyTo `**`                                           | validation tiers, branch/PR and commit rules         | selected                                               |
| Instruction         | `docs/reference/method/tracking-retention-policy.md` | referenced by AMA instructions for generated output   | retention of tracking evidence                       | selected; no cleanup of tracked evidence               |
| Skill               | web-design-guidelines and design skills            | no web file in scope                                   | none                                                 | skipped: tooling-only change                           |
| Research specialist | RPI Researcher                                     | no independent uncertainty needing isolation           | none                                                 | skipped: tightly coupled low-volume work, inline fallback |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                         | Answers / unanswered | Resulting decision                                    |
|------------------|-------------------------------------------------------------------------------|----------------------|-------------------------------------------------------|
| Intake           | Non-interactive run; the coordinator brief fixes scope, tier and branch      | n/a                  | proceed with the brief as active direction            |
| Direction change | none                                                                          | n/a                  | none                                                  |
| Convergence      | none; evidence supports a single bounded recommendation                       | n/a                  | no further research cycle                             |

## Scope and Success Criteria

* Scope: see brief. Assumption to verify, not trust: issue text says eight sensor tests; current main pins ten (C3).
* Success criteria: reproduce the omission, identify the exercised SQL initialization dependency, choose the smallest fail-closed change, record the correction budget and the transitive limitation.

## Task Research Requests

* Explicit requests: reproduce; smallest fail-closed selector fix; preserve discovery exception, execution and receipt controls; regression for selection and receipt expectations; record transitive limitation; establish correction history before any correction.
* Caller constraints: demo-targeted validation, owned non-queued SQL if needed, Refs only.

## Direction Controls

| Control type | Direction or boundary                                         | Source / checkpoint | Effect                                         |
|--------------|---------------------------------------------------------------|---------------------|------------------------------------------------|
| narrow       | only `tools/rpi-checks.py` and `tools/test_rpi_checks.py`     | coordinator brief   | related `src/README.md` sentence updated only if it becomes false |
| exclude      | no exhaustive dependency claim, no expanded heavy matrix      | coordinator brief   | transitive closure is recorded as a limitation |
| exclude      | old branch not modified or adopted                            | coordinator brief   | old diff is read only as adverse comparison data |

## Research Questions

|  # | Sub-question                                                                                        | Type            | Priority | Status   |
|---:|-----------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | Does the omission reproduce on current main?                                                        | straightforward | H        | answered |
| Q2 | Which exact SQL-specific definitions does the sensor fixture execute from `chatthreads.py`?         | depth           | H        | answered |
| Q3 | What is the smallest fail-closed selector change and what existing tests constrain it?              | depth           | H        | answered |
| Q4 | Which existing receipt/execution controls already reject missing or failed sensor SQL evidence?     | straightforward | M        | answered |
| Q5 | What is the transitive-dependency limitation?                                                       | depth           | M        | answered |
| Q6 | What are the historical productive correction counts and grants for #1298?                         | straightforward | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: issue #1298 body and its single comment; issue #1297 body and comments; PR #1299 (merged, ancestor of main); old branch commit `fef352e0` and its tracking records (adverse comparison only); coordinator brief and `demo-rpi-common.md`.
* Reused (verified) findings: the issue's mechanism claim is verified independently below (C1 to C4); its "eight tests" statement is stale (C3).
* Superseded / stale: eight pinned sensor methods (now ten on main); the old attempt's records are not reused as evidence for this attempt.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

* Candidates: selector rules in `changed_groups`; the sensor dependency tuple; SQL store construction chain; receipt verification; README coverage text; correction-history sources (issue timeline, PRs, branches, ledger).

#### Wave 2: Deeper

* Q1 reproduced: calling `changed_groups(["src/core/src/zava_forward/core/chatthreads.py"], [])` on this worktree returns `project-core`, `project-agents`, `project-api`, `project-orchestrator`, `project-importer`, `namespace`, `static`, image groups and `logo-0600`, with `mssql selected: False` (C1).
* Q2: the sensor fixture constructs `MssqlStore` (C5). `mssqlstore.py` imports `MEMORY_ADDED`, `MSSQL_DDL` and `MSSQL_INDEX` from `chatthreads` (C6). `MssqlStore` creates the chat tables from `CHAT_DDL[0..3]` (C6), runs `_migrate_chat_memory` with `CHAT_MEMORY_ADDED` and appends `CHAT_INDEX` in `_create_indexes` (C7). `chatthreads.py` defines those objects (C8).
* Q3: the rule at C1 selects `mssql` for paths containing `store`, `schema`, `sql`, `assistants`, core paths containing `sensor`, or members of `SENSOR_MSSQL_DIRECT_DEPENDENCIES` (C2). `chatthreads.py` matches none and is not in the set. The existing set holds three named, individually evidenced paths (C2). Existing tests pin the set exactly: `test_direct_sensor_suite_dependencies_select_mssql` asserts `missed | {indoor_projection.py} == SENSOR_MSSQL_DIRECT_DEPENDENCIES` (C9), so adding a path requires a matching test change. `test_changed_core_sensor_paths_select_mssql_and_the_flagged_command` already asserts the flagged sensor command, flag and pinned count for each selected path (C10).
* Q4: `verify_commands` mutation checks already reject a missing sensor command, altered selector, removed or zero flag, altered cwd, altered counts, skips, a missing pinned test and a skipped pinned test (C11). `required_sql_tests` and `required_sql_count` bind the selector to the pinned names (C12). Discovery skips are accepted only for the exact pinned (name, reason) pairs (C13).
* Q6: see Correction budget.

#### Wave 3: Contrarian

* Alternative A: select `mssql` for every `src/core` path. Rejected: expands the heavy SQL matrix, contradicts the issue's smallest-change criterion and the brief.
* Alternative B: match the substring `chat` in core paths. Rejected: over-selects (for example `chat_panel.py`, `chat_privacy.py`, which are not imported by `mssqlstore.py`, C6) and implies unproven coverage.
* Alternative C: derive the set from an import walk at runtime. Rejected for this issue: adds selector logic and a failure surface; the exact-path set with an AST regression test keeps the rule explicit and fail-closed.
* Alternative D: add a general skip-reason waiver. Rejected: forbidden and would conceal missing execution.
* Counter-evidence: `sqlstore.py`, which `mssqlstore.py` also imports, itself imports at least fourteen sibling modules at top level, plus function-local imports (C14). `sqlstore.py` matches the `store` keyword, but those fourteen modules do not, so a change to any of them alone omits `mssql` in the same way if their code runs in the sensor fixture. Only `chatthreads.py` is demonstrated here (direct import by `MssqlStore`, direct execution of its DDL and index). The remainder is undemonstrated and is the recorded limitation, not covered by this fix.

#### Parent synthesis

* Accepted: add `src/core/src/zava_forward/core/chatthreads.py` to the explicit sensor MSSQL dependency set; adjust the existing pin test; add a focused regression asserting the AST evidence that `mssqlstore.py` imports and executes the chat definitions plus selection and the flagged command for the path; update the comment and the README sentence that describe the set.
* Rejected: alternatives A to D above.
* Deferred: transitive closure over `sqlstore.py` imports and any wider coverage or cost decision remain an owner decision.
* Re-entry: not required; no material claim lacks evidence and the contrarian wave did not weaken the recommendation.

## Correction budget (Q6)

* Evidence reviewed: the issue timeline for #1298 (cross-references to #1297, #1299, #1300, #1294, #1301 and one owner comment); `gh pr list --search 1298` (only merged #1299 and #1301, neither a #1298 candidate); branch `fix/chat-schema-sql-gate-1298` containing one commit `fef352e0` on top of `b46a9ad9`; the coordinator ledger and briefs, which record no #1298 grant and state #1298 was not a demo prerequisite.
* Finding: the old attempt was the initial implementation. A pre-gate readiness assessment (1 High, 3 Medium process findings, comment 2026-11-09T05:27:41Z) asked the owner to authorize a fresh attempt or hold; no source review-correction commit followed and no PR was opened. Productive review-correction cycles consumed on #1298: 0. Issue-specific extra grants: none found. The #1297 cycles C1 to C4 belong to #1297 and the owner's five-additional-cycle grant is for named exhausted issues; neither is a #1298 count.
* Consequence: the standing owner default of at most five total review-correction cycles per issue applies with five remaining. This fresh attempt is the initial implementation, not a correction cycle, and resets nothing. Process findings on the old attempt stay as adverse evidence. Any later correction in this session is C1 and must be recorded.
* Uncertainty: the ledger is a coordinator session file and not a repository record; the conclusion rests on the absence of any other correction record. No blocker.

## Evidence Log

| ID  | Evidence                                                                                      | Location                                                                       |
|-----|-----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| C1  | `changed_groups` keyword rule and dependency membership; `chatthreads.py` reproduces as not selecting `mssql` | tools/rpi-checks.py:757-759                                       |
| C2  | Explicit dependency set with three paths and "not transitive" comment                         | tools/rpi-checks.py:205-212                                                    |
| C3  | Ten pinned sensor tests including the two weather-only cases                                  | tools/rpi-checks.py:187-200                                                    |
| C4  | `chatthreads.py` is not in any selector                                                       | tools/rpi-checks.py:721-763                                                    |
| C5  | Sensor fixture constructs `MssqlStore`                                                        | src/core/tests/sensor_consumer_fixture.py:72-83                                |
| C6  | `mssqlstore.py` imports the chat definitions and builds chat tables from `CHAT_DDL`           | src/core/src/zava_forward/core/mssqlstore.py:20-21,51-54                       |
| C7  | Chat memory migration and chat index executed during index creation                           | src/core/src/zava_forward/core/mssqlstore.py:250-256,292-295                   |
| C8  | `MSSQL_DDL`, `MSSQL_INDEX`, `MEMORY_ADDED` definitions                                        | src/core/src/zava_forward/core/chatthreads.py:34,48,51                         |
| C9  | Exact-set pin test                                                                            | tools/test_rpi_checks.py:557-609                                               |
| C10 | Flagged sensor command and count per selected path                                            | tools/test_rpi_checks.py:513-541                                               |
| C11 | Receipt mutation rejections for sensor evidence                                               | tools/test_rpi_checks.py:643-760                                               |
| C12 | `required_sql_tests`, `required_sql_count`                                                    | tools/rpi-checks.py:1596-1603                                                  |
| C13 | Exact discovery-skip pairs                                                                    | tools/rpi-checks.py:202-204,1650                                               |
| C14 | `sqlstore.py` has at least fourteen top-level relative imports, plus function-local imports not counted                                                | src/core/src/zava_forward/core/sqlstore.py (relative imports, AST listing)     |
| C15 | README states the selector contract for the dependency set                                    | src/README.md:183-192                                                          |

## Findings and Decisions

* Selected approach: smallest explicit-path addition plus pin-test and a focused AST-backed regression. Evidence: C1 to C13.
* Unresolved: broader transitive coverage and cost (owner decision); the literal issue full-gate criterion (unproven under the demonstrator policy).

## Planning Readiness

* Research disposition: executed (one complete three-wave cycle, inline).
* Planning Readiness: Ready.

## Self-check

* Every codebase finding has a `C#` ID with a path and line; no external findings; no source edits made during research; no secrets recorded.
