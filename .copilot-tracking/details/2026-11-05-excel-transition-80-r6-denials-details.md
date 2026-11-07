---
title: Issue 80 round 6 details
description: Phase details
ms.date: 2026-11-05
---

* Phase 1: reuse `FormApi.raw`, `two_versions` and `call`. Register extra synthetic staff (Application Administrator, an unregistered role, Grants and Evidence Officer) in the store's staff table and cache so the real login and `_actor` re-read see them. For each actor: expect 403, no `SYN-TECH`, digest, `pam@example.test`, resident name or case id in the body; compare `form_schemas`, cases and audit chain length before and after; patch `store.ai._chat` to raise. Also assert the JSON route denial for the same actors, so the CSV is not stricter or looser than the authoritative list.
* Phase 2: from `src/api`, `python3 -B -m unittest tests.test_form_staging_api tests.test_list_export_api tests.test_role_endpoint_inventory tests.test_loading_feedback`; `ruff check --no-cache .`; `ruff format --no-cache --check .`; `mypy --cache-dir /tmp/r6-80-mypy`. Print `server.py` and `forms.py` paths first.
* Phase 3: r6 changes, review and state records, then commit with the repository-local privacy-safe identity.
