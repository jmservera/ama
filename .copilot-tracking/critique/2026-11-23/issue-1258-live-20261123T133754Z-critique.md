# Critique: issue 1258 plan (2026-11-23), executed once

Verdict: compatible.

* The new test duplicates the existing existing-folder concurrency test's shape but covers a distinct path (concurrent `os.makedirs` plus ancestor syncs on first run). Accepted.
* Risk: the test passes without the fix in `_confirmed` (it asserts outcome, not syscall order). It is stated as a regression guard for concurrent first-run behavior only, not as proof of ancestor durability. Applied: the changes record says so.
* No src change, so FOCUSED tier. Real crash durability is not claimed.
