# Test log A1 (sandbox 5)

* Run type: full. Fidelity: simulation (read-only HVE Artifact Tester, dispatched via host task tool; model not observable, proxy). Executor status: Complete. 16 scenarios executed.
* Target revision: HEAD 2f1aa2e4d42b79364b95622d6198975203c1417e plus uncommitted C4 edits (target-diff-vs-2f1aa2e.patch). Source identities before dispatch: source-identities-pre-dispatch.txt; recomputed after the executor returned: unchanged (sha256 of all four targets equal).
* Raw executor return retained verbatim: test-log-executor-trace.md (sha256 91ce2ac07d712d09ee04c576c0ed5eb31f291ee499d21a7ae7c4d5d68ca776b1). Observed [O], inferred [I] and verification [V] labels are the executor's own.
* Executor-reported containment: nothing written; files read are listed at the end of the trace. Lead git status after return: only the expected C4 tracked and untracked files plus the ignored tools/__pycache__ (unchanged). Not independently verifiable: that no other read occurred.
* Executor-reported observed gaps (8) are in the trace; none was repaired by the executor.
* Untested: real browser run, timing, resume execution, receipt schema, hosted CI observation, native runtime.
