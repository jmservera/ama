<!-- markdownlint-disable-file -->
# Issue 107 R1 proactive forecast: details

* Authorisation: each capability's `authorize` (role, current staff record, scope); contractors and unknown roles are denied.
* Per capability: scoped open cases, eligible cases, new proposals (no existing task ID), `max_calls_this_period` = new proposals x `max_calls_per_request`.
* Scan reach per period = `scan_size` x (period // `scan_interval`); call allowance from limits.
* Read-only: no insert, no provider call, no case text in output. Works with proactive off.
* Cost string: Unknown (no price source).
