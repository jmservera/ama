# Research: issue 2245 live recheck (run 20261127T125527Z)

Date: 2026-11-27. Research disposition: executed (fresh live probes; earlier notes reused for history). Evidence note: docs/reference/research/issue-2245-live-20261127T125527Z.md.

Findings (revision ca-cutover-test-demo-api--0000136, created 12:27Z, 100 percent traffic, healthy):

* 8 of 8 direct thread creates 200 (155-289 ms); 5 of 5 ask-probe creates 200; 5 of 5 asks 200 (3.3-6.2 s). No 500.
* The demo spending control was holding AI answers in this window: the free-form case asks and the widget showed "Model calls: 0" with the plain text "This reply uses rules only because the demo spending control is holding AI answers, so no model was called". So "Model calls: 1" was not reproducible now (proven live earlier on revision 0000130); the banner-states-plainly criterion is proven live.
* Revision 0000136 image digest cannot be mapped to a commit (ACR denied); the answer-save retry (#2460, 09:51Z) predates the revision (12:27Z) but inclusion is unproven. Logs show background-route 503 sql-write-lock-busy still occurring.
* Source: after the answer save, ChatPanel._ask.finish (chat.answer audit) and ChatPanel.ask finally (chat.turn audit) each write under the SQL lock without retry, so a lock timeout there turns a saved or paid answer into a 500 (residual path routed by the 2026-11-27T02 review). Not live-reproduced; real by code reading.

Planning Readiness: Ready.
