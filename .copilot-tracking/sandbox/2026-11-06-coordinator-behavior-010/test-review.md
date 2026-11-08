---
title: Test review, run 010 (issue 1204)
ms.date: 2026-11-06
---

* Grader verdict: Pass with coverage misses, 0 target defects, 5 Low plus 2 Info findings (grader-return.md).
* Fixture defects (Low): N-07 supplies no post-launch readback; N-02 omits some merge-gate facts. Oracle defects (Low): N-07 "treat as draining" wording predates the final blob; N-02 oracle read one merge per tick.
* Target observation (Low, ambiguity not defect): N-08 "admit none and re-read this tick" could be tightened; the owner rule supports the executor's reading.
* Coverage misses carried forward: rebuild-from-evidence path, drain write failure, count failure while draining, failed merge gate during drain, two ready issues for one slot, exited-worker slot, more than 20 PRs with a full cap.
* Not changed: no further correction round is taken; misses are reported as residual work.
