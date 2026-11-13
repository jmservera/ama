# Research: integrate #146 and #79 audit commits

Disposition: reused (evidence from commits dd90536f and 45e821cc, already reviewed on their source branches).
Planning Readiness: Ready.

* Base: 34b11967b on docs/demo-146-79-audits-pack-1531, clean worktree.
* dd90536f touches infra/monitoring-runbooks.md, docs/reference/README.md, docs/reference/log.md and 1515 tracking files.
* 45e821cc touches only 1520 tracking files.
* Risk: docs/reference line shifts may stale docs/architecture/cutover-reference-inventory.tsv.
* Checks: test_cutover_audit, test_bicep_policy (src/orchestrator), relative links in added lines, secret scrub, code-review-readiness.
