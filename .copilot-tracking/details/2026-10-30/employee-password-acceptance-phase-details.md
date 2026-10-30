---
title: Employee password acceptance phase details
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

Task ID: employee-password-acceptance-2026-10-30.

## Final-Candidate Corrections

PC-001: Exact app origin is
https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io.
Username is the owner-supplied AadiK test account, defined literally inside
automation, never retained in output. Credential path is ~/.ama-test-user.
Provider HTTPS hosts: login.microsoftonline.com and login.microsoft.com only;
no userinfo, unexpected ports or host suffix matches. Revalidate immediately
before credential entry; callback and /api/me use the exact app origin.

PC-002: JSON object takes precedence when trimmed content begins with `{`;
accept exactly one nonempty string `password` or `Password`, reject malformed,
duplicates or ambiguous keys. Otherwise accept a first-line password:/password=
value (case-insensitive) preserving punctuation, or the trimmed first plain
line; trailing lines ignored, no alternate candidate retries. Empty/username
first line or password-like malformed keyed input is rejected.
Sanitize exact secret, encoded secret, identity/email and URLs before any
output. Never extract input values or raw exceptions. Offered text excludes
script/style/input DOM content. If sanitizer fails, capture only categorized
failure; exact-text requirement remains unmet. Constructed tests cover these
cases, including CRLF/whitespace, punctuation, malformed/ambiguous structures,
encoded variants and rejected origins. No actual file access in tests.

PC-003: At most 12 visible-control transitions, each fingerprint visited once
with at most two repeated-state observations while waiting; navigation <=60s,
action <=8s, total auth <=180s. Only offered password/other ways/sign-in
options/Cancel/Back and initial username Next are allowed. Escape dismisses
native passkey prompt. After one password submission, rejection, renewed
MFA/passkey, unexpected host, timeout or unconfirmed callback is terminal.
No second password submit and no other app navigation after no-route outcome.
Record exact sanitized final page text/controls, then close context/browser.

PC-004: No screenshots in this runner: omission eliminates pixel-capture
uncertainty and satisfies secret-field masking by never capturing that field.
No whole authenticated page/panel text extraction. Only allowlisted booleans,
geometry and control counts may be retained after callback. Owner explicitly
authorizes chat/map/case interactions at this exact employee demo site; that
direction, not authentication alone, is the interaction authority. No record
text, case identifiers, answers or pixels are retained; queries request generic
help without resident/case details. The critique's additional requirement to
prove synthetic provenance before any UI interaction is rejected where it
would contradict that explicit interaction scope. Synthetic provenance remains
unknown and no record/data acceptance is inferred. Its capture-safety concern
is applied through strict boolean/geometry extraction and zero screenshots.

PC-005: Finalize original Review/dispositions, commit evidence, fetch main,
record HEAD/base and clean state. Run
`python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <new-external-directory> --lock-timeout 0`.
If receipt exists, fetch and verify with
`python3 tools/rpi-checks.py --verify-receipt <receipt.json> --base <current-origin-main-sha>`.
Keep receipt/results external, do not amend to add them. Later commit, dirty/
untracked/ignored input or source/base/tool/image change invalidates success.
Non-ancestor, occupied lock or missing prerequisites block without repair,
waiting, skip or cloud fallback. No push.

<!-- phase: P01 -->
## P01: Safe employee browser evidence

<!-- task: P01-T01 -->
### P01-T01

Create a separate employee-only runner; never import/execute the old resident
runner. Parse JSON/keyed/plain first line without output. Prefer a single
unambiguous candidate; do not spray multiple credentials. Fail explicitly if
unsupported/empty. Test with constructed secrets only. Disable captures and
network logging; scrub exact credential, identity and URLs from offered text.
Use browser-owned ephemeral context, no session export. Bind executed bytes
and output bytes, close browser/context even on exception. Completion means
offline safety tests and syntax pass, not authenticated acceptance.

Completion: separate runner and 10 constructed offline tests; AST parse,
Ruff check and formatting passed before live execution. No secret access
by offline tests. Initial missing Playwright/Ruff restored only after failures.

<!-- task: P01-T02 -->
### P01-T02

Navigate /app, username Next, inspect the actual challenge. Use offered
password/other ways/cancel controls; Escape native passkey prompt if present.
Do not navigate to guessed protocol endpoints, call account-management APIs
or alter policy. Check visible password route after each supported transition.
If absent after ordinary alternatives, record exact sanitized visible page
text and controls, password_submitted=false, then terminate browser work.
If offered, read and trim file within automation, fill allowed provider field,
submit once, decline persistent sign-in, and require employee callback plus
boolean-only authenticated /api/me. Authentication failure is not missing roster.
If successful, observe bottom-right widget, Enter/Shift+Enter, selector,
AI/sources or honest fallback, persistence, expanded map filter updates and
single-case desktop/narrow geometry. Unobserved touch/AT/baseline/provenance
and resident obligations remain unmet. No unsupported success simulation.

Completion: four in-phase attempts, adverse intermediates retained and
disqualified where appropriate in changes. Definitive
`employee-102500-185604-evidence.json` (10:25:00-10:25:07 UTC) exercised actual
username Next, Escape, keyboard Back, then keyboard Sign-in options. Offered
passkey and GitHub only, no password/other ways/cancel control. No actual
password authentication, app callback, /api/me or employee features observed.
Browser/context closed and owned scratch removed; no live work after this stop.

<!-- phase: P02 -->
## P02: Evidence, Review and local persistence

<!-- task: P02-T01 -->
### P02-T01

List every original 550-01..09, 551-01..04 and 552-01..06 criterion with concrete
evidence and missing compound subparts. Preserve original logs, no historical
JSON corrections. Record manifest hashes, errors, checks and limitations.
One fresh independent rpi-review reads bounded artifacts only, writes its own
review and does not run live login/read secrets. Route findings to later work.

Completion: one independent Review Complete / Not accepted, preserved at
.copilot-tracking/reviews/logs/2026-10-30/employee-password-acceptance-review.md.
Five original findings routed once, no repairs or repeated Review. Complete
19-row matrix reconciled; actual acceptance and human approval unperformed.

<!-- task: P02-T02 -->
### P02-T02

Resolve `gh api user`; use local privacy-safe author/committer identity. Commit
only this task's new evidence and state with required coauthor trailer and Refs.
Fetch main; inspect lock ownership read-only; run complete external local gate
with nonqueued admission. Do not repair lineage, push, close issues, change
protection or claim gate success without verified exact-head receipt.

Completion: privacy-safe local original-evidence commit `6d29aa27` and full
nonqueued external gate executed against base
`63422cdf9fd477dd8892a27ac8b11487bc3a2429`. Initial admission rejected only the
task-created Ruff cache; archived/restored/byte-compared that exact cache and
moved it externally, touching no original tracking evidence. Full gate then
ran and failed on unexpected required API SQL integration skips. Browser/
MSSQL groups did not complete; no receipt pass. Original failed receipt stays
external at `/tmp/ama-employee-accept-6d309f30-gate-clean/receipt.json`.
Main advanced during this run; no source or lineage repairs. Final metadata
commit will receive its own fresh exact-head attempt with results external,
so no receipt is invalidated merely to commit that final result. No push.
