<!-- markdownlint-disable-file -->
# RPI Phase Details: Capacity page correction

## Metadata

* Task ID: 523-correction
* Task slug: capacity-page-523-correction
* Related plan: .copilot-tracking/plans/2026-10-28/capacity-page-523-correction-plan.md
* Evidence: correction research C1-C8/W1 and original RV-002/RV-003

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Correct recovery and browser proof | Complete, runtime proven | P01-T01, P01-T02 |
| P02 | Validate and review | Complete; independent Review Conformant | P02-T01, P02-T02 |
| P03 | Publish exact candidate | Pending P02 | P03-T01 |

Single critique Complete / Revise; PC-001 applied directly below. No repeated
critique or changed owner decision.

<!-- rpi:phase id=P01 -->
## P01: Correct recovery and browser proof

<!-- rpi:task id=P01-T01 -->
### P01-T01: Keep capacity retry read-only and draft-safe

ops.js go currently catches successful-mutation/failed-refresh and offers route.
Instead allow a no-mutation invocation and bind retry to that closure. Retain old
DOM on read failure and existing success-only draft capture/restore. Captured
abort/session state must prevent obsolete rendering or refresh after navigation.
Do not invoke saved mutation from retry or change shared routing.

Browser proof: two appointment forms, fill draft values/checkboxes and retain
context/event reference; save a provisional configuration in one, fail subsequent
packages or orders GET, retry once while still failing, then recover. Verify live
draft edits during failure survive, unrelated unsaved form remains marked/open,
saved form is clean, and exactly one real successful POST/configuration persisted.
Use existing configure action rather than fabricate contract authority in legacy data.
If runtime forbids configure on these rows, use a separately constructed authorized
fixture, not mocked mutation success.

PC-001: Hold a refresh/read-only retry after a real mutation; leave for #/time
with explicit unsaved-draft dialog handling. Release/abort held request; assert
Staff time capture and successful status read, no stale capacity status/focus
or new capacity reads/POSTs after departure. Separately inject named 401 through
local recovery; assert login stays rendered/focused, no retry/rerender/replay.
Scope only these exact expected failures; retain unexpected-error detection.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Prove manager destination/read/render success

Harness owns all new browser assertions. Map actual navigation hrefs to exact main
headings, relevant endpoint/query contracts and specific content/empty states.
An unknown navigation entry must fail as unchecked. Record successful browser GET
responses, unexpected API HTTP errors and requestfailed transports with current
route identity. External map requests intentionally blocked by loopback policy are
not local API failures or provider acceptance.

Capacity: compare actual GET rows to rendered package headings and work-order list
identities/count, not just independent context.request responses. Each injected
read/retry must recover to real rows. Cancellation must show Staff time capture
and its successful status read, not any non-error heading. Expected injections
are explicitly scoped; never blanket-ignore transport or console errors.
No more than two new helpers, no removed tests or new dependencies.

<!-- rpi:phase id=P02 -->
## P02: Validate and review

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run scoped and heavy local validation

Use existing source distributions and dev environment; install only on demonstrated
missing dependencies. Never inspect .env or default/private datasets. Generated
fixture uses fictional geography and explicit seed. Ruff strict E/F/I/B/UP and
format line length 100, Node syntax and API mypy precede heavy work.

Personally run nonblocking flock admission every 60s for at most 2400s; no foreign
resource/output access or interruption. Use each tool's own nonblocking lock and
explicitly record contention/race. After admission run generated --mssql harness
and API full suite with existing synthetic fixtures. SQL container is task-owned
and loopback-only. Preserve failures and cleanup exact owned resources.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile and obtain one original independent Review

Update plan/details/changes and actual command results. One fresh independent
worker assesses full correction boundary and prior retained repair, required
web rules, new regressions and evidence; write only new correction Review.
No in-task fix/review loop. Open material findings block P03 and route later.

Completion evidence for P02-T01: changes record contains all original adverse
attempts plus real SQL/Chromium PASS and full API 1154 tests/316 opt-in skips PASS.
Strict Ruff/format 100, Node syntax, diff and API mypy pass. Reversible,
archive/restore-verified generated cache/metadata relocation leaves no ignored
candidate inputs. No earlier RPI artifact was modified.

<!-- rpi:phase id=P03 -->
## P03: Publish exact candidate

<!-- rpi:task id=P03-T01 -->
### P03-T01: Commit, complete gate, verify and create PR

Commit implementation and original dated evidence on current topic. Author and
committer use returned gh id/login noreply email; required Copilot trailer.
Complete gate is mandatory for SQL-inclusive repair: new external directory,
current fetched origin/main, --all and nonqueued admission. Do not modify runner
or use skip flags. Arrange admission with caller's 60s/40m policy, runner
--lock-timeout 0, and retry only genuine pre-execution lock contention.

Full receipt external; any later candidate/base/tool/image/input change requires
a new valid gate. Fetch main again and verify immediately before separate
independent exact-head publication assessment and push. Keep that assessment
external too; it is not a second RPI Review. Push never force/main; create PR
to main with Refs #523, evidence and pending owner live verification.
Required hosted/owner approval remains pending; do not merge.
