<!-- markdownlint-disable-file -->

# Research: issue-152-empty-queue-coverage-correction-3

| Field | Value |
|---|---|
| Task ID | issue-152-empty-queue-coverage-correction-3 |
| Parent | issue-152-empty-queue-coverage-correction-2 (recovered, same retained branch, no reset) |
| Start | 2026-11-10T01:41:52Z (actual `date -u` output; first timestamp) |
| Branch / head | feat/workbench-empty-coverage-152 at e4f77fa7514e265a2125bb2c3e89aac53e8c8baf; original base b46a9ad9a9619db535368d1b2cbbddec8110e122 |
| Research disposition | executed (read-only inspection before any change) |
| Planning Readiness | Ready |
| Position | Correction 3 of 5 total; two remain afterward. Not an initial delivery. `Refs #152`; AC-034/043 and whole 152 remain unmet |

## Recovered evidence

* The original task, correction 1 and correction 2 records under `.copilot-tracking/*/2026-11-09/issue-152-empty-queue-coverage*` are complete and preserved unchanged. Correction 2 removed a two-line comment that failed `tests.test_content_standard`, and ran only 25 focused tests plus Node syntax. Its review lists RV-001/RV-002: fresh exact-head changed gate, browser run, independent review and full API suite unperformed. The coordinator's failed API receipt (`/tmp/ama-g152-c1-1109/0024-project-api.log`: 2038 tests, 1 failure, 363 skips) is adverse evidence and not a Pass; it is not modified or reinterpreted.
* Exact branch PR query across all states returned none (coordinator statement). No push, PR, issue or board write is made here.
* Branch is four commits ahead of the base: `c934312ee`, `85c7a3741`, `06954540e`, `e4f77fa75`. The product diff against the base is four files: `src/api/src/zava_forward/api/web/app.js` (+`queueEmptyExplanation`, `listView` empty render), `src/api/tests/test_queue_empty_state.py` (new), `src/api/checks/workbench_browser_check.py` (+two checks) and `src/api/README.md` (+12 lines).
* Fetched `origin/main` is now `0385ad6a50d25c98cc902f199186c4fd1b50eca7` (coordinator's preview named `e9c98eb2...`; main has since advanced by `fix(resident): deny unbound supersession...` and a rubric score commit). Merge base with the branch is still `b46a9ad9a`. `git merge-tree --write-tree HEAD origin/main` is clean (tree `076b2877ebf060cd5ceb0dca35bea8ab80730485`), a preview only and not integration or validation.

## Coupled integrity

* `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` lists `src/api/checks/workbench_browser_check.py` as source id `recipe` with a SHA-256 that must equal the changed file. The Core scenario-manifest and needs-inventory tests check it. The branch changed this file, so the recorded hash is expected to be stale. The existing mechanism (the Core scenario manifest code and tests) is to be read and used; hashes, source sets, expected data, audit and permissions are not weakened.

## Scope boundary

* In: ordinary merge of fresh `origin/main`; keep both intents; the four existing product/evidence paths; recipe-hash binding correction and minimal index/log maintenance if repository rules need it; new C3 records.
* Out: runtime coverage producer or trusted declaration, `server.py`, navigation registration or routes, intake, shared persistence, finance, `resident_decisions`, SQL, images, models, Azure, release, human, accessibility-testing or usability acceptance. Main's app.js changes elsewhere (account label, simulator navigation, priority history controls) must survive the merge. The 132 ownership reservation covers intake/shared API/navigation/store/procurement/sqlstore hooks; the empty-state surface is separate and no widening is planned. Any overlap or new source bug outside the slice stops with evidence.

## Alternatives

* A (chosen): ordinary `git merge origin/main` into this branch, resolve nothing unless conflicts appear, then targeted DEMO validation and served browser harness.
* B: rebase or cherry-pick onto main. Rejected: forbidden, rewrites history.
* C: skip the merge and validate on the old base. Rejected: leaves the stale-base gap that C2 left open.

## Validation plan (targeted DEMO tier, not `--changed` or full gate)

Queue-empty, content-standard and workbench tests; `node --check`; strict mypy on the `src/api` project and Ruff check/format for applicable files; Core scenario-manifest and needs-inventory integrity; the existing served workbench browser harness (`python -m checks.workbench_browser_check` from `src/api`, loopback synthetic server, committed fixtures, `ZF_STORE=json`, no private data). Distribution install: a throwaway venv with editable installs of this worktree's `src/core`, `src/agents`, `src/api[dev]`, because the globally listed editable distributions point at another worktree.

## Open items

* Whether an in-tree harness case covers the empty own-queue for a non-Contractor role is checked by running it; an unrunnable harness is reported as blocked, never as a pass.
