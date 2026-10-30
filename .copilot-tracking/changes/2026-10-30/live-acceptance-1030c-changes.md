<!-- markdownlint-disable-file -->
# Changes: live-acceptance-1030c

Task ID: live-acceptance-1030c-2026-10-30. Date: 2026-10-30.
Declared scope: full bounded evidence plan, no application modifications.
Research executed / Ready. One critique Complete / Revise, direct dispositions
recorded in plan. Bounded execution complete; acceptance Partial / Not accepted.
P01-T01/T02 and P02-T01 complete. P02-T02 Review and persistence next.

## Plan and Evidence Pointers

* .copilot-tracking/research/2026-10-30/live-acceptance-1030c-research.md
* .copilot-tracking/plans/2026-10-30/live-acceptance-1030c-plan.md
* .copilot-tracking/details/2026-10-30/live-acceptance-1030c-phase-details.md
* .copilot-tracking/plans/2026-10-30/live-acceptance-1030c-critique.md

## P01: Guarded Live Execution

Runner/test implemented. Pre-live commands:

```bash
/tmp/mv/bin/ruff check --no-cache .copilot-tracking/changes/2026-10-30/live-acceptance-1030c
/tmp/mv/bin/ruff format --check --no-cache .copilot-tracking/changes/2026-10-30/live-acceptance-1030c
/tmp/mv/bin/python -B -m unittest discover -s .copilot-tracking/changes/2026-10-30/live-acceptance-1030c -p 'test_*.py' -v
```

Final results: Ruff pass, two files formatted, eight constructed safety tests
passed. Initial lint/format failures corrected before live execution. Tests
cover literal parsing, origins, diagnostics, canary output, durable admission/
restart refusal, cap, fixed failure output and Node-executed strict binding
projection. They do not prove all browser cleanup/crash interleavings.
No credentials read or login performed by those tests.

Next exact live command:
`/tmp/mv/bin/python -B .copilot-tracking/changes/2026-10-30/live-acceptance-1030c/acceptance.py`.
Capture-free evidence and durable manifest are the only generated outputs.
Each started login counts; runner never re-enters after a submitted/uncertain
credential. One attempt per site is selected initially; two is a ceiling.

### First live run: 13:55:20-13:59:54 UTC

Exact runner hash before/after:
bfca66bdc4623e35c33f056497613592d417a3db3e98d61363b64bd2fe8e10ee.
Original acceptance.py, manifest.json and evidence.json remain unchanged.
Both health endpoints returned 200 after 31.7s/44.6s warming, not failures.
Resident authenticated on its one attempt and proved consent-blocking, explicit
"AI not enabled" fallback/housing-officer route/no AI label, multi-turn thread,
Enter/Send/newline, scroll/pinned composer and three-width geometry.
Employee used one submission, reached Stay signed in and handled No, then
exhausted the full 180s settling window without verified admission.
No employee feature checks ran. Both contexts and browser closed.

### Immediately relevant second-slot amendment

The first employee run observed KMSI after a completed password action; this
is not an unknown-delivery retry. Its diagnostic defect is that failed
/api/me boolean projections were not retained, so the cause stays unknown.
Use only the second and final caller-authorized employee launch in a separate
supplemental runner. Cryptographically bind the immutable first evidence and
manifest, require completed cleanup and observed KMSI, and retain only boolean
binding/origin/status diagnostics. No resident rerun. No repeated submit within
either attempt. If the second launch fails, stop with the two-slot cap.
Additional owned outputs: second/attempt2.py, second/manifest.json,
second/evidence.json. This narrow output-budget increase preserves original
executable/evidence provenance rather than overwriting failed history.

## P02: Reconciliation, Review and Local Persistence

### Second and final employee attempt: 14:01:22-14:04:25 UTC

Command:
`/tmp/mv/bin/python -B .copilot-tracking/changes/2026-10-30/live-acceptance-1030c/second/attempt2.py`.
Supplemental exact runner hash before/after:
861d494e8665fa057d07534b5f1ce0bf3db6015d4b212b50b7a238d06596f356.
Original first source/evidence/manifest hashes were verified before admission.
Final offline command used the same explicit unittest selector: nine passed;
Ruff passed after formatting supplemental code. No new dependencies installed.

