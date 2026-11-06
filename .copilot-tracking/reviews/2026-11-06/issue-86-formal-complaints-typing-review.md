# Issue 86 formal-complaints typing correction: author review

Scope: jmservera/ama#86 only. Author Review by the implementing agent after implementation, once. It is not independent exact-head assessment, hosted CI or human approval.

## Assessment

* Research, plan, details and an actual independent critique were committed (`7cc0d461f`) before source edits. Two critique blockers were applied; the plan records the deviations.
* The correction maps one-to-one to the 14 recorded errors and mypy strict now passes over the same 267 files with unchanged configuration.
* Runtime behaviour: `complaints_route.py` bodies are unchanged; `Store` gains no runtime attribute; test helpers return the same objects. `_receiver` still uses `getattr(...)`. Default remains unconfigured, so nothing is sent.
* `parse_acknowledgement(value: Any)` is a deliberate boundary choice for an untrusted external reply, validated at runtime as before. Reviewers may prefer a narrowing rewrite later; that would be new runtime logic and was out of scope.
* The Protocol return type `object` means mypy does not check receiver replies, which is the accurate contract.

## Residual and unproven

* Focused checks only: whole core suite, API tests, SQL variants (101 skipped here), browser and images were not run at this head. R3 FULL must be admitted by the coordinator; old R2 neither passes nor covers this head.
* The earlier residual risks stay: free text is not screened, no real receiver, no two-process concurrency proof, no web control.
* Not proven: external receiver acknowledgement, named appointments, resident consent, or the operational criterion that residents reach independent review and the formal route without detriment. No #86 acceptance or review box was ticked.

## Gates pending

R3 FULL receipt (stack parent `c5edb320ad10d3d73bb985bfb82b2d0bee94381a` plus the new tip), independent exact-head assessment for parent and child, hosted CI, human approval, whole-issue acceptance.
