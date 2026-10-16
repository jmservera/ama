---
title: Issue 118 phase details
description: Dependencies and completion evidence
ms.date: 2026-10-16
---

Task ID: 118. Slug: issue-118.

## P01

P01-T01: add shared stdlib entrypoint under src, infra unit tests (outside
packages), Docker harness. Refuse root/writable root/nonzero capabilities/
missing NoNewPrivs. Positive run checks data isolation and API health.
P01-T02 depends on T01: copy guard into all images, exec ENTRYPOINT and existing
CMD; run harness in existing image matrix. Trivy includes unfixed findings,
uses empty config/ignore files rather than repository-discovered suppression.
Existing mvp-ci is a workflow name only, still builds src, keep name.

## P02

P02-T01 depends on P01: explicitly include the guard in maintenance command
overrides instead of relying on unverified ACA args-only semantics. Compiled
tests assert API 2-4 replicas, health probes, identity/image wiring across six
consumers, edge default-off/production-only Premium/WAF/private origin.
Use subTest loops to consolidate the per-image, per-consumer and per-edge
assertions within the 25-method limit. The new harness is src/check-container.py.
P02-T02: disabled Defender opt-in submits no pricing resources, never downgrades
an existing subscription plan. Keep existing audit policy decisions, document
synthetic development rationale and financial approval boundary.

## P03

P03-T01 depends on P01/P02: build all images locally; run Docker harness and
Trivy if available; test infra and project suites with absolute external-test
PYTHONPATH per project; Ruff/mypy; app health through harness. Record failures
and unresolved findings honestly. No cloud changes.
P03-T02 depends on T01: one review, record outcome and bounded findings,
authenticate commit identity, repo-local privacy email, required coauthor,
push topic branch and PR to main with Refs #118. Do not tick issue body.
