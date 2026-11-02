---
title: Issue 691 plan
date: 2026-11-02
---

* Phase 1: add a regression test that serves `/vendor/leaflet.js` through the real trusted-proxy provider with a genuine principal header, with and without a failing `identity.bind`, and checks the unauthenticated path is a 302.
* Phase 2: focused validation only (unit tests, ruff); no full gate (test-only change).

Critique (single pass, executed): compatible. The test strengthens evidence but cannot prove the live cause; the PR must use `Refs #691`.
