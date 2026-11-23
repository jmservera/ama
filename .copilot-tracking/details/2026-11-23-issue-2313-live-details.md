# Details: issue 2313

## Phase 1

Workflow `Infrastructure PR image build`: `on.pull_request.paths: [infra/**, src/**, .github/workflows/infra-image-build.yml]`; top-level `permissions: contents: read`; concurrency per PR with cancel-in-progress; job `build` on `ubuntu-latest`, matrix project api, agents, orchestrator, importer; steps: pinned checkout (persist-credentials false), compute tag in shell from `GITHUB_SHA`, `GITHUB_RUN_ID`, `GITHUB_RUN_ATTEMPT` (`sha-<sha>-r<run>-a<attempt>`), `docker build -f src/$PROJECT/Dockerfile --build-arg ZF_BUILD_COMMIT=$GITHUB_SHA -t zava-forward-$PROJECT:$TAG src`, `docker image inspect`, `python3 src/check-container.py`. No `${{` inside `run:`; values flow through `env:`.

## Phase 2

Test class reuses `workflow_errors` semantics by importing `test_pipeline` helpers is avoided (module executes heavy setup); instead the test file loads YAML with BaseLoader and asserts: trigger is only `pull_request` with infra path; permissions exactly `contents: read` at top and job level; every `uses` is a 40-hex SHA; no `azure/`, `docker/login`, `docker push`, `az `, `id-token`, `environment`, `secrets.`; tag shell matches `sha-...-r...-a...`.
