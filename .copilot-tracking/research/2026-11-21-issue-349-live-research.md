# Research: issue 349 live round 7 (2026-11-21)

Disposition: executed. Planning Readiness: Ready.

Findings (evidence in evidence/2026-11-21/issue-349-live7/ and docs/reference/research/issue-349-tenant-prerequisites-live-r7-2026-11-21.md):

* Browser proof reproduced: anonymous 302, forged headers 302, signed-in /api/me 200 with ProgrammeManager, /api/cases 200, logout and account picker.
* Vault private (public Disabled, Deny, 1 private endpoint); secret is a Key Vault reference.
* Graph read denied: criterion 1 cannot be proven.
* Resident account is federated to sts.microsoftonline.com, NXDOMAIN publicly; round 6 DNS-on-host diagnosis corrected.
* Azure CLI token for the app audience is refused by Entra with AADSTS501051 (unassigned principal).
* No defect found; no src change planned.
