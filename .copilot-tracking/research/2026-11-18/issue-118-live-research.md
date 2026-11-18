# Issue 118 live research (opened 2026-11-18)

Scope: docs/evidence only. Issue #118 has one unticked criterion: "Azure Policy and Defender plans decided".
Owner decisions 2026-11-18: synthetic demo, live Azure read-only authorised (rg ama), no changes.
Status: open; evidence is recorded in docs/reference/research/issue-118-hardened-deployment-live-evidence-2026-11-18.md.

## Findings

* Policy: `az policy assignment list` returned an empty list at subscription scope; `az policy state summarize -g ama` showed 2 non-compliant policies and 6 non-compliant resources, from platform-managed assignments.
* Defender: `az security pricing show` returned AuthorizationFailed, so plan tiers cannot be read.
* Recorded decision: `infra/defender-decision.json` (audit-only policy, Defender deferred, Deny open).
* Raw probe output was not retained.
