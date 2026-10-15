# Plan: Bicep quality gates (issue #139)

* [x] Phase 1: `infra/bicepconfig.json` with enabled linter rules at `error` (criterion 1).
* [x] Phase 2: `infra/tests/test_bicep_policy.py` compiles the template and checks the README security claims and the production profile default (criteria 2 and 3).
* [x] Phase 3: `infra/modules/guard.bicep` wired in `main.bicep` rejecting unsupported combinations (criteria 3 and 4).
* [x] Phase 4: README quality gates section; CI already runs lint and `infra/tests`.

Critique (executed once, compatible findings applied): the guard cannot use `@allowed([true])` (type error), so `@minLength(1)` is used; the test evaluates guard expressions to cover the matrix.

## Review fix pass

* Add `dependsOn: [guard]` to all modules and the budget; test transitive guard dependence.
* Set `REQUIRE_AZ_BICEP=1` in CI infra test step so a missing `az` fails the job.
