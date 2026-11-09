---
title: Infrastructure integration topic 136 details
description: Phase details for the planning-only issue 136 integration topic record
ms.date: 2026-11-08
---

## Record structure (topic record sections, in order)

1. Identity and boundary: task, branch, base, local-only, Refs 136 only.
2. Provenance table: item, path or ref, blob or SHA, status, ms.date, source of observation, classification.
3. Integration boundaries: included (the parent record itself), excluded (every sibling branch and child), and the 144 stacking rule.
4. Hierarchy and dependency map: table of 136, 137 to 148, 113, 118, 107, 195, 201, 440, with state, labels and dependency basis (body text or API).
5. Module coverage register: columns module or unit, path, wired from, status class, delivered or missing or manual, owner, approver, unknowns.
6. Acceptance criteria status for 136: five rows, all unmet, with missing evidence.
7. Contradictions C1 to C8 as review items.
8. Human decision register.
9. Gates, currency rule and resume points.
10. Not claimed: explicit list.

## Module coverage seed (from research, to be re-read from files when writing)

Status class vocabulary: delivered code (static reading), observed local (this session), authorized Azure observed (none), planned, unknown. A row is "delivered" only as authored Bicep; none is claimed live or accepted.

* In Bicep and wired from `main.bicep`: guard, identity, network, monitoring, keyvault, storage, registry, sql, foundry, iothub, operationalMonitoring, budget and alerts in main.
* In Bicep, conditional: containerapps (apps), edge (`enablePublicEdge` default false), authTokenStore (`enableEntraTokenStore` default false).
* In Bicep, separate unit not wired from main: governance (policy audit only, locks, Defender plans, activation deferred), iot-hub-live, live-simulator-job, public-edge-existing, private-proof-publisher, resident-assistant, resident-demo, staff-initializer-rbac.
* Scripted, run by the owner: SQL users and grants, Entra registration, staff initializer.
* Intentionally manual (owner is the repository owner unless a human role is named; confirmation open): Entra tenant items, contractor B2B policy, Microsoft 365 grants, GitHub environments, OIDC federation, branch protection, subscription and group.
* Missing or deferred: Defender activation (cost approval pending), public edge deployment for the synthetic demo, ledger digest upload and scheduled verification, AI Search, Service Bus, Content Understanding (out of scope), real worker images and queue adapter (144), live hardening, Azure load and restore proof.

## Verification method for each step

* Provenance: `git rev-parse`, `git ls-tree`, `git rev-parse HEAD^{tree}`, `git fetch`, `gh issue view`, `gh pr view`, `gh api` reads only.
* Coverage: file existence and `grep` of module and resource declarations; no template compile.
* Contradictions: quote the exact current file or issue text with its path or number.
* Validation: `git diff --check`, ASCII scan via grep, closing-keyword scan; no other command.

## Stop conditions

* `origin/main` differs from the base SHA: record and stop for re-planning.
* Any step would need a test, build, service, Azure, model call, private dataset, `support/` read or a source change: stop and record a blocker.
* A record would imply acceptance, a tick, approval of a Proposed ADR or an agent decision on a named human item: remove the wording.
