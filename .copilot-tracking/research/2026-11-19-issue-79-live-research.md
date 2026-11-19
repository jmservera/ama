---
title: Issue 79 live research (2026-11-19)
ms.date: 2026-11-19
---

Refs #79. Research disposition: executed. Planning readiness: Ready (outcome: no buildable criterion).

* Unticked criterion 3 (named owner signs first rule order): human signature, `ranking-v1` owner is "to be named". Not buildable.
* Unticked criterion 4 (snapshot publication scheduled and retained): code exists (`src/orchestrator/.../ranking_publish.py`, `src/core/.../ranking_publication_runner.py`, `ranking_archive_blob.py`), Bicep job `rankingPublish` exists in `infra/modules/containerapps.bicep`, and tests pass. What remains is deploying an image containing the entry point, provisioning the job, and an owner-approved retention period with Blob immutability: deployment, infrastructure and owner decisions.
* Prior live evidence: `docs/reference/research/issue-79-live-ranking-publication-evidence-2026-11-18.md`.
* Local check 2026-11-19: ranking tests `src/core` 146 OK, `src/orchestrator` 11 OK; `src/api` ranking tests ran (timing output only, no failures printed).
