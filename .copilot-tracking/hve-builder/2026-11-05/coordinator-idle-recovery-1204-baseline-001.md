<!-- markdownlint-disable-file -->
# HVE Builder baseline: coordinator agent (issue 1204)

* Mode: improve. Classification: Major.
* Target: .github/agents/ama-backlog-delivery-coordinator.agent.md (578 lines at HEAD ead177ef9)
* Write boundary: that file plus dated evidence under .copilot-tracking/. Frontmatter (name, description) preserved; no `tools:` or `model:` present or inspected.
* Baseline method: bounded read of the known target and the supplied canonical references (retention policy, issue body, approved prompt snapshots). The `rpi-research` bridge was satisfied by reuse: see .copilot-tracking/research/2026-11-05-coordinator-idle-recovery-1204-research.md.

## Baseline findings (before edits)

* B1 High, Outcome and stop rules: the idle rule ("nothing changed" acceptable after confirming everything is merged, human-blocked, dependent or running) names no evidence, no unknown class and no recovery trigger, so status-only ticks complied.
* B2 High, Evaluation hooks: the closure audit relies on printing the backlog-sync queue; no cursor, batch or persistence.
* B3 High, Safety and workflow contract: step 5 reuses `/tmp/brief-{number}.md`, applies tiers "before every push" and has no no-publication or parent-target instruction, contradicting step 6 publication.
* B4 Medium, Workflow contract: step 5 `/every 5m` check and "stop when every issue merged or blocked" conflict with the approved 10-minute schedule and stop rule; step 8 rebases overlapping PRs by default against the CI economy rule.
* B5 High, Safety: Owner delegation and step 10 allow worktree and branch removal without finite manifest, unknown-upstream, receipt-ownership or squash-lifecycle rules.
* B6 Medium, Evidence fidelity: no approval register, no rule that acknowledged approvals must be routed.

## Next action

Author one coherent batch, then fresh-context static review.
