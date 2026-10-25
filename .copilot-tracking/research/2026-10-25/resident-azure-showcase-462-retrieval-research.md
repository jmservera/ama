# Research: private demo-password retrieval route (issue 462)

Written 2026-10-25 after the read-only probes below ran (probes 21:50Z to 21:54Z, so research is a record of them, not predictive). The plan and proposal were written after this file. Refs #462.

## Owner directions (2026-10-25)

* "Prepare a minimal private retrieval proposal for my approval."
* "Accept the disclosed deviation and continue through all remaining gates." This clears only the initial ungated planning-push process hold (`5963fa3f`). It is not retrospective compliance and no technical gate is cleared. The original adverse review and chronology are kept.

## Scope and limits

Management-plane metadata for resource group `ama` only, plus the public Azure Retail Prices API. No secret list, read or generation, no Azure write, no data-plane call, no Graph, no private file. Earlier raw cost JSON was deleted; no budget headroom is claimed.

## Facts proved (az, resource group ama, 2026-10-25T21:50Z to 21:54Z)

* Vault `kv-cutovertest-rzsrg`: Standard, RBAC authorisation on, public network access Disabled, default action Deny, bypass None, no IP or VNet rules, soft delete 7 days, purge protection not set. Diagnostic setting `to-log-analytics` sends the `audit` category (enabled) and `allLogs` (disabled) to the group's Log Analytics workspace.
* Private endpoint `pe-kv-cutovertest-rzsrg` is Approved and Succeeded in `snet-pe` (10.40.4.0/24). `privatelink.vaultcore.azure.net` has one A record for the vault (10.40.4.18) and a virtual-network link to `vnet-cutover-test` only.
* `nsg-cutover-test-pe` allows inbound HTTPS from the VirtualNetwork tag only and denies the rest.
* The group holds no virtual machine, Bastion, VPN, gateway, DNS resolver, peering or dev-box resource. Existing in-network compute: two Container Apps environments (`cae-cutover-test` internal on `snet-aca`, `cae-cutover-test-demo` external on `snet-aca-demo`), three container apps and eight jobs (`init`, `verify`, `ledger-verify`, `import`, `orchestrator`, `smoke`, `mi-http`, `public-audit`). These are workload or test jobs, not owner retrieval clients, and a job's output goes to container logs, which this task forbids for the password.
* Roles on the vault scope including inherited: one Key Vault Secrets User, held by the `id-cutover-test-api` managed identity at vault scope; no Secrets Officer, Administrator or Crypto role; Owner held by users and service principals above the group (management plane only). Owner does not imply secret read.
* The signed-in `az` principal on this VM is a service principal, so the owner's personal object identity cannot be resolved from here and was not looked up.
* No existing client in the group can be used by a remote human without a new resource or a job. Hypothesis, not proved: a client exists elsewhere (another tenant network, a corporate VPN). Absence in this group does not prove none exists.

## Public price metadata (Azure Retail Prices API, queried 2026-10-25T21:53Z, uksouth, single page, NextPageLink null)

* Virtual machine `B1s` Linux consumption: 0.0118 USD per hour (effective 2025-10-01). Disk, public IP and egress not priced here.
* Azure Bastion Standard gateway: 0.29 USD per hour (effective 2021-07-01). A Developer or Basic SKU row was not isolated in the returned rows, so its price is unknown here.
* Key Vault secret operations: priced per 10K operations; a handful of reads is negligible but not quantified here.

## Options assessed

* A, retrieve from the vault with a new private client: a short-lived VM plus Bastion in `vnet-cutover-test`, owner given Key Vault Secrets User on one secret. Adds a network resource, an inbound path, a human data-plane role, a terminal transcript risk, and cost against an unproven cap.
* B, a job prints the password: rejected (container and job logs).
* C, owner chooses the password and the vault holds only a verifier. The owner picks a complex password in their own password manager. An offline command (to be written after approval) reads it from a hidden prompt and prints only the scrypt verifier. The verifier and a random session key are written to the existing vault by the secure management-plane ARM deployment, and the app reads them by its managed identity inside the network. The password never touches the cloud, so no owner retrieval route is needed and no role, VM, Bastion or network change is required. Trade-off: this departs from "generate a complex one" and "retrieve from the vault"; the owner generates it, which still meets "complex, shared, demo only".

## Unproven

* Budget headroom (G1) and anything billable.
* Whether the owner has a corporate private path to the vault.
* The management-plane ARM secret write path with `publicNetworkAccess` Disabled: documented as management-plane, not tested here.
* Whether a time-bound data-plane role is possible without Privileged Identity Management; an explicit named removal is the proven-possible cleanup.
