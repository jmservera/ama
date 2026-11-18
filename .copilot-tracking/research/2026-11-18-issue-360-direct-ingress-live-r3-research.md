---
title: Research, issue 360 live criterion d third measurement
ms.date: 2026-11-18
---

Refs #360. Task slug `issue-360-direct-ingress-live-r3`. Mode automatic, docs and evidence only (no src change, FOCUSED tier).

## Scope and decisions

* Owner decisions 2026-11-18: synthetic demo, desktop only; live Azure authorised (rg `ama`, cap USD 700, no drills, no Key Vault rotation, no production change); no billing reconciliation, DPO/Legal or assistive-technology testing for the demo. Criteria c and e need owner decisions and are recorded as such.
* Unticked criteria: c, d, e.
* Research disposition: reused plus executed. Prior measurements are in `docs/reference/research/direct-ingress-live-demo-2026-11-18.md` (08:36 and 11:30 UTC runs). Open gaps there: browser-mode 401, a second staff role, per-replica or restart persistence (restart is a drill, excluded), a fresh AI call.
* Planning Readiness: Ready.

## Questions for this run

1. Do the live facts (external environment, own subnet, NSG, private backing services, no Front Door) still hold at 14:00 UTC?
2. Do anonymous probes and a real browser sign-in still pass, and does the role claim hold?
3. Can a second identity or role be obtained? (Check available credential files by purpose without printing them.)
4. Does a fresh grounded chat call return a model answer, with the throwaway thread deleted?
5. Can SQL persistence be shown without a restart drill, for example by a write-then-read through the app?

## Findings (measured 2026-11-18 14:05 to 14:25 UTC)

Evidence: `.copilot-tracking/evidence/2026-11-18/issue-360-live-r3/` (credential scan of 19 non-image files: 0 hits).

* Configuration unchanged: `cae-cutover-test-demo` external, Succeeded, subnet `snet-aca-demo`, environment `publicNetworkAccess` Enabled (the new fact versus earlier notes; expected for external ingress); `cae-cutover-test` still internal and Disabled. NSG `allow-internet-https-in` 443 priority 100. Both apps external, `allowInsecure` false, API revision `0000031`, one replica now. Easy Auth `RedirectToLoginPage` with the same excluded paths. No Front Door or Cdn resource; group `ama` Succeeded.
* Backing services: SQL, Key Vault, storage (default Deny), registry, Foundry `aif-cutover-test-rzsrg`, IoT Hub Disabled. Adverse and unchanged: `evhns-cutover-test-demo` and `aoai-resident-469` Enabled.
* Anonymous: `/healthz`, `/`, `/welcome.html` 200; `/api/me`, `/api/cases`, `/app` 401; forged `X-ZF-Role` and invalid bearer 401; HTTP 301 to HTTPS; TLS 1.3, Microsoft-issued certificate. Browser User-Agent with JSON Accept: `/api/me` and `/api/cases` 302 (browser-mode 401 gap persists).
* Staff browser sign-in (Playwright, 1366 by 900): redirect to `login.microsoftonline.com`, return to the app, title "Zava Forward | Zava North Homes". `/api/me` role `Retrofit Programme Manager`, `ZavaForward.ProgrammeManager`, `identity_source` `entra`. `/api/sensors` 403. Forged role and principal headers with a session leave the role unchanged. `/api/cases?view=all` total 443 in two fresh logins.
* Persistence: a chat thread created in session 1 was fetched (200) by a second, separately signed-in session, then deleted (200). The list endpoint did not include it, so only the direct GET proves cross-session storage; no restart drill, one replica.
* AI call (adverse): both runs returned `workflow-only`, `model_calls` 0, `provider_outcome` `activation-not-approved`, although `/api/chat/status` shows `activation` demo-only and `demo_activation` true. The code path (`chat_demo_meter`, one synthetic authority per UTC day capped at 20 calls) points to that day's meter, probably spent by the other live AI proofs today; this is an inference and was not confirmed by reading the ledger. The 08:36 UTC run on the same revision returned a model answer (`model_calls` 1, 1230 tokens). No reset or restart was attempted. The first run's throwaway thread was deleted in the second run (200).
* Second role: unavailable. The resident credential file is for the separate resident showcase login.

Planning Readiness: Ready. Gaps to record rather than close: c and e (owner), browser-mode 401, second role, restart persistence, fresh AI call today.
