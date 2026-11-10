---
title: Infrastructure integration topic 136 record
description: Planning-only parent integration topic record for the issue 136 Bicep and platform epic, with provenance, boundaries, hierarchy, module coverage and honest status
ms.date: 2026-11-08
---

## Identity and boundary

Task `infrastructure-integration-136`. Worktree `/home/azureuser/source/ama-wt/issue-136-integration`, branch `feat/infrastructure-integration-136`, declared PR target `main`. Local only: not pushed, no PR exists for this topic, and nothing here is remote. References use `Refs #136` only. This record is a planning anchor on the parent. It integrates no child and no sibling branch, meets no 136 criterion and approves nothing.

Planning basis: `.copilot-tracking/research/2026-11-08-infrastructure-integration-136-research.md`, `.copilot-tracking/plans/2026-11-08-infrastructure-integration-136-plan.md`, `.copilot-tracking/details/2026-11-08-infrastructure-integration-136-details.md`, `.copilot-tracking/plans/2026-11-08-infrastructure-integration-136-critique.md`, planning commit `ca9da0eae92b58522d7cc0609f5b23acdcc9c5b1`.

## Provenance

Observed this session by git and read-only gh. Classification column: observed local (O), static reading of delivered code or document (S), unknown (U).

| Item | Path or ref | Pin | Status or date | Class |
| --- | --- | --- | --- | --- |
| Base commit | `origin/main` | `0f05e9aae70768def8d1d9c300215f9ee2f11638`, tree `577947cb2d94de5b79f24d38b6f459ebb0aa13a8` | Commit time 2026-11-08T08:14:36+01:00; re-fetched before this record and still equal | O |
| ADR 0001 | `docs/adrs/0001-azure-architecture.md` | blob `d42fa5c4615f4107cee83e07555dba6985c1f53e` | Proposed, ms.date 2026-10-24; non-production demonstrator design, not approved | S |
| ADR 0002 | `docs/adrs/0002-pilot-readiness-architecture.md` | blob `cbe21530043ff15432cc6dce1086d080f5eb15b4` | Proposed, ms.date 2026-10-24; only the staff identity decision is owner-accepted (2026-10-24); decision 6 (deployment, replicas, region, hardening, CI) remains a proposal | S |
| ADR 0003 | `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md` | blob `d60645397b20fb70ac3d1dc47c7a6c8671201306` | Accepted with owner amendment 2026-10-15, reconciled 2026-10-18, ms.date 2026-10-29; decision 6 (Basic IoT Hub) is an owner decision, not evidence of deployment, cost or credential authority | S |
| ADR 0006 | `docs/adrs/0006-src-layout-and-cutover.md` | blob `956da1a3b804c803041fe2e8a312bd9f400273ae` | Accepted 2026-10-15 by the owner, ms.date 2026-10-27 | S |
| Infra README | `infra/README.md` | blob `7988be37fab8e467c7973f018d9f4a6f733cda3b` | Contains the Resource coverage register (issue 136, 2026-11-04), a documentation record, not machine-checked | S |
| Entry template | `infra/main.bicep` | blob `20ef78d888fdad6568d039ea1c898628468ed310` | Resource group scope, 691 lines | S |
| Case study | `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md` | blobs `0aec2d8070117a647574b1fadc8cfbdd2af68598`, `888d9ff7d0190799308618dc7f153c00adabd6f6` | Read as framing; preserved unchanged | S |
| Reference index and memory | `docs/reference/README.md`, `docs/reference/memory.md` | blobs `1f5f310d40b87019c18c20bc2f9c0a446d6c701a`, `e1268db9a452b5db1ca0796f32ccae00b0b418dd` | Memory is context, not evidence | S |
| Defender and Policy record | `infra/defender-decision.json` | not pinned | 2026-11-01, owner Juan Manuel Servera; Policy audit only; Defender deferred; cost approval pending | S |
| Azure state | none | none | No authorized Azure observation in this session | U |

Draft, in-review and Proposed documents are not approval, and none is approved through this plan.

## Integration boundaries

