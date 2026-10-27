---
title: Resident assistant 469 phase details
description: Bounded implementation task evidence and completion conditions
ms.date: 2026-10-27
---

Task #469. Evidence IDs refer to the dated research artifact.

<!-- P01 -->
## P01 - Design and contracts

### P01-T01

First write docs/architecture/resident-assistant-prototype.md with explicit
owner decision and zero-spend local path. Compare local rules, small Azure
deployment and generated prose; no verified numeric quote. USD 4 reserved
inference allocation plus USD 1 headroom, expires 2026-11-01 UTC. Require
future atomic durable budget reservation before every external attempt.
Core accepts typed topic and authenticated view-derived status strings only,
not the reader/store, identifiers, address, email, measures or history.
Use authoritative C2 mappings, including unknown and closed states. Documents
unknown because C2 has no requests. Form advice never fills personal details.

<!-- P02 -->
## P02 - API and separate panel

### P02-T01

Reuse C1 authentication and C3 CSRF/origin/body checks. POST /demo/assistant
accepts only {"topic": enum}; no path/query/header case selection. Forbidden
extra body keys fail. Return source labels and mode/notice. Generic errors
never stringify exceptions. Provider protocol only selects topic; adapter
never receives case data. Strict Azure HTTPS endpoint/deployment validation,
no redirects, bounded reply read, timeout and no retries. Explicit enabled
flag defaults false, with mandatory token and reserve callbacks; no environment
auto-discovery. Shipped app always defaults deterministic. Fixed enum-only
ASCII prompt <=512 bytes and model max_tokens=16 define the reservation
envelope; failed/ambiguous attempts never refund reservation or retry.

### P02-T02

Separate assistant.js global mount function loaded before demo.js; demo render
mounts one panel. Native labelled select/form, three plain-language questions,
visible rules/advisory notice, person help and no action controls. Mark loading,
error and result with live announcement, preserve selected topic and focus.
Clear prior result on new request and prevent pending response writing after
sign-out/re-render via node connectivity. Use textContent, never innerHTML.
Reuse Fluent token controls and add only scoped panel CSS as needed.

<!-- P03 -->
## P03 - Verification and publication

### P03-T01

Core: topics, unknown/closed status, document unknown, form boundaries.
API: two different stages, forged selectors, missing auth/CSRF, revoked row,
malformed/oversized topic, injection, expiry, provider failure, no logs.
Provider: mocked HTTP only, disabled/expiry/reservation fail before credentials,
enum-only prompt, invalid output, redirection/error and timeout.
Assert max_tokens=16, prompt byte bound and reserve-before-token/transport order.
The host must reserve conservative cost for this exact envelope using verified
rates and durable shared USD4 accounting; that host is not activated here.
Browser: actual loopback server backed only by existing constructed fake rows,
native cookies and sign-in; keyboard topic/submit, source/advisory messages,
own-case difference, loading/failure/retry, 320px reflow and reduced motion.
No SQL and no actual model transport.

### P03-T02

Run full core/API unit discovery with normal shared test-fixture paths, ruff
and mypy changed Python, node syntax checks and the new browser selector.
One independent post-implementation Review preserves findings without an
implementation/review loop. Owner's scope replaces full 2-hour gate; never
claim that gate or hosted checks passed. Resolve GitHub account/privacy-safe
email, conventional commit plus requested trailer, push without force and
create PR against feat/resident-interactive with Refs #469 and parent dependency.
Implementation completion is the validated candidate and reconciled handoff.
The RPI parent owns the subsequent one-pass Review and publication actions;
those actions are not implementation-phase completion claims.
