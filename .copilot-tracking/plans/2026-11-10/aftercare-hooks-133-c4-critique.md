<!-- markdownlint-disable-file -->
# Critique: aftercare runtime hooks plan (one pass, final candidate)

Date: 2026-11-10. Executed once. Verdict: Approve with applied findings.

* Applied: classification must not treat "persisted equals previous" as safe when a third writer moved the value; any third value is unconfirmed, never "not saved".
* Applied: after a failed `save()` on SqlStore the in-memory document is not restored; the adapter restores it explicitly for uncommitted failures and resyncs through the store for unknown ones.
* Applied: the mutator result for an unchanged document (replay) must not call `save()`, so replay never overwrites a concurrent success.
* Applied: the actor passed to the service is built only from the session user; a test proves a body `recorded_by` is ignored.
* Applied: the home allowlist is asserted non-None in a test and the served form lists only constructed homes.
* Noted, no change: MSSQL is required for the changed binding; SQLite results are reported separately and are not a substitute.
* No advice conflicted with a confirmed decision. No significant or divergent issue needs a user decision.
