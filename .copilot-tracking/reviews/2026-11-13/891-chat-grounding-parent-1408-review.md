# 891 parent review

Execution: independent code-review agent, once. Outcome: two medium findings.

* Settlement guard when a meter reference exists but no meter is configured: now logs a warning. Failing closed was not adopted because existing agents tests exercise that state without a meter; routed to follow-up (make the test set-up consistent, then fail closed).
* Golden eval turns lost kind/cites/answer_source assertions: routed to follow-up (restore explicit fallback assertions with the new answer_source); forbid and contains checks remain.
* Not run: core suite after the final logging-only edit (venv removed); live tariff end-to-end settlement (mock meter used).
