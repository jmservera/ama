# Details: issue 810 slice 2 (2026-11-04)

## Phase 1: live isolation

* Warm, baseline, concurrency scan, in-container burst, keep-alive test (revision `--k810`, deactivated), transport `Http`/`Http2`/`Auto` toggles, revert override (revision `--t810`), final bursts. Original template retained in /tmp only (deleted at close).

## Phase 2: source

* `infra/modules/containerapps.bicep`: API ingress `transport: 'http'` with a one-line reason.
* `infra/tests/test_api_ingress_transport.py`: asserts the API ingress block pins `http`.

## Phase 3: records

* Research note, `docs/reference/README.md` row, `docs/reference/log.md` entry, `infra/README.md` section, these artifacts, issue comment.

## Validation

* Run: new infra unit test, ruff, mypy (`--cache-dir=/tmp/mypy-530`), `az bicep build` of the module (rc 0).
* Not run: complete gate, benchmarks, full suites, Bicep deployment, `tools/rpi-checks.py --changed` is the focused tier run before push.
