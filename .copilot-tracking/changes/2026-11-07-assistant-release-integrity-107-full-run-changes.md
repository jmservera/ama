---
title: Changes for the 107 score-only main merge before FULL
description: Second normal merge, verified delta and honest limits
ms.date: 2026-11-07
---

Plan: [plan](../plans/2026-11-07-assistant-release-integrity-107-full-handoff-plan.md), second amendment. Earlier records are preserved.

* Pinned main 8af3aea6b042f5dfb3305e18334439717f7c5649 merged once with `--no-ff`; merge parents are the amendment commit b2a9c37a8 and 8af3aea6b. No conflict, rebase, force or rewrite. Ref `backup/issue-107-35bc44a97-pre-merge2` keeps the prior head.
* Verified: delta versus the prior head is the plan amendment and `.github/rubric/scores/latest.json` (parses as JSON) plus these records; `src` is byte-identical to the prior head; the only source delta versus main is `src/api/tests/test_assistant_release.py`; `git diff --check` clean. No production change. No new tests were run after this merge; the earlier light results stand for the unchanged source, and FULL follows.
