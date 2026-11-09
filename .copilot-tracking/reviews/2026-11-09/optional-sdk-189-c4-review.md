<!-- markdownlint-disable-file -->
# Issue 189 C4 optional streaming SDK import review (2026-11-09)

One author review of the implemented change against the plan, performed once; independent exact-head Functional review, hosted CI and coordinator decision remain required.

* Outcome: no significant finding. The root cause (a pure-data annotation forcing `iot_stream`'s SDK imports at API boot) is removed at the single coupling point; the real streamer (`iot_stream`, `live_receiver`) keeps its hard SDK imports and the CLI iothub branch reports `IOT_SDK_MISSING` explicitly.
* Constraints checked: no blanket except or `pass`, no success fallback, no SDK installed to hide the contract, fixture/check/CI unchanged, no `Any`, cast or ignore, no module extraction, limits/estimates/guards/duration/auth/control state unchanged.
* Reported, not changed: `pyproject.toml` still lists the SDKs as base dependencies; the `--sink stdout` dry run no longer needs the SDK; the quoted `"DeviceActivation"` annotation is intentional (`TYPE_CHECKING`).
* Open for others: other hosted src API jobs were still running when C4 began; any additional finding must be retained, and fixed only if directly coupled, without silent budget extension.
* Web-design-guidelines review: not applicable, no web files changed.
