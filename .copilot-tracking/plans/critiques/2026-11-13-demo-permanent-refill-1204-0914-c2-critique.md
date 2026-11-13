# Prospective plan critique: refill correction 2 (issue 1204)

Executed once, before any source edit, by an independent rubber-duck subagent (runtime-default model) against the c2 plan and research. Verdict: Revise (PC-001 to PC-004 blocking, PC-005 non-blocking). Written to disk before source changes; this one is prospective.

Dispositions (all compatible, applied to the plan and implementation):

* PC-001: the launcher takes positional arguments (number, role, timestamp, worktree) and derives brief, log and script paths from them; one launch id binds brief, script and log.
* PC-002: each attempt writes a `--- launch {timestamp}` delimiter and its own `exit=` line after it; a missing exit line for the current attempt is unknown, never success; the `tee` status is separate from the producer status.
* PC-003: reconcile the other unconditional `ready` rules (missing gate, review) so eligibility depends on the next action: authorised assessment is ready; repair or publication needs dependencies, a finite permission, the selected validation and run-owned source.
* PC-004: execute the exact documented launcher with a stub worker (success, failure, retry, path with spaces) plus `bash -n`; tmux invocation is shown, not run against a model. HVE behavior-gate evidence stays Deferred (owner unavailable for the canonical test model); no Pass is claimed.
* PC-005: exit 2 handling inspects every reported session, separates bad input, recounts live sessions and re-arms only valid live names, without ending the run.
