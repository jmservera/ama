---
title: Issue 1837 failure-path evidence, 2026-11-27
description: Browser test of the standalone nomination form error branches; synthetic demo only
ms.date: 2026-11-27
---

Refs #1837. Synthetic loopback fixture, Chromium, no live Azure write.

* New angle: the repaired script's failure branches had no browser test. `test_route_form_failures_show_feedback_keep_form_usable_and_write_nothing` covers a real server rejection (stale `expected_version`), the network-failure message, focus on feedback, button re-enabled and nothing extra written.
* Result: 12 tests in `tests.test_nomination_api_routes` pass; removing the button re-enable line in the script makes the new test fail, then the script was restored.
* No defect found; the earlier fix holds on base `b64c6e95dd`.
* Unproven for the demo: live Azure submissions (would add irreversible records to the shared demo), independent exact-head review and hosted CI (need publication).

Per-criterion table: see `.copilot-tracking/changes/2026-11-27-issue-1837-live-changes.md`.
