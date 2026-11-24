# Research r11 (2026-11-24, Refs #107)

Open criteria: (1) independent SQL connection/worker and race tests for mismatch, revocation, restart; (2) delivered-build acceptance.

Findings from code and prior notes (r10 note, merged in #2357):

* Separate-process harness varies policy, prompt, permissions, data, provenance, model. The bound fields also include `registry_version` and `schema_version`; no separate-process test moves them. This is the remaining gap.
* `runtime_binding` takes `registry_version=VERSION` and `schema_version=SCHEMA_VERSION`; `data_version` also hashes `SCHEMA_VERSION`.
* Criterion 2 needs an approved release on the deployed build and a named approver (OQ-017): unprovable for the demo.
* Live Azure SQL is excluded by the fixture's localhost-only guard; disposable local SQL Server container is the actual-SQL route.

Planning readiness: Ready. Disposition: executed (code and notes read).
