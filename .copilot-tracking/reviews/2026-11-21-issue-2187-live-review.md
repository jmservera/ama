# Review: issue 2187

Date 2026-11-21. Review executed once after implementation; outcome conformant for local scope.

* Diff is small: one selector, one branch in `main()`, two tests, one README sentence.
* `verify` and the runner remain inside the same block, so behaviour for heavy selections is unchanged; `--heavy-lock-fd` is ignored (not borrowed) for lock-free runs, which is harmless.
* No open material findings. Unproven: behaviour against a live competing gate (not run by instruction); full-tier receipt and exact-head review belong to the coordinator.
* Routed follow-up: decide whether `browser` may skip the lock (criterion names Docker and SQL only).
