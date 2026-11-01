# Issue 687 benchmark outlier research (2026-11-01)

* Task: issue-687-benchmark-outlier. Research disposition: executed. Planning Readiness: Ready.
* Evidence: `src/core/tests/test_sqlreads.py` `Scale.test_sql_reads_at_60000` asserts every timed read under 1,500 ms and printed only the elapsed time, with no load context.
* Measurements on this host (4 CPUs, 60,000 cases): filtered page 110/114 ms uncontended; 226 ms with 4 CPU burners; 246 ms with 16; with 32 burners (8x oversubscription) the filtered page took 1,533 ms and other reads 600-2,360 ms (all queries slowed together).
* Attribution: the query itself is fast (about 110 ms) and degrades proportionally under CPU contention, so slowness of a single group with the other 16 passing is not explained by query cost. 17,383 ms was not reproduced under CPU contention (max about 14x); it is consistent with severe environmental stall (e.g. IO or overlapping image restores) but remains unproven. No query or index change warranted.
* Gap: the original receipt is gone, so the exact cause stays unproven; the new diagnostics classify any future failure.
