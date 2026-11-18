---
title: Plan for #162 live isolation proof (r2)
ms.date: 2026-11-18
---

1. Run `probe-isolation.py` against the live demo (staff and resident sign-ins read at runtime), retaining redacted raw output and labelled desktop screenshots.
2. Run `src/api` `tests.test_chat_isolation` as the local proof for what cannot be done live.
3. Write the research note `docs/reference/research/issue-162-live-isolation-evidence-2026-11-18.md` with a per-criterion proven/unproven table; update the knowledge-base index and log.
4. Delete `/tmp/state-*.json`. No `src/` change; tier FOCUSED; no `rpi-checks.py --all`.
5. Commit locally; no push.

Details: [critique](../critiques/2026-11-18-issue-162-live-r2-critique.md).
