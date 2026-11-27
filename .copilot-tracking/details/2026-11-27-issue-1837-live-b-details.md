# Issue 1837 details (run b), 2026-11-27

Phase 1: in the one test, after `button.click()` inside `expect_response`, wait until the `-feedback` element text is non-empty, then assert equality with the server `error`, focus and re-enabled button. Phase 2: validation runs and records.
