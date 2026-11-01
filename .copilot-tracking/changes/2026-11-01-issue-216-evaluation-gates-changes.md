# Changes: #216

* Added `authorise_model_run` to `src/agents/src/zava_forward/agents/regulatory_gates.py` (finite owner-authorised call/token/budget/expiry guard; decision only).
* Added `test_model_run_requires_finite_unexpired_owner_authority` and a README note.
* Validation (focused tier): `test_regulatory_gates` 18 OK; earlier run of gates, answers, registry 32 OK; ruff check, ruff format --check, mypy (`src/agents`) clean.
* Divergence: the harness already existed (#355, #506); only the tokenomics limit guard was missing. Recorded report unchanged.
* Review fix (PR #684 thread): `authorise_model_run` now requires `owner` to be a non-blank string; negative controls for whitespace, boolean and list owners added to the test.
