# Details: issue 216 live3

* Each batch starts a fresh throwaway server (temporary SQLite store, fresh synthetic demo meter of 20 calls, 100,000 tokens, amount 1) via az containerapp exec, so the meter does not stop later batches. Deployed store untouched; threads deleted.
* Raw outputs saved under docs/reference/research/eval-gates-live-216-2026-11-18/raw-live3/ (no credentials; synthetic case only).
* Merge raw rows, then score with the declared cases.json using scripts/score_inner.py.
* Stop if the model-call count passes 30 or any error suggests a production change.