Health returned 200 immediately. Password action completed, KMSI No handled,
app origin reached, /api/me returned 200 with valid schema, trusted-proxy
provider, programme-manager role and not-view-only projection.
However `expectedIdentity=false`, `rosterBound=false`; therefore this run
does NOT verify admission as the requested Aadi account. No raw identity,
claims, response body or exception was retained. A different/missing email
claim, alias, tenant mapping or account fault is not diagnosed by that boolean.
The first run did not retain failed binding projections; it cannot be
retroactively assigned this second-run cause.

Both employee slots are consumed. No third login, no reuse of historical
session material, no employee chat/map/case branch executed. Context/browser
cleanup recorded. One of two resident slots consumed, with no resident rerun.

### Per-step command and result ledger

Full UTC start/finish and predicates are in the immutable JSON steps.

| Step command/action | Result | Boundary |
| --- | --- | --- |
| First employee GET /healthz, timeout 120000, retries up to 3 | HTTP 200 on first try, 31.7s | Warming delay, not failure |
| Public employee GET /chat-widget.js | HTTP 401, empty-body hash | Not a deployed widget mismatch; protected asset unavailable anonymously |
| Resident GET /healthz, timeout 120000, retries up to 3 | HTTP 200 on first try, 44.6s | Warming delay, not failure |
| Resident GET /chat-widget.js | HTTP 200, SHA256 a3ae12e567df405ff7bcf9394d2f74e2d06367480e560e6d0b9f5078d38bd849 | No employee matching bytes available |
| Resident actual masked form login | HTTP 200; authenticated content visible; fields cleared | Exactly one resident attempt |
| Resident Chat via Enter | Visible native dialog, bottom-right, live log, composer and Send | Attach/Voice disabled with reason |
| Rat Enter without consent | Explicit consent error, zero assistant POSTs | Client ordering only |
| Check consent, rat Enter | Actual POST after recorded consent time, one reply | AI not enabled, human route, no AI label, collapsed sources |
| Shift+Enter then status via Send | Newline/no new message, second actual reply, four ordered messages, chat open | No raw answer retained |
| Escape/reopen, focus, direct log scroll at 1280/390/320 | History retained, focus returned/visible, no page overflow, composer stable/below log, exact bottom | Browser semantics only |
| Reduced-motion emulation | 150ms normal token to 0s reduced | No full animation/AT assessment |
| Employee attempt 1 actual Entra form | KMSI No handled; 180s elapsed without accepted projection | No feature branch |
| Employee attempt 2 GET /healthz | HTTP 200 | App warm before final attempt |
| Employee attempt 2 actual Entra form and /api/me | HTTP 200, schema/provider/role true; expectedIdentity false | Requested identity not established |
| Employee chat widget | Blocked, not executed | Identity guard, not a feature failure |
| Employee expanded map filters | Blocked, not executed | No live marker/keyboard/narrow proof |
| Employee single-case view | Blocked, not executed | No live icon/density/blocker/tab proof |

### Complete 24-entry criterion matrix

"Partial" and "Unproven" mean missing compound evidence, not necessarily
product defects. Scoped Proven never accepts a whole both-site issue.
No issue checklist was edited.

