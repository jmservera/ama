# Issue 2195 r5 review

One review of the implemented change. Outcome: conformant with routed follow-ups.

* Fix is minimal and matches the plan; regression test fails without it.
* F1: deploy an image and rerun the probe to prove the 500s are gone (also confirms root cause).
* F2: explicit transactions can interleave across threads; consider a connection per request or transaction-scoped lock.
* F3: log the driver message and SQLSTATE on ProgrammingError.
