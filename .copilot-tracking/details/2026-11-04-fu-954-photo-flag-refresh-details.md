# Details: issue 954

## Phase 1

* `src/api/src/zava_forward/api/web/app.js`: constants `PHOTO_RECHECK_MS` (60 s) and `PHOTO_UNAVAILABLE`; state `photoFailed`, `photoServiceCheckedAt`.
* `loadPhoto`: a 503 or 403 answer sets `me.services.photo = false`, shows the unavailable text, returns without throwing. Other failures set `photoFailed`.
* `recheckPhotoService`: no-op unless Microsoft sign-in, a signed-in account and no photo shown; throttled; fetches `/api/me` quietly (failures ignored); merges `services`; reloads the photo when the flag becomes true or a previous load failed; shows the unavailable text when false.
* `visibilitychange` listener calls it when the tab becomes visible.

## Phase 2

* `src/api/tests/test_photo_availability.py` runs the real functions under node with stubs: false flag makes no photo request; flag turning true loads the photo; 503 flips flag and is not retried; throttle respected; recovery after the interval; failed `/api/me` check is silent. Verified to fail on the previous `app.js`.
