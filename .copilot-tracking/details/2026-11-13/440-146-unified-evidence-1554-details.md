---
title: "#440 unified evidence pack details"
ms.date: 2026-11-13
---

## Phase details

* Order: checkpoint first, then audits by issue number desc as listed in the brief; the inventory is regenerated last because earlier picks change referenced files.
* Tests install `src/core` and `src/agents` into a `/tmp/venv-*` with pip only; remove before commit.
* Link check: parse added lines of changed `.md` files for relative links and verify the targets exist.
* Secret scrub: grep added lines for key, token, password and connection-string patterns.
* Commit: single commit containing the cherry-picks (use `--no-commit` picks, then one commit).
