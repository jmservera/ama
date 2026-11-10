<!-- markdownlint-disable-file -->
# Plan and details: aftercare hooks final correction (issue 133, C5)

Task slug: aftercare-hooks-133-c5. Input: C4 HEAD 9efdeb0149a2945780dcc8e58208833000d10327. Research: .copilot-tracking/research/2026-11-10/aftercare-hooks-133-c5-research.md. This file is both plan and phase details. Refs #133, #89, #134 only.

Scope: aftercare_store.py and test_aftercare_store.py; web/aftercare.js; the existing aftercare browser check and served test; the two C4 typing exemptions and the new test modules' annotations; minimal README corrections. No change to the unchanged service, register, allowlist, roles, CSRF, projection, auth or session code. app.js is changed only if proven necessary (none expected).

## P1 F1 recovery under exclusion (aftercare_store.py)

* Red first: add a deterministic real-JSON two-thread test. A's save raises; A's `_persisted` is held by an event after it reads; the test asserts the store lock is held by A during the pause (non-blocking acquire from the test thread fails), starts B, gives B a bounded join, then releases A. Assertions: A raised a plain "Nothing was saved" PersistenceError (not unconfirmed); B succeeded; B's receipt, register entry, request index and actions are in memory, survive a reopened Store, and survive a later unrelated save; same-request retry of B replays idempotently; A's request can be sent again and is recorded once. Record the actual red on C4 source, then green.
* Fix: perform `_classify` (read persisted value, restore memory, map outcome) inside the same `with store.lock` as the save. If the failure surfaces only from the outermost lock exit, recover in a second step that reacquires the lock first and then reads and reconciles; if reacquiring or reading fails the result is the unconfirmed error with the notes and cause preserved. The mutator runs once; no retry, no restore of a pre-acquisition snapshot.
* Keep: unconfirmed versus not saved versus conflict mapping, notes, chained cause, SQL lock-exit and two-writer tests, replay without write.

## P2 F2 session and view ownership (web/aftercare.js)

* Each aftercareWorkspaceView call takes a module token and the session object. After the submit settles the continuation always persists draft values, request id, unresolved flag and message. It renders and focuses only when the session object is unchanged, the token is current and the form element is still mounted. A confirmed receipt in a non-owned view clears the draft and renders nothing.
* No change to api(): its login screen on 401 is left intact. Same-actor sign-in restores the draft and request id (existing actor key); another actor or sign-out starts empty.
* Browser regression: a real 401 on POST (session cookie dropped, no mocked authorization) leaves sign-in visible, no aftercare form or concerns text, then same-actor sign-in, draft and request id preserved, retry reconciles with exactly one concern. A late POST reply held by a route handler while the hash changes to a safe route must not overwrite the current page.

## P3 F3 document navigation guard (web/aftercare.js)

* One window beforeunload listener registered once by aftercare.js. Dirty means the user has edited the form since the last confirmed receipt, or a request id is unresolved. Clearing on confirmed receipt, sign-out reset and actor change. No browser storage. It does not use hasUnsavedChanges(), so safe hash-route changes keep the draft with no new prompt.
* Browser regression: edited draft warns, unconfirmed draft warns, including after a hash route change; confirmed receipt does not; hash routes keep draft and request id. Check both a cancelable beforeunload event and a real close with run_before_unload dialog.

## P4 Typing

* Remove the C4-added ignore_errors entries for test_aftercare_store and tests.test_aftercare_store (Core) and test_aftercare_served and tests.test_aftercare_served (API). Annotate or fix the two new test modules. Keep every pre-existing exemption. No blanket ignore, type: ignore or cast to hide a problem.

## P5 Validation (DEMO targeted tier, no full gate)

* Core: test_aftercare_store, test_aftercare, test_aftercare_intake, test_sqlstore, test_sqlqueues, scenario manifest, needs inventory, generator coverage if the workbench recipe input changes.
* API: test_aftercare_served, test_aftercare_screen, role/endpoint inventory, browser checks (aftercare, workbench). Known baseline failures are re-run for classification only, never waived.
* Static: Core and API ruff check and format, strict mypy for Core and API (adapter and new tests actually checked), node --check.
* Real disposable MSSQL for the changed adapter under the shared heavy lock, nonqueued flock -n, own container, zero unexpected skips. If busy, record the exact validation hold; no fallback.

## P6 Docs and closeout

* Minimal README corrections in src/core/README.md and src/api/README.md. Changes artifact, review (once, after implement-done), local commit, commit-complete witness, verify, refused stop event, handoff at root.

## Exclusions

Whole 133, 89, 134 stay unproven. No human, resident, deployment or model acceptance. No push, PR, merge, rebase or GitHub edits. C1 to C5 spent; no automatic C6.
