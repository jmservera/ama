# Issue 358 live pass 3 details

* Phase 2: criteria rows 1, 2, 2b, 3. Criterion 2b (full setup-entra.py run on the deployed demo app) needs Graph
  addPassword and Key Vault writes; owner forbids Key Vault rotation, so it is stated as not provable for the demo.
* No Key Vault rotation, no Azure write, no secret read. Mutation runs only on a temp copy.
* Needed src/infra change: none identified. Any future change would be a full-tier follow-up.
