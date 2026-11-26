# Plan: issue 2190 (Refs #2190)

- [x] Research and re-verify three flake fixes on current head.
- [x] Critique once.
- [ ] Catch BrokenPipeError/ConnectionResetError in the Slow handler of src/api/tests/test_rai_release_readiness_api_218.py; confirm no traceback in verbose output.
- [ ] Run 218 suite, mypy and ruff for src/api; record per-criterion table.
- [ ] Review once; commit locally. Tier FULL (src change), no `--all`.
