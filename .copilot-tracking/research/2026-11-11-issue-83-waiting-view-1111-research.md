---
title: Issue 83 read-only handoff waiting-time screen research
ms.date: 2026-11-11
---

## Brief

* Task: `issue-83-waiting-view-1111`. Branch `feat/demo-handoff-waiting-view-83-1111`, worktree `/home/azureuser/source/ama-demo-wt/issue-83-waiting-view-1111`, pinned starting main `7880b95b19525ff465cab27870ba9d55b57110a3`.
* Purpose: decide whether an on-screen read-only waiting-time view of the existing scoped `GET /api/handoffs/unaccepted` projection is missing, and the smallest coherent entry point and tests.
* Output mode: convergence. Posture: `focused` (bounded internal task, named source targets, supplied owner scope). Provenance: caller brief.
* Non-goals: new fields, route, persistence, permission, threshold, scheduling, automated escalation, provider or cloud call, CSV export change, ticking C3, closing #83, new issues.
* Interaction: `vscode_askQuestions` unavailable (non-interactive run); inputs sufficient, so no question was asked.
* Delegation: none. Lanes were small, tightly coupled and read-only; all three waves ran inline (fallback recorded). No `RPI Researcher` worker ran.
* Extensions: repository instructions (selected, caller-listed authority); `web-design-guidelines` skill (selected, rules fetched W1); company/regulatory agents skipped (no resident or regulatory claim is made).

## Evidence

