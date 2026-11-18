# Research: 7-day sensor trend summary (Refs #1288, Refs #111)

Date: 2026-11-14. Research disposition: executed. Planning readiness: Ready.

## Evidence

* Issue #1288: the retained per-home read model (`src/core/.../sensor_view.py`) already exists and is delivered; the employee payload is `sensor_view.view`, served by `AssistantService.sensors` (`assistants.py`) and `simulation_lane.py`.
* `view` is built on `capture_source`, whose newest-12-reading window feeds the Quality AI snapshot digest. Adding fields to `capture_source` would change snapshot digests and model inputs, so the trend must be added in `view` only.
* The 12-reading window covers about one hour of five-minute readings, so it cannot support a 7-day trend. A separate bounded read is needed.
* Consent: `capture_source` returns `consent-withheld` unless every control is granted. The trend must not read values in any other state.
* #111 deterministic analysis (`sensor_analysis.py`) has no trend concept; it is context, not proof of AI use or threshold approval.
* Readings are synthetic and uncalibrated. Temperature and humidity are stored as text.

## Design constraints

* Read only, bounded by count and time, no generation, no stage-gate writes.
* Directionality must be labelled `advisory_only` with provenance and must not affect Quality gates, snapshot or model request.
* Missing or too few readings yield `insufficient`, never a zero or steady substitute.

## Planning readiness

Ready. No open questions; thresholds are advisory and declared in the payload.
