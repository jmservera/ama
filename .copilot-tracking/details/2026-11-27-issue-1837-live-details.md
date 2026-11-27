# Issue 1837 details, 2026-11-27

Phase 1: one test in the existing nomination API test file. Stale version arises from a second JSON ack through the API after the page loads; assert status >= 400, feedback equals the server `error`, focus on feedback, button enabled; then abort `**/resident` and assert the offline message and enabled button; finally the stored acknowledgement reference is the other session's value.
