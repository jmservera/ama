# Critique 2026-11-23: issue 157

* Executed once. Verdict: proceed.
* Risk: existing callers pass users without role or cases; mitigated by running all chat tests. Same error for missing and hidden case avoids an oracle; API route already returns ChatNotFound so behaviour there is unchanged.
* Rejected alternative: enforce in `chat_create_thread` (also used by regulatory_chat with its own case handling); wider blast radius.
