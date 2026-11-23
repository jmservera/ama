# Critique: issue 2311 plan (executed once)

Verdict: accept with direct dispositions.

* Risk: adding the contract to registry entries would change registry_hash and release bindings. Applied: kept separate, exposed via `data_contract`.
* Risk: regexes may reject legitimate facts. Applied: patterns limited to high-precision identifiers; full core suite is the regression check.
* Risk: assistants and chat build prompts outside `render`. Disposition: contracts declared and callable via `enforce`; wiring those builders is a follow-up.
