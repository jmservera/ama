<!-- markdownlint-disable-file -->
# Changes: coordinator current-source intake (issue 1204, pass 5)

* Local rebase of the clean unpublished branch onto origin/main bb3a3b03cb (named reason: current-source intake; no conflict). Backup ref backup/issue-1204-pre-rebase-6465 keeps 6465ac16d. Pre-rebase SHAs and all earlier validation are historical.
* G1: admission bullet now counts frozen unpublished candidates within the eight, one unit per issue.
* G2: schedule provenance names the live read-back as authoritative (delivery 15, cleanup 8 per operator-supplied evidence; 9, 7, 6, 2 historical). No schedule touched.
* G3: activity-handoff premise updated (flags on main since #1209), `--help` gate and legacy `--apply` prohibition kept.
* No divergence from the plan. Frontmatter lines 1-5 unchanged.
