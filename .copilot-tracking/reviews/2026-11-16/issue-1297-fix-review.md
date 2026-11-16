# Review: issue 1297 rpi-checks skip allowlist (single pass)

Review executed once on the working tree before commit. Outcome: conformant for the reviewed boundary (tools/rpi-checks.py, tools/test_rpi_checks.py, src/README.md); no open material findings.

* Skips are bound to exact class, reason and group; foreign classes, reasons and groups, and integration runs are rejected (tested).
* Required executions cannot be satisfied by skips: zero skips plus at least one ok test per pinned class; plan, Runner and receipt verification agree (receipt tests pass).
* Selection couples opt-in test modules and infra Bicep to their execution groups.
* Tests: 106 pass; ruff, format and mypy --strict pass.
* Not assessed here: the full gate on real SQL, Chromium and the image; its external receipt is the evidence and is verified after commit.
* Routed follow-up: `ZF_RESIDENT_MSSQL` classes execute nowhere in the gate (out of scope; separate issue).
* Human review and hosted CI approvals remain unchecked and required.
