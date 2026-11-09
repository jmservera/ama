# Research: issue 1288 E3 (typing fix, main integration, synthetic-demo route feasibility)

Disposition: executed. Task `issue-1288-e3`, parent `issue-1288-e2`. Cycle: third of five additional cycles after historical C1-C8; two remain. All spent and adverse evidence (E1 and E2 findings, E2 126-count claim) is preserved.

## Pre-work completed before research closed

* Part 1 typing: same-tool, same-config (pinned `.venv-1288` mypy 2.4.0) normalized diagnostic comparison between `c772364` and head. Red: 141 new diagnostics, all in `tests/test_quality_sensors_e2.py` (E2's "126" was counted differently; both recorded). Green: 0 new, 246 resolved (921 baseline vs 675 head). Core unchanged (63 vs 63). No `ignore`, stub or `cast` suppression. Commit `ed6f14f1b`. Logs: `logs-1288-e3/e3-red-*`, `e3-green*`.
* Main integration: pinned `23e944c1f` (IoT 1304) merged locally as `4b8d87801`. One conflict, the import block of `core/sensor_consumer.py`; both `SensorMssqlConnector` and `home_digest` imports kept. Sensor and SQL schemas both preserved. `origin/main` is now `df8e858b2` (rubric chore on top of the pin); not merged. No unmerged 1292 code.
* Overlap with merged 184: 1304 moved live rows out of `canonical_rows` and into `retained_envelopes`; the Quality capture path consumes `sensor_view` citations, unchanged by the merge. Re-verified by the post-merge test runs.

## Part 2 question

Can a dedicated simulation-only route let the real Quality model input carry the exact simulated reading IDs and values shown in the UI, without inferring provenance?

## Evidence

* The model payload (`assistants.capture` and `build_request`) is the whole `snapshot`: closed-allowlist case facts (home address, town, postcode, tenure; measures; documents id, kind, hash; quality records with free-text checklist `evidence`; checklists) plus `sources.sensors` citations.
* Case facts come from the working store (`ZF_DATA` or SQL). Nothing on a case or quality record carries a trusted synthetic marker. Quality checklist `evidence` is user-entered free text.
* Readings are accepted by `SensorConsumer` only as `source_type == "SYNTHETIC"`, but that is a contract on the row, not a namespace or store. The live receiver (`live_receiver.open_store`) writes into the same application store as everything else. Device IDs `SYN-<sensor_key>` are naming only.
* Existing switches (`ZF_CHAT_DEMO_ACTIVATION` plus `ZF_DEPLOYMENT_PROFILE=demo`, `ai_registry.demo_activation_honoured`) are operator composition choices for chat. They do not establish that a dataset, case or reading is synthetic, and the owner decision (2026-11-03) is chat-only.
* Existing trusted public generators (`core/synthetic/*`: `live_readings`, `sensor_identity`, `device_provision`, `provenance`, `privacy`) produce constructed data but write to the same store shape. `provenance` is hashes and non-destructive output, not a runtime gate.
* The egress point (`Ai._request`) sees only a prompt string and cannot classify it. E2 already proved (research F1) that free-text chat and direct `Ai` use cannot be classified without inference.

## Conclusion

A sound invariant needs a positive, non-caller-switchable lane: a separately composed simulation store plus a simulation-only case source, with the egress point verifying a lease or provenance token minted by that lane over the exact payload bytes. That is a new provenance architecture or lease-enforcing egress, which the brief forbids building speculatively and E2 reserved for an owner decision. Every cheaper variant reduces to inference from SYN IDs, a boolean or env flag, value coincidence, free text or a dataset path.

Planning Readiness: Ready, for a freeze decision (no activation), regression tests that lock the boundary as still closed with the new merged main, and the exact future admitted step.

## Future admitted demonstration step (documented, not performed)

1. Owner chooses one of: (a) lease-enforcing egress proxy that only forwards a payload whose hash was minted by a simulation-only composer, or (b) a dedicated simulation store (distinct connection, schema and credentials) with a bundled public fixture case and a payload allowlist that is verified at `Ai` by token over exact bytes.
2. A separate finite, verified admission for one live model call (budget, window, deployment, approver named) is recorded.
3. One admitted request is made with persisted simulator readings; the UI IDs and values are compared byte-for-byte with the request recorded by the meter; the output stays an unapproved proposal and manual approval stays required.

## Open items and residuals

* Real-AI sensor grounding stays withheld; the mock route and manual route remain. Real/private captured-data path stays OFF.
* Native assistive-technology acceptance, live acceptance and the whole 1288 criteria remain open.
