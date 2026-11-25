---
title: Issue 1844 live r9 details
description: Phase details for the r9 plan
ms.date: 2026-11-25
---

## Phase 1: browser-free test

Parse `style.css` with `re`; no Playwright, no network. Assert the three rules above and that `app.js` still places the card in `.map-stage`.
