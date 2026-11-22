# Critique: issue 2256 plan (executed once)

Verdict: proceed with changes, applied directly.

* Do not assume a timezone for a naive offered_at (invents a fact). Keep the row with unknown age.
* Naive due_at would raise TypeError in the same function; harden it.
* The web view validates `Number.isFinite(age_hours)`; a null age would make the whole screen an error. Update waitingRows and the display, and run the web tests.
* Sorting must tolerate null ages.
* Tier FULL (src change); gate economy: no rpi-checks --all here, coordinator runs gates.
