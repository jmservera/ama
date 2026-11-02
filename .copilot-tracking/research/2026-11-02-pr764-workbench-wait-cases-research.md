# PR 764 workbench wait_cases timeout: research

* CI run 41457218122 job 125317820034: design_system_browser_check -> run_browser -> wait_cases TimeoutError (flaky, reproduced locally ~2/3 runs).
* Debug hooks showed `/api/briefing` ends in net::ERR_EMPTY_RESPONSE on the synthetic server; fetchReadRetrying retries network errors (500+1500+3000 ms) and writes the shared `#workspace-status` retry message.
* That message overwrites the "N cases" status set by the case list, and was never restored on failure/abort, so wait_cases (needs "N case" in status) times out.
* Planning readiness: Ready.
