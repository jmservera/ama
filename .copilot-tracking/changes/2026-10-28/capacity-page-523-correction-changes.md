<!-- markdownlint-disable-file -->
# RPI Changes: Capacity page correction

## Metadata

* Task ID: 523-correction
* Task slug: capacity-page-523-correction
* Implementation date: 2026-10-28
* Plan: .copilot-tracking/plans/2026-10-28/capacity-page-523-correction-plan.md
* Details: .copilot-tracking/details/2026-10-28/capacity-page-523-correction-phase-details.md

## Execution Status

Full plan declared. P01 and P02 complete; the single correction-cycle Review is
Complete / Conformant with no new findings. P03 publication is the remaining
post-commit operational step, not a source correction.
One critique Complete / Revise,
PC-001 applied to required recovery-origin cancellation/401 scenarios.

## Execution Summary

Implement only ops.js, existing browser harness, directly related API README and
new correction artifacts. Preserve original evidence and prior compatibility fix.
No Azure, secrets, environment files, private/default datasets or foreign resources.

## Completed Work

### Draft-safe local recovery (P01-T01)

ops.js permits a no-mutation go() invocation; Try again uses that closure, not
route(). Captured signal is checked after mutation and catch ignores aborted or
ended sessions. Existing success-only draft restoration remains unchanged.
New browser scenarios exercise both failed endpoint refreshes, failed retry,
live draft edits, eventual success, saved cleanliness and exact one-POST persistence.

### Destination and read proof (P01-T02)

Harness now maps actual navigation to exact headings, content and expected browser
GET paths/query; records unexpected HTTP and requestfailed with scenario origins;
compares real browser response IDs/count to rendered package/order rows.
Recovery-origin cancellation/401 scenarios implement PC-001. README describes
the proof boundaries and separately constructed authorized fixture.

## Implementation-Time Plan and Detail Updates

The supplied contract helper must be used for a separately constructed authorized
mutation fixture: _proc_operation requires delegation even for configure. The
generated legacy read fixture stays unmodified through initial capacity/navigation
acceptance; then use existing supplied_contract_fixture for one explicit fictional
supplier. This is the plan's documented authorized-fixture alternative, not a
production grant or fabricated mutation response.

## Validation Record

* Procurement API module: PASS, 32 tests, 26.737s, clean inherited application environment.
* Node syntax and git diff --check: PASS.
* Strict Ruff E/F/I/B/UP 100 and format: PASS.
* API mypy: initial callback tuple-return errors, corrected with typed injection
  helper and separate listeners; PASS, 91 source files.
* Heavy-lock owner observed via lslocks: PID 4061333, python3. No foreign output read.
  Beginning caller-authorized nonblocking flock attempts every 60s, maximum 40m.
  SQL/browser and full API are pending admission, not passed.

### Heavy execution attempts and ordinary harness corrections

* First admission succeeded on attempt 18 after 17 one-minute busy intervals.
  Three early launcher attempts failed before SQL/browser because the external
  script resolved sys.executable to system Python without Playwright. Direct
  sanitized import of the installed API-dev interpreter passed; pinning that
  explicit interpreter fixed the launcher, without installing/unpinning packages.
* First actual owned SQL/browser run created and cleaned
  ama-capacity523-5010d7579c92, port 33216. It exposed a hidden closed-details
  form used as visible content. Corrected to its visible appointment region.
* Next run ama-capacity523-574d7ddd48d5, port 33217 proved 1 package/601 rendered
  orders, then correctly rejected missing fresh queue read. Hash-only page.goto
  can reuse navigation lifecycle; changed inventory/capacity setup to distinct
  full-document URLs so network/read evidence belongs to that visit.
* Next run ama-capacity523-259d5b66dfdc, port 33218 passed ten manager routes,
  then rejected the legitimate empty specialist-menu visibility. Added explicit
  no-installed-screens content proof and visible manual return link.
* These are ordinary test-fixture/assertion refinements under P01/P02 and the
  same critique; no production scope or user decision changed. All adverse logs
  remain in separate external validation directories, never overwritten.
  Required full-pass SQL/browser and API results remain pending.

### Real SQL Server and Chromium success

Final command (parent personally executed, clean application environment):

```bash
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp \
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests \
/tmp/ama-capacity-523-venv/bin/python src/api/checks/capacity_browser_check.py --mssql
```

PASS, exit 0. External log:
/tmp/ama-capacity523-correction-validation-20261028-13/sql-browser-1793212006552977822.log.
Seed 20260901, as-of 2026-10-13, fictional register: 980 cases, 443 open,
10 staff. Owned SQL Server ama-capacity523-b4fe8dc75f00, loopback port 33230;
container cleanup verified (no remaining task-labelled capacity containers).
Actual browser reads/render compared: 1 package, all 601 work-order identities.
Both failed endpoint initial retries, transport, structured 403, cancellation,
known-empty state and 401 passed. Both mutation/failed-refresh/failed-retry/
successful-recovery scenarios passed: exactly one real successful POST each,
saved form clean, other draft values/check/context/event/expansion retained.
Recovery-origin navigation and 401 passed without stale rendering or replay.

