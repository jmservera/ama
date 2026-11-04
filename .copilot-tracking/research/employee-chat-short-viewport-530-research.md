<!-- markdownlint-disable-file -->
# Employee chat short viewport Send: research (2026-11-04)

Task: `employee-chat-short-viewport-530`. Research disposition: executed (delta). Planning Readiness: Ready.

## Delivery already on main (not redone)

* #541 delivered one chat agent with five skills (criteria 1 to 7); #568, #743, #752 refined stay-open chat and grounded replies when AI is off.
* #579, #634, #680, #721, #759 recorded local unit, SQL and browser checks; #814 repaired the browser check and left two open short-viewport findings.
* Owner decision 2026-11-04: proceed with the first slice (chat for the five bounded agents as skills plus general questions). That slice is already merged, so this task takes the remaining employee-side open item.

## Evidence

* Probe on main before the change (Chromium, synthetic loopback app): at 320x480 Send sat at y 430 to 472 while the panel ended at y 392; at 640x360 Send at y 323 to 365 while the panel ended at y 272. Send was clipped by the composer scroller (the #814 review records the same as open).
* Cause: `.chat-widget-composer` caps at 55% of the panel and scrolls; the tools row (agent skill select and Send) scrolled with it.

## Unmet acceptance criteria (unchanged by this slice)

* Criterion 8: live employee-site verification, owner confirmation of the five agent names, and local SQL selectors of the complete gate. Not run here.
* Screen-reader and voice-control acceptance is not claimed.

## Selected slice

Pin the tools row to the bottom of the composer so Send stays visible on short or narrow windows; assert it in the existing widget browser check. No security, infrastructure, SQL or deployment surface: focused tier.
