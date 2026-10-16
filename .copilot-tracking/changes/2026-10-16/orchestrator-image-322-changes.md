---
title: Orchestrator image resolution changes
description: Implementation and validation evidence for issue 322
ms.date: 2026-10-16
---

Task #322; slug orchestrator-image-322. Full plan scope.

## Implementation State

P01 complete and P02-T01 complete. One plan critique passed with no findings.
No blockers or material divergences. Parent rpi-quick proceeds under explicit
user implementation/publication direction; no automatic-session opt-in inferred.

## Validation

All 103 infra unittest cases pass in a pip venv with REQUIRE_AZ_BICEP=1.
The first full-suite attempt exposed missing installed source packages, then
pip --no-deps editable installs of core/agents/api/orchestrator resolved it.
Fifteen resolver test methods execute the actual CLI with temporary fake az,
including four source mutations; compiled Bicep tests reject three mutations.
Compiling the actual pre-change HEAD main.bicep in a temporary infra copy
fails the new default assertion, proving regression sensitivity to old code.

Ruff check (E,F,I,B,UP; Python 3.12; line length 100), Ruff format check and
mypy --check-untyped-defs pass for resolver/tests. Existing compiled-policy
test file also passes Ruff. main.bicep local build and lint pass.
Git diff --check passes. No real deployment, private dataset or Docker access.

## P01: Implementation

Empty Bicep default and conditional module forwarding; unchanged three job
consumers. New canonical infra/scripts/deploy.py preserves a unique real job
image, otherwise uses the newest updated repository tag, otherwise warns on
placeholder. Explicit override skips discovery. Conflicting real images,
lookup errors and malformed output stop deployment. what-if default; --apply
uses create and returns the command exit code.

Local judgment refinement: list repositories before show-tags rather than
depend on Azure CLI error text for absent repositories. This preserves the
approved contract and prevents authorization/network errors becoming defaults.
No additional scope or user decision required.

## P02: Documentation and Delivery

Updated infra README with usage, parameter precedence, fallback/override
semantics, failure behaviour and rollout limits. Added KB routing and appended
the log. Extended the existing CI lint selector without adding/renaming checks.

One Review executed: Complete, Conformant, no findings. Publication remains
(P02-T02). Follow-up #138 integration remains outside scope; no source changes
or further review loop will follow Review.
