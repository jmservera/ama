---
title: Plan for issue 185 live device identity demo
date: 2026-11-18
---

Goal: fresh, independently re-queried live proof of the two open criteria, docs only.

* [ ] Phase 1: grant temporary Registry Contributor to `id-cutover-test-api` on the hub; run throwaway job `job-185b-probe` that creates 3 SAS devices (Hub keys), maps each to a stock home id via tags, sends with issued key, then deletes; capture redacted job logs via Log Analytics or `az containerapp job execution`.
* [ ] Phase 2: independently re-query hub stats and registry count, scan captured output for key text, delete job and role.
* [ ] Phase 3: write the research note section and per-criterion table; changes and review records; commit.

Validation tier: focused (documentation only). No source edits.
