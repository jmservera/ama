---
title: Demo AI verification 0603 research
description: Increment A readiness inputs and exact-source proof search, documentation only
ms.date: 2026-11-13
---

* Source: branch test/demo-ai-verification-0603, HEAD `3c42b381ed33c6acb3db63ad3d1dd021358b0118`, tree `befb492b2f0857bc94b5139affd9be90b3658c19`; source identical to main `15bfee2d7f6ae9b73d24c51d3dbbea7c7b78f626` (`git diff` of src is empty because HEAD only adds tracking files). Research disposition: executed.
* Read: the seven `demo-ai-readiness-0548` records (3c42 readiness Pass-with-comments; its unread items were not treated as facts), `docs/reference/memory.md` (first 80 lines), `src/core/README.md` test commands (line 341, 368), test imports, mock/skip scans, `test_chat_model.py` lines 1-110 (full file not read line by line), `test_ai_consumption.py` Port header, `foundry_provider`. Not read: the two case-study specifications and `docs/reference/README.md` index (time budget), full bodies of `test_chat_panel.py` (880 lines) and `test_ai_consumption.py` (798 lines) beyond grep scans. These are disclosed gaps; execution did not occur, so none was relied on.
* Owning projects: `test_ai_consumption`, `test_chat_panel` -> `src/core/tests` (an `src/api/tests/test_chat_panel.py` also exists and is out of scope); `test_candidate_comparison`, `test_chat_model` -> `src/agents/tests`.
* Mocks and gates: no `skip` decorators found. `test_chat_model` patches `urllib.request.urlopen`, `Ai._token` and `data_protection.dispatch_hold` with a synthetic endpoint; core tests use temporary SQLite via `SqlStore`/`Port` (`mssql = False`). `test_chat_model` imports `dataset` from core tests, so core test dir is a required fixture path.
* Retained exact-source proof: none. The only references to `test_candidate_comparison` are older issue-108 records on earlier commits and the 0548 plan; no retained local or hosted result exists for HEAD source with these four selectors. Hosted CI was not queried (no push, time).
* Provenance: user-site editable installs `zava-forward-*` resolve to the primary checkout `/home/azureuser/source/ama/src/*`, so default `python3` does not test this worktree. Wrong-primary provenance proven.
