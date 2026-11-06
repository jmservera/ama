---
title: Test log, coordinator behavior run 001 (abd6b3f5f)
---

## Execution record (lead-owned, no grading)

* Target: byte-identical copy of the agent at abd6b3f5f (sha256 2bd539c3d0111f9330110482426b5502cc9ccb9ee5853070a768cd36bb8fa05f, git blob acefb44a4d254ede6d86413343127b763dec42cb) in isolated repo /tmp/h1204/native-sbx.
* Executor: native `copilot --agent ama-backlog-delivery-coordinator --model auto --available-tools view grep glob --no-ask-user --disable-builtin-mcps --max-ai-credits 60 --no-auto-update -s -p`, one run per scenario, 21 real runs, all exit 0 (raw/exit-codes.json).
* Auto-selected models per share transcript: GPT-6.1 Sol (high or medium complexity) for most runs; GPT-6 Luna for SC-14 and SC-21. autoTier unknown. Selection per run is router-chosen; no model was pinned.
* Prompt: neutral wrapper (text-only, nothing executed) plus verbatim scenario text from test-design.md. Scenario text has no target path or framing.
* Containment: read-only tools only, built-in MCPs disabled, cwd an isolated throwaway repo. After all runs `git status --short` in native-sbx and native-neg showed only the untracked copied `.github/` (no writes by runs). Native shell, merge, cleanup and Graph actions were described as text only; no live action occurred.
* Negative control: isolated copy /tmp/h1204/native-neg (sha256 7d5cae62a21b604944f2afa9a29b32514f9fd0d0edbfd9d18ef4d35b9d81cfb5) with deliberate mutations: exited worker frees slot, missing upstream counts as zero unpublished, S02 gate and handoff clauses removed. Discriminating scenarios SC-08, 10, 11, 12, 13, 14, 15 run on it (7 runs, all exit 0).
* Raw outputs: raw/{real,neg}-SC-NN-out.txt and -share.md, byte-exact copies, sha256 in raw-manifest.sha256. No whitespace normalization.
* Observed vs emulated: model outputs are observed; all described commands and actions are emulated text.
* Not tested: schedule replacement, rebase mechanics, tmux syntax, live schedules, real tools configuration, repeated-run variance (one run per scenario).
* Real source mutation: none (source blob verified separately).
