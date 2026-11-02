# Research: live employee verification (#570 criterion 3)

* Disposition: reused (existing runner and guide are adequate); Planning Readiness: Ready.
* Evidence: `src/api/README.md` (acceptance section), `src/api/checks/employee_live_acceptance.py`, `employee_acceptance_check.py` (strict `verify_employee`), cut-over evidence pack 2026-10-31 (blocked: directory lookup denied).
* Gap: independent expected `oid`. `az ad user show` still denied. Resolution: take `oid` from an Entra token-endpoint `id_token` for the test account (independent of the app's `/api/me`), memory only.
* Credential file `~/.ama-test-user` holds only the password; UPN from repository docs. Never printed in artifacts.
* Constraint: app scales to 0, warm with `/healthz`; one sign-in, no Azure changes.
