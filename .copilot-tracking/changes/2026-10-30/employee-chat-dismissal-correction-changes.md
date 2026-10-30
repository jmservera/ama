<!-- markdownlint-disable-file -->
# RPI Changes: employee-chat-dismissal-correction

## Metadata

* Task ID: employee-chat-dismissal-correction-2026-10-30
* Date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/employee-chat-dismissal-correction-plan.md
* Details: .copilot-tracking/details/2026-10-30/employee-chat-dismissal-correction-phase-details.md
* Original baseline: 366ca4a2, fix/employee-chat-closes-on-send.
* Declared scope: full correction plan.

## Execution Status

P01 and P02-T01 execution complete. Research executed / Ready; one independent plan critique Complete / Pass, no findings; one independent Review Complete / Not accepted on broad AC4. Original RV-001/RV-002 resolved within the assessed boundary, no new source defect. P02-T02 independent Review complete, authorized local commit pending. Original Review and parent artifacts preserved.

## Execution Summary

Correct delayed-dismissal focus with unchanged-source failing browser proof before minimal show-local correction. Complete full unit discovery under owner-authorized waiting lock, static and focused/shared/employee/resident browsers. One independent correction Review then local Refs-only commit. No push/live/Azure/credentials.

## Completed Work

### P01-T01: Red-before-green regression

Before any runtime edit, the extended focused browser exited 1 at `Escape: delayed render redirected deliberate dismissal focus`. All 12 original send combinations passed first. Raw log: external dismissal-correction/submit-red.log. This is actual healthy loopback app / Chromium, not a DOM-only model. Runtime app.js was still byte-identical to 366ca4a2.

### P01-T01: Focus correction

show now records last-rendered authenticated session/path. Same-context connected external focus survives app replacement; body/root, removed controls and real context changes keep app fallback. Visible chat retains prior focus ownership. No widget/auth/resident/timer/dependency change. Existing focused module also tests Close plus normal workspace landing counterexamples; README documents exact boundary.

Focused browser green exited 0: exact Escape/Close/external focus, hidden/no reopening, draft retention, composer/log/Sources, real destination/session/lost-focus fallback, all 12 original sends, actual start auth variants/stale race and resident actual Enter/Send rules replies. External submit-green.log and submit-green/results.json, Chromium version in JSON. node --check and git diff --check passed.

## Implementation-Time Updates and Divergences

### P02-T01: Coupled shared regression assertion

First shared browser exited 1 in employee_refresh closed-chat branch: retained launcher was inactive according to the obsolete expected #app focus. That repeats original RV-001's opposite expectation. Updated only that existing shared assertion to expect launcher; amended plan test-owner boundary/details directly as an immediately relevant correction preserving FR1. No source runtime change, user decision or repeated critique. Original shared-green.log retained. Focused body fallback now explicitly blurs; external disconnected-node fallback remains separate.

## Validation Record

Pending. Raw evidence destination: /home/azureuser/.copilot/session-state/fd7592c3-4f6e-4765-8151-ac243697d1d6/files/dismissal-correction/.

### P02-T01: Current measured validation

* Full API command admitted under flock -w 600; `LOCK acquired for full API unittest discovery` in full-api-units.log. Suite running; no pass inferred.
* Final ruff check ., ruff format --check ., mypy all exit 0: 59 formatted files, 114 source files (static-final.log). Python 3.12.3, ruff 0.17.1, mypy 2.4.0.
* Final focused and integrated shared browser checks exit 0 (submit-green-final.log, shared-green-final.log and results.json); Chromium 156.0.8078.4. All 12 sends, three deliberate dismissals, ordinary destination/session/lost-focus fallback, actual auth lifecycle and stale race passed. Shared also passes 48 focus/denial combinations, 12 obsolete-result combinations, employee/resident axe/layout/following/consent/recovery.
* Employee dedicated chat browser exit 0, including real unavailable-model fallback, selections, nine late successes, denials, keyboard/reflow/axe (employee-green.log).
* Additional resident assistant browser exit 1 at existing checks/resident_assistant_browser_check.py:330: prompt `documents help` expected `Survey: Missing`, actual current finite-grammar refusal. resident-green.log retained. This check and resident runtime/shared assets are byte-identical to 366ca4a2 (`git diff --exit-code 366ca4a2 --` those paths exit 0). No employee app.js is served by this resident fixture. This is a pre-existing, out-of-scope check/runtime contract mismatch, not claimed passing or repaired silently. Broader AC4 remains unmet even though focused/shared resident boundaries pass.
* Pinned axe 4.10.3 SHA-256: 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb.

### P02-T01: Full-suite environment correction

First admitted full discovery completed 1361 tests in 476.743s, exit 1, 45 errors / 318 skips. All 45 errors were FileNotFoundError for `node`: the intentionally sanitized PATH omitted existing Node at /home/azureuser/.nvm/versions/node/v24.21.0/bin/node. Original full-api-units.log retained. This is execution-environment failure, not a source regression or acceptable full-suite result.

