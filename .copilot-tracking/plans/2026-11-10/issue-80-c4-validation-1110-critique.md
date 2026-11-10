---
title: Issue 80 capacity C4 instrumented validation, critique
description: One native critique of the validation plan (not independent)
ms.date: 2026-11-10
---

Executed once on the final candidate plan; native author critique, not independent. Verdict: proceed with dispositions.

* Risk, accepted: the observer adds listeners and a print shadow, so timing is not identical to an unobserved run. A pass is still a pass of the unchanged checker; a failure cannot be proven identical to the unobserved failure. Disclosed as an observer limitation.
* Risk, accepted: one sample cannot separate host load, a checker race and an application defect. The observer captures evidence but cannot decide cause; no repeat is admitted.
* Compatible, applied: no `fsync` per event, to reduce perturbation; the snapshot and served-asset hashing happen only at browser close.
* Compatible, applied: exit code captured directly from the python process with no pipe.
* Boundary kept: no source, assertion, timeout, intercept, role or data change; observer faults cannot mask the primary exception.
* No conflict with a confirmed Root decision; no significant or divergent issue needing a user decision.
