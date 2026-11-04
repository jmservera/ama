# Deploy main 810/462 research (2026-11-04)

Research disposition: satisfied-and-skipped (existing evidence: infra/README.md live-apply recipes, easy-auth-intermittent-500 research note). Planning Readiness: Ready.

* origin/main `b0080d4e1` includes #1043 (API transport http) and #1044 (resident UX).
* Live before: demo API image tag `891-1022` (transport already `Http` set live via `az containerapp ingress update`); resident image digest `sha256:0408917d...`.
* ACR `crcutovertestrzsrg`: private (public Disabled, Deny, no rules, exports disabled).
* `az acr build` fails in the window: hosted build agents get 403 at registry login (the IP rule admits only the operator). Local `docker build` plus `docker push` inside the window works.
* Staff Entra token unavailable to the operator (AADSTS501051, not assigned a role); no new roles allowed. Resident shared demo password is owner-held; not available to the agent.
