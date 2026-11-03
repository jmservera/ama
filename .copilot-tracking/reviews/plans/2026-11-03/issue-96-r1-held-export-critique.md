<!-- markdownlint-disable-file -->
# Critique: issue-96-r1-held-export (executed once, verdict Proceed)

* Risk: an export could be read as a reviewed pack. Mitigation: fixed Held/reviewed false/Not submitted/Not assessed and notice; no readiness key.
* Risk: overlap with open #888. Mitigation: new module, `form_review.py` untouched.
* Direct dispositions: tests assert no reviewed_ready/approved/award/payment keys; no ticks proposed.
