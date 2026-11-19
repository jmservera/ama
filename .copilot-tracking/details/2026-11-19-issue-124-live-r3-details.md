# Details: issue 124 live r3
Phase 1: run `PYTHONPATH=src:tests python3 -m unittest test_discovery_contract test_discovery_flow test_discovery_register` in src/core; read-only `az containerapp show`, `az eventhubs eventhub list`; git grep for consumers.
Phase 2: write the changes record with the table. Phase 3: review, commit.
Stop rule: all three unticked criteria need a named human or real company data, so no code is built.
