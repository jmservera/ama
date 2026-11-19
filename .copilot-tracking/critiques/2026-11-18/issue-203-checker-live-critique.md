# Critique: issue-203-checker-live (executed once)

Verdict: proceed. Findings applied directly.

* Risk: a broad regex could hide a live document. Applied: anchor to `docs/reference/research/`, require an `issue-N-` or `src-repoint-` prefix and a date in the name; test that an undated research note is still flagged.
* Risk: weakening criterion 1 without owner agreement. Applied: do not tick the box; report it unproven and name the exemption in the changes record for owner decision.
* Package-name rule stays active for non-exempt files.
