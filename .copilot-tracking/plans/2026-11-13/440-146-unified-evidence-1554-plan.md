---
title: "#440 unified evidence pack plan"
ms.date: 2026-11-13
---

## Plan

1. Cherry-pick the five commits in order: 6b1040920, 49c04e7ba, 86063622c, 035e859e6, b8387e019. Resolve conflicts keeping both sides' content (log.md, README.md); take either side for the TSV.
2. Regenerate `docs/architecture/cutover-reference-inventory.tsv` with `zava_forward.core.synthetic.cutover_audit`.
3. Run `test_cutover_audit` (9), `test_bicep_policy` (61), link check on added lines, secret scrub.
4. Independent review, then one clean local commit with Copilot trailer. No push.

## Critique amendments

Pick 8df9d6108 and 378d0f997 before 49c04e7ba (parents of the #146/#79 commit); stage before regeneration; install `src/orchestrator`; link-check all changed Markdown; scan all staged additions.
