# Changes: issue349 tenant readiness preflight

Task: 349-tenant-readiness-preflight. Refs #349 (bounded offline/read-only prerequisite slice; not live acceptance).

## Files created

* `infra/scripts/tenant-readiness-preflight.py`: standalone read-only checker. Exact-template command guard (account show, containerapp show/auth show, Graph v1.0 GET for applications and servicePrincipals only), closed sanitized report schema, exit 1 blocked / 0 ready / 2 usage.
* `infra/tests/test_tenant_readiness_preflight.py`: 28 offline tests (guard, UUID vs systemAssignedIdentity audience, 12-role contract and drift against `auth.py` role maps, callback and forwarded-header requirements, unavailable capability reporting, sanitized output, CLI).
* Dated research, plan, details, plan critique, this changes record, review and state artifacts under `.copilot-tracking`.

No existing file was edited.

## Validation

* Focused tests: 28 pass. Ruff (gate options) and format check clean.
* Live read-only run, sanitized statuses only: api-audience mismatch (system-assigned-identity literal), api-credential-setting absent, graph-read-capability denied, all Graph-dependent checks unknown (blocked). Exit 1 as designed.
* Full `unittest discover -s infra/tests` under bare system python: 8 errors, all pre-existing and environmental (7 `No module named 'zava_forward'` because src packages are not installed in that interpreter, 1 post-deployment health check in test_pipeline). None involve the new files. The official gate is the authority for the full run.

## Divergences

* Added a `graph-read-capability` probe (`$top=1`) so denied Graph access is distinguished from an absent app.
* Replaced dataclass with a plain class (importlib loading of a hyphenated script).

## Unmet (human blockers)

Original ACs remain unmet: actual tenant setup, private credential delivery (#360), staff binding, real-user callback/API/browser denial tests. Current credentials cannot read Graph.
