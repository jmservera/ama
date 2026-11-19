# Research: issue 1818 live, 2026-11-19

Task: `issue-1818-live`. Disposition: executed (opening note; findings below).

## Question

Which acceptance criterion of #1818 is unmet, and can it be implemented with code and tests for the synthetic desktop demo?

## Findings so far

* Only criterion 5 is unticked: live Azure IoT Hub -> SQL -> UI map walkthrough.
* Merged note `docs/reference/research/issue-1818-live-iot-map-walkthrough-evidence-2026-11-18.md` (PR #2004) already records a live run (9 stored rows, fresh then stale map and resident views) but says the raw output is not retained in the repository.
* The `live_demo` sender and the receiver fix (`7bde5f149`) live only on a sibling branch; they touch SQL ingestion, so adding them to `src/` is FULL tier and out of scope here (brief: stop and report).
* Plan: read-only live re-observation of the deployed demo (map and resident views with retained readings), retain redacted raw JSON in the repo, and record a per-criterion table.

Planning Readiness: Ready.
