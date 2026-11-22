# Review: issue 2256 (executed once)

Outcome: conformant for local scope.

* Null age is handled in core, JS validation and display; CSV unaffected (same 13 columns).
* Exception register now raises no unrouted note for naive offers; they are listed, not escalated (needs_escalation false without a reason).
* Open: live verification after deploy; browser tests not run.
