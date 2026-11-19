# Issue 360 live changes (2026-11-18)

Tier: FOCUSED (documentation and evidence only; no src, infra, SQL or workflow change; `rpi-checks.py --all` not run). Refs #360. Disclosure: the research note, index row and log entry were drafted during the live research phase, before the implement-start witness; the implement phase only reconciled them.

## Files

* `docs/reference/research/direct-ingress-live-demo-2026-11-18.md` (new)
* `docs/reference/README.md` (index row), `docs/reference/log.md` (entry)
* `.copilot-tracking/evidence/2026-11-18/issue-360-live/` (scripts, outputs, screenshots), plus research, plan, details, critique, changes, review and state files.

## Per-criterion proven/unproven table

| Criterion | Proven | Unproven |
| --- | --- | --- |
| a (ticked) | Not re-tested; live external environment, own subnet, HTTPS NSG rule, private SQL/Key Vault/storage/registry/Foundry/IoT Hub agree | None for this run |
| b (ticked) | Not re-tested | None for this run |
| c migration plan approved | Nothing | Owner approval before replacement is not on record; replacement already exists; agent cannot supply it |
| d live acceptance | Direct HTTPS health/welcome 200, HTTP to HTTPS 301, TLS 1.3; non-browser anonymous 401 and forged-header/bad-bearer 401; Entra browser sign-in with screenshots; role claim and forged-header immunity; shared SQL state across two replicas (443 open); real chat AI call (model_calls 1) | Browser-mode anonymous API 302 (fails 401 requirement); real named user; second-role denial; restart persistence; assistant release (human decision) |
| e Front Door retired | No Front Door/WAF/CDN resource found in `ama`; group `ama` Succeeded | Owner authorisation and ordering after d not on record |
| f (ticked) | Not re-tested | None for this run |

## Validation

* Documentation link and diff review; secret scan of the evidence directory (27 files, 0 hits); throwaway chat threads deleted (delete 200). No unit tests apply.
* Adverse evidence kept: run1 and run2 403s, run3 400, run5 abstain, public Event Hub and `aoai-resident-469`.
