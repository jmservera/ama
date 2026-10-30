<!-- markdownlint-disable-file -->
# Phase Details: employee-acceptance-attempt-3

* Task ID: employee-acceptance-attempt-3-2026-10-30.
* Date: 2026-10-30.
* Plan: .copilot-tracking/plans/2026-10-30/employee-acceptance-attempt-3-plan.md.
* Initial direction: no application edits; one new bounded runner, one offline test module; no live attempts yet.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete as bounded investigation, access unconfirmed | P01-T01, P01-T02 |
| P02 | Complete as evidence/persistence/gate attempt, not acceptance | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Safe bounded execution

Context: prior Reviews reveal no password route and dormant callback/deadline/submit defects. Owner changed tenant configuration at 11:45Z; this task must not change it.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement and validate capture-free runner

* Targets: new attempt-3 runner and tests only; old runners/evidence unchanged.
* Parse trimmed line 1 as password and nonempty trimmed line 2 as TAP. Reject missing first line/ambiguous data. Never print lengths, actual formats, values or hashes of secrets.
* Prefer TAP via supported Other ways > Temporary Access Pass when present; never mislabel a password field as TAP based only on type. If a password page is offered and TAP is unavailable as a method, record available methods before bounded supported selection; do not guess.
* Pinned inputs: APP is the exact HTTPS employee origin in the user prompt; USERNAME is the exact supplied AadiK account (already public task context, never emitted as a claim). PROVIDERS are login.microsoftonline.com and login.microsoft.com from original real provider observations. Refuse missing/ambiguous inputs before browser launch; no expected value comes from a session.
* Exact expected identity is compared inside browser evaluation; only booleans leave. Concrete /api/me schema: object user and account; account.provider and user.auth_provider equal trusted-proxy; account.email case-insensitively equals configured account; user.role equals Retrofit Programme Manager and app_roles contains ZavaForward.ProgrammeManager; user.view_only is false; user.tid/oid are canonical GUID strings; user.code/email are nonempty strings. HTTP 200 protected nonredirected JSON is independently required. Optional user.bound object means roster-bound; unbound is permitted after authentication. No claims/keys/values leave this projection.
* Use remaining monotonic budget in every navigation/wait/action; bound each step and recheck before side effects. Preserve attempted/submission-unknown intent in fsynced task manifest before pressing Enter. Exclusively create this single manifest before any launch; any interrupted/incomplete/ambiguous manifest refuses a new invocation. Explicit continuation of the observed completed pre-username/pre-credential failure is allowed only with original source/evidence hash verification and exclusively held lock; consume remaining slot without reset.
* Offline tests use fake credentials and fake pages only; no secret read on import. Match plan ownership lock.
* Completion: passing focused unittest and Ruff, recorded counts; no live evidence claim from mocks.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Execute at most two sign-in attempts

* Read secret file only in guarded main automation. Disable core dumps/debugging and trace/video/HAR; no screenshots or state export.
* Count each browser context before app navigation; stop immediately on unavailable route even if second attempt unused. Second attempt only after explicit definitive rejection/failure that is safe to retry; never retry uncertain delivery, lockout, consent/MFA/enrolment/recovery challenge. Observed first-run initial /app failure reached no username/secret actions; public /app is HTTP401. Use the existing supported /.auth/login/aad?post_login_redirect_uri=%2Fapp entry for the FINAL remaining attempt (server.py normal sign-in target), no resource change.
* Native passkey Escape/Cancel then rendered Back/options/password/TAP controls allowed; no virtual credential/provider bypass.
* Capture exact sanitized provider DOM text/control labels only, not input values, scripts or authenticated body text; redact both secrets and identity before persistence.
* After admission, employee shell check exports only a flat boolean predicate mapping per feature; in-browser counts/geometry become comparisons, never exported. Offline serialization rejects numeric/string/list/nested nonboolean employee observations. API responses remain in page memory. Separate nonsensitive stage status can identify unperformed checks; do not encode an unperformed acceptance assertion as false. Questions are generic, no case/resident details and no consequential actions.
* Chat: actual Enter/Send, second turn, remains-open, scrolling/pinned composer, active skill, AI/rules metadata and collapsed sources. Natural errors retained; full 200ms/AT acceptance left unmet absent direct timing/AT evidence.
* Map: compact top header, keyboard selected/non-colour state and marker totals checked against same-origin in-browser reads, restoration and 390/320 widths. No private IDs/coordinates retained.
* Case: normal offered case link, no ID retained, desktop/390/320 geometry/icons/tab ancestry, keyboard and genuine emulated-touch blocker open/close. No record text/crops.
* Completion: exact runner hash + run evidence + manifest, <=2 attempts; failure/stop remains valid bounded execution, never acceptance.

