# Review: employee chat (#617)

* Review executed once; outcome: conformant for code, with one open acceptance item.
* Storage gate preserved: no thread or message is stored when unapproved; no model call; audit holds skill and outcome only (tested with a canary).
* Web: native controls reused from the shared widget (dialog, log, status, reduced motion, Escape, focus return); no new visuals. Source guidelines were not re-fetched in this run (disclosed).
* Open: live check with the test user on the deployed site (routed to owner or a later task). Reply uses rules fallback; AI-backed replies still need approval references.
* Follow-ups: record CHAT_* approval references if stored chat is wanted.
