# Details

Phase 1: replace lines "requests_at_end ... Enter ... requests nothing" with assertions that Next is disabled, Previous enabled, focus is programme-prev, and no extra request was made (len(paging_gets) unchanged). Remove the `check(..., True)` line. The later row-link block stays reachable.
Phase 2: append " Owner: you, the signed-in reviewer." before "Next action:" in HELD_CHECK_UNREADABLE; add a test with reason, Owner:, Next action: order and BANNED.
Phase 3: run the listed suites; confirm manifest digests unchanged.

Critique amendment (Phase 1): after Previous returns to page 1, assert focused == programme-next (syncPager) and press Enter, replacing press_until Tab.
