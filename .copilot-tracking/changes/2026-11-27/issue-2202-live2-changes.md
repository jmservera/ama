---
title: Issue 2202 live changes (second pass)
---

Refs #2202. Tier: focused; no src change, so the full tier does not apply. Azure was read-only; no throwaway resource was created. No `rpi-checks.py --all` run.

Files: docs/reference/research/issue-2202-live-2026-11-27-r2.md, docs/reference/research/issue-2202-live-20261127T080139Z/ (probes, outputs, screenshots, tiles), docs/reference/log.md, docs/reference/README.md.

Validation: live probes and Azure CLI output recorded; Markdown links reviewed against the git diff. Hosted CI for the exact head is not observed (no push).

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Images rebuilt from main and rolled | Partly proven | All four run; API revision 0000131 post-dates #2386; digest-to-commit unreadable (registry firewall) |
| Revisions Running and Healthy | Proven | az-state.txt |
| ZF_CONTAINER_HARDENING enforced | Proven | `enforced` on 3 apps and 2 jobs |
| Rollback noted | Noted, not exercised | Redeploy prior digest or set `off`; no drills authorised |
| Agents app difference explained | Proven | ScaledToZero by design, no ingress |
| Sensor charts | Proven | chart probe; 30 of 30 GETs 200 under a running receiver |
| Map gauges | Proven | card probe (7.7 degC, 91.9 %RH meters) |
| Consent checkbox | Proven | resident probe |
| Chat routing | Proven | six routed or refused questions, corrected probe |
| Half of homes with readings | Proven (58.9%) | 261 of 443 over 16 tiles |
| Live receipt and log entry | Proven | research note and log entry |

Unproven: digest-to-commit provenance, rollback drill, generative answer quality, freshness within 15 minutes at read time.
