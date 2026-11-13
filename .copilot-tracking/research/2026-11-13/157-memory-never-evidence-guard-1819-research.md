---
title: Issue 157 memory never evidence guard research
ms.date: 2026-11-13
---

## Scope

Epic #157 Criterion 3: no memory is used as evidence for a controlled decision (gap from `157-104-epics-criteria-audit-1652`).

## Findings

* `chatthreads._clean_evidence` already rejects references starting `CM-` for chat message evidence, covered by one test in `test_chat_memory.py`. It does not reject `memory:` or `chat-memory` forms.
* `chat_privacy.prompt_memory` labels every item `authority="none", evidence=False`; `ChatIsolation.build_prompt` embeds it in an UNTRUSTED `memory` block. No test asserts the prompt-level labels.
* `gates.evidence_gate` and `signoffs._missing_evidence` take evidence by document kind from the fixed checklist; they never read chat memory, so memory cannot satisfy them structurally. No test pins that.
* Gap: controlled hazard decisions (`workflows.py` `record_referral`, `receive_hazard`, `accept_hazard`, timing, `record_repair`, `release_hazard`) accept free-text evidence via `controls.text`, which would store a `CM-` or `memory:` reference as decision evidence.
* Existing test locations: `src/core/tests/test_chat_memory.py`, `test_hazard_referral.py`, `test_chatthreads.py`. There is no `test_chat_isolation.py`; chat isolation tests live in `test_chat_privacy.py`.

## Planning readiness

Ready. Disposition: executed (direct file inspection).
