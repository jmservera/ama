# Issue 185 plan (2026-11-01)

* [ ] P1 `device_identity.py`: `DeviceIdentity`, `Manifest` (run id, identities, derived from `Selection.sensors()` output), one-to-one validation matching `iot_stream.Binding` rule.
* [ ] P2 `Registry` and `CredentialStore` protocols; `provision()` registers identities, issues credentials into the store, returns manifest of references only; secret-free repr, errors and logging.
* [ ] P3 `teardown()` deletes exactly manifest identities and store entries, then verifies none remain; fails loudly otherwise; never touches non-run identities.
* [ ] P4 Tests (outside package) with in-memory fakes incl. no-secret-in-logs/repr and teardown completeness.
* [ ] P5 Decision section in research plan; ruff, format, mypy, unit tests; commit, push, PR.

Critique (single pass): keep DPS, real Azure SDK, cert generation out of scope; compatible. Verdict: proceed.