| ID | Criterion | Outcome | Evidence and missing boundary |
| --- | --- | --- | --- |
| 550-01 | Both sites share component and bottom-right popup | Partial | Resident rendered use proven; employee/public asset protected, no matching bytes or rendered use |
| 550-02 | Persistent scroll thread, newest bottom, pinned input, remains open | Partial | Resident four ordered messages, exact bottom, direct scrolling, stable composer and reopen proven; employee untested |
| 550-03 | Enter sends, Shift+Enter newline, Send | Proven, resident only | Actual rat Enter and second Send; newline/no message; employee untested |
| 550-04 | Compact in-composer selector changes employee skill and shows active | Unproven | Resident fixed selector present; employee switch/reply not reached |
| 550-05 | Attach/Voice present or disabled with reason | Proven, resident only | Both disabled with visible reason; employee untested |
| 550-06 | Actual AI content thin label and collapsed sources | Unproven | Actual rules/fallback sources collapsed with no AI label; AI not enabled |
| 550-07 | Resident consent precedes data use | Partial | Client explicit error/zero POST then consent-before-POST; server/model data-use order not observed |
| 550-08 | Rat question relevant answer or honest human route, not home summary | Proven, resident | Actual rat fallback explains disabled AI and human route; no home-summary predicate true |
| 550-09 | Loading after 200ms, errors, keyboard/screen-reader semantics, reduced motion | Partial | Actual consent error, native keyboard/live/focus/Escape and motion proven; exact loading timing and AT untested |
| 551-01 | Expanded-map compact top-edge header filters | Unproven | Employee identity guard prevented map observation |
| 551-02 | Filters update markers/header consistently | Unproven | No actual map/filter API agreement or restored-header proof |
| 551-03 | Keyboard/non-colour/narrow map readability | Unproven | Employee branch not reached |
| 551-04 | Behavior covered by browser/unit test | Partial, source coverage | C5 tracked browser assertions inspected, not executed against fresh deployment |
| 552-01 | Presentation icons and labels on steps | Unproven | Source C6 exists, no live case/icons or served provenance |
| 552-02 | Visibly thinner reduced-height workflow | Unproven | No live case or trusted deployed-before baseline |
| 552-03 | One-line blocker and full keyboard/touch disclosure | Unproven | No employee case or real blocker reached |
| 552-04 | Attached tabs outside inner scroll, panel below scrolling | Unproven | No live case geometry/interaction |
| 552-05 | Fluent 2 and WCAG baselines preserved | Unproven | Resident scoped basics do not establish case/whole-baseline preservation or AT acceptance |
| 552-06 | Desktop/narrow case browser evidence | Unproven | Resident chat geometry does not substitute for employee case |
| 563-01 | Consented repair question gets grounded AI answer/collapsed sources | Unproven | Disabled AI cannot prove enabled model or grounding |
| 563-02 | Thin AI label; fallback explains why | Partial | Disabled-AI reason and no incorrect AI label proven; actual AI label unavailable |
| 563-03 | No resident data reaches model without consent | Partial | Client no POST proven, not server/model non-use proof |
| 563-04 | AI unavailable shows fallback and housing-officer route | Proven, resident | Actual rat reply matched disabled-AI and housing-officer predicates |
| 563-05 | Authenticated live Playwright proves all above | Partial | Authenticated fallback proven; enabled model/label/grounding and server non-use not proven |

Count: four scoped Proven, eight Partial, twelve Unproven. No whole issue
accepted. No AI/model execution or assistive-technology/conformance claim.
Refs #550, Refs #551, Refs #552, Refs #563 only.

### Pre-Review reconciliation

P01 and P02-T01 completed as bounded execution/evidence, not employee feature
acceptance. P02-T02 remaining: one original independent Review, local commit
and complete gate attempt. Original failed/partial evidence and critique are
preserved. No product repair, Azure/policy/role writes, remote publication or
issue mutation. Current branch descends from freshly fetched main 29eab2e5;
redeployment PR #566 identifies payload main a72cb268, but live executable
parity was not independently attested by these browser predicates.

Web Interface Guidelines fetched in full 2026-10-30 before execution.
No changed application web files to audit. This scoped runtime rerun is not
a fresh full-source guidelines review, axe run or WCAG acceptance.

### Follow-up items

1. Reconcile authoritative requested-account projection with expected identity
   using owner/identity-admin evidence before any separately authorized login.
   No cause is inferred from false expectedIdentity or false rosterBound.
2. Then complete employee widget/skills/map/case live acceptance and shared
   rendered-component proof; all currently blocked, not diagnosed failures.
3. Separately authorized enabled-AI and human accessibility acceptance remain
   outside this disabled-model/browser-only run.

## Original Independent Review and Parent Dispositions

Original record:
.copilot-tracking/reviews/logs/2026-10-30/live-acceptance-1030c-review.md.
Execution Complete; outcome Not accepted; one High, two Medium, one Low.
Review independently verified immutable hashes, first/second bindings, attempt/
cleanup/timestamp/matrix counts and strict synthetic binding projection.
It did not perform live authentication, full unittest/Ruff or complete gate.
Its separate runtime restrictions are reviewer-local, not a parent prohibition.

* RV-001 High retained: requested employee identity and all employee feature
  acceptance remain unverified. Route to later identity research, no third login.
* RV-002 Medium retained: original 550-05 "visible reason" assertion exceeds
  the executable check, which establishes nonempty associated description text
  but not its rendered visibility. Current parent claim for 550-05 is therefore
  Partial, not Proven. The original matrix and JSON remain unchanged historical
  evidence; no new observation or verified closure is asserted. Effective
  conservative totals are three resident-scoped Proven, nine Partial and
  twelve Unproven. Later runner/evidence work must add visibility predicates.
