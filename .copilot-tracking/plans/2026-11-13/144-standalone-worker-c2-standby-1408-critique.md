# Critique (rubber-duck, executed once)

Verdict: Revise. Dispositions applied directly:

* Existing runtime test must set `ZF_AGENT_RESULT_ROUTE=enabled`: accepted (plan already lists it).
* Queue scale rule may start standby replicas while messages sit unconsumed: accepted as a documented consequence; no Bicep change this cycle (a later cycle sets the route and the allowance together).
* Add a real-SIGTERM subprocess test for exit 0 and heartbeat: accepted.
