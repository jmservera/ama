---
title: Resident chat logout follow-up phase details
ms.date: 2026-10-28
---

Task 520-logout-followup. Plan shares this slug and date.

## P01

P01-T01: In existing Handler._logout, retain same-origin, CSRF, strict sid and
codec.revoke; return signed_in false with no cookies argument. Explain why a
revoked HttpOnly cookie remains until expiry/replacement, not a live session.
Extend the existing logout test to inspect actual headers, revoked token,
protected read denial and /session signed_in false. No methods removed/added.

P01-T02: In existing shared_session_checks, pre-open two pages, use one-shot
held logout routing. Fetch accepted response using stdlib urllib without a
cookie jar, forwarding the intercepted cookies/headers/body. This transport
cannot install response cookies into the browser. Assert browser cookies at
upstream acceptance and before release. On fulfillment retain upstream headers/
body and add only a test-only nonauthentication cookie marker; assert it appears
only after release to establish actual Chromium Set-Cookie application timing.
Wait for actual server response before signing into the second page. For
different-resident and same-resident replacements: capture new sid and exact
cookies, grant chat/callback permission, show own answer, fulfill held response,
wait for old-tab recovery and new-tab session recheck; assert cookies/view/
transcript/permissions survive. Inspect successful logout response has no
Set-Cookie. Replay old cookie via isolated request headers must be 401.
Require unchanged full authentication cookie; allow CSRF expiry refresh from
/session but require its value and security attributes unchanged.
Retain all existing cross-tab/malformed-binding and ordinary sign-out checks.
Do not remove the corrected times=1 session/view synchronization.

## P02

P02-T01: Run focused HTTP test before heavy work. Existing
checks.resident_assistant_browser_check --axe with hash-checked axe 4.10.3,
constructed fixture, loopback and fresh external output. Acquire
/tmp/ama-rpi-heavy.lock with flock -n; every failed attempt waits 60 seconds,
total at most 3600 seconds. Keep descriptor open throughout browser execution.
Record lock timeout as Blocked and stop affected execution, never bypass.
All five original scenarios remain required: session isolation, punctuated
periods, manual retry/loading focus, typed-ahead draft, dismissed callback focus.

P02-T02: Use installed src projects and documented test fixture paths. Run all
owning unit suites and prescribed Ruff/check-format100/mypy, JS syntax and diff.
Inspect canonical gate to execute only its independent non-az operations; no
az command even for version checks, no gate modification or false full receipt.
Keep validation output external, no ignored generated inputs in candidate.

## P03

P03-T01: Reconcile all markers, actual results and blockers before a fresh
independent rpi-review for this distinct child only. Prior original Review is
never rerun or rewritten. Route findings to later work, no Review loop.

P03-T02: Resolve gh api user, derive local noreply author/committer identity,
Conventional Commit plus required Copilot trailer. Fetch remote; rebase only
if newly required by caller's bot ancestry direction. Commit before final
exact-head gate; later commit/base changes invalidate receipts.

P03-T03: Repository requires current-main exact-head full receipt before push.
If mandatory az makes this impossible, record blocked publication and do not
push or resolve threads using partial evidence. Never claim hosted/human
approval. If all prerequisites are met, fetch main again, verify the external full receipt
against current origin/main, obtain one independent exact-head assessment,
then normal push and reply/GraphQL resolve only each fixed and verified thread.

## Current Execution

Research Ready; exactly one critique Complete / Revise, PC-001/002 adopted.
P01 implemented. P02-T01 passed actual final-byte Chromium/pinned-axe in
/tmp/ama-520-logout-browser-20261028-3, all five scenarios and both logout
replacement identities, 31 scanned states and zero reported violations.
P02-T02 complete: 2822 project tests (504 general-discovery skips), all project
Ruff100/format100/mypy; 10 non-az runner groups/77 commands including 263 SQL
tests (one enumerated JSON-only skip); 26 standalone Bicep builds and 26 lints,
all runner infra lint/type sets and 379 non-az infrastructure tests (zero skips).
All permitted checks passed. Permitted matrix retains an external
detached HEAD checkout plus exact source patch, never a purported full receipt.
Compiled az-dependent tests remain excluded even if standalone Bicep is run.
Four az-dependent infrastructure modules were excluded explicitly, not accepted.
Publication blocker is unchanged; P03-T01 original Review Complete / Not accepted,
no additional confirmed implementation defect. P03-T02 local commit prepared;
full-receipt/exact-head publication work and P03-T03 remain blocked. Review
RV-001 routes later validation evidence to rpi-research; RV-002 routes existing
unfixed image findings to a distinct maintenance owner. No repeat Review.
Six axe contrast incompletes and unfixed image vulnerabilities remain disclosed.