Included: this parent record and the five planning records only.

Not included, each by number and state at the pins above:

* 137, 138, 140, 142, 143, 145, 146, 148: open, not integrated, no branch brought in, not implicitly accepted.
* 139, 141, 147: closed on the tracker; closure is not acceptance of any 136 criterion.
* 144: open, paused for this parent topic and demo priority. Published PR 1141 (open, not draft, base `main`, head `1a9616d4e9ab89d93a72204d82ee26c70baee06c`, listed checks pass at that head) is unchanged and not retargeted or pushed. Local `feat/slice-144` at `ea7f36c030e7a6fbac740d382fafa54f2de2dbf4` is in its own worktree, not read into this topic.
* Siblings in other worktrees and unmerged branches: not integrated.
* Source, Bicep, config, workflow, requirements, ADR and README files: not changed.

## 144 stacking rule

This topic performs none of the following steps and authorizes none. Future order, owned by the coordinator or owner: (a) independent exact-head assessment of the final head of this topic; (b) fresh selected CI on that head; (c) coordinator exposure as a draft parent PR to `main`; (d) a separate decision and new RPI task for 144 that pins the reviewed parent commit SHA as its base. In that task, the 107 and 118 source prerequisites are verified in the proposed 144 base first; a missing prerequisite stops the task with a recorded blocker, with no rebase or recreation. Establishing a reviewed topic clears only the stacking topology blocker. It does not supply child source prerequisites, human acceptance or live acceptance, and it does not make 144 unblocked. 144 identities: published `1a9616d4`; local `ea7f36c0`; body candidate `6496f61f0361c27c297b97b12a5c46e374cd6a5f`, observed as an ancestor of `ea7f36c0` and not of the published head; supplied original `0bd489d3` is unresolvable in this repository and remains unverified.

## Hierarchy and dependency map

Refreshed with gh immediately before this record; no state changed from the research pass.

| Issue | State | Role and dependency basis |
| --- | --- | --- |
| 136 | Open, last updated 2026-10-23 | Epic, five criteria all unticked; body says relates to 113 and 118 |
| 137 | Open | Child, environment parameter sets |
| 138 | Open | Child, pipeline; body: depends on 137 and 118; no tracker edge |
| 139 | Closed | Child, Bicep quality gates beyond build and lint |
| 140 | Open | Child, IoT Hub module |
| 141 | Closed | Child, identity, RBAC and Entra registration as code |
| 142 | Open | Child, Key Vault secret lifecycle |
| 143 | Open, `delivery:deferred` | Child, private networking and public edge |
| 144 | Open | Child, container hosting; body: depends on 107 and 118 (text only, the tracker shows no blocked-by edge); PR 1141 open |
| 145 | Open | Child, Azure SQL tier and recovery proof |
| 146 | Open | Child, monitoring coverage |
| 147 | Closed | Child, Policy, Defender, locks and tagging as code |
| 148 | Open | Child, from-empty rebuild and teardown automation |
| 107 | Open | Source prerequisite for 144; RAI release admission criteria unticked; parent 104 |
| 118 | Open | Source prerequisite for 144 and 138; Policy and Defender criterion unticked; parent 113 |
| 113 | Open | Parent of 118 |
| 440 | Open | Scoped stabilization checkpoint required by 136 criterion 1 |
| 195, 201 | Open | Mention 136; restructure epic and cut-over gate; not hierarchy |

## Module coverage and honest status

Status words: delivered means authored Bicep or script exists at the base and is statically read; none is Azure observed, deployed by this topic or accepted. Source of rows is the file listing and declarations at the base plus the README register; the register itself is documentation, not machine-checked.

