# Changes: issue #124 live proof (2026-11-18)

Tier: FOCUSED (docs and evidence only; no src change; rpi-checks.py not run).

Files:
* docs/reference/research/issue-124-phase0-discovery-evidence-2026-11-18.md (new research note)
* docs/reference/README.md (index paragraph), docs/reference/log.md (appended entry)
* .copilot-tracking/evidence/2026-11-18/issue-124-live/probe.py, probe.json

Per-criterion result (Refs #124; no closing keyword):

| Criterion | Proven for demo? | Basis |
| --- | --- | --- |
| Discovery owner nominated and endpoint agreed | Unproven (rule enforcement proven offline) | Needs a real sponsor decision; probe shows human-only, distinct, accepted-handover rules with placeholder names |
| Lifecycle and event dictionary validated | Unproven (schema proven offline) | 49 owner-validation gaps open; needs operational-owner workshops |
| Constraint register supporting and contradicting evidence | Unproven (two-sided rule proven offline) | Seed register 0/0 evidence; needs approved twelve-month extract and owner review |
| Findings not company findings until owners validate (ticked) | Re-confirmed offline | owner_validated=false, candidate status, fail-closed guard |

Validation: `PYTHONPATH=src:tests python3 -m unittest test_discovery_contract test_discovery_flow test_discovery_register` in src/core: 59 tests OK. Live Azure not applicable (no deployed consumer); nothing created, nothing to delete.
