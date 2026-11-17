<!-- markdownlint-disable-file -->
# RPI Phase Details: resident-showcase-azure-deploy-462

Plan: .copilot-tracking/plans/2026-11-17/resident-showcase-azure-deploy-462-plan.md

<!-- rpi:phase id=P01 -->
## P01: Admission

Record resource list of `ama`, month-to-date actual cost, SQL SKU and the live app metadata (names, image, scale,
ingress only; no env values, no secret names beyond references). Incremental plan: no new resource; one new
revision, 0.25 CPU / 0.5 GiB, min 0, max 1, test window at most 30 minutes; ACR push egress negligible.
Stop if cost readback fails.

<!-- rpi:phase id=P02 -->
## P02: Build and push

Hold `/tmp/ama-rpi-heavy.lock` with timeout zero if present, otherwise just build locally. Build:
`docker build -f src/api/Dockerfile.resident-demo -t zava-resident-demo:<sha> src`. Capture the registry
policy (exports, public access, default action, rules) before any change; arm a trap that restores exactly that
state. Enable exports and public access and add the VM /32 rule, `docker login` with an exposed token via stdin,
push, read the digest, restore, and read back equality. Max three retries. Never print the token.

<!-- rpi:phase id=P03 -->
## P03: Deploy

`az containerapp update -n ca-resident-demo -g ama --image <registry>@sha256:<digest>`. Compare a safe metadata
projection before and after: only the image and generated revision may change. Verify revision Healthy,
`/healthz` 200 over HTTPS with insecure traffic disallowed. If startup fails, record the failure and restore the
old digest.

<!-- rpi:phase id=P04 -->
## P04: Live verification

Local Playwright script, credentials read from `~/.ama-resident-test-user` inside the process, never printed.
Checks: sign-in page landmarks, HTTPS-only, wrong password and unknown email give the same generic message,
no case content before login, forged cookie denied, staff route denied, real login reaches the mapped synthetic
home and shows no staff or canary fields, sign-out ends the session. Screenshots without credentials.

<!-- rpi:phase id=P05 -->
## P05: Close

Ingress state: left as found (external true, as the owner approved demo) unless the expiry plan says otherwise;
record it. Confirm replicas return to 0 by scale-to-zero. Record expiry (`ZF_DEMO_EXPIRES_AT`, readback of the
non-secret value) and stop plan: `az containerapp ingress disable` or the `--no-ingress` rerun. Update
infra/README.md deploy note, docs/reference/log.md, commit.
