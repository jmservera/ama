---
title: Issue 891 VM demo release changes
description: Cloud and repository changes made by the VM release
ms.date: 2026-11-08
---

## Cloud changes

* `ca-cutover-test-demo-api`: image `zava-forward-api:1f465bf5e` (revision `--0000026`) to `zava-forward-api@sha256:1605ca20f06598e62441c2894e4c34b554c31bdd9b1e1e88103d3bc3bcca0f64` (revision `--0000027`). Same env names; demo activation unchanged.
* ACR `crcutovertestrzsrg`: temporary export, public access and one IP rule; all restored and read back before the app update. New tag `e2ecee25c` remains in the registry.

## Not changed

Production, pilot, Bicep, resident app, roles, finance, ledger, runners, GitHub workflows.

## Repository

Only `.copilot-tracking` records on `chore/demo-vm-release-891`. Deployed source is pinned main `e2ecee25`.

## Divergences

* Local scans replaced the `src-deploy.yml` build job only; its deploy job needs the absent private runner (owner decision, comment 6723702746).
* Local scratch and docker images created for the build were removed.

## Rollback

Set the app image to `crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:bf7d604510f04347d3344c62c4b487211b489284fa6c5db6ec2c7b85142dcb8f` (revision `--0000026` was healthy).
