<!-- markdownlint-disable-file -->
# Issue 1818 live round 7: research (Refs #1818)

Task `issue-1818-live7`, mode automatic, tier focused (no `src/` change planned). Date 2026-11-18.

## Question

Prove the last unticked #1818 criterion (live IoT Hub to SQL to UI map walkthrough) on the deployed synthetic demo, desktop only, and state per criterion what is proven.

## Prior work reused

* Rounds 1 to 6 (2026-11-17) live in sibling worktrees `issue-1818-live-1117` to `issue-1818-live6-1117`; record in `docs/reference/research/iot-live-map-walkthrough-2026-11-17.md` on that chain (not on main).
* Round 6 reached a fresh reading in both views. Its fix (`SensorConsumer.process` writes `sensor_register`, commit `7bde5f149`, image `demo-1818live6`) is unmerged and the demo app still runs the round 4 image (revision `0000031`).
* Merged on main: #1826 (feature), #1829, #1838 (map regression tests). Criteria 1 to 4 are ticked.

## Observed state at start (2026-11-18 12:5x UTC)

* Demo app `ca-cutover-test-demo-api` revision `--0000031`; resident app `ca-resident-demo--0000012`.
* Event Hubs namespace `evhns-cutover-test-demo` and IoT Hub route `route-demo-sensor` (enabled) remain from round 3.
* ACR public access Disabled; no push is planned, a temporary job reuses the existing round 6 image.

## Planning readiness

Ready. Plan: one bounded send window with a temporary Container Apps job (9 messages, cap 200 cumulative 45 so far), fresh Playwright proof in the employee map and resident `#sec-sensors`, redacted evidence note, cleanup.
