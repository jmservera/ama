---
title: Issue 153 pending-handoff HTTP refusal and error guidance plan
ms.date: 2026-11-11
task_id: 153-http-handoff-1111
---

## Objective

When the personal "Handoffs waiting for you" read ends in an HTTP refusal or error, or in a malformed success, the card states a fixed reason, a truthful unknown queue state, an existing responsible role and a safe manual next action. It shows no raw server text and never looks empty or successful. Refs #153 C3 only (initial increment).

## Status: prospective, NOT implemented

Planning only. No source or test edit, runtime run, Review or publication has occurred. Implementation resumes only after the coordinator confirms #1444 (issue #83 waiting-time screen) merged and this branch adopts fresh `origin/main` by ordinary merge.

## Scope and boundaries

* Change `src/api/src/zava_forward/api/web/app.js`: `pendingHandoffs` catch/then logic and one adjacent constant, placed after `const HANDOFF_READ_ERROR` and before `function pendingHandoffs` so existing source-slice tests keep working.
* Change `src/api/tests/test_handoff_read_guidance.py` only: update the two assertions that pin the old HTTP text and the constant-count guard, add bounded cases.
* Optional, recorded at implementation: one dated note in `docs/reference/research/ux/content-standard.md` and an append-only `docs/reference/log.md` entry. No `src/api/README.md` edit (#83 owns that file's new section; avoids a merge collision).
* Unchanged: `api()`, `fetchReadRetrying`, server, API, roles, permissions, storage, thresholds, both CSV download links, empty-list hiding, loading text, `AbortError` and 401 behaviour, the #83 screen/route/link, `/api/handoffs/unaccepted`, other panels.
* Not added: retry, polling, timer, new button, new request, mutation, named person, access approval or role grant.
* Tier: focused owner demo policy. No full gate, SQL, Docker, provider/model, real data, cloud or installs. Historical correction balance UNKNOWN; no repair allowance, no new default five, no transfer from other issues. Classified focused: `app.js` edit is a web copy change with no permission, secret, dependency, deployment, security-control or gate-semantics change.

## Design

Fixed ASCII copy, active voice, three parts (reason, owner, next action), content-standard vocabulary:

* Refusal (403), new constant `HANDOFF_DENIED`: "Your account cannot see the handoffs waiting for you, so we cannot tell whether any are waiting. Refreshing will not change this. Owner: your Retrofit Programme Manager or Programme Support Officer. Next action: ask them to check your role. Until then, ask the sender or open a case you already know, because the case list may not show every handoff waiting for you."
* Load failure (any other HTTP status, or a non-array 200), existing `HANDOFF_READ_ERROR`, unchanged text: reason, owner application support, next action refresh then contact application support.

Control flow in `pendingHandoffs`:

* `then`: if the value is not an array, paint the load-failure alert (card visible) instead of hiding. `[]` still hides; non-empty still renders.
* `catch`: `AbortError` returns silently (unchanged); `status === 401` keeps `Could not load handoffs: ${e.message}` (message is the fixed client string from `api()`; the sign-in screen has replaced the view); `status === 403` paints `HANDOFF_DENIED`; anything else paints `HANDOFF_READ_ERROR`. One shared paint helper keeps `h("p", { role: "alert" }, ...)` as the single alert element. No server `e.message` reaches the page except the fixed 401 string.

## Phases

1. Source edit (after #1444 merge adoption): constant and logic above.
2. Regression edit in `test_handoff_read_guidance.py` (details file).
3. Focused validation (listed in details), recorded in a changes record.
4. Original author Review once, state, commit; independent exact-head assessment before any publication.

## Success criteria

* 403: refusal copy with owner role and manual next action, no retry advice, no server text, card visible, queue unknown.
* 500, 502, 404, 429 and generic (no `data.error`) read errors: fixed load-failure copy, no server text, card visible.
* Transport rejection: unchanged message and behaviour.
* Malformed 200 (`{}`, string, number, null): load-failure copy, not hidden.
* Success, empty, download links, loading text, 401 and abort paths identical to base.
* One GET per render from card code; no automatic retry added; manual page refresh re-reads and shows rows when the read succeeds.
* #83 screen, navigation and its tests unaffected after main adoption.

## Out of scope and routed

Other panels' raw HTTP text, every-UI audit, the cold-start `fetchReadRetrying` policy, universal C2/C3, C5 named-human review, any acceptance tick or new issue.
