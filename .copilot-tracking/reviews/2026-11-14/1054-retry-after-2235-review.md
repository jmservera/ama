<!-- markdownlint-disable-file -->
# Review: Resident Demo 503 Retry-After and Accessible Retry Guidance (Issue #1054)

## Scope and Evidence

* Task ID: 1054-retry-after-2235
* Review date: 2026-11-14
* Review scope: full task (`P01`, `P02`, `P03`)
* Assessed boundary: Server bulkhead `Retry-After` configuration, clamping (`1..10`, default `3`), and `503` JSON payload in `resident_demo/app.py`; client non-JSON error handling, retry-signal classification, `loadingTimer` / `aria-busy` / `Promise` continuity, and plain-language `"try again in a few seconds"` guidance in `resident_demo/web/demo.js`; focused unit/VM/UX validation in `src/api`; and `web-design-guidelines` conformance on changed web code. Excludes remote push, PR publication, hosted CI execution, and live `ca-resident-demo` Azure burst traffic per caller boundary (`Do NOT push`).
* Plan: .copilot-tracking/plans/2026-11-14/1054-retry-after-2235-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/1054-retry-after-2235-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/1054-retry-after-2235-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/1054-retry-after-2235-research.md (`C1`-`C12`), `git diff -- src/api/`, refreshed `web-design-guidelines` source (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`), and local `mypy` / `ruff` / `unittest` outputs (`341` tests run, `0` failures).

## Opening Review State

* Interpreted review goal: Verify that the completed implementation of Issue #1054 satisfies all functional and non-functional requirements, resolves every `PC-001`–`PC-004` critique finding, complies with Zava North Homes UX/WCAG/plain-language rules and refreshed `web-design-guidelines`, and leaves reconciled tracking and test evidence.
* Review scope: full task (`P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01`)
* Evidence readiness: Ready; research, plan, phase details, plan critique, changes log, git diff, and validation runs are complete and current.
* Acceptance basis: `FR-1` through `FR-5`, `NFR-1`, `NFR-2`, Plan Acceptance Criteria, Critique Dispositions (`PC-001`–`PC-004`), and `.github/copilot-instructions.md` Web Development and focused-tier validation rules.
* First comparison boundary: Plan markers, critique dispositions, and source/test diffs across `src/api/src/zava_forward/api/resident_demo/` and `src/api/tests/`.
* Active read-only boundaries: Write only `.copilot-tracking/reviews/2026-11-14/1054-retry-after-2235-review.md` (and parent RPI session state); do not mutate source, tests, plan, details, critique, research, or changes artifacts.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full-boundary evidence comparison on 2026-11-14 across research (`C1`-`C12`), plan/details (`P01`-`P03`), critique (`PC-001`-`PC-004`), changes log, `git diff`, refreshed `web-design-guidelines`, and `src/api` static/unit validation results.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01` | Bounded Configurable Server `Retry-After` on Bulkhead Shedding | Reconciled | Checked `[x]` in plan, marked `complete` in phase details, backed by `app.py` diff and `test_resident_demo_api.py`. |
| `P02`, `P02-T01` | Resilient Accessible Client Retry Classification and Copy in `demo.js` | Reconciled | Checked `[x]` in plan, marked `complete` in phase details, backed by `demo.js` diff, `web-design-guidelines` check, and `test_resident_demo_script.py`. |
| `P03`, `P03-T01` | Focused Server and Client Test Additions and `src/api` Validation Suite | Reconciled | Checked `[x]` in plan, marked `complete` in phase details, `5` focused tests added (`<= 6` cap, `0` removals), `341` tests + `mypy` + `ruff` passed. |
| `Follow-Up Items` | Live post-deploy 30-viewer authenticated burst verification against `ca-resident-demo` | Reconciled | Kept outside active `Pxx`/`Pxx-Txx` completion claims and mirrored in changes record with owner attribution. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01`, `P01-T01` | src/api/src/zava_forward/api/resident_demo/app.py | Kept `MAX_CONCURRENT = 8`; set `MIN_RETRY_AFTER_SECONDS = 1`, `MAX_RETRY_AFTER_SECONDS = 10`, `RETRY_AFTER_SECONDS = 3`; added `mypy`-clean `clamp_retry_after(seconds: object) -> int` and `ResidentDemo(..., retry_after_seconds: int = RETRY_AFTER_SECONDS)`; emitted `app.retry_after_seconds` in `Retry-After` header and `retry_after_seconds` JSON field on slot exhaustion only. | `git diff` on `resident_demo/app.py`; `FR-1`, `FR-2`, and `PC-004` satisfied. | Passed (`mypy`, `ruff`, `test_resident_demo_api.py`) | Reconciled |
| `P02`, `P02-T01` | src/api/src/zava_forward/api/resident_demo/web/demo.js | Hardened `api()` for non-JSON `!r.ok` bodies while preserving `2xx` parse errors and `Retry-After`; added `retryWaitSeconds()` (`1..10s` monotonic clamp, `3s` fallback on non-numeric/non-positive retry headers, `0` when unhinted) and `busyErrorCopy()` (`/try again in a few seconds/i` check + punctuated guidance); updated `loadView()` to set `aria-busy="true"`, clear `loadingTimer !== null`, reset `loading = false`, announce polite second-person retry guidance with singular/plural seconds, and return the `Promise`-chained retry guarded by `current === transition`; applied `busyErrorCopy()` to `/demo/view`, `/demo/session`, and `/demo/login`. | `git diff` on `resident_demo/web/demo.js`; `FR-3`, `FR-4`, `FR-5`, `NFR-1`, `NFR-2`, and `PC-001`–`PC-003` satisfied. | Passed (`test_resident_demo_script.py`, UX/content suites, refreshed `web-design-guidelines` audit) | Reconciled |
| `P03`, `P03-T01` | src/api/tests/test_resident_demo_api.py, src/api/tests/test_resident_demo_script.py | Added `2` server tests (`configurable_and_bounded`, `expired_503_omits_retry_after_header`) and `3` client VM tests (`expired_503_without_retry_hint`, `generic_and_non_json_shed_503_clamp_delay`, `login_shed_view_clears_slow_timer_and_keeps_promise_chain`) with `0` test removals. | `git diff` on both canonical test files (`5` additions total `<= 6` cap). | Passed (`284` resident tests + `57` UX/content/a11y/asset tests, `0` failures) | Reconciled |

## Web Interface Guidelines Audit (Refreshed Before Review)

Refreshed rules from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` and audited changed web file `src/api/src/zava_forward/api/resident_demo/web/demo.js` (modified range `741-819, 840, 899` and surrounding file context):

```text
## src/api/src/zava_forward/api/resident_demo/web/demo.js

✓ pass
```

Notes on checked web rules:
* Async status updates use `#status` (`role="status" aria-live="polite"`) and `#main[aria-busy="true"]`, cleared deterministically via `endLoading()`; terminal failures use `#error` (`role="alert"`) and focus `#error-title`.
* Loading and retry announcements terminate with Unicode ellipsis `\u2026` (`…`), use numerals (`1 second`, `3 seconds`, `10 seconds`), use active second-person phrasing (`"Retrying automatically... try again in a few seconds…"` / `"Please try again in a few seconds."`), include a clear next action, and preserve native `<button>` / `<form>` controls without colour-only status cues or banned internal jargon.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| None (marker completion only) | Checked `[x]` on `P01`-`P03` and `P01-T01`-`P03-T01` as completion evidence accrued; no scope or design amendments were needed during implementation. | Passing diffs and validation runs; no new user decision required. | Plan checklist, Handoff, Phase Details index, and Changes log synchronized. | Finalized ready state with `PC-001`–`PC-004` preserved. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four critique findings (`PC-001` High, `PC-002` Medium, `PC-003` Medium, `PC-004` Low) were resolved directly in the plan and phase details prior to implementation and verified in the shipped code and tests (`loadView()` returns the `Promise`-chained retry with `current === transition` and `loadingTimer !== null`; `retryWaitSeconds()` clamps `"99" -> 10s`; `api()` rethrows malformed `2xx` JSON and `busyErrorCopy()` checks `/try again in a few seconds/i`; `clamp_retry_after(seconds: object) -> int` passes `mypy` cleanly).
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: Execution respected `P01 -> P02 -> P03` dependency order with no early resumption.
* Justification assessment: Supported by primary code, diffs, and automated test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Live post-deploy 30-viewer authenticated burst verification against `ca-resident-demo` | Caller explicitly forbade pushing (`Do NOT push`), so container image publication and live Azure Container App burst verification cannot run from this offline worktree turn. | Repository owner: after merging and deploying the updated `zava-resident-demo` image digest, run the authenticated 30-viewer burst check recorded on Issue #1054. | Open non-blocking operational follow-up; routed to distinct follow-up owner outside active `Pxx`/`Pxx-Txx` scope. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No material defects, decision gaps, or evidence gaps were found within the assessed task boundary (`0 Critical`, `0 High`, `0 Medium`, `0 Low` defects).

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| none | none | No `rpi-implement`, `rpi-plan`, or `rpi-research` re-entry required | Implementation is conformant across all `P01`-`P03` criteria |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Post-publication hosted CI observation, independent exact-head PR review, and live `ca-resident-demo` 30-viewer authenticated burst verification remain owner-controlled steps after pushing/deploying (explicitly excluded here by caller `Do NOT push` instruction).

## Blockers and Remaining Work

* Blockers: none for local commit completion; hosted CI and human approval gates apply at future PR publication time per `.github/copilot-instructions.md`.
* Remaining active work: none (`P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01` complete).

## Validation Evidence

Validation classification: **Focused tier** (owner decision D4 / Issue #1294 — targeted `resident_demo` application/client UX fix and unit tests; touches no Bicep/infra, SQL schema, Dockerfile, workflow, dependency manifest, gate script, or security boundary). Note: hosted CI workflows did not run because the caller instructed `Do NOT push`; all relevant local checks ran directly and passed.

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `web_fetch` (`web-design-guidelines`) | `src/api/src/zava_forward/api/resident_demo/web/demo.js` | Passed | Refreshed rules before edits and before Review; `demo.js` passed (`✓ pass`) |
| `python3 -m mypy` | `src/api` (`282` source files) | Passed | `Success: no issues found in 282 source files` |
| `python3 -m ruff check .` | `src/api` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/api` (`198` files) | Passed | `198 files already formatted` |
| `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest discover -s tests -p "test_resident*.py" -v` | All `resident*` suites in `src/api/tests` | Passed | `Ran 284 tests in 123.412s — OK (skipped=9)` |
| `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src:tests python3 -m unittest tests.test_content_standard tests.test_accessibility_baseline tests.test_epic149_manual_fallback_continuity tests.test_static_assets -v` | Content standard, WCAG 2.2 AA baseline, manual fallback continuity, and static assets | Passed | `Ran 57 tests in 4.243s — OK` |
| Hosted GitHub Actions CI | Branch `feat/ux-1054-retry-after-2235` | Skipped | Not pushed per explicit caller constraint (`Do NOT push`); must run when branch is pushed |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every requirement (`FR-1`–`FR-5`, `NFR-1`, `NFR-2`), acceptance criterion, critique finding (`PC-001`–`PC-004`), `web-design-guidelines` rule, plain-language/WCAG check, and caller-requested validation command (`mypy`, `ruff check`, `ruff format --check`, and `resident_demo` unit tests) is satisfied with direct evidence and zero open defects.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | Owner: push branch when ready for hosted CI / PR review, then verify 30-viewer authenticated burst against deployed `ca-resident-demo` |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused local tier passed (`mypy` `0` issues, `ruff check` & `ruff format --check` clean, `341` unit/VM/UX tests passed); hosted CI unobserved locally due to `Do NOT push`
* Blockers: none
