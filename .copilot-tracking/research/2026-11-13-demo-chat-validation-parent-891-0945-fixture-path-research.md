---
description: Research for the fixture-path factual correction of the chat validation parent integration
date: 2026-11-13
---
# Fixture-path correction research (2026-11-13)

* Disposition: executed, bounded, read-only. Planning Readiness: Ready.
* Independent Readiness (provenance below) found one Medium documentation defect: the canonical observation and parent details line 11 and research line 13 say the fixture resolved "under site-packages".
* Source evidence (immutable `plans/2026-11-13-chat-clean-validation-891-0901-recovery-plan.md` line 8): the module `ai_eval.__file__` was under site-packages, but `GOLDEN` resolved to `/tmp/v891-0901/lib/python3.12/evals/ai_priority_golden.json`, outside site-packages, exists False; the repository fixture `src/agents/evals/ai_priority_golden.json` exists.
* Preserved: cause supported but unconfirmed; the preflight probe was separate from, and not, the original test process; 37/37 historical; no new AI, privacy or live acceptance.
* Readiness coverage limit: the reviewer fully read all 19 tracking Markdown files and the complete 30-path diff, but only changed and adjacent canonical-doc sections, not complete histories. No full historical-body review is claimed.
