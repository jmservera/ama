# Cut-over evidence changes

Task: issue-201 / cutover-evidence-201. Scope: full evidence preparation plan.

## P01 execution

Starting local pip-venv checks and bounded Azure bootstrap. Existing group ama
has no generic resources, but retains budget-forward-test (hidden from generic
resource inventory); preserve that pre-existing budget. Azure principal is an
application, not a signed-in owner; tenant provisioning is not available.
Owner comment #322 specifies future image resolution and #323 confirms warning
rulesets, not enforced checks. Record both without changing workflows here.

## P02 implementation

Added a bounded tracked-text audit and external tests. Reconciles all 130
historical rows, including sandbox patterns; five explicit actual-target
exceptions prevent stale proposed paths being treated as current.

Immediately relevant amendment: four documented az acr build calls failed
because classic builder cannot execute existing RUN --mount. ACR task with
DOCKER_BUILDKIT=1 reaches the real API build and exposes a second existing
failure: src/.dockerignore excludes the runtime golden explicitly COPYed by
the API Dockerfile. Add src/acr-cutover.yaml (unique run-ID tags) and a narrow
golden-only context exception, plus regression in the same test module.
No Dockerfile, dependency, image privilege or application authority changes.
This preserves existing API runtime intent rather than rebuilding products.

Azure deployment has an observed Microsoft.Devices NotRegistered failure.
Subscription registration is out of scope; no registration attempted.

Final bootstrap Failed also on SQL DenyPublicEndpointEnabled; actual public
interface Disabled. No app exists, endpoint lookup exits 1 ResourceNotFound.
No actual HTTP smoke, tenant initialization, private seed or subscription
registration. Final sanitized inventory is 65 generic resources plus two
budgets (one pre-existing, one run-created). Resources retained; no current
post-evidence teardown instruction established. Cost exposure documented.

Run db7 built four images after the context fix; final db8 rebuilt and passed
four remote runtime contracts (UID/read-only/no capabilities/no working-data
paths; agents no SQL/Azure clients), then pushed unique cutover-db8 tags.
Digests, command outputs, source hashes and IDs are in the public evidence pack
and sanitized JSON. No deployed revision or vulnerability-scan pass claimed.

Local validation: core full 482/one skip, then final nine targeted tests
(sandbox case added after full run); agents70, API542/103 skips, orchestrator22,
importer39. Five Ruff/format/mypy passed; infra86, rename25, namespace/no-data/JS,
Chromium shared-IA harness passed. Agents discovery initially failed from
overbroad fixture PYTHONPATH; corrected invocation passed. Missing rename
dependencies installed from existing manifest, then passed.

Mutation: disabling actual target overrides produces two assertion failures
without import/discovery errors. Substituting the actual base-commit ignore
file fails the golden-context regression. Restored code passes. Fixtures
also prove missing-target/reference drift and exclusions-before-read.
No document-specific semantic checker added; direct docs review preserves
unchecked owner gates. Generated reports enumerate tracked text only.

## P03 handoff

Ready for one Review; publication pending. Evidence pack explicitly not ready
for cut-over. Current-task build blockers corrected; external subscription,
SQL/network, tenant and owner gates remain unfulfilled. No owner approval
or deletion authorized.
