# Details issue-223-live-r9

P1: iterate `recs`; when `review_evidence` is a dict, count reviewed; if `review_seconds` is a non-bool number >= 0 count timed and add. Mean is `None` when none timed. Seconds are never reviewer-identifying; no new data exposure.
P2: seed records with seconds 30, 90, null, and an unreviewed one; assert totals and mean.
