# Issue 462 corrections: changes record (2026-10-25)

Prospective artifacts written before implementation: corrections research, plan, details and one
critique (Revise, two blocking and four non-blocking findings, amendments appended to the plan).
Original local-slice review (Medium limiter, Low stale email) is preserved unchanged.

## Process disclosures

* The ungated planning push `5963fa3f` remains disclosed. The owner accepted it as a process
  disposition only; no technical gate is satisfied by that acceptance. Nothing here is pushed.
* Details said the verifier CLI would live in `tools/`. It was placed in `infra/scripts/` beside the
  other operator scripts (`resident_showcase_sql.py`). Behaviour is unchanged by the location.
* A mistaken `ruff format infra/scripts` reformatted 13 unrelated scripts. They were reverted with
  `git checkout` before any commit; the diff contains none of them.

## Changes

* Medium limiter: `resident_showcase.client_key` and `ShowcaseConfig.client_address`
  (`ZF_DEMO_CLIENT_ADDRESS`, `peer` default, `ingress-rightmost`). Under `ingress-rightmost` only the
  last `X-Forwarded-For` entry is trusted (Azure Container Apps appends it; earlier entries are
  client-controlled; source: Microsoft Learn ingress overview, retrieved 2026-10-25). A missing or
  non-bare-IP entry falls back to the peer bucket. `resident_demo/app.py` and `__main__.py` use it.
* Low stale email: `authorise` now requires `row.email` to equal the email admitted in the identity map
  (`IdentityMap.email_for`), on login and on every protected request.
* Verifier tool: `resident_showcase_verifier.py` (strength policy, `build_verifier`) and
  `infra/scripts/resident_demo_verifier.py` (no arguments, interactive stdin required, hidden double
  prompt, verifier only on stdout, generic errors, core dumps disabled).
* Docs: api, core and infra READMEs; `docs/reference/log.md` entry.

## Tests (actual, local, no SQL, no Docker, no heavy gate)

* Core: `test_resident_showcase`, `test_resident_showcase_verifier`: 44 OK; with
  `test_resident_showcase_sql` 62 OK and 13 SQL tests skipped; `test_dependency_rule` OK.
* API: `tests.test_resident_demo_api` plus `tests.test_dependency_rule`: 36 OK; with
  `test_resident_preview_api` the 46-test run was OK.
* Core and api `ruff check`, `ruff format --check` and `mypy`: clean. The new CLI file is ruff clean.
* Mutation check: forcing `client_key` to return the peer and removing the email comparison made 4 API
  and 2 core tests fail; both mutations were reverted and tests pass.
* Only fake fixtures (`Fq7!rT4#kL9@wX2$mB5%vN-fixture`) were used. No real password was generated,
  entered or read. No secret, Azure, SQL, Graph or container action occurred.

## Residuals (not solved)

* The overall failure cap (60 per 10 minutes) can be exhausted by a distributed attacker, blocking
  sign-in for the window; per-source buckets are shared by users behind one NAT.
* Another proxy in front of the app would make the rightmost entry that proxy (hypothesis, untested).
* The verifier cannot guarantee strength or prevent swap or memory exposure; run on an owner machine.

## Open gates (unchanged)

Budget headroom (G1), live email equality and provenance with at most 25 allowlisted rows (G2),
SQL view and principal (G3), vault write principal and path (G4), complete `tools/rpi-checks.py --all`
gate on the exact head, hosted checks and independent assessment. No deployment is ready.
