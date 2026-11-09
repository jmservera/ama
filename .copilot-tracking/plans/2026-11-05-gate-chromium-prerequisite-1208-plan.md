---
title: Gate Chromium prerequisite plan (#1208)
description: Plan to install isolated Chromium before project-api in the local gate
ms.date: 2026-11-05
ms.topic: reference
---

* Phase 1: add red regressions (replay contract order, receipt rejection without install, runner order).
* Phase 2: add install_chromium helper; call it in Runner.run after the api install when project-api runs; add the install to required_checks for project-api; reuse the helper in Runner.browser.
* Phase 3: focused validation: tools.test_rpi_checks, isolated ruff and mypy --strict on the two tooling files; small native-browser check only under a nonqueued heavy lock.

Critique: executed once, self-review; compatible findings applied directly (keep browser-group install; no skip changes). Tier: focused; no full receipt for tooling alone. Details: [details](../details/2026-11-05-gate-chromium-prerequisite-1208-details.md).

