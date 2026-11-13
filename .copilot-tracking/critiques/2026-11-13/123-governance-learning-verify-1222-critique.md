# Plan critique: 123-governance-learning-verify-1222

Executed once by independent rubber-duck agent before any venv or test run. Verdict: Revise.

* Blocking: omitted core/tests/test_governance.py; count mismatch. Applied (17/10/4 modules).
* Blocking: bare-import and `tests.*` shadowing risk. Applied (PYTHONPATH per package, verify __file__).
* Blocking: offline install risk. Applied (--no-build-isolation, PIP_NO_INDEX, no bytecode).
* Blocking: api test_case_journey uses local node DOM harness and tests.test_mvp import (an in-repo test file, not the mvp path). Applied: allowed, no browser or network.
* Non-blocking: verify HEAD and src cleanliness; separate import errors and skips.

Disposition: all compatible findings applied directly in the details file. No repeat critique.
