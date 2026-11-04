<!-- markdownlint-disable-file -->
# Review: issue 946

Execution: one self-review of the final diff. Outcome: conformant for the slice; one open question routed to the owner.

* Criteria 1 and 2 are met by code and an exact-text test.
* Open: the issue's line reference (437) does not match the receiver message at #898's head; the receiver message was chosen as the most plausible target. If the owner meant `accept_hazard`, whose message is already accurate, no further change is needed. This is why the PR uses `Refs #946`, not `Closes`.
* Independent exact-head review, hosted CI and human approval remain required and are not claimed.
