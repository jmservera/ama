<!-- markdownlint-disable-file -->
---
title: Issue 350 main acafc6ee integration research
description: Prospective research for merging origin/main acafc6ee into the topic
ms.date: 2026-10-26
---

Written 2026-10-26 before plan, critique and merge. Topic head `7a43bbbeb682feb6c75ae4267d2eed8f7896fedf`, clean; remote `a9bdae31` ancestor; merge base with main `c8d16059`. Fresh `origin/main` `acafc6ee04e3612cd62349ab9e4a0af3b24e8109` (PR 460, one commit, 42 paths, docs, tracking, rubric, requirements). Earlier reviews and the c8d16059 candidate and gate plan are historical and unchanged.

Evidence (`git diff HEAD...origin/main`): main touches docs/capstone, sandbox and hve-builder tracking, docs/reference (including the append-only `log.md`), `.github/rubric/scores/{badge.svg,latest.json}`, one agent file, a presentation, a new root `requirements.txt` (`markitdown==0.1.9`) and `tools/cowork-native-recovery/` (new script and content). The topic changed `tools/check-demo-feedback.py`, `tools/test_check_demo_feedback.py` and `.copilot-tracking/` 2026-10 issue-350 artifacts. The two path sets do not overlap, so no textual conflict is expected. The topic never touched `log.md` or the rubric, so main's versions apply with no score synthesis; if a rubric conflict appeared, main's baseline would be used with rationale.

Integration relevance: no `src` change; the new root `requirements.txt` is not referenced by `tools/rpi-checks.py` (which uses `src/api/requirements.txt` and `tools/rename-zava-requirements.txt`); the checker and its 88 tests are unaffected. No reinstall needed. Shared-runner edits are out of scope (issue 349 owns the durable no-cache image gate correction); a full gate waits for that fix to be published and integrated, recorded as an explicit dependency.