* RV-003 Medium retained: fault-path cleanup, injected ordering, uncertain
  delivery and concurrent interleavings were not fully tested. Actual successful
  cleanup is not blanket failure-path proof. Route to later runner/test hardening.
* RV-004 Low retained: later acceptance coordinator must reconcile all
  outside-scope owners across planning/handoff. This parent routing record
  carries identity owner, runner maintainer, acceptance owner, model owner and
  accessibility owner without naming unavailable human appointees.

No source repair, new live run, repeated critique or second Review follows.
Original PC-004 disposition is partially verified by actual tests, not fully
discharged. Human approval remains unchecked and unclaimed.

## Local Persistence Preparation

Authenticated GitHub account resolved with `gh api user`: id 8036360,
login jmservera. Both author/committer use repository-local
8036360+jmservera@users.noreply.github.com, required Copilot trailer,
Conventional Commit and Refs-only references.
Exact allowlisted task files only; original critique and Review included.
No push, PR or issue mutation. No ignored task artifacts observed.
Before complete gate, actual shared-lock inspection found no holder.
Fresh fetched main 29eab2e50dd7f958ea2f8d385411562e5573e8e9 matches branch base.

Implementation/evidence commit is next, then full nonqueued gate to an external
session directory. Gate outcomes are not inferred from nine targeted tests.
Git-commit skill's referenced commit-message instruction file and
get_changed_files tool are unavailable. Existing repository Conventional
Commit, narrow allowlist, git staged inspection, privacy-safe identity and
required coauthor rules are used; no broad staging fallback.

## Local Commit and Original Complete Gate

Original implementation/evidence and dated critique/Review committed locally
as 040e2a4a5fe7d858d6b99bf21455c6990e8fe712. Author and committer use the
authenticated privacy-safe address; required coauthor trailer retained.
All fourteen allowlisted files committed, no foreign or ignored files.

Command:

```bash
python3 tools/rpi-checks.py --all --base 29eab2e50dd7f958ea2f8d385411562e5573e8e9 --lock-timeout 0 --out /home/azureuser/.copilot/session-state/c954d59d-b202-4376-b450-a9e92fdcc546/files/live-acceptance-1030c-original-gate
```

Result: exit 1, full-scope receipt status failed, sealed 2026-10-30T14:37:52Z.
Lock acquired without waiting at 14:10:08Z; runner selected one worker.
Preflight, core, agents, orchestrator, importer, namespace, static, infra,
migration, four image groups and logo-0600 are in the receipt's completed
groups. Project-api failed its unexpected required integration/dependency-skip
guard, including disposable SQL selectors and opt-in browser tests.
Browser and MSSQL groups did not execute; receipt sql is empty.
This is not a successful complete gate and does not prove SQL/browser coverage.
Original raw failure list, commands, group logs and receipt remain external:
the output directory above and sibling live-acceptance-1030c-original-gate.log.

No product or gate-tool repair, skip token, cloud fallback, protection change,
Azure action, push or extra live sign-in. Existing gate failure is a separate
validation/publication blocker, not a diagnosed deployed-site defect.
Fresh origin/main still equals 29eab2e50dd7f958ea2f8d385411562e5573e8e9.

P02-T02 complete as original independent Review, local persistence and an
honest complete-gate attempt; no passing gate or human approval claimed.
This final parent metadata commit invalidates the first receipt as exact-final-
head evidence. Final same-command run uses the new external directory
files/live-acceptance-1030c-final-gate and sibling .log; its result stays external
in files/live-acceptance-1030c-closeout.json to avoid another receipt-invalidating
commit. Original source/evidence/critique/Review remain unchanged.

## Parent Closeout

All bounded plan tasks complete. Research, Plan, Implement and one Review ran
in order. Overall live acceptance remains Partial / Not accepted, with three
resident-scoped Proven, nine Partial, twelve Unproven after the explicit RV-002
qualification. No issue accepted or checklist changed.
Automatic task transitions to Follow-up / completed; session remains running
for an explicitly selected later work item, with no child started here.
Ranked later work: identity reconciliation; runner predicate/fault-path hardening;
employee widget/map/case acceptance; separately enabled-model acceptance;
named human accessibility/AT acceptance. Full-gate failure is a prerequisite
for any later publication. No further source repair or Review in this task.