All actual manager destinations passed exact heading/content/read contracts:

| Route | Expected reads | Observed result |
| --- | --- | --- |
| #/ | facets, cases view=mine | PASS, matching queue rows/empty content |
| #/all | facets, cases view=all | PASS, matching queue rows |
| #/overview | stats, map | PASS, overview and team workload |
| #/visits | visits view=all | PASS, matching visits or explicit empty |
| #/funding | funding | PASS, response-matched table row count |
| #/finance | finance | PASS, response-matched rows or explicit empty |
| #/capacity | packages, workorders | PASS, actual rows and IDs |
| #/closed | cases view=closed | PASS, response-matched rows |
| #/assistants | assistants/proposals | PASS, role-owned content/empty state |
| #/time | time/status | PASS, exact recorded status |
| #/screens | No page-data read required | PASS, explicit no-installed-screens state/manual return |

No other confirmed same-class manager-page failure was observed in this local
inventory. This is not a map-provider, real-user, screen-reader or live claim.
Expected navigation aborts can produce server BrokenPipe diagnostics; exact
cancelled browser requests are scoped, not blanket-ignored transport errors.

Further adverse harness attempts (external directories 7-12) exposed positional
Playwright handler dispatch, same-URL no-navigation setup, pending parallel-read
abort timing, retry completion timing and a workorders/work orders copy mismatch.
Corrections bind injection status keyword-only, create fresh setup documents,
wait for both named requests before cancelling, wait for both successful recovery
responses and compare the actual plain-language label. Last re-admission acquired
on attempt 34, within its 40-minute authorized window. No failed receipt/log was
overwritten and no foreign lock/resource/output was used.

Final strict Ruff/format 100, Node syntax, diff check and API mypy all PASS
(91 source files).

### Full API and publication-input preparation

Initial full API invocation from repository root failed import discovery (8 errors,
928 tests/392.664s/128 skips). Re-ran the existing documented component command
from src/api, with absolute shared fixture paths in the sanitized environment:
`python -m unittest discover -s tests -q`. PASS, 1154 tests in 413.531s,
316 opt-in skips, exit 0. External log:
/tmp/ama-capacity523-correction-validation-20261028-14/api-full-1793212676882593075.log.
These general-suite skips do not replace the required full gate's real SQL suite.

The gate rejects ignored inputs. A finite selection of eight generated cache/
editable-metadata directories (62 files) was archived, fully read back, restored
into new external scratch and hash-verified before reversible relocation.
Archive, restored proof, preserved original trees and manifest:
/tmp/ama-capacity523-correction-generated-backup-20261028/.
No source or tracking artifact was moved/deleted; prior RPI evidence is untouched.
`git ls-files --others --ignored --exclude-standard` is empty.

Fetched origin/main remains 413ccaf253fce4566e855bae9d0a924b2a82b506.
Final tested source identities:
ops.js SHA-256 49b91f128719bb6968e8709caa891d2c6251b5dc01d80868e503b3bb74f772c3;
capacity_browser_check.py SHA-256 d32c617373ba3f91ff4f3e8d7c9c5cfcf23885fc848d24e8b4964aee84c39c46.

## Pre-Review Reconciliation

Plan/details/source markers and tested evidence reconciled. The single new
original independent Review completed with outcome Conformant and no new finding.
P03 remains pending commit, complete full local
gate, current-base receipt verification and independent exact-head assessment.
Original Review/critique outcomes remain unchanged. Live verification remains
pending owner; use Refs #523 only.

## Blockers

No current source/design/runtime blocker. Full exact-head publication gate and
assessment remain required, not yet passed.

## Remaining Work

P03/P03-T01 (publication). Final receipt, independent exact-head assessment and
operational state will be external; this is the committed pre-publication snapshot.

## Follow-Up Items

Owner live verification; historical RV-004/005/006 distinct UI follow-ups.

## Return-to-Caller State

Automatic parent completed Review; P01 and P02 complete. No new user decision
or material divergence. Prior test-harness/launcher refinements preserve approved
intent and the two-new-helper ceiling; no tests removed.

## Original Review Disposition

The new independent Review is Complete / Conformant, zero new Critical/High/
Medium/Low findings. It assessed full retained repair and correction source,
fresh web rules, tested source hashes and attributed runtime evidence. Original
adverse Review/critique outcomes remain unchanged. P03 is correctly pending, not
silently treated as approved publication. Owner live verification and historical
RV-004/005/006 remain distinct follow-ups.

Authenticated identity re-resolved with gh api user: id 8036360, login jmservera.
Only repository-local email 8036360+jmservera@users.noreply.github.com will be used
for author/committer. Conventional Commit and required Copilot coauthor trailer.
