# Changes 2244 live r3 (2026-11-23)

Tier FULL (infra deployment setting; no src code change). `rpi-checks.py --all` not run; the coordinator runs gates. Local commit only, not pushed, not deployed.

## Edits

* `infra/modules/containerapps.bicep`: API StartUp probe failureThreshold 40 to 80 (window 121 s to 241 s, above the 211 s lock retry budget).
* `infra/tests/test_bicep_policy.py`: pinned probe updated.
* `infra/tests/test_container_hosting_completeness.py`: new test deriving the retry budget from `mssqlstore.py` constants; confirmed failing at 40, passing at 80.
* Docs: `docs/reference/research/issue-2244-live-r3-2026-11-23.md`, README index, log.

## Validation

* `tests.test_container_hosting_completeness` 18 OK; `tests.test_bicep_policy` 63 OK; `ruff check` and `ruff format --isolated --line-length 100 --check` clean on the changed test file.
* Not run: full local gate, hosted CI. Live: read-only `az containerapp show`; nothing created, nothing to delete.

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| C1 retry with backoff | Proven (SQL store live in run 2; law store in code and tests) | research r3, r2 |
| C2 skip lock when schema current | Proven live (run 2) | research r2 |
| C3 live start without crash-loop | Unproven: needs deploy of the law store retry and the probe change (owner-gated) | research r3 |
| C4 long writer cannot take the demo down | Unproven live; Bicep window and retry budget now aligned and test-pinned | research r3, tests |
| C5 lock holder identified | Unproven: no log names the holder | research r2 |
