# Review 2026-11-23: issue 157

* Executed once. Outcome: conformant for the assessed boundary (start_thread case scoping; tests and docs).
* Findings routed later: a similar visibility check in `chat_create_thread` itself (shared with regulatory_chat) was deliberately not changed; consider if another core caller appears. Independent human review and hosted CI remain required.
