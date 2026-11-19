---
title: Issue 203 criteria refresh at head 7ea3a1ff6, 2026-11-19
description: Re-run of the legacy-reference checker and read-only live health for the two unticked issue 203 criteria; no source change was possible without the FULL tier
ms.date: 2026-11-19
---

Refs #203. Head `7ea3a1ff6`. Synthetic demo, desktop only, resource group `ama`. Read-only Azure CLI and unauthenticated `/healthz`; nothing created, nothing to delete; no credential read.

| Criterion | Result | Evidence |
| --- | --- | --- |
| Repository search returns only intentional historical references | Proven for the checker scope (observed, re-run) | `python3 tools/check-legacy-references.py` exit 0; `python3 -m unittest tools.test_check_legacy_references` ran 8 tests, OK (includes `test_repository_has_no_violations`). The exemptions (generated cut-over records, dated notes, guard files) are the ones recorded on 2026-11-18. |
| Deployed app and CI green from `src/` | Partly proven; not tickable | `ca-cutover-test-demo-api` provisioning `Succeeded`, ready revision `--0000033`, image digest `sha256:5368f4e4...`; `/healthz` returns 200 on it and on `ca-resident-demo`. `Source projects CI` latest three runs `success` (pull-request branches, 2026-11-19). The digest has no build provenance to a `src/` commit and no push CI on `main` exists. |

## Why no code was built

The only way to close the second criterion is a provenance label or a `src-deploy.yml` run. That edits a Dockerfile or deployment workflow and publishes an image, which is the FULL tier (deployment) and needs a push, so it is out of scope for this run. The first criterion is already enforced by an existing test, so a new test would only restate it.
