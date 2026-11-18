# Research: issue 184 live simulator stream, run 2 (2026-11-18)

Refs #184. Synthetic desktop demo; owner authorised live Azure in resource group `ama` (cap USD 700).

## Opening state

* Existing state `issue-184-live-state.json` and its artifacts (earlier run, docs-only) are preserved; this run uses the `-r2` names.
* Earlier note `docs/reference/research/issue-184-live-simulator-stream-evidence-2026-11-18.md` proved no live stream: the hub send path was proven only by #110/#185 drivers, not by the repository simulator pipeline.
* Unticked criterion: "All child stories closed or deferred" (children #185 and #189 open at last reading).
* Repository publisher `IotHubSink` is X.509 only; owner decision says symmetric Hub keys. Plan: out-of-repo driver imports the real `live_simulator.send_slot`, `Generator`, `Limits` and supplies a SAS `Sink`. No source change.

## Planning readiness

Ready pending Azure facts (hub, route, job pattern from #110/#185 notes).

## Findings (Azure and source, 2026-11-18)

* Hub `iot-cutover-test-rzsrg` (host redacted in the note), route `route-demo-sensor` (condition true, DeviceMessages) to endpoint `eh-demo-sensor`, entity `sensor-readings` in `evhns-cutover-test-demo`, 2 partitions, consumer group `$Default`. Public access Disabled, so a job in `cae-cutover-test-demo` is needed.
* `live_simulator.run(list_homes, generator, sink, limits, max_slots=N)` is the real streaming loop; `Sink` is a two-method Protocol, so an out-of-repo SAS sink reuses the repository generator, pacing, retries and summary unchanged. `IotHubSink` itself is X.509 only and is not usable under the owner's no-X.509 decision.
* Demo API image already carries `zava_forward.api` and the Azure SDKs; managed identity `id-cutover-test-api` holds only an Event Hubs Data Receiver on the hub scope, so temporary roles are needed (Registry Contributor on the hub, Event Hubs Data Receiver on the event hub).
* Earlier #110, #185 and #188 notes proved devices, sends and Event Hub read-back with hand-written drivers; none ran the repository `run` loop and none retained Event Hub raw output.

## Planning Readiness

Ready.
