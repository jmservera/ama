# Research: employee chat closes immediately (#617)

* Task: issue-617-employee-chat; disposition: executed; Planning Readiness: Ready.
* Reproduced live (local synthetic data, Retrofit Coordinator): opening on a case, then sending, ends with the widget removed.
* Cause: `POST /api/chat/threads` returns 403 (`ChatNotApproved`) because `CHAT_DPIA_REF`, `CHAT_LAWFUL_BASIS_REF` and `CHAT_NOTICE_REF` are unset (src/core chat_privacy.py `_require`). `chat.js` treats any 401/403/404 as access ended and calls `deny()`, which disposes the widget.
* Size: employee widget was created without `resizable: true`, so it kept the small 28rem x 40rem default; the resident chat (resident_demo/web/assistant.js) uses `resizable: true` (35vw x 70dvh, docking, size controls).
* Constraint: the DPO storage gate must not be bypassed. A reply is therefore possible only without storage and without a model.
* Not verified: the deployed site's CHAT_* settings and the live test-user check (no access from this session).
