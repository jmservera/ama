<!-- markdownlint-disable-file -->
# Research: Correction 2 (Refs #350)

* Task ID: issue-350-demo-feedback-correction2
* Parent task: issue-350-demo-feedback-correction1
* Research disposition: executed (read runtime source) plus reused independent review of head afb5aaab
* Planning Readiness: Ready

## Evidence

* Review finding: submitted note not compared to the persisted contact.
* API contract: POST /api/cases/{id}/call passes body.note to Store.log_call, which stores `(note or "")[:500]` unstripped in the contact `note` field (src/core/src/zava_forward/core/store.py log_call; src/api/src/zava_forward/api/server.py call handler).
* Projection: roles without a recorded need see staff free text replaced by the held note, so a held note is not comparable and must be blocked, not passed or failed.

## Decision

Compare note as written truncated to 500 characters in write response and reload; mismatch fails; held note blocks. Durability stays blocked; no scope broadening.
