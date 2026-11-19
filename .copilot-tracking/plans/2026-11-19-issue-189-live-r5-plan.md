# Plan r5: issue 189

* [x] Phase 1: verifier selects the hub budget by resource-scope filter as well as by name (code and tests, src/core).
* [x] Phase 2: live governed run on the demo hub: throwaway job runs the repository simulator with a control file (owner, 3-minute expiry); observe halt at expiry; delete job and any role assignments.
* [x] Phase 3: research note with per-criterion proven/unproven table; index and log; changes and review records.

Validation tier: FULL is required only for src changes under security/infra/SQL scope; verifier edit is read-only tooling, classified FOCUSED (ruff, mypy, targeted tests). rpi-checks --all is not run.
