# Critique: issue 462 fourth pass

Executed once. Verdict: proceed.

* Change is one class attribute (`sys_version = ""`) plus one test; no behaviour change besides the Server header. Low risk.
* Resident preview and employee API handlers share the pattern; employee API out of scope (employee login untouched per issue). Preview is local-only; left alone.
* Do not claim live effect: the header only changes after a redeploy.
