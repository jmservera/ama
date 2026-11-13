# Plan: unified pack 1905

1. Cherry-pick 36477121e, d88a16926, 32d7328c3, 22e8b2528 in order; resolve README conflicts keeping both rows.
2. If docs/reference lines shifted, regenerate docs/architecture/cutover-reference-inventory.tsv with the existing tool.
3. Verify: test_cutover_audit, validation.json SHA-256, 441 verify test, ruff, relative links, secret scrub (0 hits).
4. Independent review; commit cleanly with trailer; no push.

Critique amendments: audit tool check mode post-pick; semantic README merge; full validation.json hash verification; per-commit secret scan.