Immediately corrected only the validation environment to `env -i HOME=... LANG=C.UTF-8 PATH="/tmp/mv/bin:$PATH"`: retains existing tool paths, still excludes inherited credential/model/storage environment. No dependency installation, selector change or source change. Fresh full-api-units-final.log confirms lock admitted again with flock -w 600; complete discovery running anew. Existing skip declarations inventoried separately in declared-skips.json (317 declaration-time cases, not represented as execution results); dynamic JSON COMMIT non-applicability is explicitly in test_progress_report_api.py.

### P02-T01: Complete full-suite success and RV-002 evidence

The fresh complete discovery finished with exit 0: `Ran 1361 tests in 474.769s`, `OK (skipped=318)`. Exact command from src/api:

```bash
env -i HOME="$HOME" LANG=C.UTF-8 PATH="/tmp/mv/bin:$PATH" \
  flock -w 600 /tmp/ama-rpi-heavy.lock sh -c \
  'PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q'
```

Raw full-api-units-final.log begins with lock-acquired marker (wrapper also printed that marker before the shown python command). Full requested API discovery, not selected tests or a skip-token substitute. Initial missing-Node attempt remains retained. No SQL/browser opt-ins were enabled for general discovery; dedicated relevant browsers ran separately.

318 skips reconcile as 317 declared opt-in cases (all IDs/reasons in external declared-skips.json) plus test_progress_report_api.JsonProgressApi.test_committed_handoff_failure_returns_existing_explicit_outcome_contract: JSON has no SQL COMMIT acknowledgement boundary. Declaration groups: 201 SQL Server, 50 disposable SQL, 36 continuity owned MSSQL, 11 loopback SQL, seven coordinator loopback MSSQL, six resident isolated SQL; six browser cases (two coordinator journeys plus one each rendered/Chromium/Playwright/resident browser). This is standard full discovery's actual skipped total, not full SQL integration or publication evidence.

### P02-T01: Resident baseline confirmation

Read-only `git archive 366ca4a2 src/api src/core src/agents` extracted under the external evidence root, then the original standalone resident browser ran against those original source paths with the same sanitized tools and pinned axe. It exited 1 on the identical `Survey: Missing` assertion for `documents help`. Raw resident-baseline.log and archived source retained alongside candidate resident-green.log. No worktree source changed. This independently demonstrates pre-existing failure; it is not waived as passing.

### Pre-Review Reconciliation

P01 checked with red/green proof; P02-T01 checked as executed with actual pass/failure/skip evidence, not broad AC4 acceptance. Details, plan summary/handoff and state distinguish RV-001/RV-002 corrected evidence from baseline resident residual. P02-T02 remains unchecked for independent Review/local commit. One critique Complete / Pass, no findings; compatible shared-assertion and PATH corrections recorded as immediately relevant, no new user decision or repeated critique. Review must assess the four source/check/doc diffs plus all new dated artifacts against 366ca4a2 and preserve original artifacts.

### P02-T02: Independent Review and Routing

Exactly one independent Review executed Complete; outcome Not accepted on broad AC4, original RV-001 and RV-002 resolved within the source/test/full-unit boundary, no new source defect. New RV-003 Medium retains baseline standalone resident failure and routes it to distinct resident follow-up. Canonical new Review: .copilot-tracking/reviews/logs/2026-10-30/employee-chat-dismissal-correction-review.md. No source correction, repeat Review or source edits after Review. Original Review and critique remain byte-identical.

Automatic child task is completed at Follow-up with session running, distinct from acceptance. Parent prepares the authorized local commit only; repository-local authenticated privacy-safe identity configured via gh api user without printing credentials. Required coauthor trailer and Refs #550 only; no push, issue closure or PR creation. Local delivery completion is recorded after commit, not assumed here.

## Changed-Web Guidelines Review

Current source retrieved before edits and refreshed 2026-10-30 immediately before this changed-block review. All categories considered; only imperative focus ownership changed, no markup/style/content/ARIA/native events or animation. Review boundary: app.js variable/show block, not whole application.

### src/api/src/zava_forward/api/web/app.js

Pass for changed block: src/api/src/zava_forward/api/web/app.js:93 retains connected chosen focus within rendered context; normal context/lost-focus landing maintained. No changed-block finding. Local browser/axe is not human assistive-technology or whole-app conformance.

## Blockers and Remaining Work

P02-T02 remains for independent Review and local commit. No blocker to source correction or RV-002 full API evidence.

Broader AC4 acceptance blocker: pre-existing standalone resident-assistant prompt/grammar mismatch, baseline-proven. Full API succeeded. Continue one Review/local delivery; do not broaden correction to unrelated resident behavior. No complete publication gate/hosted/human acceptance claimed.

## Follow-Up Items

Coordinator-owned live-site verification only after separate authorization. Human accessibility, live-model and publication acceptance not established by this local cycle.

Additional bounded follow-up: reconcile standalone resident-assistant browser fixture's legacy `documents help` topic prompts with the current deliberate finite grammar, with resident-answer authority tests. Owner/coordinator; outside employee-focus correction. Evidence: resident-green.log and unchanged baseline paths.
