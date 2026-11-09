---
title: "Plan and details: issue 233 tensions correction 3"
description: Region-label checker correction
author: Copilot
ms.date: 2026-11-05
ms.topic: reference
---

Tier FOCUSED; no production, CSS, route, fixture or policy change. Light validation only; no heavy lock, browser or gate.

* Add `tests/test_atlas_tensions_checker.py` (page doubles, no browser): absent, empty, whitespace, no-region, valid reach and unreached cases.
* Prove RED on the intake helper, then require every label to be a non-blank string.
* Run role conformance, atlas trace, stronger Ruff, format 100 and strict mypy with external caches.

Critique (single pass): compatible; no assertion redesign.
