---
applyTo: '.copilot-tracking/changes/2026-11-03/issue-920-expected-denials-changes.md'
---

# Issue 920 plan: quiet expected denials

## Overview

Single slice, no stacking. Details: [details](../../details/2026-11-03/issue-920-expected-denials-details.md).

## Checklist

* [x] Phase 1: `/api/me` reports `services.photo` and `services.law_alerts`.
* [x] Phase 2: client skips the four predictable denials and shows plain words.
* [x] Phase 3: unit test and Chromium check asserting no console errors.

## Critique (one pass, direct)

* Verdict: proceed. Server authorisation unchanged; client skips are only a courtesy.
* A 200 envelope instead of 503/403 was rejected: it changes existing API contracts and tests.
