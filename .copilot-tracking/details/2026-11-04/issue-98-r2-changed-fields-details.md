<!-- markdownlint-disable-file -->
# Details: issue-98-r2-changed-fields

* `_freshness` compares `draft["fields"][fid]` state and value (via `_equal`) to `snapshot["fields"][fid]`; sorted ids returned as `changed_fields`.
* Snapshots, history and unrelated decisions are not modified. Manual path: reviewer re-runs `diagnose`. No AI involved.
