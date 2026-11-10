# Issue 1292 E3 plan (2026-11-09)

Authorized: third of five additional cycles; E1/E2 spent; two remain after E3.

* Replace the single unused ignore with a typed local seam valid whether or not the driver module is typed: `fake_driver: Any = types.SimpleNamespace(Error=self.Error)` then `conn.driver = fake_driver`.
* No change to unused-ignore settings, CI, executable SQL, assertions or other typing; the second ignore (`attr-defined`, line 1490) was not reported and stays.
* Validation (demo-targeted tier): clean CI-equivalent venv mypy, ruff check/format, priority test module. No SQL contract rerun (no executable SQL change).
* Any other #1308 failure is recorded, not expanded.

Order note: reproduction research preceded the edit; this plan/critique file was committed after the edit was applied in the same session, recorded as a process divergence rather than backdated.
