# Review: issue 2061 live deploy with sqlTier dtu (2026-11-20)

Refs #2061. Task `issue-2061-live-dtu`. One review, after implementation. Boundary: commits `16331ca89` and `ed3890a32` plus the live deployment from `ed3890a32`.

## Outcome

Conformant for the delivered scope, with open findings routed to later work.

## Checks

* The source change is infra-only, default tier unchanged, dtu limited to the development profile by a guard; tests cover the sku, the null serverless settings and the guard.
* Deploy evidence: three deployments; the failed one led to a separate fix commit, and the deploy that counts ran from the final commit.
* Protected resources untouched: SQL (still Standard 10, Online), storage, Key Vault, IoT Hub, `cae-cutover-test-demo`, its static IP.
* Deletions used ids from the runbook list; both public URLs return 200 afterwards.

## Findings (open, routed to follow-ups)

1. Telemetry end to end was not shown, so `evhns-cutover-test-demo` stays. Route to Research: a device path (X.509 device or an in-environment sender) for IoT Hub with local auth disabled.
2. Entra redirect and logout URIs cannot be tabled without directory privileges; resident account sign-in was not exercised.
3. The runbook does not yet say that SQL users must be created from inside the environment or that old apps and jobs must be deleted before their environment. Route to Implement as a small docs change.
4. The before-change role inventory was not captured.
5. The full local gate receipt for the exact head is not produced here (FULL tier, coordinator-owned).
6. ACR `defaultAction` moved from Deny to Allow with public access still Disabled; the owner should confirm that is intended.