<!-- rpi:phase id=P02 -->
## P02: Evidence, Review and local persistence

<!-- rpi:task id=P02-T01 -->
### P02-T01: Reconcile and append

* Record every original criterion individually in changes; strict compound decisions, with employee subparts distinct from original cross-site/resident requirements.
* Preserve original original Reviews and adverse JSON. Append new dated attempt-3 sections to both existing changes records, not historical rewrites.
* One independent read-only Review gets exact paths and evidence, no credential file, no live rerun, no repairs.
* Completion: all nineteen decisions, counts reconciled, stage markers and state consistent before Review.
* Execution 11:55Z: nineteen decisions recorded in current changes; dated attempt-3 sections appended to both historical changes records without replacing prior sections. New independent Review remains separate; parent may append a clearly dated continuation pointer to the old Review log after preserving its outcome.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Review preservation, local commit and gate

* Preserve one independent outcome and route findings to later work, no fixes or repeat Review within this task.
* Resolve gh api user id/login; repository-local privacy-safe author/committer address, required Copilot trailer. Stage only this task's files and intentional dated append sections.
* Local Refs-only commit, no push. Fetch main (read-only remote operation), full gate with new external directory. No concurrent gate queue/wait/bypass or prerequisite skips.
* Final result can remain external to avoid another receipt-invalidating metadata commit. Missing full receipt blocks publication; no publication is requested.
* Completion: local committed evidence plus accurate attempted gate outcome, clean final worktree. Human acceptance remains unchecked.

## Completion Evidence

P01-T01 complete: attempt3.py/test_attempt3.py created. Fifteen offline constructed tests pass, including actual Node-executed /api/me response projections, decoy field, both secret redactions, origin refusals, deadline expiry, durable interrupted/competing invocation refusal, two-attempt cap and unknown submit delivery. Ruff check and format pass using existing runtime. Initial format-only failure corrected before execution. No secret read or live attempt yet; P01-T02 is next.

11:53Z implementation update: first counted attempt stopped during initial /app navigation before username/secret actions; exact source and JSON preserved. One safe explicit continuation via the supported auth-entry consumes only slot 2; no-route/uncertain-delivery stops remain unchanged. Preserve one generated immutable first-run source snapshot before correcting the entry point. Rerun offline regressions before the final live attempt.

11:55Z completion: seventeen constructed tests and Ruff checks pass on final executed source. TWO of TWO sign-in slots consumed. Attempt 2 reached actual Enter password, filled/submitted once and reached Stay signed in, then app-origin observed on exception handling. No verified binding or employee features were returned. Retain raw conservative outcome submission_delivery_uncertain_stop alongside keypress_completed_not_authentication; it does not establish that the credential was never delivered or that authentication failed. Browser closed and scratch removed. P01 complete only as bounded investigation; current acceptance remains eighteen unmet plus inherited source-only 551-04. P02-T02 local commit/gate remains post-Review.

Original independent Review now Complete / Not accepted, task execution Partial, 2 High/2 Medium findings retained in its one original log. RV-001 later research, RV-002..004 later runner implementation, no repairs or repeat Review. Dated continuation pointers appended to original Review logs, preserving all original content and outcomes. P02-T02 local commit and full gate attempt are the only remaining parent work.

P02-T02 completion: original evidence/Review committed locally as 441bc564 with Refs #550, Refs #551, Refs #552 and required trailer, privacy-safe author/committer. Complete external local gate attempted against fetched main, blocked: candidate does not descend from reviewed main base. No checks/receipt, no bypass/rebase/merge/push. Final bookkeeping commit invalidates previous exact-head gate; a final same-policy attempt and closeout stay external. All bounded markers complete; feature acceptance remains Not accepted/Partial, with no further live attempts.
