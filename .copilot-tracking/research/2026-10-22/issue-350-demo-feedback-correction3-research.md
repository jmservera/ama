<!-- markdownlint-disable-file -->
# Research: Correction 3 for PR 436 review (Refs #350)

* Task ID: issue-350-demo-feedback-correction3
* Parent task: issue-350-demo-feedback-correction2
* Research disposition: executed (runtime source read) plus reused independent PR review of head 0393b258
* Planning Readiness: Ready

## Evidence

* Finding 1 validated: src/core/src/zava_forward/core/store.py `detail` sets `d["contacts"] = list(reversed(d["contacts"]))[:40]`, so contacts are newest-first and capped at 40; `log_call` appends oldest-first in storage. The checker compared `contacts[-1]` (the oldest returned entry) and counted `before + 1` without the cap. The POST `/api/cases/{id}/call` handler returns the same detail projection.
* Finding 2 validated: `json.loads` accepts NaN, Infinity and -Infinity; `isinstance(float('nan'), float)` passed the latency check.
* Corrected rule: newest contact is `contacts[0]`; write length is `min(len(before)+1, 40)`; `write[1:]` equals `before[:len(write)-1]`; reload newest and fields match; NaN/Infinity constants rejected at load and non-finite or negative latency fails.

## Decision

Scope stays the two tools files. SQL durability remains blocked; offline-only, fail-closed.
