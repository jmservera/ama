# Details r15

* Runner reads base64 chunks to /tmp inside the replica (ephemeral, no persistent change), imports `assistant_real_ai_acceptance` and `zava_forward.agents.heldout_aoai`, calls `get_token("managed-identity")`, `make_provider(endpoint, deployment, "gpt-4.1-nano", token)`, `run(auth, listing, "live", provider, True)`, prints the report only.
* Evidence goes to `.copilot-tracking/evidence/107-live-r15/`.