| Module or unit | Path | Wired from | Status | Owner and approver | Unknowns |
| --- | --- | --- | --- | --- | --- |
| Identity (managed identities, role assignments) | `infra/modules/identity.bicep`, `infra/role-assignments.json` | `main.bicep` | Delivered code | Repository owner; child 141 closed | Live role state not observed |
| Network (VNet, NSGs, private DNS), env DNS, private endpoint | `network.bicep`, `envDns.bicep`, `privateEndpoint.bicep` | `main.bicep` | Delivered code | Repository owner | Live network state, 143 open |
| Monitoring, operational monitoring, alerts, workbook | `monitoring.bicep`, `operationalMonitoring.bicep`, `main.bicep` alerts and scheduled queries | `main.bicep` | Delivered code | Repository owner | Alert tuning and live runbooks; 146 open |
| Key Vault | `keyvault.bicep` | `main.bicep` | Delivered code; secret values set outside the repository | Repository owner; rotation and expiry owner in 142 | 142 open; secret lifecycle unproven live |
| Storage | `storage.bicep` | `main.bicep` | Delivered code | Repository owner | Immutable audit behaviour live not observed |
| Registry | `registry.bicep` | `main.bicep` | Delivered code; images built outside Bicep | Repository owner | Release workflow acceptance in 138 |
| SQL | `sql.bicep` | `main.bicep` | Delivered code | Repository owner | Tier, restore proof; 145 open |
| SQL users and grants | `infra/scripts/create-sql-users.*` | Run by owner | Scripted, manual run | Repository owner | Not observed |
| Foundry | `foundry.bicep` | `main.bicep` | Delivered code | Repository owner | Model availability and quota target-specific |
| IoT Hub and Event Hubs | `iothub.bicep`, `iot-hub-live.bicep`, `live-simulator-job.bicep` | `main.bicep` (hub); live units separate | Delivered code | Repository owner; live apply is owner-gated | 140 open; live acceptance and cost authority unknown |
| Container Apps, jobs | `containerapps.bicep` | `main.bicep`, conditional | Delivered code; worker images and queue adapter incomplete | Repository owner | 144 open; hosted hardening, rollout, load and restore evidence missing |
| Edge (Front Door, WAF) | `edge.bicep`, `public-edge-existing.bicep`, `edge-existing-*.bicep` | `main.bicep` only when `enablePublicEdge` (default false) | Delivered code, optional, deferred for synthetic demo | Repository owner | 143 open; not deployed publicly |
| Entra token store | `authTokenStore.bicep` | `main.bicep` only when `enableEntraTokenStore` (default false) | Delivered code, optional | Repository owner | Not observed |
| Budget | `main.bicep` | `main.bicep` | Delivered code | Repository owner | Cost values unknown |
| Governance (Policy, locks, Defender) | `infra/governance.bicep`, `infra/defender-decision.json` | Not referenced from `main.bicep`; separate unit | Delivered code; Policy audit only; Defender deferred | Juan Manuel Servera (named in the decision record) | Cost approval pending, deny stance open |
| Parameter sets | `main.bicepparam`, `main.test.bicepparam`, `main.pilot.example.bicepparam` | Inputs | Delivered; pilot example non-deployable | Repository owner; subscription owner per 137 | Pilot values and approvals absent |
| Pipeline | `.github/workflows/infra-plan.yml`, `src-deploy.yml`, `src-ci.yml` | GitHub | Authored; 138 unticked | Platform owner | OIDC, environments, reviewers unverified |
| Entra registration, roles, staff assignment | `infra/entra/app-registration.json`, `scripts/setup-entra.py` | Owner runs | Intentionally manual in tenant | Repository owner | Not observed |
| Contractor B2B guest policy | Entra tenant | none | Intentionally manual | Tenant owner, confirmation open | Unknown |
| Microsoft 365 and SharePoint grants | `scripts/grant-sharepoint-access.sh` | Owner runs | Intentionally manual | Tenant administrator | Unknown |
| GitHub environments, OIDC, branch protection | GitHub, Entra | none | Intentionally manual | Platform owner | Unverified in repository |
| Subscription and `ama` resource group | Azure | none | Existing, no teardown | Repository owner | Not observed |
| Ledger digest upload and scheduled verification | none | none | Missing, ADR 0001 open item | Unassigned | Unknown |
| AI Search, Service Bus, Content Understanding | none | none | Out of scope, deferred by ADR 0001 | Not applicable | None |

