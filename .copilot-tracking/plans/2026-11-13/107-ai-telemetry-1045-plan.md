# Plan: #107 AI telemetry raw-content exclusion (107-ai-telemetry-1045)

Details: [details](../../details/2026-11-13/107-ai-telemetry-1045-details.md). Research: [research](../../research/2026-11-13/107-ai-telemetry-1045-research.md). Tier: Focused (tracking-only, local offline).

* [ ] Phase 1: independent critique (this file's companion `...-critique.md`) before any venv or run.
* [ ] Phase 2: copy 14 `demo-ai-*` tracking files byte-identically from `bdecadacf`; verify 14 sha256.
* [ ] Phase 3: create `/tmp/venv-107-1045`, editable-install core and agents, verify module origin in this worktree.
* [ ] Phase 4: run `test_ai_consumption` and `test_chat_panel` with `unittest -v`; record counts, skips, producer exit codes.
* [ ] Phase 5: run synthetic sentinel probe (5 assistants, accepted-proposal, chat turn, limit-fallback); record script, sha256, result.
* [ ] Phase 6: write changes file, remove venv, independent code-review, commit with trailer, record witnesses.

Outcome rule: a sentinel hit is reported as an adverse finding, not hidden; no `src/` edits. Criterion stays unchecked unless the probe is clean and review accepts.
