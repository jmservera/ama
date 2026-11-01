# Issue 687 IO contention research (2026-11-01)

* Task: issue-687-io-contention (follow-up to PR #689). Research disposition: executed. Planning Readiness: Ready.
* Gap from PR #689: CPU contention reached only about 14x slowdown; the 17,383 ms outlier, a single slow group with 16 others passing, was not reproduced and IO contention was untested.
* Measurements (4 CPUs, 60,000 cases, fsync writers of 8 MiB blocks in the benchmark temp directory): 4 writers, all reads 108-175 ms. 16 writers: filtered page 59,647 ms, search 3,353 ms, first page 1,445 ms, while keyset page 179 ms, my cases 91 ms, sort 64 ms and contractor list 61 ms in the same run.
* Attribution: the one-off pattern (one group stalling by tens of seconds, others fast) is reproducible under disk contention and not under CPU contention. The query is about 110-175 ms uncontended; no query or index change is warranted.
