# Execution-readiness plan (issue 462), written 2026-10-26T13:30Z, before any source edit

Prospective. Original history (late plan for correction 1, accepted by the owner at 13:14Z only to continue publication) is not altered. Evidence: `/home/azureuser/.ama462-evidence/release-readiness-2026-10-26-1316/readiness-assessment.txt` (private, external).

## Facts

* Local head `a24f8003`, PR 463 remote head `2af9a186`, main `acafc6ee`; only `.github/rubric/scores/latest.json` conflicts.
* ACA is paused: three apps min 0, eight jobs Manual. `infra/modules/containerapps.bicep` still defines API min 2 and cron/event triggers, so `main.bicep`/`deploy.py` must not be used for the resident app.
* Cost upper bound since 24 Oct 00:00Z (whole group, all baseline) 30.89 USD, fresh and reconciled grouped/ungrouped; additional spend estimate well under the owner's 5 USD.
* Vault is private-only (public Disabled, default Deny); the caller has Owner on `ama` and no vault data actions.

## Proposed next change set (smallest; none started)

1. A resident-only Bicep template `infra/resident-demo.bicep` (new file) that deploys exactly: one user-assigned identity `id-resident-demo`, one container app `ca-resident-demo` in the existing `cae-cutover-test-demo` environment (min 0, max 1, 0.25 vCPU, 0.5 GiB, one external-ingress port, image by digest from the existing registry), and role assignments scoped to the exact secrets and registry (Key Vault Secrets User on the two secrets, AcrPull on the registry). No schedules, jobs, environments, networks or SQL. Parameters carry no secret.
2. Tests (existing `infra/tests/test_bicep_policy.py` style): resource-type allowlist, min 0/max 1, no job or schedule resources, role scopes exact, no secret literal, and a guard that `main.bicep` defaults are untouched.
3. Authority: the template is written and what-if previewed only; deployment, role assignment, SQL principal creation and secret writes each remain explicit later stages released by the coordinator.
4. Publication: merge main (take main's bot file for `latest.json`), fresh full gate and verify under the heavy lock when released by the 349 lane, independent review, no push before then.

## Open and not decided here

* Exact secret-reference mechanism (Key Vault reference through the identity) is a Container Apps feature to confirm against the live environment by a non-secret what-if, not by assumption.
* The vault write path (G4) and SQL steps follow in separate stages.

## Critique

One independent critique of this plan runs before any edit; findings and dispositions are appended below.

## Critique result and dispositions (one independent rubber-duck pass, 2026-10-26T13:35Z)

Verdict: Revise. I verified finding 1 by grep before accepting it.

| # | Severity | Disposition |
|---|---|---|
| 1 | Blocking | Accepted and verified. The 12:00Z window is hard-coded in `resident_showcase.py:29` (`AUTHORITY_END`), `resident_demo_secrets.py:46`, `infra/sql/resident-showcase.sql:21`, the READMEs and tests, and has passed (now past 13:30Z). The app would refuse to start, so no cloud stage can proceed. The next source change must move the bounded expiry for the 13:14Z owner approval (ama only, additional spend to 2026-10-31). The new end value is the owner's approval date window; propose the end of 2026-10-31 UTC minus margin and let the coordinator confirm. This is a source change to security-relevant time limits, with matching tests; it never relaxes it to an open-ended value. |
| 2 | Blocking | Accepted. The template must state the full runtime contract (`ZF_DEMO_*`, SQL settings, identity client ID, `secretRef`s, allowed host/FQDN) and compiled-output tests must assert every required setting. |
| 3 | High | Accepted. Order: secret write, secret-scoped RBAC (supported on a single secret resource, precedent `authTokenStore.bicep`), then app. The environment, not the app process, must reach the private vault; add a non-secret live check of DNS/connectivity and secret-reference provisioning before opening ingress. A what-if alone is not proof. |
| 4 | High | Accepted. Add explicit stop conditions, ingress-disable/scale-to-zero rollback and a post-expiry "no active revision" check; "under 5 USD" stays an estimate, not an enforceable cap. |
| 5 | High | Accepted. Separate explicit resident command/template; deploy.py gets no resident path; what-if must reject modifications outside resident-owned resources. |
| 6 | Medium | Accepted. Add compiled-template tests (exact resource set, all runtime settings, versionless secret URLs, single-secret RBAC scopes, min/max scale, expiry guard) and a controlled live acceptance stage (secret resolution, SELECT only on `resident_showcase.v_resident_case`). |

Consequence: the plan's change set grows by an expiry-window change across core, SQL, helper, docs and tests (all with regression tests, original adverse reviews preserved) before the resident template. Nothing was edited in this pass.

## Coordinator corrections and stage release (2026-10-26T13:25Z, appended before any source edit)

* Cost correction: the 30.8926 USD figure is an observed LAGGING subtotal, not a safe upper bound on incurred spend. My statement "at least 19.11 remaining" is withdrawn and not established. The old 50 USD window expired at 12:00Z and is not execution authority. The statement that the 25 Oct baseline was "with ACA paused" is wrong: the pause happened 2026-10-26T10:27Z (coordinator). The 700 USD ceiling must cite its actual owner provenance rather than be assumed. The raw responses and `readiness-assessment.txt` are preserved unaltered; this correction is the amendment.
* Current authority: owner approval 2026-10-26T13:14Z, ama only, up to 5 USD ADDITIONAL spend through 31 Oct. Needs a timestamped baseline tied to 13:14Z, a conservative allowance for unreported usage, exact planned incremental estimates and stop controls before any billable step. Current evidence is planning context, not proof of complete headroom.
* Expiry decision (coordinator): exclusive cutoff 2026-11-01T00:00:00Z (through 31 Oct UTC), enforced by service and tooling, documented as UTC.
* Key Vault writer: the earlier proposal of an extra Key Vault writer role is corrected. The caller is Owner on ama; if the ARM secret write path is verified, no extra data-plane role is proposed. Whether it works through the private-only vault stays unproven (G4); no broad role.
* Stage released (local only): expiry update; resident-only template and explicit command with a what-if deny guard; all six critique findings. No cloud action, no main.bicep/deploy.py route, no secrets, no heavy checks.
