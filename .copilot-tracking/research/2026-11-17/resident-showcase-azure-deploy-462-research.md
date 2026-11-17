<!-- markdownlint-disable-file -->
# Research: deploy current-main synthetic resident showcase to Azure (issue 462)

Date: 2026-11-17. Task: resident-showcase-azure-deploy-462. Session rpi-462.
Base: 488c5a0c8cbf03785e4f258c4b265cebe3772862. Tier: FULL (coordinator runs the gate).

## Question

Can the current-main resident demo image be deployed to the existing `ca-resident-demo`
(resource group `ama`) and verified in a real browser, within the recorded owner authority,
and what blocks it if not?

## Opening state (before substantive search)

* Code slice: merged to main through PR 1841 (issue comment: local engineering criterion ticked).
* Live resident app per issue comment: revision `ca-resident-demo--0000010`, image digest
  `24a9cbe3` (source 8b9553d8b), 0.25 CPU/0.5 GiB, min 0/max 1.
* Open criteria: prospective RPI history, financial record before mutation, deployment and
  live browser verification, plus the unticked dependency criterion.
* Authority: coordinator brief 2026-11-17: demo only, resource group `ama`, cheapest sizing, cap USD 700,
  no production, SQL S0 and employee app unchanged, test-user files read at runtime only.

## Findings

Appended below as evidence is gathered (see sections added during the research phase).

## Findings (read-only, 2026-11-17 about 18:05Z)

* Live app `ca-resident-demo`: latest and ready revision `--0000010`, 100 percent traffic, 0 replicas now,
  min 0 / max 1, 0.25 CPU / 0.5 GiB, external ingress currently true, image
  `crcutovertestrzsrg.azurecr.io/zava-resident-demo@sha256:24a9cbe3...` (source 8b9553d8b, 2026-11-04).
* Registry `crcutovertestrzsrg`: Premium, public access Disabled, default Deny, exports disabled. A push needs the
  documented short window (README line 1628 precedent): enable exports and public access, one IP rule, trap restore.
* SQL: database `retrofit` Standard capacity 10 Online. `git diff 8b9553d8b HEAD -- infra/sql/resident-showcase.sql`
  is empty, so the deployed view still matches current main; the update is image-only, no SQL change.
* Cost: RG `ama` ActualCost month-to-date USD 85.39 (pre-tax actual, billing may lag). Against the owner cap of
  USD 700 the RG-only headroom is about USD 614.6. The incremental plan is below USD 1: local image build (no Azure
  resource), one ACR push, one revision at 0.25 CPU / 0.5 GiB min 0, a bounded test window.
* Test credentials: `~/.ama-resident-test-user` has two lines (fake email, demo password). Read at runtime by a
  local script only; values are never printed or written to tracking.
* Local tooling: Docker 29.9, Playwright Python with chromium installed, `az` signed in with a managed identity.
* Code slice and local SQL/image/browser evidence: PR 1841 (merged `c38c85a3`), already recorded on the issue.

## Planning readiness

Ready. Disposition: executed (read-only). Unknowns carried forward: cold-start latency (earlier 44 s first byte),
all-in cost lag, and whether the existing Key Vault references and managed-identity grants still resolve.
