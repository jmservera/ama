---
title: Resident chat logout and validation follow-up research
ms.date: 2026-10-28
---

## Research Brief

Task 520-logout-followup, slug resident-chat-520-logout-followup, is a distinct
child of 520-review-correction. Preserve that task's original Not accepted Review.
The owner explicitly authorizes all four manual RPI phases in this turn, not an
automatic-session mode switch. Scope is RV-002, then RV-001, required local
validation, normal publication and five verified Copilot thread resolutions.
No merge, deployment, az, secrets, .env or private data. Existing methods/files
are the implementation boundary. Output mode: convergence; posture: focused,
selected from the named defect and supplied evidence. Evidence root:
.copilot-tracking/. Audience: implementation and publication reviewers.

## Prior Knowledge and Extensions

Read original case study, addendum, reference index/memory, sector primer,
src/README.md, prior correction state, changes and original Review.
Read current PR #525, issue #520 and all five unresolved Copilot threads.
Repository guidance and rpi-research selected; web-design-guidelines loaded and
its complete current source fetched on 2026-10-28. No redesign is requested.
No specialist research worker: this is one coupled source trace. No interactive
checkpoint is needed because scope and boundaries are explicit.

## Questions and Direction Controls

* Q1: Can logout revoke the old login without writing shared replacement cookies?
* Q2: Can the existing harness prove delayed logout across different/same-resident
  login, together with all five original review scenarios?
* Q3: Which canonical gate operations can run without the prohibited az command?
* Caller lock rule supersedes the older no-retry guidance: nonblocking flock,
  retry every 60 seconds for at most 60 minutes; never bypass foreign ownership.
* Preserve original evidence; do not modify PR body or add a closing keyword.

## Cycle 1

### Wider

Current server logout writes two unconditional Max-Age=0 headers after token
revocation. Browser transition checks fence JSON/UI but cannot fence cookie
application. The existing browser harness already owns shared-context pages,
held responses and pinned axe; no replacement harness is needed (C1-C3).
Reflection: the response-cookie effect, not another JS epoch, is the root cause.

### Deeper

SessionCodec verification rejects revoked tokens. Ordinary sign-out therefore
does not require deleting the browser's HttpOnly cookie. Keeping the old revoked
cookie until its existing expiry or a later login avoids any logout Set-Cookie
effect. Existing sign-out calls start(), which revalidates the actual current
cookie and clears permission before rendering. Extend the existing logout unit
method and shared browser method; retain strict binding and replay denial.
Reflection: changing cookie deletion expectations is intentional, not weakening
authentication. The old token must remain unusable (C1-C4).

### Contrarian

JS-only guards, conditional server deletion and BroadcastChannel serialization
cannot protect a response already accepted before another tab's login. Dynamic
cookie naming would unnecessarily widen the session protocol. Retaining a
revoked cookie is safe only if replay fails and a newer login remains valid.
Test both different-resident and same-resident replacements, renew permission
on each login, assert exact browser cookies and protected view after release,
and verify old-token rejection. Canonical full-gate preflight always invokes az;
do not run it or fabricate a full receipt. Run its independent non-az groups
with explicit partial coverage and retain publication blockers (C4-C5).
Reflection: actual browser execution and gate feasibility remain evidence gaps,
not reasons to redesign or claim acceptance.

## Evidence Log

| ID | Finding | Source |
| --- | --- | --- |
| C1 | Logout revokes, then unconditionally clears shared cookies | src/api/src/zava_forward/api/resident_demo/app.py:548-563 |
| C2 | Sign-out clears local state then checks the actual session | src/api/src/zava_forward/api/resident_demo/web/demo.js:350-422 |
| C3 | Existing shared browser checks and all five scenarios are present | src/api/checks/resident_assistant_browser_check.py:32-167,287-322,367-381,482-496 |
| C4 | Existing real HTTP logout/replay regression owns cookie assertions | src/api/tests/test_resident_demo_api.py:403-414 |
| C5 | Full runner includes az in tool preflight and infrastructure commands | tools/rpi-checks.py:71; src/README.md:69-156 |
| C6 | Prior original Review identifies exact open defects | .copilot-tracking/reviews/logs/2026-10-28/resident-chat-520-review-correction-review.md:169-224 |
| W1 | Current Web Interface Guidelines, fetched in full 2026-10-28 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md |

## Synthesis and Decision State

Accept response-side-effect removal, server revocation, and real delayed-browser
regressions. Reject JS-only and cookie-naming alternatives for the reasons above.
Defer human/resident, assistive-technology/native zoom and real-model acceptance.
The branch is clean at 618777a2; open PR #525 is the matching workstream.
Fetched remote topic remains 685547ed, already an ancestor; no new bot commit
requires rebase at research intake. Main is 413ccaf253fce4566e855bae9d0a924b2a82b506.
Shared heavy lock was actually held by PID 38089; do not interrupt it.

Research disposition: executed. Planning Readiness: Ready for bounded fix and
validation. No additional research cycle is indicated: the relevant source
trace and counterexamples are resolved. Full-tier publication remains conditional
on required exact-head evidence, and az-dependent validation is explicitly
unavailable under caller direction. Self-check: claims trace to evidence;
unknown validation is not represented as a pass.
