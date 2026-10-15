# Details: retire prototype/ (#202 step 1)

* Remove files: `git rm -r prototype .github/workflows/prototype-validation.yml`.
* Registry: `infrastructure.include` becomes `["infra/**/*"]`; takes effect after merge, dip accepted.
* Required check `Prototype validation / validate`: not verifiable (403); do not guess, flag in PR.
* Tests: drop stale prototype fixtures from `test_prepare.py`, replace generated-file cases with `src/` equivalents.
* Docs: rubric README, capstone README, ADR 0006 status, parity matrix status, coordinator agent, index, log.
