# Paid execution plan 126 — critique

## Metadata

| Field | Value |
| --- | --- |
| Review date | 2026-10-20 |
| Scope | Read-only review of the research, plan, and frozen phase-details artifacts for task 126 |
| Decision constraint reviewed | USD 500 total calendar-month cap, including accrued charges; authorization expires 2026-10-25T16:02Z |
| Verdict | **Revise** |

## Blocking Issues

1. **PC001 — The USD 500 cap is not demonstrably enforceable with the available billing scope.**  
   **Severity:** Blocking  
   The model explicitly excludes subscription-level/other-RG charges, credits, tax, commitments, and an unbounded billing-latency amount. A USD 30 “billing-latency/unknown reserve” is an assumption, not evidence that those unknown charges are at most USD 30. This conflicts with the stated rule that unknown spend or price blocks execution.  
   **Recommended directly-applicable fix:** Make a successful subscription-scope actual-cost query (including the required charge types) and the applicable effective prices a T0 precondition with an owner-recorded timestamp. If it cannot be obtained, state that **all paid tranches are blocked**; do not permit S1 or S2 to authorize execution.

2. **PC002 — S1 cannot pass the plan’s own stop threshold.**  
   **Severity:** Blocking  
   The frozen calculation gives S1 plus tranche ceilings and reserve as USD 481.32, which is above the “stop and clean up” threshold of USD 475. Yet T0 allows the owner to choose S1 or S2. Consequently, the first tranche is already prohibited under an allowed T0 outcome.  
   **Recommended directly-applicable fix:** Either make S2 the sole eligible disposition for paid execution, or revise the reserve/ceiling/threshold model and recalculate every option so each approved option has a stated, positive margin below the stop threshold and USD 500 cap before T1 starts.

3. **PC003 — T1 lacks the required executable approval record and evidence-based acceptance checks.**  
   **Severity:** Blocking  
   “Usable sign-in on the existing demo API” is not an approval-ready definition of work. The artifacts do not supply the approver identity/time, exact subscription and resource scope, approved cost envelope, expiry acknowledgement, named identity changes, rollback, or a pass/fail evidence set. The planned “expected browser/roles/SQL/AI checks” are only a future task, not the required fields and checks.  
   **Recommended directly-applicable fix:** Add a T1 approval template requiring all of those fields before any command is run. Define pass evidence as a real authenticated session for the approved principal and the minimum authorized role/action; explicitly state that a redirect, 401, or 403 establishes only ingress/restriction and is not sign-in evidence. Require no action where the invalid client sentinel, tenant consent/registration, roster, quota, or private executor remains unresolved.

4. **PC004 — T3 has uncapped resources and prices despite the finite-cost requirement.**  
   **Severity:** Blocking  
   T3 says it uses “temporary synthetic resources,” while the plan gives no resource inventory, SKU, region, lifetime, deletion/retention cost, logging volume, private-endpoint impact, or price evidence for them. The same gap exists for restore/scan simulation log ingestion and storage. These are paid-resource changes for which unknown spend must block execution.  
   **Recommended directly-applicable fix:** Replace T3 with a per-operation bill of materials listing every resource/change, SKU, region, maximum lifetime, data/log volume, effective price source, and bounded incremental ceiling; or mark the affected operation blocked. Include teardown verification that preserves the `ama` resource group and all identities.

5. **PC005 — The expiry is stated but not made into a hard tranche gate.**  
   **Severity:** Blocking  
   The 2026-10-25T16:02Z authorization expiry does not appear as a start/stop condition for T1–T3. The plan can therefore approve work whose validation, billing observation, or cleanup runs after authority ends.  
   **Recommended directly-applicable fix:** Add an explicit UTC “do not start” time that leaves time for validation, charge capture, and rollback before 16:02Z; require an automatic/manual stop-and-cleanup record at expiry; and require fresh written owner approval for any continuation after it.

## Non-Blocking Issues

6. **PC006 — The required generic transport-design reference is absent.**  
   **Severity:** Non-Blocking  
   The plan mentions private publication and a private executor but does not state the transport design at the required generic level, leaving reviewers unable to tell which connectivity boundary T1/T3 are expected to preserve.  
   **Recommended directly-applicable fix:** Add one concise, non-implementation-specific statement that the approved path uses the existing private transport design and that no public bypass, new publisher capacity, or alternate network route is authorized by this plan.

## Summary

**Verdict: Revise.** The current artifacts correctly identify major cost and access unknowns, but they do not yet turn those unknowns, the S1 arithmetic conflict, first-deployment approval evidence, temporary-resource costs, and expiry into gates that can safely authorize paid execution.
