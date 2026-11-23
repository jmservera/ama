# Critique 2026-11-23, issue 116 live r10

Executed once. Verdict: proceed.

* Strict base64 only; magic-byte checks would break deliberate fixtures and widen scope: accepted as stated.
* Place the check before the size check so oversize garbage reports a type refusal consistently: compatible, applied.
* Risk: legitimate base64 with whitespace or newlines is refused. `look_at` uses `b64encode` (no newlines), so no regression.
