---
title: UI and cache required observations follow-up details (Refs #440)
description: Commands and acceptance for the two focused observations
ms.date: 2026-11-05
ms.topic: reference
---

* Auxiliary: `git worktree add --detach /tmp/m440b bb3a3b03...`; output `/tmp/o440c` (new), scrubbed `env`, `PYTHONDONTWRITEBYTECODE=1`, external `TMPDIR`, `PYTHONPATH` with `/tmp/m440b/src/{core,agents,api}/src` and tests first.
* Lock: `fcntl.flock(LOCK_EX | LOCK_NB)` once for both checks; stop if held.
* Check 1 from `/tmp/m440b`: `python -m unittest -v tools.test_rpi_checks.GateTests.test_api_install_prevents_scrubbed_server_child_writing_source_bytecode`.
* Check 2 from `/tmp/m440b/src/api`: Runner `BROWSER_ENTRY` equivalent around `checks.case_journey_browser_check --axe <pinned axe> --out <new dir>`; exits captured with `subprocess`.
* Acceptance: both actual exits 0, module identities under `/tmp/m440b`, no skip or threshold change, auxiliary status clean afterwards.
