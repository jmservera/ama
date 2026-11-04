# Plan: resident demo 503 retry (#1054, slice 2)

* `loadView` in `demo.js` retries `/demo/view` once after the `Retry-After` delay (3 s default, only when 1-10 s) on 503, with status text "The showcase is busy. Trying again in a few seconds...". A second 503 shows the existing error panel with its manual "Try again" button (manual path kept).
* No change to the bulkhead, server, security, SQL, infrastructure or deployment: focused tier.
* Critique: one pass, compatible; retry limited to one to avoid amplifying load.
* Test: node scenario `busy` in `test_resident_demo_script.py`.
