---
title: Changes for issue 1820
ms.date: 2026-11-16
---

## Status

Complete. Single file changed: `.github/agents/ama-backlog-delivery-coordinator.agent.md` Step 5.

* Witness ordering (artifact before record; research-open after research Markdown, implement-start after changes Markdown and before source edits) and never-stage cache directories.
* Execution hygiene (sequential src/core and src/api suites, read_bash delay <= 600, heavy-lock check or --lock-timeout 0).
* Model-fit guidance replaces the blanket Sonnet 5.5 rule; `--claim-model` and the launcher `--model` are now `{model}` parameters. No silent fallback rule retained.
* `.github/copilot-instructions.md` unchanged by design (model-agnostic).

## Validation (Focused tier)

* `git diff --check` clean; no other repository references to the replaced sentence.
* HVE static evidence: diff read for internal consistency (launch record, launcher and run command all carry `{model}`). HVE behavior simulation: not applicable, as no executable path or hve-builder-tester fixture covers this agent file; independent exact-head review stands in.
