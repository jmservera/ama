# Plan: second main integration for PR 459 (issue 360)

Date: 2026-10-26, committed before the merge with the details file and critique record. Documentation only.

1. Commit research, plan, details and the single critique record.
2. `git merge origin/main` (commit with the noreply identity and Copilot trailer from the start). Resolve per the research decisions.
3. Validate: no markers, `git diff --check`, Markdown links in the topic's contribution, log entry count equals the sum of both parents, and the diff of the merged tree against origin/main is only the intended topic paths with no deletions and no source.
4. One independent bounded integration review compared against the first parent and main; commit changes and review records.
Stops: unexpected source conflict or ambiguous intent. No push, PR or issue edit, gate or heavy action. A future gate needs coordinator admission after the shared runner fix reaches main, and a new head and base.
