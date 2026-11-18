# Changes: issue 144 live evidence (2026-11-18, live2)

Tier: FOCUSED (documentation only; no src, SQL, infra or deployment change). Refs #144.

## Files

* `docs/reference/research/issue-144-container-hosting-live-evidence-2026-11-18.md`: second-run section appended.
* `docs/reference/log.md`: entry appended.
* `live2` research, critique, plan, details, changes and review artifacts; same-named earlier artifacts are untouched.

## Per-criterion status (unticked criteria)

| Criterion | Status | Evidence or reason |
| --- | --- | --- |
| Worker and job images are real, versioned and deployed through the pipeline | Unproven (partly) | Real and digest-pinned: proven (8 jobs, 4 apps). Pipeline: no `src-deploy.yml` run exists; the workflow needs protected self-hosted runners and OIDC; registry tags cannot be listed (private, public access Disabled). |
| Container hardening (non-root, read-only file system, dropped capabilities) enforced in the deployed app | Unproven (partly) | Non-root proven by exec (`uid=10001`, `CapEff` 0). Root file system `overlay rw`, `NoNewPrivs: 0`, `securityContext` null, `ZF_CONTAINER_HARDENING` absent from all deployed apps and jobs. Fix needs a redeploy from current main, outside the demo authorisation. |
| Ticked criteria (scale, load test, restart) | Not re-run | No load generated this run; cost cap untouched. |

## Safeguards

No resource created, so nothing to delete. No credentials read or printed. No Playwright proof applies (no web page claim). `rpi-checks.py --all` not run.
