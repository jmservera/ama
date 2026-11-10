<!-- markdownlint-disable-file -->
# Research: aftercare hooks final correction (issue 133, C5)

Date: 2026-11-10. Task slug: aftercare-hooks-133-c5. Parent task: aftercare-hooks-133-c4.
Research disposition: executed. Planning Readiness: Ready.

## Pinned input and authority

* Frozen C4 input: HEAD 9efdeb0149a2945780dcc8e58208833000d10327, tree 9e2e2cee6343480a47ba834abd3ef8286f245013, one commit on the reviewed parent a05b7e6b29145e620ca70f69c6f3f5c00be493c2 (declared parent branch feat/demo-quality-workflows-89-1109). Main d52f20a5 is not adopted; no merge, rebase or other source is imported. Held 132 and 189 and the CSV siblings are not copied.
* Budget: C1 to C4 spent. This is C5, the fifth of five, authorized once by Root to fix the three findings below. There is no automatic C6. The WAIT132 semantic exclusion is unchanged: only serialization was superseded for this bounded integration, never 132 acceptance.
* Independent reviewer 1de8d934 read all 24 files (1442 lines) of C4 and returned REQUEST_CHANGES: 2 High, 1 Medium. It executed no tests. Original findings and read ledger: root independent-133-hooks-c4-1110 (functional-findings.json, read-ledger.json). They are preserved unedited. Reviewer verdict is not an approval and this task does not invent an independent pass.

## Reproduction before any fix (scratch scripts outside the repository, preserved in root c5-repro-133-1110)

* F1 reproduced (repro_f1.py, real JSON Store, two threads). A's save fails; A's persisted read is paused; B commits and is acknowledged; A then restores its stale snapshot. Result: A raised PersistenceError, memory requests were empty (B's acknowledged request lost), and a later unrelated save left only the later request durably, so B was erased. Output: repro_f1.out.
* F2 reproduced (repro_f23.py, real Chromium against the owned loopback server). The session cookie was dropped so the POST received a real 401. The login screen was replaced: sign-in field count 0, stale aftercare form visible. Output: repro_f23.out.
* F3 reproduced (same script). With an edited draft a dispatched cancelable beforeunload was not prevented (False).

## Source findings that shape the fix

* `aftercare_store.py` update(): the lock is released before `_classify`; `_classify` reads persistence outside the lock and later re-enters the lock to restore. `Store.lock` is an RLock; `SqlStore.lock` is `_SyncLock`, a re-entrant lock that syncs from the database on the outermost entry and runs `_finish` on the outermost exit (which can raise after a commit). `SqlStore.save` has finished and released its transaction before it raises, so a read under the held lock does not open a read inside an uncommitted transaction. `dblock` is an RLock, so `_persisted` under the held lock cannot deadlock.
* Lock-exit ambiguity: an exception from the outermost `__exit__` happens after the lock is released. Recovery must reacquire the lock first (the entry sync refreshes memory from SQL) and only then read and reconcile, never restoring a snapshot taken before that acquisition.
* `app.js` `api()` on 401 sets `me = null` and calls `login()`; `show()` re-renders the app region. `route()` only runs for the current session `me`. `hasUnsavedChanges()` looks for `form[data-unsaved="true"]` or case state and is also the hash-route confirm gate, so reusing it would add an unwanted discard prompt on safe hash navigation and cannot see a form that is no longer mounted. The existing `beforeunload` handler calls it. An aftercare-specific listener is therefore needed.
* `aftercare.js` keeps the draft per actor in module memory (`acDraftState`), cleared on sign-out and actor change. `signOut` already calls `aftercareScreens.reset()`.

## Design decisions

1. F1: run failure classification and restoration inside the same `with store.lock` that performed the save. Lock-exit failure is recovered in a second step that reacquires the lock before reading. The mutator still runs once.
2. F2: each workspace view owns a token. After a submit settles it persists the draft and outcome and renders or focuses only when the session object is unchanged, the token is current and the form is still mounted. A confirmed receipt outside an owned view clears the draft without rendering. 401 therefore leaves the login screen intact.
3. F3: a single window `beforeunload` listener owned by `aftercare.js` warns while the in-memory draft is edited or unconfirmed. It is independent of hash routes, is cleared by a confirmed receipt, sign-out or a different actor, and uses no browser storage.
4. Typing: remove only the two C4 `ignore_errors` entries per project, annotate the new test modules, keep every earlier exemption.

## Boundaries

No auth or session implementation change, no models, real households, evaluator or resident accounts, payments, consent, safety or quality rules. No quality-note intake. Out-of-scope baseline failures stay unrepaired and unwaived: full API AdminHttpTests expired fixtures (PR1377), employee_workspace missing_ops_recovery original_ops==3, workspace_scripts exhaustion len(requests)==count.

## Web guidelines

Source refetched 2026-11-10 from raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md: HTTP 200, 8055 bytes, sha256 d246b026f4f29b5823a9cc857f9edf3d2507002e055e32040cadeaf3b38e0234, identical to the root copy. Installed redesign skill read; the Fluent 2, WCAG and plain-language baseline governs over generic typography. Keyboard and axe observations are constructed, not assistive-technology, WCAG or human acceptance.
