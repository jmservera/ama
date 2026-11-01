<!-- markdownlint-disable-file -->
# Issue 176 research: determinism, seeds, versioning for synthetic data

Date: 2026-11-01. Branch: feat/synthetic-determinism-policy. Disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue 176 comment (2026-10-31 closure audit): criterion 3 (refresh policy) proven; criteria 1 and 2 unmet because the original OSM stock register generator is absent and no single repeatable check covers every in-repo generator.
* `docs/reference/research/retrofit-synthetic-data/README.md` lines 120-130 and 246-251: per-generator matrix and acceptance table; stock register row says no generator in repo.
* In-repo generators with seed/revision/hash manifests: `scale_fixture` (version, seed, as_of, generator_revision, file_sha256), `sensor_backfill` (same), `stock_fabric` summary.json (version, seed, generator_revision, as_of, file_sha256), support pack and MVP builders (support/, out of scope for src work).
* Gap found: `sensor_scenarios.write` manifest records `seed`, `generator_revision`, `schema_version` and `method_version` but no `version` field, and has no as-of label.
* Gap found: no single command replays every in-repo generator twice and reports byte identity plus manifest fields; replay evidence is scattered across tests.
* Unresolvable: the private 60,000-home stock register generator and pinned OSM inputs are not in the repository; no receipt can be produced for it.

## Selected approach

* Add `zava_forward.core.synthetic.determinism_audit`: replays each in-repo generator twice with a fixed seed/as-of into temp dirs, asserts byte identity and manifest seed/version/generator_revision, and lists the original stock register generator as `unavailable` (unmet) rather than passing it.
* Add `version` to the sensor-scenarios manifest.
* Tests in `src/core/tests/`; update README acceptance table and knowledge-base log.

## Follow-ups

1. Owner provides or retires the original stock register generator (blocks criterion 1 and 2 fully).
