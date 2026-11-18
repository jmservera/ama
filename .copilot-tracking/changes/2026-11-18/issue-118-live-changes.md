# Issue 118 live changes
Added the evidence note, an index entry and a log entry. No source, infra or Azure changes. Tier FOCUSED, docs only: link and diff review; no code tests apply.

| Criterion | Status | Basis |
| --- | --- | --- |
| Non-root, read-only rootfs, dropped caps in Dockerfile | Already ticked | Not re-audited |
| Image scan and tests in CI | Already ticked | Not re-audited |
| Application defined in Bicep | Already ticked | Not re-audited |
| Front Door Premium, WAF, Private Link before public edge | Already ticked | Not re-audited |
| Azure Policy and Defender plans decided | Decision recorded (audit-only policy, Defender deferred); not independently shown to be adopted; stays unticked pending owner acceptance | Research note; Defender tiers unreadable (AuthorizationFailed), repository policy assignments not deployed |
