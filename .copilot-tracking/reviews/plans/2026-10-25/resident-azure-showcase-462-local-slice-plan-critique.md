# Resident Azure Showcase 462 Local Slice — Plan Critique

Date: 2026-10-25  
Verdict: REVISE  
Critique execution status: Complete

## Assessment boundary

Reviewed the supplied local-slice plan, phase details, and research, plus the merged preview and SQL `cases` DDL context. This assesses only the proposed local implementation boundary; it does not establish live-data equality, cloud-role correctness, or the gated deployment steps.

## Findings

1. **PC-001 — Blocking: SQL ownership-chain and direct-denial model is unspecified.**
   - **Evidence:** `/home/azureuser/source/ama-wt/issue-462-resident-azure/.copilot-tracking/plans/2026-10-25/resident-azure-showcase-462-local-slice-plan.md:21,36`; `/home/azureuser/source/ama-wt/issue-462-resident-azure/.copilot-tracking/details/2026-10-25/resident-azure-showcase-462-local-slice-details.md:12`.
   - **Issue/impact:** A view principal can read `dbo.cases` through the view only when the ownership chain is deliberately aligned; a direct `DENY SELECT` on `dbo.cases` should still deny direct access. The plan requires both outcomes but does not state the schema/object owner, exact grants/denies, or a no-extra-role assertion. A script can therefore either break the view for the intended principal or accidentally grant base-table access.
   - **Recommended change:** Specify the ownership-chain model and direct-deny semantics in the SQL phase, and require the SQL test to prove both `SELECT view` success and direct base-table denial under the actual showcase principal, including its effective roles and schema permissions.
   - **Action owner:** Planning parent. **Resolution evidence:** local SQL Server test against the provisioned schema/principal. **Decision route:** direct planner correction.

2. **PC-002 — Blocking: SQL email uniqueness cannot be proved from the stated normalisation rules.**
   - **Evidence:** `/home/azureuser/source/ama-wt/issue-462-resident-azure/.copilot-tracking/details/2026-10-25/resident-azure-showcase-462-local-slice-details.md:7`; `/home/azureuser/source/ama-wt/issue-462-resident-azure/.copilot-tracking/plans/2026-10-25/resident-azure-showcase-462-local-slice-plan.md:21-22,36`; `/home/azureuser/source/ama-wt/issue-462-resident-azure/src/core/src/zava_forward/core/mssqlstore.py:24-34`.
   - **Issue/impact:** Admission uses Python NFKC/trim/lower, while the view must extract the email from `cases.body` and count matches across every case. The plan never defines an equivalent T-SQL canonicalisation, JSON path/error handling, or explicit comparison collation. The existing `cases.body` is unconstrained JSON text and the store uses `Latin1_General_100_BIN2`; divergent case/Unicode handling can count an email as unique in SQL when the application treats another case as the same identity, disclosing the wrong mapping.
   - **Recommended change:** Define one enforceable, identical email grammar/canonicalisation and explicit collation for the view count and application admission (or constrain accepted showcase emails to a grammar for which equivalence is exact). Add local SQL cases for case variants, Unicode-normalisation variants, missing/malformed/non-string JSON values, and collisions in non-allowlisted rows.
   - **Action owner:** Planning parent. **Resolution evidence:** SQL definition plus passing local SQL tests demonstrating all listed cases fail closed or count correctly. **Decision route:** direct planner correction.

3. **PC-003 — Blocking: the local sign-in test path conflicts with secure `__Host-` cookies.**
   - **Evidence:** `/home/azureuser/source/ama-wt/issue-462-resident-azure/.copilot-tracking/plans/2026-10-25/resident-azure-showcase-462-local-slice-plan.md:24-25,37`; `/home/azureuser/source/ama-wt/issue-462-resident-azure/.copilot-tracking/details/2026-10-25/resident-azure-showcase-462-local-slice-details.md:18,24`.
   - **Issue/impact:** The plan requires `Secure` `__Host-` cookies but its local HTTP tests bind to `127.0.0.1`; a browser may reject or not return Secure cookies on that insecure origin. The required Playwright “real sign-in” could thus fail or tempt a later insecure-cookie exception, weakening the deployment design.
   - **Recommended change:** Define a supported secure local browser-test origin (and certificate/trust handling), or explicitly document and test the browser-specific loopback rule being relied on, while retaining the same Secure cookie policy in the deployed app. Make real sign-in success conditional on that path.
   - **Action owner:** Planning parent. **Resolution evidence:** browser test that verifies the browser stored and returned both cookies over the defined local test origin. **Decision route:** direct planner correction.

4. **PC-004 — High: proxy-source limiting is knowingly spoofable without a trust boundary.**
   - **Evidence:** `/home/azureuser/source/ama-wt/issue-462-resident-azure/.copilot-tracking/plans/2026-10-25/resident-azure-showcase-462-local-slice-plan.md:26`.
   - **Issue/impact:** Enabling `ZF_DEMO_TRUST_PROXY=1` without defining authenticated immediate proxies permits arbitrary forwarded-client values. Attackers can bypass the five-per-source limit and consume the global 60-request budget, creating a cheap denial of service against the small database.
   - **Recommended change:** Require a concrete trusted-proxy boundary before forwarded headers affect the limiter, otherwise always key on the peer address; test spoofed forwarded headers in both modes.
   - **Action owner:** Planning parent. **Resolution evidence:** API tests show untrusted forwarded headers do not alter the limiter key and only the defined proxy path does. **Decision route:** direct planner correction.

5. **PC-005 — High: revocation/expiry behaviour is ambiguous in the presence of the 30-second cache and is not tested.**
   - **Evidence:** `/home/azureuser/source/ama-wt/issue-462-resident-azure/.copilot-tracking/plans/2026-10-25/resident-azure-showcase-462-local-slice-plan.md:22,24,26,35-36`.
   - **Issue/impact:** The plan says admission is rechecked on every fetch, but also builds an identity map and caches per-case data. It does not state whether cached state can authorize an existing session after `revoked`, `valid_to`, or showcase expiry changes. A stale authorization path would violate the database-owned allowlist boundary.
   - **Recommended change:** Separate cached presentation data from fresh authorization state, state the maximum permitted revocation staleness (preferably none for authorization), and add an API test that revokes/expires a case after login and proves the next protected fetch is denied.
   - **Action owner:** Planning parent. **Resolution evidence:** documented cache/auth invariant and passing mid-session revocation/expiry tests. **Decision route:** direct planner correction.

## Strengths and residual risk

The plan correctly keeps the #444 preview harness separate, starts the allowlist empty, bounds mappings, and avoids live/cloud access in this slice. The shared-password identity limitation is explicitly acknowledged.

## Limitations

No live database, private principal configuration, vault route, or deployment configuration was inspected; those remain gated as the research states.

## Closeout

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: make the SQL ownership/grant/deny model testable and explicit before drafting the SQL file.
* User response required: No.
