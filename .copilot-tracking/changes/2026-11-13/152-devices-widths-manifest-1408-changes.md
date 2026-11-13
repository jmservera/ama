# Changes: #152 devices and widths

* design-system.md: new "Supported devices and widths" section (owner decision 2026-11-13).
* supported-devices-proposal.md: status changed to decided.
* workbench-manifest.json: supported_devices decided; 360 added to widths.
* test_design_system.py, test_workbench.py: new contract tests (RED first: 3 failures), simulator-absence with negative control; old "stay proposed" test replaced.
* Validation: 54 unit tests OK, ruff check/format OK, mypy OK. Chromium workbench check not run; 360px browser result unverified. No criterion ticked.
