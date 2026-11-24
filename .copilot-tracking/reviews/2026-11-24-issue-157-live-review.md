# Review 2026-11-24: issue 157 live recheck

Execution: one post-implementation review of the diff against head 3adf3f4698 (`git diff`), by the worker; no independent reviewer exists in this local task. Outcome: conformant with the limits below; no open material finding.

## Checks
* Behavior: sweep runs only when a period is recorded (`purge_retention` returns `applied: False` otherwise); throttle time is set before the purge; exceptions are logged, not raised, so chat availability is unaffected. Tests cover period enforced, throttle, no period, live-only memory limit and the isolation trigger on both stores.
* Isolation and consent: the sweep deletes by age only, touches no content, and adds no cross-user read path. The memory limit now counts exactly the items `list_memory` shows.
* Concurrency: `_swept` is an unsynchronised float; a race at worst runs the idempotent purge twice. The purge uses the repository transaction like every other write.
* Scope: no scheduler, infra, API-surface or web change; web tests were not required.

## Routed later work (not actioned here)
1. Deploy a revision with the sweep and re-read `/api/chat/threads` after a thread passes 30 days (live proof; needs a build and new revision).
2. A scheduled purge for an idle app (infrastructure, own review).
3. #440 criteria 7 and 8 and the child-acceptance remainders stay with the owner.
