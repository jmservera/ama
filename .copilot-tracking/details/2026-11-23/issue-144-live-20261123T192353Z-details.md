# Details
Phase 1: symbol table api->api, agents->agents, orchestrator->orchestrator, tokenRenewal->auth-renewal, ledgerVerify->ledger-verify, rankingPublish->rank-publish, importJob->import. Image param from `image: X`; module from `command: ['python','-m',MOD,...]` (api uses a recipe, skipped for module check). Project owning the image: apiImage->api, agentImage->agents, orchestratorImage->orchestrator, importImage->importer; module path src/<project>/src/<module with dots>.py or package __init__/__main__.
Phase 2: python3 -m unittest in infra/tests; ruff.
