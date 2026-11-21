# Critique 2026-11-21: issue 350 repair skip

* Executed once. Verdict: proceed.
* Catching broad exceptions is risky; restrict to KeyError, TypeError, ValueError, IndexError (covers JSONDecodeError). Applied.
* Skipped bodies stay untouched, so the legacy row is not rewritten or corrupted.
* Tier FULL (src change): run src/core tests plus the mssql selector if SQL is available.
