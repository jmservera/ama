# Critique: assisted aftercare 133 C2 plan (executed once)

Executed 2026-11-09T23:05Z (finished before 23:06:02Z readback) by an independent rubber-duck subagent. Verdict: Revise. Eight findings, all compatible with confirmed decisions, applied directly to the details; no user decision required. No second critique.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | `_txn` increments `version` and rewrites on a replay | Applied: replay returns the stored text unchanged (no version change, identical bytes); test bytes and concurrent same-id retries |
| 2 | Blocking | 400/403 on a retry after an unconfirmed attempt must not clear uncertainty | Applied: `unresolved` option on submit; refusals keep the id and the original-details instruction until a save or replay is confirmed |
| 3 | Blocking | 409 may be the shared client's local pending guard | Applied: 409 is an ambiguous conflict, id retained, wait then check the concerns list before a new record |
| 4 | Blocking | Context cap only per call; merged keys can exceed it | Applied: merged key count checked inside the transaction; existing oversized documents are not rejected on restore, but adding to them is refused |
| 5 | Non-blocking | Guard bypass: `phone_0712...`, zero-width, full-width, trailing newline | Applied: NFKC plus zero-width strip plus separator normalisation before `_redact`; `fullmatch` for keys; best-effort limitation stated |
| 6 | Non-blocking | 503 hides invalid state vs persistence failure | Applied: unconfirmed message adds ask-a-colleague and paper-route-after-checking guidance; no claim of no earlier save |
| 7 | Non-blocking | Weak malformed-receipt check | Applied: receipt needs string `receipt_id`, `concern_id` and a `request_id` equal to the sent one |
| 8 | Non-blocking | Real fixtures cannot cover all cases | Applied: real payloads plus retained synthetic adversarial cases, including an error without `errors` (current shared client) |

Hook contract: unchanged. `StateStore.update` still takes a mutator returning `(text, result)`; a replay returns the unchanged text and a store may skip the write.
