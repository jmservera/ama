---
title: Issue 157 memory never evidence guard details
ms.date: 2026-11-13
---

## Phase 1 details

* `controls.MEMORY_REF = re.compile(r"(?<![\w-])(CM-\w|memory:|chat-memory)", re.I)`; `is_memory_reference(text)` returns a bool via search.
* `evidence_text(value, label, limit=300, required=True)` calls `text`, raises `ValueError("Memory is never evidence and cannot be cited.")` when the cleaned value matches.
* `chatthreads._clean_evidence` calls `controls.is_memory_reference` per ref (any position match), keeping its message. `MEMORY_ID_PREFIX` stays for id generation.
* Hazard evidence: replace `controls.text` with `controls.evidence_text` at the six call sites only.
* Gates and sign-offs: unchanged; they take document kinds from a fixed checklist, pinned by test.

## Phase 2 details

* Chat: parametrised refs `CM-abc`, `cm-1`, `memory:CM-1`, `Memory:x`, `chat-memory/1`, mixed with a valid ref; all raise ValueError and a normal ref passes.
* Prompt: `ChatIsolation(store, env=APPROVED)` build_prompt output contains `authority": "none"` and `"evidence": false` in the memory block.
* Hazard: receive_hazard with each memory form raises ValueError and records nothing.
* Gate: `evidence_gate(["CM-1"])` stays FAIL; signoffs `_missing_evidence` unaffected by a document of kind `memory:x`.
