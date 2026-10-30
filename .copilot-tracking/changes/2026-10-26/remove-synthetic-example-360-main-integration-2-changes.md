# Changes: second main integration for PR 459 (issue 360)

Date: 2026-10-26. Documentation only; no source change.

* Prospective research, plan, details and the single critique were committed first (15815de3).
* Normal merge (no rebase, amend or force) of origin/main acafc6ee into the topic (first parent 15815de3, which sits on bot head f3658ced).
* Conflicts: `.github/rubric/scores/latest.json` resolved to main's file (bot-owned baseline, no scoring intent here, no synthesised score); `docs/reference/log.md` kept all entries of both parents, main's block first, then the topic's two 2026-10-25 entries.
* Validation: no markers, `git diff --check` clean, links in the changed Markdown resolve, merged tree against origin/main is 18 paths, 293 additions, 0 deletions: exactly 14 evidence paths (12 tracking, `docs/reference/log.md`, `infra/README.md`) plus 4 integration-2 artifacts. No `src/`, infra source, rubric or other path.
* Not run: any gate, install, Docker, browser, scan, Azure, SQL or Graph action.

Limits unchanged: obsolete case removal verified independently (980 cases, 443 open, 0 obsolete); prior audit-row preservation is inferred from chain integrity, not row comparison; no browser map, provider or whole-issue acceptance claim; the process deviation was accepted by the owner and is not a technical gate waiver.

Gate holds: receipts 96232201, e2081c02, a98e1e08 and 46a1a06f are historical and not valid for the merged head. A fresh full gate on the final head against the then-current main is needed, after the shared image-scan runner fix is on main (a head/base change again), with separate coordinator admission. Push, PR update and hosted CI are also pending coordinator authority.
