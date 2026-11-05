---
title: Issue 82 non-string measure fallback research (2026-11-05, correction 3)
ms.date: 2026-11-05
---

* Start HEAD 63e77e3c7, tree e90ec214e, main bb3a3b03c, parent ead177ef9, clean with nothing ignored. The 2273ec5f... full receipt genuinely passed and is historical for any new commit.
* Defect (independent probe, session 77149bdf files/82-63e77-measure-fallback-independent-probe.log): persisted `checklist="Unlisted"` with `measure=["Loft insulation"]` makes `evidence_gaps` call `checklist_for(list)`, which raises `AttributeError: list has no lower`. This is the case my own Review left unreproduced.
* Contracts read in `quality.py`: `checklist_for(measure)` accepts `None` or `""` (legacy: `(measure or "")` then the General checklist); callers `job_pack` and `assistants` pass known string measures. `submit_quality` only stores measures from `_measures(c)` (strings). So a non-string stored measure is corruption; absent or empty is valid legacy and keeps the General fallback.
* Fallback is reached only when `checklist` is absent or unrecognised, so the guard belongs only on that path.
* Boundary: this slice does not repair measure identity. A corrupt record is replaced only through the existing supersession, which is matched to a known measure; it is never reassigned to a different measure, coerced to a string, or mutated. A record whose measure is non-string cannot be matched by `submit_quality` for any measure, so no replacement route is added or claimed here.
* Planning Readiness: Ready.
