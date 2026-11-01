# Changes: issue 148 rebuild and teardown automation (2026-11-01)

Plan: [plan](../plans/2026-11-01-issue-148-rebuild-teardown-plan.md)

## Added

* `src/orchestrator/src/zava_forward/orchestrator/rebuild_azure.py`: Azure adapter, secret-argv and synthetic guards, dry-run default, `--apply`, `--from-stage` resume, operator-gated stop (exit 2).
* `src/orchestrator/tests/test_rebuild_azure.py`: 19 tests against a stateful fake `az`.

## Modified

* `infra/README.md`: scripted rebuild/teardown section; criteria status updated.

## Review-thread corrections (PR 672)

* Overrides: `deployApplications`, `deployEnvironmentOnly`, `apiImage` and the secure `teamsWebhookUrl` are rejected before any Azure operation; declared non-secret `entraClientSecretName`, `enableEntraTokenStore` and `entraTokenStoreReady` are accepted.
* Teardown: private-endpoint-owned network interfaces are discovered via `az network private-endpoint show` and approved explicitly (`Backend.removed_with`, `OWNED_KINDS`); other drift still stops.
* Images: private registries need an approved `--build-pool` (`az acr build --agent-pool`); the parameters stage stops before provisioning otherwise.
* Authentication: roster forwarded to `setup-entra.py`; only a clean (0 items) check whose single remaining item is the SQL staff/restart gap is tolerated, since `staff` reconciles it.
* Probes: browser redirect uses `/sign-in`; health retries bounded transient 0/5xx (6 x 10 s); denial checks strict. Fake `health_for` is now a method (fixes the mypy CI failure).
* CI: `activation` failure is the GitHub API quota guard of the daily scan, not repository code; rerun.

## Validation

* Orchestrator unittest: rebuild, rebuild_azure and dependency-rule suites pass (44 tests). Full discovery with core/agents test paths: 88 run, 1 error in `test_version` because the distribution is not pip-installed locally (unrelated to this change).
* `ruff check`, `ruff format --check`, `mypy src` for `src/orchestrator`: clean.

## Divergences

* None from plan. No live Azure run (not authorised).
