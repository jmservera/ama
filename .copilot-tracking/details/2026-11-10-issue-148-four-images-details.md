<!-- markdownlint-disable-file -->
# Details: issue 148 four-workload image wiring

Readback 2026-11-10T01:30Z. Plan: `.copilot-tracking/plans/2026-11-10-issue-148-four-images-plan.md`.

## rebuild_azure.py

* Add frozen dataclass `WorkloadImage(project, repository, parameter)` and tuple `WORKLOAD_IMAGES` in pipeline order api, agents, orchestrator, importer; `parameter=None` marks the orchestrator (explicit `--orchestrator-image`). Add `ORCHESTRATOR_OPTION = "--orchestrator-image"`.
* `RESERVED_PARAMETERS` gains `agentImage`, `importImage`, `orchestratorImage`.
* `AzureBackend._image_ref(image)` returns `<found registry>/<repository>:<tag>`.
* `AzureBackend._missing_images()` runs `az acr repository show-tags` per repository; `ScriptExit` or a tag absent from a list counts as missing; a non-list result is a `RebuildError`. Returns project names.
* `AzureBackend._require_images()` raises `RebuildError` naming missing projects and `--from-stage images`.
* `perform("images")`: pool check unchanged, then a build loop; wrap `RebuildError` (incl. `ScriptExit`) as `Image build failed for <project>: <original message>` `from exc`.
* `verify("images")`: `_require_images()`.
* `_deploy(True)`: `_require_images()` first, then `--parameter <name>=<ref>` for the three, `--orchestrator-image <ref>`, then overrides.
* `plan()`: `report["images"]` static list of project, repository, dockerfile, deploy input.

## test_rebuild_azure.py

* `FakeAzure`: `tags` dict, `build_fail`, `skip_push`; `acr build` parses `--image`, `-f`, raises `ScriptExit` for `build_fail`, records the tag unless skipped; `show-tags` is per `--repository`, `ScriptExit` for unknown.
* New tests: all four builds (Dockerfile, context, pool, tag); four tag-to-input mappings with the explicit orchestrator argument and no `orchestratorImage=`/quickstart/latest; build failure stops before later builds and the application deploy and keeps the original message; built-but-unpublished image stops before deploy; resume at `applications` with only the API tag stops with no application deploy and with all four deploys with the mapping; reserved overrides; dry-run listing with zero calls.
* Existing tests updated only where the fake contract changed (`test_image_build_uses_the_approved_pool`).

## Validation

`python -m unittest discover -s tests -q` in `src/orchestrator`, `ruff check .`, `ruff format --check .`, `mypy` there. No blanket gate; fake-runner evidence proves wiring only.
