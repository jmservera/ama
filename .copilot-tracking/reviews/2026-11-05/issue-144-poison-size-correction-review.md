# Review: issue 144 poison-copy size correction (2026-11-05)

Author review, one pass. The independent REQUEST_CHANGES report, the 9f14e6cb9 preparation review and the full-r5 receipt are preserved and not regraded.

Outcome: F1 addressed in source with offline regressions; NOT accepted. FULL validation and independent exact-head assessment are PENDING for the new head.

* The stored poison copy is now bounded by encoded bytes; a truncated copy is explicitly marked. Evidence is an offline size model, not live Azure.
* Residual: a truncated poison copy loses the tail of an oversized original (intended, marked); no token source, post-back or serve wiring; criteria 1 to 5 of #144 stay unmet; linkage `Refs #144`. No human approval claimed.
* Next: coordinator admits a new full gate (`tools/rpi-checks.py --all --lock-timeout 0 --base <fresh origin/main> --out <new short dir>`, then `--verify-receipt`), then independent assessment. Intended child target is `feat/infra-hosting-integration-136`; PR 1141 untouched.
