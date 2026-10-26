# Proposal: minimal private retrieval of the resident demo password (issue 462)

Drafted 2026-10-25 after the retrieval research and plan. For owner approval. Nothing here is approved, executed or implemented. Refs #462.

## Finding

No existing usable private retrieval route is proved. `kv-cutovertest-rzsrg` is private-only and reachable only from `vnet-cutover-test`; the group has no VM, Bastion, VPN or resolver, and its only in-network compute is workload jobs whose output goes to logs. A client elsewhere is possible but unproved. Owner on the group is management-plane only and does not give secret read.

## Recommended: Option C, a different operating model (not a retrieval route)

Status of Option C: it replaces "generate and retrieve from the vault" with "owner chooses, vault holds a verifier". It is a design for owner approval, not a route that exists today.

The owner chooses the shared password in their own password manager. A small offline command, written only after approval, reads it from a hidden prompt and prints only a scrypt verifier. A deployment then writes the verifier and the app's session-signing key as vault secrets, and the showcase app reads them with a managed identity inside the network. Protocol as implemented in `resident_showcase.py`: scrypt verifier `scrypt$N$r$p$salt$hash` with a per-password random salt, N between 2^14 and 2^16, constant-time comparison (`hmac.compare_digest`), one scrypt run per attempt. The session key (32 or more random bytes, base64url) is the HMAC key for the signed session and CSRF tokens, so it is needed; it is a second vault secret and is never shown to the owner. Its lifecycle is the showcase window, and a restart also invalidates sessions through a per-process nonce.

Unproven write and read authority (explicit pre-deployment gate, nothing done now): (1) the deployment principal and role that may write secrets to the private-only vault by the management plane are not identified or proven; the only proven vault role is Key Vault Secrets User (read) for `id-cutover-test-api`, and the showcase would need either that identity or a new dedicated one, which is a role decision for approval; (2) the ARM secret-write path to a public-access-disabled vault is documented but untested. The password itself is not stored, generated, logged or transported by Azure; the verifier and session key are.

* Human principal resolution: none needed for the vault. The owner shares the password with demo viewers out of band; the owner must name the sharing channel and the recipient boundary before use, because this proposal does not supply a channel.
* Data-plane role for the owner: none. Duration: not applicable. New resources: none. Network change: none.
* Cost: no new billable resource is proposed. Secret operation charges are not quantified and no affordability is claimed; the USD 50 cumulative incremental cap is not reset and headroom is unproven.
* Audit: the vault's `audit` category goes to Log Analytics and would record data-plane secret reads, not values. Whether a management-plane ARM secret write appears there or only in the Activity Log or deployment history is unverified. The verifier is not the password; the session key is a separate secret held only in the vault and app.
* Cleanup: removal of the two secrets by name after 2026-10-26T12:00Z. Soft delete (7 days) applies, no purge is planned, purge protection is unchanged. The owner discards the password from their manager.
* Residual risk: the owner knowing the password locally is the intended state; the shared password still permits cross-demo-identity access by design (labelled synthetic). A scrypt verifier of a long random password is offline-guessable only at that cost. If the owner insists on vault retrieval, use Option A.
* Departure from the brief: "generate a complex one" becomes "owner generates"; "retrieve" becomes "not needed".

## Alternative: Option A, retrieve from the vault (only if the owner requires it)

A short-lived Linux VM plus Azure Bastion in `vnet-cutover-test`, reached through the Entra-signed-in portal, with the owner granted Key Vault Secrets User scoped to the single secret `resident-demo-password`. Public prices (Retail Prices API, 2026-10-25T21:53Z, uksouth): VM B1s 0.0118 USD per hour; Bastion Standard 0.29 USD per hour (a Developer SKU price was not isolated, so unknown). Partial public-rate figure only: about 0.30 USD per hour for those two lines, excluding disk, IP, egress, Log Analytics and billing granularity; it is not an estimate of cost, not a statement of affordability, and execution is barred until a complete incremental estimate and the headroom gate pass.

* Needs: a new VM and Bastion (network change); Bastion normally requires a dedicated `AzureBastionSubnet` that does not exist in the VNet's three subnets, so a new subnet is probable. Before it can be treated as viable, validate subnet capacity, Bastion SKU and region support, VM DNS resolution of the private-link zone and NSG reachability, none of which is proved; a secret-scoped role assignment for the owner, generation by the existing ARM path, and a reading procedure that does not print the password into a terminal transcript (for example, copy straight to the clipboard of a password manager through the Bastion native client, then clear).
* Owner principal resolution: the owner runs `az ad signed-in-user show --query id -o tsv` in their own session and supplies the object id in the approval. It is not stored in the repository.
* Role duration: until explicit removal of that one assignment (no time-boxed role without Privileged Identity Management, unproven); removal due before 2026-10-26T12:00Z.
* Cleanup: delete the VM, disk, NIC, Bastion and public IP by exact name; remove the role assignment; soft-deleted secret retained per policy.
* Residual risk: a new inbound administrative path and transcript exposure.

## Proposed approval wording (Option C)

"Part 1, design only: I approve Option C as the design for issue 462. I will choose and keep the resident demo shared password myself and I name the sharing channel and recipients as: [owner to state]. Authorise writing the offline verifier tool in the repository. This approves no Azure action, no secret generation or write and no role, network, VM, Bastion or firewall change.
Part 2, not yet given: any later write of the verifier and session key to kv-cutovertest-rzsrg in resource group ama, expiring 2026-10-26T12:00Z, needs a separate approval after all of: a proven write principal and path, the corrected limiter (Medium) and email-equality (Low) findings, the budget headroom proof under the non-reset USD 50 cumulative incremental cap, the full gate and independent assessment."

For Option A the wording must instead name the owner object id, the single secret scope, the VM, Bastion and subnet resources, the expiry and the budget gate, and is likewise design-only until the gates pass.

## Still unproven

* Budget headroom, and the cost of anything billable.
* Whether the ARM secret write works to the private-only vault, and the app's secret reference at runtime (management-plane write is documented, not tested).
* Whether the owner has an existing private path elsewhere.
* Role time-boxing without PIM.
* The deployment write principal for the vault secrets.

## Independent critique

One critique ran on 2026-10-25 (verdict Revise, 7 findings, 2 blocking). All were accepted and applied above: verifier and session-key protocol specified, write authority made an explicit gate, Option C labelled a different operating model, audit claims narrowed, Option A feasibility gaps listed, cost labelled partial, approval split into design-only and later gated parts. Not repeated.

## Next engineering corrections (separate, open, block deployment)

* Medium: the login limiter keys on the peer address and collapses to one bucket behind the ingress.
* Low: `authorise` does not require the typed email to equal the row's email.
