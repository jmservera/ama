<!-- markdownlint-disable-file -->
# Issue 107 R1 proactive forecast: critique (one pass)

Verdict: proceed. Findings applied directly:

* Count only proposals with no existing task ID so deduplication is respected (applied).
* Apply the caller's case scope so the forecast does not leak counts outside scope (applied).
* Label the figure an upper bound, not a price or enablement approval (applied).
No conflict with confirmed decisions.
