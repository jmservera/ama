# Research: issue 2253 r11 (2026-11-25)

Research disposition: executed. Planning Readiness: Ready.

* Issue has no checkboxes; five "Expected" statements are the criteria (see r10 note).
* Live ca-resident-demo (revision 0000030) serves demo.js and demo.css with SHA-256 identical to the repo files; API active revision is 0000076.
* Existing tests cover temperature only (sensorMetrics[0]). Humidity (0 to 100) is a second chart rendered by the same function and has no geometry test; the r10 note listed clamp and label-flip as local-test-only.
* Angle: (1) live Playwright re-proof on API 0000076 using the r10 probe; (2) add a node test that runs sensorChart for every metric (temperature and humidity) and checks tick/label no-overlap, circle gap, clamping.
