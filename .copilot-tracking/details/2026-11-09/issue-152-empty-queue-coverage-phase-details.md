<!-- markdownlint-disable-file -->

# Phase Details: issue-152-empty-queue-coverage

Plan: .copilot-tracking/plans/2026-11-09/issue-152-empty-queue-coverage-plan.md
Research: .copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-research.md (C10, C12, C9, C18)

## Test ownership and locks (for critique)

* Removals: none. Maximum additions: one new test file (about 10 cases) plus text expectations in the existing browser check.
* Canonical targets: `src/api/src/zava_forward/api/web/app.js`; no generated targets.
* Semantic coverage: node tests of the real functions from `app.js`. Regression coverage: browser check strings (unexecuted).
* Validation evidence: ruff, node --check, unittest, all with actual versions and exits reported.

<!-- P01 -->
## P01 Pure empty-state helper and client wiring

* P01-T01: define near `defaultListState` (app.js:457) two side-effect-free functions.
  * `trustedCoverage(coverage, ctx)` returns the declaration when FR-D holds, else `null`. `ctx` is `{ role, version, asOf, policyVersion }`.
  * `queueEmptyExplanation({ view, filtered, coverage, ctx })` returns `{ state, text }`, state one of `no-match`, `coverage-unknown`, `declared-unrepresented`, `empty-all`.
  * Copy keeps the substring `No cases match these filters.` for the existing browser check.
* P01-T02: in `listView` keep `asOf = d.as_of` next to `policy` (app.js:~820) and replace the empty `li` ternary (app.js:800) by `queueEmptyExplanation(...).text`. Coverage source is only `me.work_queues.coverage`. Nothing else changes; reset and focus code untouched.
* Precondition: fetch web-design-guidelines source and read it before editing app.js.
* Helper takes `rowsLength`; it returns `null` when rows exist. All bound values need `typeof === "string"` and non-empty. Unknown text starts with the existing sentence "No open cases are assigned to you. This does not mean the programme has no work." and no-match text starts with "No cases match these filters." because other checks assert those strings (employee_briefing_browser_check.py:70, loading_briefing_browser_check.py:611,614). The declared text names source, fixture version and as-of date.
* Done when: populated results render exactly as before; empty states match FR-A..FR-E.

<!-- P02 -->
## P02 Regression tests

* P02-T01: `test_queue_empty_state.py` reads `app.js`, extracts both functions by name and brace matching, runs them in `node` with JSON cases. Cases: no-match with a valid declaration still no-match; Coordinator empty default no declaration gives Unknown; same with valid declaration gives declared; PM `ZF-5` default is a non-empty queue so helper is not used (asserted through the manifest default, read from `workbench-manifest.json`, and the live-default HTTP test remains the data check); each invalid declaration variant gives Unknown; `all` view wording unchanged; declared text does not contain "complete".
* P02-T02: add expectation lines to the Coordinator and no-match steps in `workbench_browser_check.py` (Unknown text, no-match text includes "not a statement about scenario coverage"). Not executed.
* Add tripwire: `taskqueues.contract(...)` has no `coverage` key today. Add variants: missing/empty/non-string as_of and policy_version; wrong role; wrong status; blank fixture/source; non-object.
* Browser expectations (unexecuted): Coordinator shows Unknown and not "unrepresented"; PM default shows no `.empty` element; no-match wording.
* Done when: node tests pass and failure on mutation is plausible (each invalid variant asserted individually).

<!-- P03 -->
## P03 Validation and review

* P03-T01: `ruff check` and `ruff format --check` on changed Python; `node --check app.js`; `python3 -m unittest tests.test_queue_empty_state tests.test_workbench -q` from `src/api` with `PYTHONPATH=../core/tests:../agents/tests`.
* P03-T02: fetch https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md before edits and again before review; report applicable rules with `file:line`; record unperformed visual checks.
* P03-T03: document the optional declaration contract and its absence in `src/api/README.md` only if a queue/workbench section exists.
