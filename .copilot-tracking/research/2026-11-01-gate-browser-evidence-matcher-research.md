# Research: gate browser evidence matcher (2026-11-01)

* Disposition: executed. Planning Readiness: Ready.
* Evidence: `tools/rpi-checks.py` `check_skips` required `re.findall(r"^(.+?) \.\.\. (.+)$")` to equal exactly `[(test, "ok")]`.
* Failing log (rpi-d12, `/tmp/rpi-gate-d1d2/0155-browser.log`): the test header line carries log noise (`... http-response GET ... status=503`), the noise repeats on the next line, then a bare `ok`. Test passed (`Ran 1 test`, `OK`); matcher rejected it.
* Decision: parse the single verbose header, then take the result from the last non-empty line before the `Ran N test` line; keep skip, count, summary and single-header checks unchanged.
