# Review: issue 2245 live (executed once, 2026-11-27)

Outcome: conformant for the assessed boundary (chat_panel save retry, its test, research note).

* Retry wraps only the single-transaction message save; model call, finalize meter publish (inside the same transaction) and audits are not repeated after a commit.
* Persistent lock timeout still raises, so no unsaved answer is shown.
* Test fails without the change and passes with it; chat tests (208) pass.
* Routed later work: (1) deploy and live-verify the fix; (2) find the long write-lock holder (background workers vs. concurrent probes) with SQL lock inspection; (3) audit write in `ask`'s finally block can still turn a built reply into a 500 on lock timeout.
Human and hosted review remain required and are not claimed.
