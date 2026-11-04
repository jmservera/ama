# Changes: issue 810 slice 2 (2026-11-04)

* Live (owner-approved): `ca-cutover-test-demo-api` ingress transport `Auto` to `Http`. Revisions `--k810` (temporary command override, deactivated) and `--t810` (original template, 100 percent traffic) were created. No resource group, secret or firewall change; Log Analytics and registry stayed unreachable.
* Source: `infra/modules/containerapps.bicep` (transport pin), `infra/tests/test_api_ingress_transport.py` (new).
* Docs: `docs/reference/research/easy-auth-intermittent-500-2026-11-03.md`, `docs/reference/README.md`, `docs/reference/log.md`, `infra/README.md`.
* Tracking: this set of r2 artifacts and the state file.
* Divergence: an app-side HTTP/1.1 keep-alive change in `src/api` was tried and removed because the live test showed no effect.
* Acceptance: criterion 1 met for the setting (mechanism unproven); 2 applied live and in Bicep, not yet deployed from Bicep; 3 met on 2026-11-04 (point observation). Hence `Refs #810`.
