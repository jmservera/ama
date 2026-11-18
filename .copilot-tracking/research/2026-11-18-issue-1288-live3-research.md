# Research: issue 1288 live demo audit, run 3 (2026-11-18)

Refs #1288. Demo, desktop only. Docs and evidence only unless a defect forces a src change (FOCUSED tier; never rpi-checks.py --all). Research disposition: reused plus live delta. Planning Readiness: Ready.

## Prior work reused

* Runs 1 and 2 (`docs/reference/research/issue-1288-live-quality-sensor-evidence-2026-11-18.md`, `...-live-r2-...`) hold local tests, browser and SQL evidence and the live release-gate observation. Open criteria: 3 to 8.

## Delta to research

* Re-read live state (readings, forecast, release, RAI metrics) WITHOUT invoking the Quality assistant (run 2 wrote an unintended denial proposal).
* Capture a Playwright screenshot of the real sensor panel (`#sensors`, Quality and handover tab), which runs 1 and 2 missed.
* Check Event Hub and job state read-only, and whether an approved release record exists.
