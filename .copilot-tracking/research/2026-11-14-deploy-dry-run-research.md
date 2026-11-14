# Research: deploy.py --dry-run (Refs #148)

* Issue #148 criterion 4 asks for a dry-run mode and a disposable-environment test. Comments (2026-10-31 to 2026-11-10) say Azure from-empty rebuild stays unmet.
* `infra/scripts/deploy.py` had `--apply` versus default what-if, but no dry-run; every path called `az containerapp list` first.
* `infra/tests/test_deploy.py` already uses a real subprocess with a fake `az` on PATH in a TemporaryDirectory (disposable environment), recording calls.
* Planning Readiness: Ready. Disposition: executed.

## Cycle 1 correction

* `EXE001` on `deploy.py:1`: shebang present, file mode 100644. Sibling scripts with shebangs use 100755. Fix is the executable bit.
