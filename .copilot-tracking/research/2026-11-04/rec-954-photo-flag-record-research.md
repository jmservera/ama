---
title: Research, issue 954 photo flag record
ms.date: 2026-11-04
---

## Disposition

Research disposition: executed (read-only). Planning Readiness: Ready.

## Evidence

* PR 993 (merged 2026-11-04) delivered `recheckPhotoService` in `src/api/src/zava_forward/api/web/app.js`: it re-reads `/api/me` services on tab return (at most once a minute), loads the photo when the flag turns true or the last load failed, and turns the flag off quietly on a photo 503/403. PR 929 delivered the earlier quiet skip.
* Tests: `src/api/tests/test_photo_availability.py`.
* Earlier RPI record: `.copilot-tracking/reviews/2026-11-04/fu-954-photo-flag-refresh-review.md`.
* The flag only applies in the Microsoft sign-in (`trusted-proxy`, Entra) mode. The dev `password` mode never shows a photo, so a real-browser console check needs an Entra-signed-in session (human/Azure step).

## Acceptance criteria status

* Flag updates without full reload after availability changes: met in code and tests (PR 993).
* Console stays quiet for predictable 503/403: met in the node harness; not verified in a real browser console. One first request made while the flag is still true can show in the network log.

## Slice

No code gap remains. Smallest coherent slice: a docs-only record that names the remaining human/Azure check.
