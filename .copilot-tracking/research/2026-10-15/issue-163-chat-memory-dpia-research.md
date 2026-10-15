# Issue 163 research: privacy, DPIA and retention for chat and memory

* Disposition: executed. Planning Readiness: Ready.
* Evidence: issue #163 and parent #157; ADR 0004 (accepted, OD-45/46 open); `timecapture.py` (#120 reference-gate pattern); repo grep shows no chat, thread or memory store in `mvp/`.
* Owner decisions: uksouth, DPO/Legal owner Juan Manuel Servera, retention lock deferred, Azure only, portable SQL, ADR 0005 synthetic fixtures.
* Finding: nothing to protect exists yet, so the smallest coherent delivery is a testable control module plus a draft DPIA record; legal decisions and Azure OpenAI terms cannot be verified and become open items.
