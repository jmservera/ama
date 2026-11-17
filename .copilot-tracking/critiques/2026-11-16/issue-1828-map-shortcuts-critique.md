# Critique: issue #1828 plan (single execution)

* Date: 2026-11-16; reviewer: rubber-duck subagent, read-only; verdict: proceed with changes.

## Findings and dispositions

1. Blocking, regression not deterministic (old waits may outlast the debounce; only two animation frames are observed
   after the keys, so the 200 ms read can land after the listener is removed). Accepted: add a bounded post-key quiet
   observation (400 ms, twice the Leaflet debounce) inside `check_browser_shortcuts` before the unchanged assertion, so
   a pending resize read lands inside the observed window with the old wait; add a premise check that a real viewport
   change issues a map read; demonstrate the failure before the settle is added.
2. Blocking, delayed key-triggered reads undetected. Accepted: same post-key hold; a read arriving within the window
   after the last key still fails the existing assertion.
3. Non-blocking, quiet-window boundaries. Accepted: observation starts before the wait, quiet time resets on any
   request or busy state, one overall 10 s deadline, listener removed in `finally`.

No finding conflicts with a confirmed decision. No repeated critique. The diagnosis stays as researched; the critique
notes that a single captured failure does not prove every failure has this cause, so the final full runs and the
instrumented probe are the evidence, and any other cause would surface as a remaining failure.
