---
title: Independent critique 164 chat safety plan
task_slug: 164-chat-safety-1105
---

# Critique (rubber-duck subagent, one pass)

Verdict: Approve with changes. Blocking: (1) test_chat_fixture_roles is in src/api/tests not agents; each package's own tests dir first on PYTHONPATH. (2) Offline install must use --no-build-isolation --no-index per package, fail if prerequisites absent. (3) Tests/editable installs/bytecode may write under src; use PYTHONDONTWRITEBYTECODE=1, report any src writes, remove untracked artifacts before commit, no tracked edits. (4) Exit 0 is insufficient: named memory-never-evidence test and representative grounding/injection/poisoning/isolation cases must be shown executed and passing via verbose output; skips enumerated. Non-blocking: record that test_chat_eval.py:182 states integrated memory poisoning is not covered, alongside live and human-labelled gates.

Disposition: all four accepted and applied directly to plan and details; no user decision needed.
