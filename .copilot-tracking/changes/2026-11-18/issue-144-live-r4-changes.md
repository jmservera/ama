---
title: Issue 144 live r4 changes
ms.date: 2026-11-18
---

Refs #144. Documentation only; no src, infra or workflow file changed. Tier: focused (documentation); the full tier is not triggered because no src code changed, and `rpi-checks.py --all` was not run.

## Files

* docs/reference/research/issue-144-live-r4-2026-11-18.md (new) and issue-144-live-r4-2026-11-18/ (raw apps, jobs, revisions, run list, env, template, exec probe and script)
* docs/reference/README.md (index entry), docs/reference/log.md (append)

## Per-criterion table

| Criterion | Proven or unproven | Basis |
| --- | --- | --- |
| 1. Worker and job images real, versioned and deployed through the pipeline | Unproven (partly) | Images real and digest-pinned (proven); `src-deploy.yml` has no runs, needs protected OIDC self-hosted runners outside demo authorisation; private registry blocks tag matching |
| 3. Container hardening enforced in the deployed app | Unproven | Only non-root proven; capabilities bounded not dropped, NoNewPrivs 0, root rw, `ZF_CONTAINER_HARDENING` unset; closing needs a redeploy from main, a deployment change not authorised |
| 2, 4, 5, Tokenomics (already ticked) | Not re-run | Restart, rollback and load drills excluded or out of scope; not claimed |

## Validation

* Link check of new note and raw files; git diff review. src-ci mypy, ruff and tests not applicable (no src or infra change).
* Live actions: read-only az and gh calls; one exec session in the demo API replica (temporary /tmp file created and removed). No resource created; nothing to delete. Credentials not used.
