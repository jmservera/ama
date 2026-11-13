# Review: issue 144 standalone worker (1315)

Execution: executed once, independent `code-review` agent. Outcome: Approve, no blocking findings.

* Ack happens only after a successful post (`run_once`); non-success status raises in `ApiResultSink.post`.
* No token or setting values appear in errors; tests assert this with a sentinel.
* Image CMD unchanged, so `check-container.py` and CI keep the version output.
* Medium, accepted and documented: the agents app now runs `serve`, which exits 2 until `ZF_AGENT_RESULT_ROUTE=enabled`, so a deployed revision crash-loops (fail closed, no message consumed). Follow-up: API `/api/agent-results` route, Bicep allowance, financial meter.
* Not run: image build, full agents suite after the final lint edit (targeted 125 tests passed), live queue or model.
