# Research: issue 130 live audit (2026-11-18)

* Task: audit issue #130 against repo and the live synthetic demo. Scope: demo, desktop only; live Azure authorised in rg `ama` (cap USD 700, no drills, no Key Vault rotation, no production change); billing reconciliation, DPO/Legal approval and person-run AT testing waived.
* Research disposition: executed, reusing runs 1 and 2 (docs/reference/research/issue-130-live-*). Planning Readiness: Ready.
* Unticked criterion (only one): representative participation and comprehension need authorized human evidence.
* Findings: deployed revision 0000031 and digest sha256:5368f4e4... unchanged, so the write refusal (403 "Reload your current staff identity", resident_decisions._operation) persists; route view and permissions read live; 91 core and 14 api offline tests pass.
* Fixing the identity check is a src/core security control: FULL tier, out of scope; reported only.
* Evidence: `.copilot-tracking/evidence/2026-11-18/issue-130-live-r3/`. Note: `docs/reference/research/issue-130-live-r3-nomination-route-audit-2026-11-18.md`.
