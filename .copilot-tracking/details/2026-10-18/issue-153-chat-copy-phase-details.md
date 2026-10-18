<!-- markdownlint-disable-file -->
# RPI Phase Details: issue-153-chat-copy

## Metadata

Task ID: 153. Slug: issue-153-chat-copy. Date: 2026-10-18.
Plan: .copilot-tracking/plans/2026-10-18/issue-153-chat-copy-plan.md.
Research: .copilot-tracking/research/2026-10-18/issue-153-chat-copy-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete, source batch present | P01-T01, P01-T02 |
| P02 | Complete, local evidence recorded | P02-T01 |
| P03 | Complete; PR #402 published, coordinator handoff | P03-T01, P03-T02 complete |

<!-- rpi:phase id=P01 -->
## P01: Copy and regression evidence

Use existing content vocabulary and safety glossary, not new operating policy.
No implementation before the final-candidate critique.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Extend copy guard and change application-owned labels

Research C1-C5 identify exact strings and exclusions. Update chat role guidance
to say only an authorised human makes a restart decision for stopped retrofit
work, and disclaim panel ability to restart. Use "Check recorded at" and
historical-record wording; preserve dates, source text, card versions and dynamic
values. Coupled app labels use recorded/as-of concepts without implying currentness.
Extend the six-file scanner to seven. Narrow raw `envelope`/snapshot identifier
exceptions are not a licence to skip visible labels. Add <=4 unit test methods
as locked in plan. Mutation proof restores each observed chat string in memory
and confirms guard failure without touching canonical production files.
Extend the existing real-app harness to check changed labels and exact original
source text with all six banned term families before and after history restore.
Use the existing fixture's source(text=...) parameter locally, not a shared
fixture edit. The allowed-identifier unit case must still reject an adjacent
bad visible label. Check independent hazard notices, unknowns, human boundary
and AI label.
Completion: diff is copy-only in production JS; tests/harness prove the boundary.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Update existing audit record and KB routing/history

Extend docs/reference/research/ux/content-standard.md in place, update date,
add missing glossary alternatives and dated scope/method/limits. Distinguish
application labels from raw technical JSON details and dynamic source/user/model
content. Do not imply universal errors or human acceptance. Update index routing
and append log entry without changing existing entries. No tracking links in
public documentation. Completion: local relative links reviewed, diff only adds
bounded evidence and does not tick issue criteria.

<!-- rpi:phase id=P02 -->
## P02: Validate and freeze candidate

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run local checks and freeze reviewed file hashes

Depends on P01. Record exact focused test commands and actual counts, node syntax,
API ruff/format/mypy, mutation failures, local Chromium results, guideline
retrieval/check gaps, SQL/Docker applicability. Do not install unless a missing
tool/dependency is demonstrated. Initial missing distribution failure already
justified task-local pip installation. Use wholly constructed fixture and its
own loopback HTTP server; block external browser resources and inference.
Existing harness tears down all resources. Freeze candidate as exact Git tree
plus SHA-256 file manifest (no pre-Review commit required). Public docs must not
change after this boundary without a source-correction receipt.
Use resolved `.local/issue-153-chat-copy/tmp` for TMPDIR/TMP/TEMP in fresh Python
and Chromium processes; verify tempfile.gettempdir(). Store axe input/cache
under the same task-local root; retain only intended evidence, remove scratch.
Run `ruff check --isolated --select E,F,I,B,UP --target-version py312
--line-length 100 checks/regulatory_ux_check.py` and the matching isolated
format check, because the ordinary API config exempts this harness.

<!-- rpi:phase id=P03 -->
## P03: Independent Review and publication

One original Review completed on exact candidate tree
7f7487566422ba84380608de1d2ea1b4f913b8f6: Conformant for the bounded slice,
five inherited/residual Low follow-ups, no introduced scoped defect.
No correction receipts used. Critique and Review frozen.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run one original independent Review

Fresh independent reviewer, bounded to supplied plan/changes/diff and exact
candidate. Refresh Web Interface Guidelines first; review changed web files
against all rules, report file:line findings with inherited/out-of-scope context.
One complete actionable finding set and explicit verdict. Reviewer writes only
the original Review artifact. Freeze it and the critique on completion.
At most two correction receipts may resolve scoped findings, not a second
original Review or self-awarded independent pass.
Unresolved scoped defects or implementation-caused test failures block validated
publication; correct within two receipts or report exact blockers to coordinator.
Do not bypass unavailable required Chromium proof. Demonstrated inherited
failures and optional axe/image availability limits are explicitly classified,
not silent passes. Only a clearly blocked/draft evidence handoff can publish
unaccepted work. A significant authority/semantic choice stops affected work.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Reconcile artifacts and publish for coordinator

Depends on Review/corrections. Synchronize actual markers/details/state/changes
without rewriting original records. Verify docs parity and git diff --check.
Re-resolve account and use repository-local noreply email for author/committer.
Conventional commit plus required Copilot trailer. Push only supplied branch,
create PR to main with Refs #153 and no closing directives. Report base movement
and exact base/candidate/head; do not integrate or alter another PR.
Stop for independent coordinator exact-head review after publication.

Completion evidence: initial delivery ea3208fb6068a2293210f830c71c5eed50fe8be5
was pushed; gh pr create returned https://github.com/jmservera/ama/pull/402.
Read-only verification found OPEN, target main at
f91353169756dc41ebbcca944bdd3f44f7c04b89, initial head as above and no hosted
results yet. Final tracking-only commit updates lifecycle/publication facts;
source/test/docs remain the exact reviewed tree's seven changed blobs.
No merge/integration, source correction, issue mutation or repeated Review.
