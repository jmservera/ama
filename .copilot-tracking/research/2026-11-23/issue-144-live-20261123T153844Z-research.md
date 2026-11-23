# Research: issue 144 live (2026-11-23)

Disposition: executed. Planning Readiness: Ready.

Findings: see docs/reference/research/issue-144-live-hardening-receipt-2026-11-23.md. Live guard is now enforced on all apps and jobs; PID 1 of the API replica is uid 10001, NoNewPrivs 1, empty CapInh/Prm/Eff/Amb; root FS rw (platform limit). Criterion 1 needs a pipeline run (unobtainable without Azure change).

Selected criterion: 3 (hardening). Deliverable: offline verifier infra/scripts/deployed_hardening.py plus unit tests, so the receipt is repeatable.
