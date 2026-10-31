# Review: issue 616

Execution: executed once. Outcome: conformant for the delivered scope; open items routed to follow-up.

* Proven: paged API tests, keyboard-reachable native buttons, status text that does not rely on colour, unpaged shape preserved, no animation added.
* Not proven (PR uses Refs): initial load time on the 60,000-home dataset; live check with the test user.
* Follow-ups: state filter for work orders; pager assertions in `capacity_browser_check.py`.

Correction cycle 1: four Copilot review findings (blank paging values, draft loss on page change, stale overlapping pager loads, capacity browser check envelope) were fixed with regression tests; the original Review outcome above is preserved. The browser check update remains unexecuted locally and relies on CI/human review.

Correction cycle 2: three further Copilot findings (overlapping pager refreshes, browser check paged envelopes, stale out-of-range retry guard) were fixed with regression tests; the original Review outcome above is preserved. The browser check remains unexecuted locally and relies on CI/human review.

Correction cycle 3: two Copilot findings fixed with source regression tests. (1) A failed page load now restores the last rendered offsets, so a later refresh cannot skip the orders confirmation or drop drafts. (2) Page changes (either pager) now confirm before discarding any unsaved appointment draft or New package, Record capacity, Issue work order or order-note entry; minimal confirm-before-discard rather than draft preservation. Original Review outcome preserved. Local: focused tests, ruff check, ruff format --check, node --check pass. Heavy gate not run.
