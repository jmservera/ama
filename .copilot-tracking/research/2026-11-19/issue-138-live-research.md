# Issue 138 research, 2026-11-19

Disposition: executed. First unmet criterion: C1 (OIDC federated credentials scoped per environment).
Baseline: docs/reference/research/issue-138-live-r5-2026-11-18.md (all six unmet; 0 federated credentials, no AZURE_* variables).
Gap: pipeline.py verifies GitHub environment protection (verify-environment) but nothing verifies the Entra side
(exact issuer, audience, subject per environment, no client secret). Planning Readiness: Ready.
