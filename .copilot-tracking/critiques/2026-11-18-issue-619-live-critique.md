# Critique: issue #619 live plan (one pass, 2026-11-18)

Plan under test: record live employee and resident accessibility and consent proofs with Playwright on the demo, write a per-criterion note, no source change.

* Risk: a scripted browser read as a person's screen reader, keyboard or zoom record. Disposition: the note marks those criteria unproven or engineering proof only and keeps the protocol rows `Not run`.
* Risk: the demo login limiter (HTTP 429) blocking the resident journey after retries. Disposition: the plan waits out the 600 second window; the failed attempts are retained and disclosed rather than hidden.
* Risk: credentials or personal data in evidence. Disposition: literal scan of the credential values and e-mail addresses before commit.
* Risk: Phase 4 promised deleting chat threads, but resident chat questions have no browser deletion path. Disposition: the phase is reworded to disclose the four retained synthetic questions; nothing is claimed deleted.
* Risk: closing the issue from demo evidence. Disposition: the pull request uses `Refs #619`; production-only criteria stay open.
* Verdict: proceed. Tier FOCUSED (docs and evidence only). Critique executed once; findings applied.
