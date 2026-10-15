# Review: Bicep quality gates (issue #139)

Review executed once. Outcome: conformant with open items.

| Criterion | Result |
| --- | --- |
| Lint rules configured, errors fail build | Met (config verified with a deliberate unused parameter) |
| Rule set checks README security controls | Met (compiled-template tests) |
| Production cannot deploy with public access | Met in template guard and evaluated tests; live validation open |
| Unsupported combinations fail clearly | Met in template; message surfacing in Azure unverified |

Follow-ups: run `az deployment group validate` in Azure to confirm guard message; add Azure Policy compliance evidence; document `az bicep` as a CI prerequisite if runner image changes.

## Review fix pass

Both findings fixed and tested (guard ordering; CI cannot skip). Live Azure validation remains open.
