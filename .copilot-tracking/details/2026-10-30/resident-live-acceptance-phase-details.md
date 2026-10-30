<!-- markdownlint-disable-file -->
# Phase Details: resident-live-acceptance

Task ID: resident-live-acceptance-2026-10-30. Date: 2026-10-30.
Research Ready; plan Ready after one independent critique and direct dispositions.

<!-- rpi:phase id=P01 -->
## P01: Bounded live execution

<!-- rpi:task id=P01-T01 -->
### P01-T01: Safe real-form authentication

Reuse /tmp/mv/bin/python and Playwright 1.64.0 if available; restore a pinned
task-owned external runtime only after actual dependency failure. Launch Chromium with
an ephemeral context, no recording/storage-state/profile export. No MCP form
call containing credentials. Read ~/.ama-resident-test-user only inside the
script's execution function. Require two nonempty trimmed lines; no value or
identity diagnostics. Remove DEBUG/PWDEBUG tracing environment before import.
Never print exception messages (Playwright may include filled values).
Disable core dumps. Mask email and password as password inputs before filling.
Use the actual #signin-form and #signin-button with its loaded handlers.
Observe POST /demo/login status only, not request payload/response headers.
Exactly one attempt is planned; at most two allowed, but never retry a 401.

On 401: clear fields, collect non-secret visible error/status text only,
redacting both credential strings defensively; close context/browser, stop all
live work and record the documented generic-denial/limiter limitation.
The 401 branch must not collect public-chat geometry as post-stop activity.
Do not diagnose password/account/domain from generic denial.

Completion: executed-script fingerprint, one JSON with UTC times/browser
version and bounded actual outcome. Unexpected runtime failures emit fixed
stage/type and retain partial evidence, not success.

Execution: initial load timed out before credential read/submission. The
shared runtime subsequently lost its Playwright import; after this actual
failure a task-owned external venv restored playwright==1.64.0. Final real
form login returned 200, exactly one submission, 10:31:45-10:31:59 UTC.
Final script SHA-256 matches before and after; original timeout JSON retained.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Conditional authenticated resident observations

Only if form succeeds and authenticated content appears:
open Chat using its visible launcher with keyboard. Inspect consent checked
state before any question. If unconsented, try the user question and establish
no assistant POST is made and clear consent guidance appears, then check the
actual consent control. If already consented, record that and leave the initial
pre-consent transition unproven; do not reset backend consent. If indeterminate,
do not submit and mark consent/replies blocked. Ordinary portal record reads
are not assistant consent. After confirmed permission send the rat example by Enter.
Capture sanitized chat text only, not home/address/account fields; reject a
home summary as a relevant answer. Honest inability plus contact route qualifies.
Check a second supported question without writing workflow state; actual AI
label/sources only proven if an actual corresponding response occurs.

Observe a chronological scrolling thread, bottom-follow/pinned composer,
window remains open, Shift+Enter newline without send, Send button, active
selector (including fixed-only resident limitation), Attach/Voice disabled
with reasons, polite log/status/errors, labelled controls and visible focus.
Check 1280/390/320 CSS px, no horizontal overflow, Escape-close/focus-return,
reduced-motion emulation. Do not manufacture server errors or claim an exact
200ms loading threshold from a fast response. Do not inject fake AI answers.
No screenshot at any point, no raw page dump, no account panel.
No full AT/contrast/zoom/conformance or both-site shared-use acceptance follows.

Execution: initially unconsented, actual visible consent error and no
assistant POST; permission checked before two actual assistant requests.
Rat question by Enter received honest inability plus housing-officer route,
not home summary. Status question by Send produced the second answer.
Both rules-only; actual AI output/label remains unproven. Four-message ordered
log persisted across reopen, keyboard/reflow/motion basics observed at all
three widths. Exact 200ms loading and human AT were not performed.

<!-- rpi:phase id=P02 -->
## P02: Evidence reconciliation and local persistence

<!-- rpi:task id=P02-T01 -->
### P02-T01: Matrix and canonical reconciliation

Write each 550-01..09, 551-01..04 and 552-01..06 verbatim or faithfully
summarized. For each, outcome Proven or Unmet with direct evidence, missing
subparts, applicability and source-only caveats. Earlier 551-04 source coverage
is historical, not new live acceptance. Keep owner resident-dropdown observation
separate from employee criterion. On 401 all authenticated resident obligations
remain unmet; no feature defect is diagnosed. Amendments/divergences: none
unless discovered; disclose script changes after execution.

Execution: 19-row resident-scope matrix recorded in Changes; three resident
criteria proven, sixteen compound criteria unmet/not applicable or incomplete.
This does not accept or close any entire issue.

<!-- rpi:task id=P02-T02 -->
### P02-T02: One independent original Review

Fresh bounded worker activates rpi-review, reads the exact artifacts/script/
JSON and writes only original Review. No credentials, live auth, Azure,
source fixes, extra critique or nested workers. Record execution separately
from outcome. Route findings to later distinct work, never repeat Review.
Do not claim required human approval complete.

Execution: one independent original Review Complete, outcome Residual work.
RV-001 Medium routes missing resident evidence to later rpi-research.
RV-002/003 Low route employee/accessibility obligations to separate work.
RV-004 Low retains the historical-timeout source-replay limitation. All are
preserved, none repaired or re-reviewed in this task.

<!-- rpi:task id=P02-T03 -->
### P02-T03: Local-only persistence and external gate

Resolve gh api user and configure its ID+login privacy-safe email repository
locally for author/committer. Include Copilot trailer; message Refs #550,
Refs #551, Refs #552, never closing language. Stage only owned task files.
Commit original critique/Review as well as result. Fetch main (read only),
then use tools/rpi-checks.py --all --base current-origin-main --lock-timeout 0
with a new external directory. Retain external receipt/log even if blocked.
No Azure fallback, parallel duplicate gate, foreign lock inspection/output
reuse, remediation or push. Verify any successful final receipt; a blocked
gate is not publication permission. Any later commit invalidates a prior gate.
