<!-- markdownlint-disable-file -->

# Task Research: capacity-sql-reopen-correction

| Field | Value |
| --- | --- |
| Date | 2026-10-31 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-31/capacity-sql-reopen-correction-research.md |

## Research Brief

* What to research: SQL-only legacy capacity read failure after store reopen in PR #605, Refs #523.
* Why it matters: repair the regression without synthesizing legal or procurement authority.
* Audience or intended use: implementation and independent review of this correction.
* Scope: SQL/file store lifecycle, law-store initialization, capacity API, external package tests, CI run 41212776695.
* Non-goals: UI redesign, new legal rules, deployment, full local publication gate, protected container/image removal.
* Criteria: reproduce on the existing SQL Server if available; compare file-store behavior; distinguish incorrect fixtures from production defects.
* Requested outputs: root-cause recommendation, focused regression evidence and full dated RPI loop.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Why does the reopened SQL store lack law data, and which layer should correct it? |
| Codebase scope | src/core, src/api/tests, src/api capacity read path and component guides |
| External scope | Existing GitHub CI failure only |
| Initial internal candidate areas | MssqlStore, FileStore, procurement API tests, law-store tests |
| Initial external candidate areas | https://github.com/jmservera/ama/actions/runs/41212776695 |
| Research posture | focused |
| Posture provenance | Default for bounded named regression |
| Explicit limits / deadline | User requires pip only, no secrets, existing protected SQL container reuse, CI publication gate, non-force push |
| Completion basis | Covered failure, lifecycle contract and credible alternative |
| Edits allowed during research? | No source edits |
| Resolved evidence root | .copilot-tracking/research/ |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority | Disposition |
| --- | --- | --- | --- | --- |
| Instruction | Repository guidance | Repository-wide instructions supplied at intake | Component tests, branch hygiene, authority boundaries | Selected; explicit user CI direction supersedes full local gate for this correction |
| Skill | rpi-research | Bounded investigation | Three ordered inline waves | Selected |
| Specialist | None | One tightly coupled trace | No independent research lane needed | Inline investigation |

## User Participation and Research Decisions

* Explicit full-loop request establishes automatic execution through Review and push; no interactive clarification is needed or available.
* Branch clean at intake; requested pull fast-forwarded to e5f36c13. Fetch/merge origin/main was already up to date, so no merge conflicts or log entries required resolution.
* PR #605 is open on the requested branch targeting main.

## Scope and Success Criteria

* Verify CI failure and inspect external test setup and law-loading contract.
* Reproduce using ama-350-feedback-sql without deleting or recreating it.
* Preserve unknown legal/contract authority and compare SQL and file paths.

## Task Research Requests

* Root-cause fix or test correction, external-package focused tests, requested lint/type/unit commands, commit with trailer, non-force push.

## Direction Controls

| Type | Boundary | Source | Effect |
| --- | --- | --- | --- |
| narrow | PR #605 correction only | User | No unrelated redesign or lifecycle overhaul |
| exclude | Full local gate, container/image removal, secrets | User | CI is the requested gate; protected resources reused |

## Research Questions

| ID | Question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | Which reopened-store lifecycle causes the law lookup to fail? | depth | High | Answered |
| Q2 | Is the production lifecycle incorrect or does the SQL fixture omit law loading? | depth | High | Answered |
| Q3 | Can legacy data remain readable while authority remains unknown? | straightforward | High | Answered |

## Prior Knowledge Gate

* Supplied failure is an unverified starting claim pending code/log confirmation.
* Read original specification, addendum, knowledge-base index and owner memory; no authority expansion is intended.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

* Inspect failure, SQL/file lifecycle and existing test/bootstrap commands inline.
* Reflection: W1 identifies the actual terminal failure as a SQLite-specific db_path assertion, not the incidental logged law-store errors. C1 identifies a second tightly coupled fixture defect: the SQL make_store method wipes tables on every invocation.

#### Wave 2: Deeper

* Trace law-loading and capacity rule checking; reproduce the named test.
* Reflection: local SQL reproduction matches W1 exactly (1 test, 1 failure at test_procurement_api.py:172). SQLite/file selectors both pass (2 tests). C2 confirms MssqlStore uses state_dir/mssql as a local state marker, not a SQLite filename. Reusing make_store for reopening also destroys saved procurement before reseeding it, so relaxing the path assertion alone would not be a complete fix.

#### Wave 3: Contrarian

* Challenge whether initialization belongs in production or the test fixture; check unloaded-law fail-closed behavior.
* Reflection: C3 distinguishes the separate application-owned law store from the case store. Production main loads LawStore.from_env and passes it to App. The procurement fixture intentionally has no law store. C4 already tests explicit unknown/503 rule checks and post-commit safety persistence when law is unavailable. Loading invented law data or suppressing that failure would weaken the contract, not fix the actual SQL regression. C5 supplies an existing non-wiping reopen_store pattern in another SQL HTTP fixture.

#### Parent Synthesis and Disposition

