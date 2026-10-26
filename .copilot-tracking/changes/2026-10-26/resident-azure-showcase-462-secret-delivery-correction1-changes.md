# Changes: secret-delivery correction 1 (issue 462)

Date 2026-10-26T07:17Z. Base local `a29a3849`. No push, Azure, SQL, gate or real secret.

* `infra/scripts/resident_demo_secrets.py`: `O_NONBLOCK` added to the verifier-file open.
* `infra/tests/test_resident_demo_secrets.py`: FIFO regression (15 tests now); real non-empty `assertNotIn`.
* `infra/README.md`: dry run is not what-if proof.

## Commands (new env /mnt/ama-rpi-gates/issue462-helper-correction1/venv, `-B`, no bytecode)

* `python -B -m unittest discover -s infra/tests -p test_resident_demo_secrets.py -q`: 15 OK.
* `-p test_staff_azure.py`: 43 OK. `-p test_setup_entra.py`: 124 OK.
* Runner-style ruff check and format check on the three source files: pass.
* Mutation: without `O_NONBLOCK` the FIFO test fails after 5 s.
* Reproduction of SH-001 in the retained gate4 namespace env fails because its editable paths point to a deleted checkout; explained in the correction plan. The old env was not touched.

## Residuals

Gate4 receipt remains stale for any head after `11808a01`. Full gate, capacity admission and coordinator assessment still needed. G1 to G4 open. Low2 ARM race residual.
