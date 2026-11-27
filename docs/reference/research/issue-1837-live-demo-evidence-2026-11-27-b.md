---
title: Issue 1837 re-run evidence (run b), 2026-11-27
description: Fresh unit and axe evidence for the standalone nomination forms; synthetic demo only
ms.date: 2026-11-27
---

Refs #1837. Synthetic loopback fixture, Chromium, desktop. Base `a5b36579c2`. Files are in `issue-1837-live-2026-11-27-b/`.

* The fix on main holds: the standalone forms axe run posted three requests, all HTTP 200, with no axe violations and no controls under 24 px; the challenge axe run passed.
* `tests.test_nomination_api_routes`: 12 tests pass, zero skips.
* Defect found in test code only: the inherited failure-path test read the form feedback before the page script wrote it and failed once under host load. It now waits for the text first.
* Open observation: `checks.nomination_browser_check` (read-only nomination view) times out at a 5 s call in `nomination_review`; not part of the standalone-form fix and not diagnosed here.
* Unproven for the demo: live Azure submissions (irreversible records in the shared demo), independent exact-head review and hosted CI (need publication).

The per-criterion table is in `.copilot-tracking/changes/2026-11-27-issue-1837-live-b-changes.md`.