Codebase (C#) and external (W#) IDs.

| ID | Evidence |
| --- | --- |
| C1 | `src/api/src/zava_forward/api/web/app.js:753-776`: `pendingHandoffs()` calls only `GET /api/handoffs`, hides its card when the list is empty (`:757`), shows status, owners, due, next action, and two CSV links (`:760-761`). No elapsed time and no call to `/api/handoffs/unaccepted`. |
| C2 | `src/api/src/zava_forward/api/web/app.js:897`: the card is rendered only in the "mine" list view. |
| C3 | `src/api/src/zava_forward/api/server.py:738-751`: `/api/handoffs/unaccepted` JSON, optional `max_age_hours` (never defaulted), 403 for non-staff, 400 for bad limit. |
| C4 | `src/core/src/zava_forward/core/workflows.py:60-84`: `handoff_ageing` fields `case_id,status,age_hours,due_at,chase_owner,chase_owner_code,proposed_receiver,escalated,needs_escalation,reasons,approved_limit_hours,limit_note,as_of`; reasons come only from the handoff's own due time (and a limit when one is supplied). |
| C5 | `src/core/src/zava_forward/core/workflows.py:322-350`: `pending_handoffs` and `unaccepted_handoffs` use the same state set (`HANDOFF_PENDING`) and the same party-or-manager filter. |
| C6 | `src/api/src/zava_forward/api/workbench.py:17-80`: navigation is server-supplied per role and covered by role matrix tests; `#/import` is a precedent for a non-navigation route reached by a list-header link (`app.js:901`, route `:445`). |
| C7 | `src/api/src/zava_forward/api/web/app.js:410-422`: unknown route uses `destination?.scope || "Case workspace"` as the screen-reader route status. |
| C8 | `src/api/src/zava_forward/api/web/app.js:2100-2106`: accessible table precedent (`table-scroll` region, caption, `th scope`). |
| C9 | `src/api/tests/test_unaccepted_handoff_download_ui.py` and `test_handoff_read_guidance.py`: Node slice between `function pendingHandoffs` and `let briefingBox` plus opt-in Chromium cases with a loopback `Served` fixture; `ZF_BROWSER_TESTS=1`. |
| C10 | `src/api/tests/test_handoff_api.py:140-167`: existing route contract tests (scope, no default limit, 400, 403, 404 on POST). |
| W1 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md retrieved 2026-11-11 (full text retrieved). |

GitHub history (retrieved 2026-11-11 with `gh`): issue #83 body (C3 unchecked); comment 2026-10-27 (OD-09 timings needed); closure audits 2026-10-31 and 2026-11-05 (comment `IC_kwDOUU8JX88AAAABjIwreg`: independent read-only ageing screen using the existing scoped route is allowed engineering, OD-09 times remain a human decision); comment 2026-11-11 `IC_kwDOUU8JX88AAAABlLxfRg` (this increment).

## Wave 1: wider

Candidate ideas: (a) new screen route with list-header link; (b) new server navigation destination; (c) expand the pending card; (d) link from the pending card only; (e) fetch with `max_age_hours`; (f) escalation action buttons. Source inventory: grep of `unaccepted` across `src/` found the route, CSV link, role inventory and tests only; no screen exists in `app.js`, `role-screens.js`, `panels.js` or `ops.js`.

## Wave 2: deeper

* The two projections have identical scope (C5). A non-manager party has a non-empty personal list exactly when the unaccepted queue is non-empty; the difference is representation: the card disappears when empty (C1), and ageing is absent from it.
* Therefore reachability for staff with an empty personal list requires an entry point that does not depend on the card (rules out d). Card load failure must not block the screen.
* Option (b) changes `workbench.navigation` for every role and its matrix tests and administrator access labels; larger than needed. Option (a) follows the `#/import` precedent and is available to every staff role that reaches the list views; the endpoint still enforces 403.
* C7: the unknown route would be announced as "Case workspace"; a one-line scope label avoids a misleading route status.
* Policy: C4 shows age alone never sets reasons without a limit; the UI must show "Approved limit: not set" and distinguish a due-time reason from mere age. (e) would invent a threshold and is rejected. (f) is excluded by the brief.
* The API returns no resident name or address; the screen links to the case by id only (manual path). No new field is allowed.

## Wave 3: contrarian

* Could an equivalent screen already ship? Source search (C1, C2) and issue history (#1419 delivered CSV only) say no; the 2026-11-04 r6 research recorded the staff screen as excluded by an earlier owner note, which the 2026-11-11 brief and comment now supersede for this one increment.
* Could a screen mislead? Risks: green or empty on failure; age read as lateness; implying escalation is automatic. Mitigations: failure and malformed responses render a fixed alert with no table; fixed policy sentence; reasons shown only as supplied; no action buttons.
* Does a permanent link add noise? One extra link in an existing header row; accepted.
* Validation honesty: a "personal list empty, queue present" case cannot occur through real data (C5). It is exercised by failing only `/api/handoffs` while `/api/handoffs/unaccepted` succeeds (card load failure), and by Node stubs; this limitation is recorded rather than hidden.

## Historical correction balance (recovered, not inferred)

* #83 RPI history found: `src-handoffs-83` (2026-10-15), `issue-83-r1` (2026-11-03), `r5` and `r6` (2026-11-04), and #1419 chain (2026-11-10). The r5 review records one Review, conformant for its slice, with the screen routed as follow-up; r6 records a docs-only slice. None of the retrieved records states a correction allowance, a spent count or a remaining count for this UI lineage.
* Conclusion: historical remaining correction authority is Unrecorded (Unknown), not five and not zero. This brief authorises one initial increment and no post-review source correction batch. Prior #131, #132 and #134 allowances do not transfer. If Review requires source correction, the exact finding goes to the coordinator for admission.

## Synthesis and decision

* Accepted: option (a), new route `#/handoff-waiting`, implemented in `app.js` only, linked from the list-view header row in both views; fixed scope text; table of the existing fields; as-of; fixed policy text; visible alert on any failure or malformed payload; read-only refresh button; route status label.
* Rejected: (b) larger blast radius; (c)/(d) card hides when empty and cannot reach empty-queue staff; (e) invents a threshold; (f) outside brief.
* Deferred: OD-09 approved times, escalation routes, scheduling and operational acceptance (human decision, not supplied by fixture or company agent).
* Whole #83 remains unaccepted; C3 is not ticked by this increment.

Research disposition: executed. Planning Readiness: Ready.

## Next Steps

Plan phase for this task (parent-owned continuation).
