# Changes: 136-bicep-verify-1045

Tracking-only; no infra/, src/ or docs/ edits. HEAD 3b05143179.

* Copied 7 ac6527569 tracking files byte-identically (sha256 verified against commit blobs, 7 OK).
* Venv /tmp/venv-136-1045 (pip: setuptools>=77 from index, then src/core editable with --no-deps); zava_forward namespace path under this worktree; venv removed afterwards. Only zava-forward-core was installed, so cryptography/azure/API deps were absent.
* Bicep (local CLI 0.48.1, `bicep build <file> --stdout`, no az/network): main.bicep, iot-hub-live.bicep, live-simulator-job.bicep, live-receiver-job.bicep, resident-demo.bicep all exit 0, 0 warnings, 0 errors. (First attempt with `--file` was a CLI syntax error rc=1, discarded.)
* Unit tests, full discover (24 modules): hit the 400 s timeout (rc=124) inside test_bicep_policy.test_committed_environment_parameters_compile_and_match_the_contract (8 tests passed before it); that module is therefore UNVERIFIED.
* Remaining 23 modules (pattern test_[!b]*.py): Ran 451 tests in 76.8 s, exit 1, failures=49, errors=31, skipped=4. Failing modules: test_staff_azure (77 of 80 failing/erroring ids), test_identity_rbac (1), test_private_cutover_proof (1). Dominant causes: ModuleNotFoundError cryptography (10) and azure (10) from the minimal venv, and operator-script preflight checks needing Azure CLI/API requirements ("2 != 0", requirements install message). These look environmental, not confirmed as product defects; not triaged further.
* Caveat: the glob excluded all modules starting with "b" (only test_bicep_policy). No other test used Docker (ZF_API_IMAGE unset). Result is partial; follow-up: re-run with src/api requirements installed and raise the timeout for test_bicep_policy.
