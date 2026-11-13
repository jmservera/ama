# Details: #164 criteria audit

## Phase 1

* File: `.copilot-tracking/changes/2026-11-13/164-chat-grounding-criteria-1652-changes.md`.
* Content: test run table (commands, counts), per-criterion table with columns criterion, code and test evidence, missing for 100% proof, verdict (`Proven`, `Not proven: awaiting human approval`, `Not proven: evidence gap`), and a recommended issue-comment wording that does not tick any box.
* Verdict rule: every clause of the criterion text must be satisfied by merged code and a passing test.

## Phase 2

* `code-review` agent checks every claim in the record against `chat_eval.py`, `ai_registry.py`, `heldout_batch.py` and the cited tests.

## Phase 3

* `git config --local user.email` from `gh api user`; commit; verify `git status --short` empty and `git diff --check` clean.
