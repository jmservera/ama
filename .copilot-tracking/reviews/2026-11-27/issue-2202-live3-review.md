---
title: Issue 2202 live3 review
---

Review executed once after implementation. Outcome: conformant for the assessed boundary (diff of `chat_panel.py`, its test, the live note, index, log).

* The retry is limited to the lock-busy error and to saves that take the lock first; other errors raise unchanged. The question save retry re-runs the thread and turn-count reads, which are side-effect free.
* The test fails without the change and passes with it; type, lint and format checks add no new findings.
* Claims match evidence: attribution of the live 500 to the question or answer save is stated as unknown; the fix is stated as undeployed.
* Routed follow-ups: rebuild and roll the API image from main, then re-probe chat under a running receiver (needs owner Azure authority for a change); provenance and rollback drill remain unproven.