Infra tests exist under `infra/tests/` (for example identity, governance, IoT, edge, container contract, pipeline, SQL tier, secret lifecycle) and were not run, by the owner CI-first direction.

## 136 acceptance criteria status

All five remain unmet. No tick, closure or closing keyword.

| Criterion | Status | Missing evidence |
| --- | --- | --- |
| Scoped stabilization checkpoint of 440 before closure | Unmet | A recorded checkpoint covering this surface, bug and refactor disposition, authorized Azure-only residuals and any owner-approved pivot or defer; merged children alone do not satisfy it |
| Every resource in Bicep or intentionally manual with owner | Unmet | Owner confirmation of manual rows, tenant owner for B2B, the ledger-digest gap, and live proof; the register is documentation only |
| Child features accepted | Unmet | 137, 138, 140, 142, 143, 144, 145, 146 and 148 open; 139, 141 and 147 closed without recorded 136-level acceptance |
| From-empty deployment reproducible | Unmet | The only observation is dated 2026-10-12, before the 2026-10-27 `src/` cut-over, and has not been re-proven; 148 open |
| Delivered versus missing status kept current in the epic | Unmet | This record is the current status; the 136 body paragraph remains stale and must be refreshed by the owner |

Child 144 criteria also remain unmet: real versioned worker images deployed through the pipeline, hosted hardening, a load test at the declared fixture, live restart with audit persistence and Finance acceptance.

## Contradictions and review items

| ID | Item | Affected | Resolves |
| --- | --- | --- | --- |
| C1 | 136 body says IoT Hub, parameter sets beyond dev, pipeline, policy and edge are not delivered; current files exist for each | 136 body, `infra/modules/iothub.bicep`, `main.test.bicepparam`, workflows, `governance.bicep`, `edge.bicep` | Owner refreshes body; files take precedence for authored status only |
| C2 | 138 body says no deployment, what-if or release workflow; `infra-plan.yml` and `src-deploy.yml` exist, all six 138 criteria unticked | 138 | Owner |
| C3 | README register unmet list omits closed children 139, 141, 147; closure is not criterion acceptance | `infra/README.md` register | Owner |
| C4 | 118 Policy and Defender criterion unticked while `defender-decision.json` records deferral with pending cost approval | 118, `infra/defender-decision.json` | Juan Manuel Servera |
| C5 | 144 body names `6496f61f`; local head is `ea7f36c0` (descendant), published head `1a9616d4` is a diverged line; `0bd489d3` unresolvable | 144, PR 1141 | Coordinator and owner |
| C6 | 144 dependency on 107 and 118 is body text only; no tracker edge | 144, 107, 118 | Coordinator |
| C7 | From-empty observation predates the `src/` cut-over (ADR 0006) | 136 criterion 4, 148 | Owner, via 148 |
| C8 | ADR 0001 and 0002 are Proposed but cited as source references | ADRs 0001, 0002 | Owner; unchanged here |

## Human decision register

Named human, not decided by an agent: Policy deny stance and Defender activation and cost (Juan Manuel Servera, pending); intentionally manual resources and their owners; real deployment, subscription, tenant and cost authority; OIDC, environments and branch protection; contractor B2B policy (tenant owner); Microsoft 365 admin consent (tenant administrator); legal and compliance approvals (not evidenced).

## Gates, currency and resume points

* Currency: if `origin/main` differs from `0f05e9aae70768def8d1d9c300215f9ee2f11638`, report the new SHA and stop for proper planning; no silent merge or rebase.
* Ordered future gates, none authorized here: independent exact-head assessment, fresh selected CI on that head, draft parent PR to `main`.
* Resume points: 440 scoped checkpoint; 107 and 118 source verification in the 144 base; owner confirmations in the register; 144 live acceptance; from-empty reproduction under 148.

## Not claimed

No remote branch or PR for this topic. No 144 unblocking. No child accepted, integrated or merged. No ADR approved. No criterion ticked or issue closed. No Azure, SQL, model, test, build or gate evidence from this session. No decision on any human-named item.
