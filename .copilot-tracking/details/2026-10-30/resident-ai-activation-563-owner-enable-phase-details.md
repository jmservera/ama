---
title: Resident AI 563 owner-enabled activation details
ms.date: 2026-10-30
---

Task: 563-owner-enable-20261030T1710Z / resident-ai-activation-563-owner-enable.
Research C1-C10 and plan FR1-FR6/AC1-AC6 apply. Owner monitors actual cost;
no live ledger pre-read or SQL networking/migration is admitted.

<!-- phase: P01 -->
## P01: Preserve and activate

<!-- task: P01-T01 -->
### P01-T01: Runtime and exact backup

Actual system playwright import/pip-show failed in Research. Restore
playwright==1.64.0 into a new session-owned external venv; use available
Chromium or install its pinned runtime only after missing-browser failure.
No repository manifests or shared runtimes modified.
Private root: current session files/resident-owner-enable, mode0700;
process umask077. Capture exact stdout bytes for app/revisions/auth/jobs and
read-only employee app config; files0600, SHA256 recorded. No secret list/show.
Validate baseline optional vars absent, expected image, SQL msi/client and
existing resident identity/account-only role; fail before mutation on mismatch.
Original active revision must be unique100%, min0/max1 and all jobs Manual.
Capture command argv/time/exit without raw secret-bearing outputs.

Completion: backups durable before any Azure write; rollback data validated.
Executed: protected original and attempt2 backups/hash annex retained.

<!-- task: P01-T02 -->
### P01-T02: One credential-safe browser baseline

GET /healthz timeout180s, up to three retries with delay, no heavy lock.
Anonymous POST /demo/assistant: expect403/401.
Real Playwright Chromium, clean ephemeral context, no recording/debug/trace.
Navigate domcontentloaded with180s; mask email/password before reading
~/.ama-resident-test-user inside automation. Exactly two nonempty lines,
credentials never output. Count login attempts persistently before submission,
maximum2 across helper restarts; intended1. Stop on401, no blind retry.
Clear fields and secret variables when no longer needed, close on exit.
Open Chat, verify consent starts unchecked; rat question produces consent
error without assistant POST. In browser-origin fetch, valid CSRF and
use_record=false must return400. Consent then send same rat question;
expect200 disabled AI rules label, housing officer and no generated label.
Do not retain raw view/account records; retain only projected source strings,
labels, Boolean checks and bounded synthetic response with secret exclusion.

Completion: baseline safety assertions pass before mutation; browser context
stays alive for T03. Baseline failure means no Azure mutation.
Executed: both baseline runs passed, one login200 each, total2/2; no more login.

<!-- task: P01-T03 -->
### P01-T03: Enable, verify or restore

Use az containerapp update -g ama -n ca-resident-demo --set-env-vars with only
the two plan values and a unique revision suffix; output captured privately.
No min/max/image/secret/auth/job/identity flags. Mutation-start marker persisted
before subprocess; capture failures and always enter restoration thereafter.
Warm health and check ready revision; compare new template modulo two vars/
suffix, unchanged shared config/identity/auth/jobs/employee.
Reload same browser, existing authenticated session must remain valid; if not,
stop or use remaining login attempt only for a documented session-loss cause,
never guessed credentials. Explicitly grant fresh chat permission.
Send one rat question. Require200 AI-generated, pest acknowledgement, honest
cause uncertainty and housing officer; no assertions of safety or work sent.
Require known host sources, initially closed details; label height<=24px,
font<=0.85 parent, weight400, no padding/border. Record response/label/source
checks without private case payload. Send capital-of-France question; require
rules label, finite-task limitation and manual route, no generated answer.
Repeat no-consent denial safely; no model request should be sent.
For grounding, compare actual response claims in memory with /demo/view's
progress/next_step/closed only and chat.py's exact host repair guidance.
No case-summary invention, visits, channels, response times, diagnosis or
sent-report claims are permitted. Store claim category, host source category
and support verdict; unsupported/indeterminate verdict triggers restoration.
Do not confuse recognized source labels with entailment or human acceptance.

Any failed changed candidate: remove only the two added env vars and wait for
the restored revision to become latestReady with Succeeded provisioning.
Verify min0 and restored100% active traffic. Compare backed-up template modulo suffix and
app-wide configuration/identity/auth/jobs/employee. Warm health. Do not delete
the failed revision or reset any accounting. Single mode cannot retarget
traffic to an old revision; no mode change is permitted. Preserve exact
effective backup in a fresh revision. SDK emits empty value alongside unchanged
secretRef; normalize only that inert empty member, never reference/value changes.
Do not treat update exit0 or health served by an old revision as new readiness.
If restore update fails, attempt original revision activation and report exact
state; protected writable template excludes SDK-only imageType/null fields.
No deletion/new-resource fallback.

Completion: either live activation meets all required checks or restoration
is proven with explicit Unmet activation and actionable failure evidence.
Executed through rollback: ready enabled configuration passed; browser
enabled_live timed out before response proof. Exact substep/cause unavailable
because exception details were deliberately suppressed. Original failures
preserved. Fresh ready owner-safe-173404 revision serves100%, exact effective
original template/config/identity/auth/jobs restored, health200/anonymous403.
No actual AI/grounding/thin-label/enabled out-of-scope acceptance claimed.

<!-- phase: P02 -->
## P02: Reconcile and persist

<!-- task: P02-T01 -->
### P02-T01: Evidence reconciliation

Changes artifact records every command/result and safe helper hashes/external
annex. Reconcile plan markers and actual outcome, cap/expiry unchanged,
owner cost monitoring, zero role/secret/SQL/network/job/employee mutations.
Distinguish source/runtime accounting guarantees from uninspected ledger.
Keep failed attempts and original predecessor outcomes. No whole issue or
human acceptance. Runtime fallback must not become AI success.
Executed: original-to-final effective template/config/identity/auth/jobs all
equal; employee configuration preserved; raw private data and credentials
not exported. Unknown whether an enabled assistant request reached server:
no observed HTTP response and request-event timestamps were not persisted.

<!-- task: P02-T02 -->
### P02-T02: Independent Review and local persistence

Activate rpi-review once with bounded independent reviewer: supplied artifacts,
safe external result projections and helper source only, no credentials/raw
config/cloud/browser/model access. Preserve Review execution/outcome and
route findings later; no return to Implement or repeated Review. Material
unresolved defects block acceptance, even if locally committed.
Resolve gh api user; repository-local noreply email for both author/committer.
Stage only new continuation evidence and commit with Refs #563 and Copilot
trailer. Fetch main, run full gate externally after commit. Use existing
runner's lock-timeout600 (its native flock corresponds to flock -w600);
do not double-acquire the same lock in an outer process. If implementation
of native locking differs, use an equivalent single-holder arrangement,
never bypass serialization. No locks around Azure/browser operations.
Preserve actual gate failures externally; evidence-only closeout commit may
record outcome but invalidates exact-head receipt and cannot claim publication.
Never push, open PR, change issue checkboxes, close issue, merge or amend.
