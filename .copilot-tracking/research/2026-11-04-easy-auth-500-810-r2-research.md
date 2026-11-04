# Research: issue 810 slice 2, live cause isolation (2026-11-04)

Disposition: executed. Planning Readiness: Ready.

## Prior delivery checked

* PR 883 (merged) localised the fault to the Easy Auth hop and left criteria 2 and 3 unmet. PRs 764, 786 and 796 are merged and do not address it.
* Branch note: the worktree branch is `feat/issue-810-r5`, not the `feat/agent-chat-skills-530` named in the request; the work targets `main` either way.

## Evidence (owner approval 2026-11-04, live changes to `ca-cutover-test-demo-api` only)

Full table: [docs/reference/research/easy-auth-intermittent-500-2026-11-03.md](../../docs/reference/research/easy-auth-intermittent-500-2026-11-03.md).

* Warmed with `/healthz` (scale to zero, first call 21 s). Baseline reproduced: 1 to 3 x 500 per 30 under `Auto`; rate roughly constant from 5 parallel upward.
* In-container burst to `127.0.0.1:8088`: 120 of 120 x 200, so the app is not the source.
* HTTP/1.1 keep-alive on the app (temporary command override): still 2 to 5 x 500 per 30. HTTP/1.0 close-per-request ruled out.
* Ingress transport `Http`: 0 x 500; `Http2`: all 500 (app has no h2c).
* Final on revision `--t810` (original template): 600 requests, 0 x 500.
* Constraints met: Log Analytics (network perimeter) and the registry (firewall, ACR build and login 403) rejected this host, so mechanism proof and a custom image were impossible; no firewall change was made (outside approval).

## Gates

* Touches infrastructure (Bicep, live Container App setting): complete gate is the coordinator's; not run here. Focused tests, ruff and mypy run.
