# Issue 159 live critique (single pass)

Verdict: proceed with changes applied directly.

* The criterion has three parts; an agent can prove keyboard operability and live-region announcement but not screen-reader testing. Record that part as unproven by design, not as failed.
* A programmatic MutationObserver shows a node was added to a live region; it is not proof of what a screen reader speaks. State the limit.
* Screenshots must exclude the log (answers name synthetic people). Use header and composer crops only.
* Live chat storage is approved on the demo, so asking creates a stored thread; delete only the probe's own thread, never a broad filter.
* No source change is needed, so FOCUSED tier applies; do not run rpi-checks.py --all.

Dispositions: all applied; none conflict with owner decisions.
