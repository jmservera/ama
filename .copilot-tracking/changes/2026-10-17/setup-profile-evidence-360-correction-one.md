---
title: Setup profile evidence correction ONE disposition
description: Coordinator findings, failing-first reproduction and correction evidence, not a new Review
date: 2026-10-17
---

## Authority and Preserved Assessment

Coordinator independent exact-head 9561938a558eed0097fba61bf2623df6ad8c42a4
assessment: Revise, two Medium defects. Correction ONE explicitly authorized.
This is a separate implementation disposition, not another full Review or
independent Pass. Original plan critique and single RPI Review remain unchanged.

## Disposition

| Finding | Correction | Evidence and remaining boundary |
| --- | --- | --- |
| Medium: literal /providers/ split rejects mixed-case ARM IDs | Full anchored case-insensitive parse of subscription/resourceGroups/ama/providers/Microsoft.App/type/name, canonical subscription UUID and normalized exact ID binding | Original mixed-case repro errored before correction. Mixed app/environment/full IDs pass; wrong RG/provider/type/subscription/extension scope and malformed UUID fail. No substring/name fallback |
| Medium: invalid exported envelopes count as neutral | Supported group ARM schema, language/content version, matching array/symbolic resource container and basic resource entries checked before parameter resolution | Missing/numeric/unrelated schema and arbitrary resource-object repros all failed before correction; now refuse. Explicit/default production and reported three-deployment safety tests retained |

## Failing-First Evidence

Before editing production source:

```bash
profile-venv/bin/python -m unittest discover -s infra/tests -p test_setup_entra.py -k test_correction -v
```

Result: two methods run, four failures (missing/numeric/unrelated schema and
unversioned arbitrary resource object accepted) and one error (valid mixed-case
Providers app ID refused). Exact errors were AssertionError: SetupError not
raised and SetupError: Demo environment is not bound to the selected app in ama.
Tests used fictional metadata only, no live Azure or private inputs.

## Supported Contract and Conservative Refusal

* Official template syntax and 2019-04-01 resource-group schema retrieved
  2026-10-17:
  https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/syntax
  and https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json.
* Supported group schema URLs: 2019-04-01 and 2015-01-01, optional trailing #.
  Missing, malformed, foreign-scope and unrecognized schemas fail explicitly.
* Omitted/1.0 language: array resources. Supported 2.0: symbolic-name object.
  Unknown/experimental versions, invalid symbols, non-resource values and
  missing/wrongly typed name/type/apiVersion refuse.
* Literal types/API dates and optional properties/child containers receive
  bounded structural guards; no provider schema engine, network schema lookup
  or new dependency. Unsupported API-profile/import extensions refuse.
* Nested Microsoft.Resources/deployments, including inline templates and
  templateLink contracts, explicitly refuse. Their parameter/default scopes
  are not evaluated or silently declared neutral. This intentionally limits
  otherwise valid nested historical exports; a separate supported evidence
  path would need later approval, not a tag or naming workaround.
* Supported envelope only establishes parseable contract structure, never
  development authority. Exact bound resource evidence, explicit/default
  production and all contradictions retain their existing veto.
* Reported three-deployment fixtures now include normal Microsoft.App
  app/environment resource declarations with name, API version, location and
  properties rather than relying only on empty resources. These remain
  fictional schema-shaped fixtures, not fresh captured live templates.

## Validation

Existing isolated profile-venv has editable src core/agents/api/orchestrator
installed for this worktree. No manifest change or dependency install needed.

* Full combined setup/staff/auth/secret suite: 206 passed (123 setup, 43
  staff_azure, 15 staff initializer, 17 auth delegate, eight secret lifecycle).
* Six additional correction methods cover independent repros, wrong binding,
  supported array/symbolic contracts, malformed/unsupported forms and nested
  parameter/default refusal. No original test removed or weakened.
* Configured README three-file ruff lint and format pass; changed correction
  lines have zero introduced lint diagnostics, 225 untouched legacy diagnostics.
* compileall and git diff --check pass. Final rerun/receipt in changes record.
* No full infra-discovery result claimed: required complete named suites run.
  Reviewer missing-YAML full-discovery observation remains distinct; no import
  failure is represented as a full-suite Pass.

## Integrity and Delivery Boundary

* Original critique SHA-256:
  48931b8edc0be01fc925293721d305a60446e61e3e7f663ba509d8d674883ed9.
* Original Review SHA-256:
  65721ae7cec37255bcf0dbc37b9baebd0282d62e50e8646b0f43d261540476a6.
* Fresh fetched main is 226702779e57e490cb10dc06ab014760c7d8a761.
  No correction rebase authorized; topic ancestry remains on 3f544fb9.
* Normal own-topic commit/push to PR #391 only. Original Review/critique
  unchanged; coordinator corrected-head acceptance still required.
* Prior exact-9561938a ordinary Source CI 39067901027 and MVP validation
  39067900996 both completed success. These are prior-head results only and
  do not supersede the coordinator's Revise or validate the corrected head.
* No cloud/live setup, Graph, SQL, tag/IAM/network writes, private inputs, paid
  rubric, merge or issue closure. ACR403/private publisher and genuine tenant/
  browser/SQL/AI acceptance remain unmet.
