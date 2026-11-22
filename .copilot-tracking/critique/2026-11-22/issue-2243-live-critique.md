# Critique: issue 2243 live probe plan (one pass)

Verdict: proceed.

* Claim risk: "fix is deployed" cannot be shown without an image-to-commit link. Disposition: wording kept as inference; criteria marked Unproven/Partly proven.
* Claim risk: usage_limit cause is one of three SQL conditions. Disposition: note lists all three and marks the expiry row as probable, not proven.
* Scope risk: reading SQL would need a firewall change. Disposition: rejected; the brief forbids estate changes.
* Scope: no src change, so the focused tier applies; no rpi-checks run.
