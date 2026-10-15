# Research: AI task registry and proposal envelope (#105)

* Existing: `mvp/zavaforward_mvp/assistants.py` REGISTRY (5 assistants, VERSION 1.0.0) and its provider envelope; `ai_tasks.py` comparison records for briefing, message, summary, funding_draft, read_document; priority path in `store.py` calls `ai.run` directly.
* Gap: no single registry covering retained paths, no authority/impact records, envelope lacked task/case/source versions on text tasks.
* Constraints: ADR 0005 synthetic fixtures only; Azure only; AI part of the prototype; no authority transferred to AI.
* Open (owner/qualified decisions, not invented): accountable individuals and delegations, personal validation by task/Assurance/Safety/DPO-Legal delegates, residual-risk assessment, dated UK/EU intended-use review, owner/PRD/task/release acceptances.
* Planning readiness: Ready.