| Material / claim | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Missing law-store error is the fatal capacity reopen failure | W1, C3, C4 | Rejected | It is incidental logged post-commit evaluation; terminal failure is db_path assertion |
| SQL reopen test uses incorrect factory and path expectation | C1, C2, W1 | Accepted | Local reproduction and lifecycle code agree |
| Correct fixture lifecycle; retain unavailable-law behavior | C3, C4, C5 | Accepted | No production rule or authority change needed |

#### Cycle Re-entry Evaluation

* No additional cycle needed: focused lifecycle and alternative are covered by source, CI and real SQL reproduction.
* Readiness: Ready; implement a distinct non-destructive reopen helper and backend-neutral persistence assertions.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | SQL procurement factory wipes tables every call; common regression calls it for reopening | src/api/tests/test_mssqlstore.py:385-388; src/api/tests/test_procurement_api.py:169 | High |
| C2 | MssqlStore uses a state marker named mssql while SqlStore uses the supplied SQLite filename | src/core/src/zava_forward/core/mssqlstore.py:222-229; src/core/src/zava_forward/core/sqlstore.py:165-171 | High |
| C3 | App owns law separately; production startup loads law and passes it into App | src/api/src/zava_forward/api/server.py:69-100,1130-1137 | High |
| C4 | Missing law is explicitly unknown/503 while human safety writes remain saved | src/api/tests/test_rule_alerts.py:160-196 | High |
| C5 | Existing SQL HTTP fixture separates initial wipe from non-wiping reopening | src/api/tests/test_mssqlstore.py:392-400 | High |
| C6 | File store prefers saved live.json over original seed | src/core/src/zava_forward/core/store.py:45-55 | High |

| ID | Finding | URL | Retrieved |
| --- | --- | --- | --- |
| W1 | CI terminal result: 269 tests, one path-assertion failure, one skip; missing-law stack traces are earlier log output | https://github.com/jmservera/ama/actions/runs/41212776695 | 2026-10-31 |

* Local SQL command: from src/api, requested PYTHONPATH with /tmp/mv/bin/python and the session-owned runtime SQL runner; named MssqlProcurementApi reopen test fails at line 172 with state marker mssql versus synthetic.sqlite.
* Local SQLite/file command: requested PYTHONPATH, /tmp/mv/bin/python -m unittest test_procurement_api.ProcurementApi.test_legacy_capacity_reads_survive_store_reopen_without_inventing_authority test_procurement_api.JsonProcurementApi.test_legacy_capacity_reads_survive_store_reopen_without_inventing_authority -q; 2 tests pass.
* SQL isolation: newly created ama_605_reopen_20261031_0845339f database only, on protected ama-350-feedback-sql. Authentication stays in runtime memory and is not recorded.
* Selector correction: initial file-store selector used nonexistent FileProcurementApi; corrected to existing JsonProcurementApi. No source defect inferred from that invocation error.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence |
| --- | --- | --- |
| Q1 | No law-load failure in the terminal capacity regression; the actual failure is a dialect-specific path assertion | W1, C2 |
| Q2 | Test fixture is wrong: it resets rather than reopens SQL data | C1, C5 |
| Q3 | Reopen persisted data without seed, preserve missing contract version and deny writes; explicitly retain unknown law checks | C3, C4, C6 |

## Alternatives and Decision State

* Selected: correct external test fixture only, with common reopen_store and non-wiping SQL override; compare actual original backend/path and independent connection; remove seed before reopen to prove no reseed; assert unavailable-law HTTP remains 503/unknown.
* Rejected: load legal rules in MssqlStore, because law is application-owned and production startup already loads it (C3).
* Rejected: tolerate missing law with successful rule evaluation, because missing-law checks must remain unknown (C4).
* Rejected: relax only SQLite filename assertion, because the fixture would still wipe saved data (C1).

## Open Questions, Risks, and Residual Uncertainty

Hosted success and human approval cannot be inferred from a local correction.

## Planning Readiness

* Status: Ready.
* Preconditions: exact CI failure reproduced on real SQL; both other backends pass; credible production alternative rejected from code.
* Blockers: none for the bounded correction; CI/human merge gates remain separate.

## Research Disposition

Executed, complete. Wider, Deeper and Contrarian completed inline for one tightly coupled trace.

## Current Decisions

Correct setup rather than production behavior (C1-C5). Explicit user CI-only publication direction is retained.

## Unresolved Decisions

None for planning; hosted outcome remains unobserved.

## Potential Next Research

No additional in-scope research selected; investigate only if focused tests reveal a distinct production issue.

## Closeout Record

Research complete; Planning Readiness Ready; automatic RPI parent owns Plan transition. Self-check: evidence IDs resolve, contradiction is explicit, no secret or new authority recorded.

## Advisory Next Step

Automatic parent should activate rpi-plan, then execute the requested correction and independent gates.

## Sources

* W1 - Source projects CI run 41212776695 - https://github.com/jmservera/ama/actions/runs/41212776695 (retrieved 2026-10-31).
