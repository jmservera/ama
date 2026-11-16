---
title: Phase details for issue 1820
ms.date: 2026-11-16
---

## P01 details

* Edit region: Step 5 of the coordinator agent file, witness call-list paragraph (around line 600) and model paragraph (around line 630).
* Ordering text: the worker persists the dated artifact first, then calls the witness: `research-open` after the research Markdown exists, `implement-start` after the changes Markdown exists and before any source edit. Never stage `__pycache__`, `.mypy_cache` or `.ruff_cache`.
* Hygiene text: run `src/core` and `src/api` suites sequentially in a worktree; `read_bash` delay at most 600; check `/tmp/ama-rpi-heavy.lock` before `rpi-checks.py --all` or pass `--lock-timeout 0`.
* Model text: coordinator on Automatic (for example gemini-4-hydrogen); code, rebase and UI RPI workers claude-sonnet-5.5; validation-only or docs-only loops may use gemini-4-carbon or Automatic; independent exact-head review gpt-6.1-terra or code-review agents. The launch script `--model` and `--claim-model` follow the selected worker model; an unavailable model is a blocker, no silent fallback.
* Validation: Markdown diff review; no executable code.
