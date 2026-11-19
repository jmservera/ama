# Issue 360 live changes, 2026-11-19

Refs #360. Tier: FOCUSED (documentation and evidence only; no `src/`, infra, workflow or dependency file changed). A source change was not made, so the FULL tier and `rpi-checks.py --all` do not apply.

## Files

* docs/reference/research/issue-360-live-20261119-2026-11-19.md (new research note)
* docs/reference/README.md (index row), docs/reference/log.md (log entry)
* .copilot-tracking/evidence/2026-11-19/issue-360-live/ (configuration JSON, anonymous probes, sign-in run, two screenshots, script copy)
* .copilot-tracking/{research,plans,details,changes,reviews}/2026-11-19/issue-360-live-* and the state file

## Per-criterion table

| Criterion | Result | Basis |
| --- | --- | --- |
| a | Proven live again | External environment, own subnet, NSG 443, private SQL, Key Vault, storage, registry |
| b | Not re-tested | Offline tests |
| c | Unproven | Owner approval of the migration plan is not on record; an agent cannot supply it |
| d | Partly proven | Proven: health, welcome, HTTPS, non-browser 401, sign-in, role claim, `/api/sensors` 403, cross-session reads. Unproven or failing: browser-mode 401 (302), AI call (workflow-only today), second role, restart persistence |
| e | Unproven | No Front Door resource exists; owner authorisation and order after d not on record |
| f | Not re-tested | Documentation |

## Stop

Browser-mode 401 requires changing `unauthenticatedClientAction` in `infra/modules/containerapps.bicep`: an authentication and deployment change, so the FULL tier is required. Not done here.

## Validation and cleanup

* Literal scan of the evidence folder for both credential values: no match. Signed-in screenshot with personal names deleted.
* Azure: read-only; one throwaway chat thread deleted via the app (200). No Azure resource created.
* mypy, ruff and unit tests: not applicable (no Python or source change).
