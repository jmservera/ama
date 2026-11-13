# Research: 136-bicep-verify-1045

Disposition: executed (bounded). Planning Readiness: Ready.

* Read at start: docs/reference/README.md and memory.md headers; case-study docs referenced by repo instructions.
* HEAD 3b05143179 on test/child-136-bicep-verify-1045; worktree clean.
* infra/tests has 24 unit modules (+ actionlint.yaml). Three import zava_forward.core (test_initialize_workbench_staff, test_public_simulation_startup, test_resident_demo_secrets), so src/core must be installed editable in a /tmp venv with pip.
* Others add infra/scripts to sys.path; no network needed expected.
* Bicep CLI 0.48.1 available at ~/.local/bin/bicep and via az bicep version (already installed; no install/login needed). Targets: main.bicep (708 lines), iot-hub-live, live-simulator-job, live-receiver-job, resident-demo; modules foundry/iothub/containerapps.
* Prior input ac6527569: 7 tracking files, read only headers/issue bodies; test bodies not run.
* Risks: bicep build may try restoring registry modules (network); tests may be slow (test_bicep_policy 2695 lines).
