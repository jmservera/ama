<!-- markdownlint-disable-file -->
# Details: issue-96-r1-held-export

* `draft_export(store, user, case_id, draft_id)` takes the store lock, requires the existing actor rights (`forms._actor`), builds the report and returns a dict with status Held, reviewed false, submission Not submitted, eligibility Not assessed.
* Unavailable evidence returns status Unavailable (manual path: recover the source, use the working review). An unknown draft raises KeyError as `form_review` helpers do.
* No store writes or audit entries; no reviewed state exists.
* Content hash is SHA-256 of canonical JSON of the body so a comparison can detect change.
