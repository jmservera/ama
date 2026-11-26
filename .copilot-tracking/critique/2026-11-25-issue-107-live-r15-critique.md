# Critique r15 (executed once)

Verdict: proceed with dispositions.

* Risk: calling the model from the app replica uses the app's managed identity, not a new control; no network, role, allowance or setting change. Disposition: accepted, nothing persisted on the estate.
* Risk: exec output could leak a token. Disposition: script prints only the harness report; the token stays in process memory.
* Risk: the harness may stop at the first call (as in r14). Disposition: record the result honestly either way; stop after one failed attempt (no retry loop).
* Cap: hard 200000 tokens, 5 calls, 400 prompt and 200 completion tokens per call, USD 1; actual use expected under 1500 tokens.
* The in-replica run proves model reachability and usage per assistant on the delivered image; it does not prove OQ-017/018/019 clearance or the invoke path of the app itself (allowance off). Stated in the note.
* Criterion 1 (older real image, independent worker): not provable without a historical image run; keep unproven unless the ACR holds an older tag usable without estate change (not attempted; would need a revision change).
