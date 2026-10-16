---
title: Environment parameter sets phase details
description: Completion evidence and bounded write surfaces
ms.date: 2026-10-16
---

Task ID: issue-137. Task slug: environment-parameter-sets.

## P01-T01

Keep main.bicepparam as the dev file to preserve callers. Test uses production
defaults; dev declares development quarantine/purge relaxations, not public
SQL. Pilot locations remain empty marked placeholders. Add separate region
and quota reference inputs with named nonempty guard checks; compile committed
examples offline but never treat compilation as deployment readiness.
Keep the current name/hash/tag scheme. Restrict wrapper scope to ama and
validate workload input against the documented lower-case alphanumeric rule.
Development alone keeps purge and quarantine. Add registryQuarantineEnabled
default true and a production rejection guard; forward it unchanged to registry.
Compute purge protection from its explicit input, retaining production safety.

## P01-T02

Compile all three bicepparam files and merge their values with compiled
defaults. Assert actual environment differences, missing-check rejections,
pilot placeholders, tag routing and naming expressions. Preserve issue 139
profile matrix and security mutations. Replace SQL-switch/firewall assertions
with unconditional private SQL and no-firewall assertions. Use fake az to
prove invalid group/workload inputs stop before any Azure call.
Use synthetic valid-check references and explicit fictional locations only in
the semantic test baseline; independently reject empty references/locations.
Extend existing production/development matrix for independent quarantine/purge
choices and their bypass mutations. Reconcile directly coupled legacy text
assertions in test_edge_module.py and test_governance.py; no new methods there.

## P01-T03

Replace the environment section's settled pilot decisions and hypothetical
groups with current open decisions/ama-only boundary. One environment
differences table includes profiles, SKUs, retention, redundancy and access.
Historical observations stay dated, never reused as current quota evidence.
Correct directly coupled SQL statements elsewhere in infra README. Record
taggable-resource exceptions and per-component workload/classification tags.
Consolidate Deployment profile into the one canonical environment table and
correct the settled pilot assertion in Governance controls.

## P02-T01

Run all infra tests with absolute source-project PYTHONPATH, REQUIRE_AZ_BICEP=1,
all Bicep build/lint and parameter compilation; targeted Python lint/type
checks. If dependencies are missing, install via pip in an isolated venv.
Local app smoke uses installed source packages and an isolated synthetic
temporary data path, loopback only, no AI or Azure call.

## P02-T02 and P02-T03

Review once against issue acceptance, current owner direction and observed
evidence; record unmet live prerequisites. Resolve authenticated GitHub user,
configure repo-local noreply identity, commit with required trailer, push the
existing topic branch, create a main-target PR. No merge or issue checkbox edit.
