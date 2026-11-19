# Research: issue #124 live proof (2026-11-18)

Disposition: executed. Planning Readiness: Ready.

Scope: three unticked criteria on #124 (owner nomination and endpoint; lifecycle and event dictionary validated; constraint register with supporting and contradicting evidence). The fourth is ticked. Demo only, docs/evidence only, Tier FOCUSED.

Findings (full record in docs/reference/research/issue-124-phase0-discovery-evidence-2026-11-18.md):
* The core contract is pure offline Python; no api/orchestrator/agents/importer consumer exists, so there is no live Azure surface to probe. No Azure resource touched.
* 59 core discovery tests pass. Probe (.copilot-tracking/evidence/2026-11-18/issue-124-live/probe.py, probe.json) proves the rules: human-only distinct nomination, endpoint fixed to accepted handover, 49 open dictionary gaps block validation, two-sided evidence rule, fail-closed candidate status.
* Synthetic pack: 992 candidates, 9,859 events, 4 of 15 contract events absent from the event log, mixed ISO and dd/mm/yyyy dates (8,818 / 1,041).
* All three unticked criteria need human sponsor/owner workshops and an approved company extract; cannot be proven for the demo.
* Heavy lock not used; rpi-checks.py not run.
