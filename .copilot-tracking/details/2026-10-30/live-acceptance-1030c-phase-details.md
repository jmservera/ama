<!-- markdownlint-disable-file -->
# Phase Details: live-acceptance-1030c

Task ID: live-acceptance-1030c-2026-10-30.
Plan: .copilot-tracking/plans/2026-10-30/live-acceptance-1030c-plan.md.

<!-- P01 -->
## P01: Guarded live execution

### P01-T01

Implement a fresh synchronous Playwright runner using existing /tmp/mv runtime.
Use requests through browser request context to warm public health endpoints,
three tries each with 120s per request, saving HTTP status or cold-start result
only. Never inspect credentials during warmup or tests. Exclusive task manifest,
two launch slots per site, persist submission intent before password action.
Offline tests cover parser, count admission, exclusive invocation and sanitization.
Reject DEBUG/PWDEBUG/Playwright logging settings before secret access; disable
core dumps. Catch browser errors to fixed status codes without exception text.
Exact HTTPS application/provider origin validation before each secret action.
No console/network listeners retaining content, no recordings or page dumps.
Test synthetic canary exclusion, diagnostic rejection, origin refusal,
restart/concurrent refusal, pre-action durable intent and cleanup on failure.
Stop a site after uncertain password delivery rather than retrying credentials.
Retry safe pre-credential navigation within a launch; fresh launch counts again.
Completed P01-T01: eight offline tests and Ruff passed, both live health
requests returned 200 with long warmup waits. P01-T02 first run: resident done,
employee KMSI observed after submit but no admission within 180s.
Second-slot amendment permits only the remaining employee attempt after
immutable first-run cleanup/KMSI/hash verification, never an unknown-delivery
resubmit. Supplemental files and provenance are recorded in plan/changes.
P01-T02 complete as bounded execution. Final employee slot reached app origin
and HTTP-200 /api/me, but expectedIdentity=false, rosterBound=false. Strict
guard stopped all employee features. Total two employee/one resident attempts.
No further live execution in this task.

### P01-T02

Resident: mask email/password before filling, actual login, clear fields.
Consent error before any assistant POST, then explicit consent, actual rat
question Enter, second own-case-status question Send, Shift+Enter no request.
Record only fallback predicates, sources state, role ordering and geometry.
Employee: normal Entra entry and supported password route only. Require
visible provider password input, one Sign in, optional Stay signed in No,
then allow 180s at app/callback before /api/me. Poll authoritative endpoint
without credential retry. No auth repair, policy change or unsupported route.
After confirmed admission, actual widget/skill, map filter/marker API agreement,
and read-only case navigation. No notes, case mutations, consent-to-works
or consequential actions.
Desktop 1280x900 and narrow 390/320 widths. Keyboard/touch browser events
may establish scoped interactions, never native AT acceptance.

<!-- P02 -->
## P02: Evidence reconciliation and persistence

### P02-T01

Map actual observations to 550-01..09, 551-01..04, 552-01..06 and
563-01..05. Keep compound failures/unknown subparts explicit. Identical
public widget SHA256 across both sites plus rendered uses supports reuse.
Record source/deployed parity limitations, no unperformed checkboxes ticked.
Reconcile plan/details/changes before Review.
P02-T01 complete: changes record contains all 24 outcomes and per-step ledger,
with immutable JSON timestamps/hashes. Four resident-scoped Proven, eight
Partial, twelve Unproven; no whole issue accepted.

Atomic observation map (any missing required subpart prevents Proven):

| IDs | Required observation and safe projection |
| --- | --- |
| 550-01 | both rendered launchers/dialogs, bottom-right geometry, equal public widget hashes |
| 550-02 | ordered multi-turn messages, stays open, close/reopen persistence, direct log scroll and fixed composer |
| 550-03 | Enter request, Shift+Enter newline/no request, Send request |
| 550-04 | employee select inside composer, change selection, next actual reply identifies selected skill |
| 550-05 | both attach/voice controls disabled with visible reason |
| 550-06 | actual AI reply, thin label, collapsed sources; disabled AI means Unproven |
| 550-07 | client no request before consent; server data-use ordering unknown, Partial at most |
| 550-08 | actual rat question gets repair/human route, not home summary |
| 550-09 | natural 200ms loading, errors, keyboard/log/live/focus/Escape/motion; absent timing/AT means Partial |
| 551-01 | expanded map compact filters at top, compare text size before/after expansion |
| 551-02 | actual selected filter API total equals markers/status, state restored on exit |
| 551-03 | actual Enter/Space activation, aria-pressed plus Selected text, 390/320 containment |
| 551-04 | existing tracked browser coverage C5; live check adds actual no-fixture execution |
| 552-01 | six loaded decorative journey-icons and adjacent labels; provenance source-only unless bytes verified |
| 552-02 | measured step heights; no trusted before baseline means Partial at most |
| 552-03 | one-line summary, actual full disclosure keyboard and touch; no blocker means Unproven |
| 552-04 | tablist outside panel scroll, panel below, selected tab and panel linked, direct scroll geometry |
| 552-05 | scoped semantics/geometry only; full Fluent/WCAG and AT acceptance Unproven |
| 552-06 | actual case desktop and 390/320 geometry, no screenshots necessary |
| 563-01 | enabled grounded AI required; disabled deployment means Unproven |
| 563-02 | fallback explains why; actual AI label unavailable, compound Partial |
| 563-03 | client consent blocking does not prove model/server non-use; Partial at most |
| 563-04 | actual unavailable explanation and human route |
| 563-05 | authenticated Playwright proves scoped fallback only, not enabled-AI compound |

### P02-T02

Fresh independent read-only reviewer receives artifact pointers and exact
source/evidence hashes; no credential access or live execution. Preserve
original findings and route them to later work, no repair/second Review.
Resolve gh account and configure repository-local privacy-safe email, commit
only task files with Refs and coauthor trailer. Fetch main, run full gate
`python3 tools/rpi-checks.py --all --base SHA --lock-timeout 0 --out EXTERNAL`.
Do not wait on a foreign lock. Gate results remain external to avoid another
commit invalidating exact-head evidence. No push, no issue updates.
P02-T02 complete: original independent Review Complete / Not accepted,
implementation/evidence commit 040e2a4a, full gate exit 1 with failed receipt.
Project-api unexpected required integration/dependency skips blocked browser/
MSSQL groups. Parent metadata commit requires a final exact-head attempt;
its authoritative result remains external as named in changes.

Parent outcome qualification after original Review: original four-Proven
matrix is retained historical; RV-002 means 550-05 visible-reason assertion is
not proven. Current conservative totals: three scoped Proven, nine Partial,
twelve Unproven. No source fix, verified finding closure or second Review.
