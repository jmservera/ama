# Plan: evidence-only re-check

1. Re-run 124 infra setup tests, ruff, mypy (focused tier).
2. Mutate the expiry guard to always-valid; confirm tests fail; revert.
3. Record evidence and unmet criterion. Critique: one pass, accepted; no source change, no security/infra gate triggered by this slice.
