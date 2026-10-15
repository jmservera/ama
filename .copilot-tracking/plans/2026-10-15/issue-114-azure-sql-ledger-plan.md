# Plan: issue #114

1. ledger.py: per-year digests and `verify_years` (independent year verification, inter-year links, sealed digests); Store methods and CLI flags.
2. loadcheck.py: NFR-002 mix harness over the 60,000-home synthetic stock; record local measurement.
3. recovery.py: erasure, external deletion register, backup, reapply after restore.
4. tests/test_recovery.py proving each; README evidence and open items.

Critique (single pass): the register must live outside the database or a restore loses it (applied); a local SQLite run must not be presented as Azure proof (applied: stated as open item). Verdict: proceed.
