---
applyTo: '.copilot-tracking/changes/2026-11-13/470-delivery-tools-verify-1222-changes.md'
---
# Plan: verify tools/ unit tests (Refs #470, #1204, #1297)

* [ ] Phase 1: run each tools/ test module separately with `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v <module>` from the repo root (rename-zava-tests.py run as `python3 tools/rename-zava-tests.py`), from a scratch log dir outside the worktree, saving `$?` directly.
* [ ] Phase 2: record per-module tests, skips, duration, log sha256 and exit code in the changes file; confirm `git status --short` shows only .copilot-tracking additions.
* [ ] Phase 3: independent code-review, review file, `git diff --check`, commit with trailer, witness records.

Stop rules: no edits to tools/, src/, docs/; no network, Docker, browsers or locks; a failing module is recorded, not fixed.
