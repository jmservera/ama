# Research: issue 521 resident authority end (2026-11-01)

* Authority source `resident-demo.json` already reads 2027-02-01T00:00:00Z on main (#590); core, SQL renderer, secret/deploy helpers and January tests are consistent.
* Surviving old copy: `src/api/checks/resident_demo_browser_check.py` `SQL_AUTHORIZATION_END` (2026-11-01) and its test enforcing it.
* Outage cause: live SQL check constraint/allowlist rows still end 2026-11-01; live apply is owner/coordinator only.
* AI tariff expiry (`assistant.py` EXPIRES, `resident_ai.budget`) is a separate approval; out of scope.
* Research disposition: executed. Planning Readiness: Ready.
