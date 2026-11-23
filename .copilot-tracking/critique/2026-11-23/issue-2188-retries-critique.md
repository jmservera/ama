# Critique (one pass, final candidate)

Verdict: proceed.

* Retry rows in `receipt["retries"]` have no timestamps, so retry seconds cannot be computed; report counts and groups only. Do not invent durations.
* Receipts predating retries have no key; use `.get("retries") or []` so old receipts stay analysable.
* Do not make retries a NONCOMPARABLE reason: that would change comparison semantics. Surface only.
* Test must fail without the change: a receipt with one retry row reports 1 and the group; a clean one reports 0; markdown shows the column.
