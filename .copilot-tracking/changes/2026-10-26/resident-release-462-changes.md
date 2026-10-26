---
title: Resident Azure release 462 - research, plan and ops note (2026-10-26)
description: Release evidence and the one source blocker found (allowlist cap). Counts and names only; no secrets, emails or case content.
ms.date: 2026-10-26
---

## Research (2026-10-26)

* The resident image `zava-resident-demo:release-462-55c239d9` was built `--no-cache` and scanned with Trivy 0.76.0 using `src/trivy.yaml`: 0 HIGH or CRITICAL findings.
* ACR `crcutovertestrzsrg` (Premium) had public access disabled, export policy disabled, bypass None, default action Allow and no IP rules. A first push attempt failed because exports were disabled; the owner approved a temporary export-policy change at 2026-10-26 23:12Z.
* Working push sequence (egress IP re-detected; `$R` is the registry name):
  1. `az acr update -n $R --allow-exports true`
  2. `az acr update -n $R --public-network-enabled true --default-action Deny`
  3. `az acr network-rule add -n $R --ip-address <ip>/32`, wait 60 s
  4. `az acr login -n $R --expose-token`, then `docker login` with the all-zero GUID user and the token on stdin
  5. `docker tag`, `docker push`, `az acr repository show --query digest`
  6. Restore in a trap: `az acr network-rule remove --ip-address <ip>` (bare IP, not `/32`), `--default-action Allow`, `--public-network-enabled false`, `--allow-exports false`, then compare a full `az acr show` with the saved before file.
* The first restore left the rule in place because the remove used `<ip>/32` while Azure stores the bare IP. It was fixed by hand and read back identical. The window was a few minutes.
* Pushed digest: `sha256:d388d2dd33b9c78a2e758d2e872f193461a1421abb040f0cbb2b92f3c938f344`.

## Plan

1. Write the vault secrets with `resident_demo_secrets.py` (done, both expire 2026-10-31T23:59Z).
2. Deploy `infra/resident-demo.bicep` with `--no-ingress` (done, 5 resident-owned changes in what-if, none elsewhere).
3. Apply the view, principal, grants and allowlist through the existing init job with a per-execution ARM `/start` override and tag-relay counts (done).
4. Open ingress for at most 60 minutes, test, close.

## Changes and outcomes

* Stage 5 execution `job-cutover-test-init-ob0tnmh` succeeded. Counts: allowlist rows 522, view rows 522, distinct emails 522, max email count 1, rows visible to the resident principal 522, base table denied to the principal yes, principal verification passed. The job definition and unrelated tags were unchanged.
* Ingress was opened once (about 23:19Z) and closed at 23:24Z. The app did not start: `Refusing to start: The allowlist supplies more than 25 showcase mappings.` The deployed code caps the identity map at 25 rows, so the owner-approved 522 emails cannot be served.
* Release blocker fixed on this branch: `MAX_MAPPINGS` raised from 25 to 1000 (core, SQL reader message, SQL comment, README and two tests that now use the constant). Focused core and API resident tests pass; ruff and mypy strict are clean on the changed files.
* Not done: rebuilding, pushing and deploying the corrected image, and the login, isolation, forged-cookie, expiry and logout browser tests. These need the PR gates and merge, or an explicit owner decision to deploy a branch build.
* Invariants after the run: the three apps and eight jobs have config hashes identical to the before snapshot; the SQL database is still Standard S0 (10 DTU); ACR is read back as before; SQL container `793cb3650397` is still running.
* Cost: no billable step beyond the init job execution (under 0.01 USD estimated) and about 5 minutes of app compute plus a crash loop (under 0.01 USD). Billing history lags, so these are estimates.

## Review

No independent review has been performed for this change. Review is pending on the PR.
