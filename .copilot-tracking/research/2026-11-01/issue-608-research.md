# Research: issue 608 Chromium socket path

* Finding: main already contains #610 (84035ae9), adding admit_browser_output in tools/rpi-checks.py, called at lines 1173, 2266 and 2450 before any check runs.
* The bound is 107 bytes minus the Chromium suffix, so --out must be at most 55 bytes for TMPDIR=<out>/tmp. It fails with an actionable message.
* Tests: tools/test_rpi_checks.py lines 602-729 bind a real AF_UNIX socket at the 107-byte boundary.
* Planning readiness: Ready. Disposition: executed (code read, 55 tests run, all OK).
* Criterion 3 (full browser and SQL groups without skips) needs a supported short-path live run; not available here.
