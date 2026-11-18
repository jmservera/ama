# Issue 122 live critique (single pass)

Verdict: proceed with changes.

* Risk: writing a change record mutates the live demo database. Disposition: accepted; synthetic flag, metadata-only subject, reversed, disclosed. The owner authorised live demo Azure and no production change.
* Risk: a fresh PITR restore costs about an hour; repeating #145 adds no value. Disposition: reuse and cite; state that this criterion rests on citation.
* Risk: suspension or restart on live would be a drill. Disposition: not run; boundary stated.
* Risk: export verification must use the bundle alone. Disposition: run `verify_export` on a saved file with no network.
