---
title: Resident chat review correction phase details
ms.date: 2026-10-28
---

Task: 520-review-correction. Plan:
.copilot-tracking/plans/2026-10-28/resident-chat-520-review-correction-plan.md

<!-- phase: P01 -->
## P01: Protocol and behavior

P01-T01: app.py verifies cookie then compares header to verified sid with constant
time comparison before personal view, chat, or agenda work; the header binds a
verified login and never selects an identity or exposes cookie credentials.
demo.js keeps the response sid tab-local, sends it on every protected request,
and clears personal page/transcript plus chat and callback permissions and
pending controllers on broadcast or server mismatch. A notification is not the
security control: loadView and assistant callbacks must fence replies by the
captured tab sid/generation so a delayed old reply cannot repaint a new login.
Use existing SessionCodec.verify random sid, with no core or CSRF change; retain
pre-opened same-CSRF sign-in usability. Extract the simple existing chat.words
helper and reuse it for route and period selection so punctuation does not turn
morning/afternoon into a different token. Cover same-account re-login as a
distinct per-login sid, not merely a resident change.

PC-001: use one tab transition epoch across start/session/login/logout/view and
failure handlers. BroadcastChannel messages are hints, not ordered authority;
fenced GET /session compares server sid against current local sid without adopting
identity/permission. Ignore hints on anonymous pre-opened sign-in pages. A delayed
hint after newer local login revalidates current sid and leaves it intact.
Test held session response, stale failure and delayed hint after newer login.

PC-002: require exactly one 16-character lowercase ASCII hex header; reject
duplicates/joined/malformed values with 409 and no personal reads or mutations.
Verify cookie first; sid alone never authenticates. Apply to view/chat/agenda
and logout so stale tabs cannot sign out a replacement login.

P01-T02: assistant.js manual route selects only a visible native control: callback
heading/email when available, sign-in or error retry when applicable, otherwise
the launcher while loading. This avoids focusing hidden or stale controls.
Capture the submitted draft untrimmed and clear only if the current field still
equals that captured value after a successful reply; a typed-ahead draft survives
both delayed success and failure. Before an appointment reply starts automatic
agenda search or focus, require the same current generation and an open panel;
Escape/outside dismissal therefore leaves focus unchanged. Do not cancel an
already confirmed callback reservation when withdrawing record use.

<!-- phase: P02 -->
## P02: Evidence

P02-T01: Client stores response session_id separately from its cookie jar and
sends X-Resident-Session for each protected view, chat, and agenda path. Test
wrong, missing, and old sid rejection before personal reads or mutations; correct
same-resident re-login; and an old cookie/header after authentication is absent.
Test punctuated morning/afternoon preference searches return only the matching
offered slots, without converting proposals into reservations. Extend existing
tests without removals or new fixtures beyond the task-owned in-memory data.
Existing SQL/sensor/image direct view probes must also send the session_id header;
retain all prior forgery and cookie isolation expectations. No new test methods
or schema/SQL changes are needed for this caller adaptation.

P02-T02: Existing Chromium test owns page/context and route.fetch/fulfill. In two
pre-opened pages sharing one cookie context, sign in A then B and assert A's
transcript, permission/callback state, and pending work clear; prove A's stale
sid cannot act with B's cookie. Hold view/chat replies across a session reset and
assert response fences prevent stale rendering. Hold an answer while typing a
different untrimmed draft; assert the draft remains, while an unchanged submitted
draft clears on success. Assert page-error retry and loading launcher focus only
visible controls. Hold an appointment reply, dismiss by Escape and outside focus,
then assert focus is unchanged and no automatic agenda request occurs; manual
routing remains available. Run pinned axe plus explicit focus/state assertions
for every browser scenario. Fixtures remain in-memory rows and task-owned SQLite,
never private/default ZF_DATA or real SQL/model.

P02-T03: Existing installed Python 3.12 venv, API shared fixtures; no new
dependencies unless validation reports a missing dependency. Browser/full runs
must own the shared lock. Keep outputs external; record failures honestly.

<!-- phase: P03 -->
## P03: Publication

P03-T01: Fresh independent reviewer assesses source and evidence once; original
adverse outcomes remain preserved. Human/hosted approval never inferred.
P03-T02: Resolve gh identity immediately before commit, local noreply author and
committer. Full gate exact clean HEAD/current main, verify external receipt.
P03-T03: Fetch main, verify current receipt then independent exact-head assessment;
normal push to topic; resolve exactly five supplied thread IDs via GraphQL.
If remote topic advanced, no force: reconcile and rerun candidate gate.
