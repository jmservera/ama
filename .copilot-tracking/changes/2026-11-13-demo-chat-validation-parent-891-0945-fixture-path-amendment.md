---
description: Amendment correcting the fixture location statement of the chat validation parent integration
date: 2026-11-13
---
# Fixture-path amendment (2026-11-13)

* Supersedes the statement in the first details record line 11 and the first research record line 13 that the fixture resolved "under site-packages". Those bodies stay unedited as history.
* Corrected fact (source: `plans/2026-11-13-chat-clean-validation-891-0901-recovery-plan.md` line 8): the module `ai_eval.__file__` was under site-packages; `GOLDEN` resolved to `/tmp/v891-0901/lib/python3.12/evals/ai_priority_golden.json`, outside site-packages, and was absent. The repository fixture `src/agents/evals/ai_priority_golden.json` exists.
* Retained: the cause is supported but unconfirmed; the preflight probe was separate from, and not, the original test process; 37/37 is the historical recovery result only; no new AI, privacy, live or provider acceptance.
* The ordering amendment is unchanged. The 15 imported records are unchanged. The canonical evidence-pack paragraph was corrected in place (unpublished branch text) and links here.
