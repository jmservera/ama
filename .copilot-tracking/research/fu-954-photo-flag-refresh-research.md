# Research: issue 954 photo service flag decided once

Date: 2026-11-04. Disposition: executed. Planning Readiness: Ready.

## Prior delivery check

* PR for #929 ("skip predictable 503/403 requests so the console stays quiet", Refs #920) merged: `loadPhoto` skips `/api/account/photo` when `me.services.photo === false`. No PR addresses #954.

## Findings

* `src/api/src/zava_forward/api/web/app.js`: `start()` fetches `/api/me` once per sign-in; `showAccount()` then calls `loadPhoto`, which reads `me.services.photo` once. Server side, `services.photo` is `bool(token)` (`server.py`, `/api/me`). If token-store setup completes or fails later, the console keeps the old decision until reload.
* A 503/403 from the photo endpoint with the flag still true is thrown as an Error and shown as a status message; the flag is never corrected and the next load repeats the request.
* The tab-visibility event is a natural "refresh" trigger and needs no new UI control, so no new accessibility surface.

## Options

1. Poll `/api/me`: constant traffic, rejected.
2. Re-evaluate on return to the tab (visibilitychange), throttled to once a minute, plus flip the flag on a 503/403 photo answer (chosen). `/api/me` returns 200, so the re-check itself adds no console error.

## Limits

* The browser itself logs a failed network request if one is made; the fix avoids making it when the flag is false and stops repeating it after a 503/403. A 503/403 on the first request when the flag was true cannot be hidden from the console.
* No manual path change: the photo is cosmetic; initials remain the fallback (AI is not involved).

## Acceptance criteria status before work

* Flag updates without reload: unmet. Console quiet for predictable 503/403: partly met by #929.
