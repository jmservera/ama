<!-- markdownlint-disable-file -->
# Critique: aftercare hooks final correction plan (issue 133, C5)

Executed once on the final candidate plan by the same worker (no nested agents). Verdict: Approve, with compatible findings applied directly to the plan. No finding conflicts with a confirmed decision and no significant or divergent issue needs a user decision. No second critique will run for this task.

## Findings and disposition

* P1, lock exit: an error can come from the outermost lock exit after a classified save failure, or after a successful save. Applied: the classified error is kept and the exit error attached as a note; for an unclassified exit error the second step reacquires the lock before reading. Both paths keep a single mutator call.
* P1, determinism: the red test must not rely on sleeps. Applied: events pause A after its read; the test proves A holds the lock with a non-blocking acquire; B gets one bounded join whose outcome does not change the assertions (on C4 source B completes and A restores stale data; on fixed source B waits and A reconciles first).
* P2, ownership: re-rendering the form replaces the form element, so a captured element is an unsound owner check. Applied: the owner check is the session object, a module token and presence of the current `ac-form` in the page.
* P2, late reply: needs a held server reply, not a mock of success. Applied: the browser route handler performs the real fetch and delays only the fulfilment; the authorization outcome stays real.
* P3, hash routes: reusing hasUnsavedChanges would add a discard prompt that contradicts intentional draft retention. Applied: aftercare-specific listener, dirty set by the user's input event, not by pristine defaults.
* P4, typing: success requires the new tests and the adapter to be reported as actually checked. Applied: record the configured mypy file counts and show that the exemption lists no longer name the modules.
* P5, SQL: heavy-lock busy means a recorded hold, not a SQLite substitute. Already in plan.
* Out of scope baseline failures stay visible and are not waived. Already in plan.
