---
title: Everything but the Software - Draft v3 Revision Report
description: Phase outcomes, verified sources, reproducible numbers and remaining author checks
ms.date: 2026-10-24
---

The original report below is historical evidence for the 24 October revision.
Its word counts and TODO locations are not current-source verification. The
dated 25 October addendum at the end identifies the later source and PR review.

## Scope and Outcome

All edits are inside docs/capstone/thought-leadership/. The starting working
tree was clean. `git worktree list` showed this checkout and two separate
worktrees; the agent-process check found no other agent using this checkout.
The branch was left unchanged. No loop, issue, pull request, commit, push,
stash, rebase or branch switch was performed.

The package matched the expected layout in everything-but-the-software/.
Additional files were existing ignored LaTeX outputs and endpoint-DLP
sidecars, which were not treated as source. The sidecars were not edited.

The revised paper is not submission-ready: registration, historical model
provenance, author checks and publication permissions remain unresolved.
No experiment was run. The results switch remains false.

## Changes by Phase

| Phase | Outcome |
| --- | --- |
| 0 | Listed the package, checked Git/worktree safety and compiler availability, counted the original body and listed its author TODOs. pdfLaTeX was available; texcount and rg were not. |
| 1 | Replaced experience-report framing, defined the case and unit of analysis, added the participant-observer design and MVP contrast, and disclosed Microsoft 365 Copilot-assisted coding. |
| 2 | Fetched all nine requested sources and SWE-CI. Added matched bibliography entries, ordered both files by key, and bounded novelty to a controlled test of an already practised intervention. |
| 3 | Softened causal attribution, added the six requested rivals and bounded the MVP/loop contrast. The migration row cites issue #196, verified in pinned ADR 0006. |
| 4 | Set four first-pass runs per arm and eight features, retained five main-study runs, corrected fixed/random effects, verdicts, failure handling, end state, fairness, registration wording and threats. Updated the protocol and added its pre-run divergence log. |
| 5 | Found the Sonnet 5.5 worker selector and its introduction in PR #420 on 21 October, Automatic coordinator selection and the separate deployed assistant model. Kept unsupported version and instruction-date TODOs. Expanded the AI-use disclosure without claiming every historical source had been rechecked. |
| 6, optional | Added pinned Git line-churn measurement, its saved output, a paper table and the artefact/source ratio. Reported literal merges separately from a squash-integration heuristic. No lizard dependency was installed. |
| 7, optional | Not attempted. A 15% body cut would require broader editorial changes; the Monday checklist and main title remain. |
| 8 | Added the v3 README section, compiled twice, ran structural and protocol checks, and checked Markdown diagnostics. Removed temporary compiler files after recording the results; retained the revised PDF. |

## Reference Verification

All URLs below were opened with the web-fetch tool on 24 October 2026.
Verification concerns metadata and the stated passages, not independent
replication or an exhaustive assessment of each source's validity.

| Key | Verified metadata and relevant evidence |
| --- | --- |
| waseem2025vibe | Muhammad Waseem, Aakash Ahmad, Kai-Kristian Kemell, Jussi Rasku, Sami Lahti, Kalle Makela and Pekka Abrahamsson; *Vibe Coding in Practice: Flow, Technical Debt, and Guidelines for Sustainable Use*; 2025. Both abstract and full text retrieved. The full text contains descriptive security-scan counts, contrary to the brief's blanket claim of no quantitative results. The paper now says it does not estimate a controlled consolidation effect. |
| openai2026harness | Ryan Lopopolo, OpenAI; *Harness engineering: leveraging Codex in an agent-first world*; 11 February 2026. Verified the roughly 1,500 PRs, million-line/five-month account, recurring targeted refactoring and doc-gardening agents. No controlled comparison was reported in the post. Only the practices, not the throughput figures, were added to the paper. |
| anthropic2025harness | Justin Young, Anthropic; *Effective harnesses for long-running agents*; 26 November 2025. The candidate URL resolved. Verified clean-state sessions, progress-file updates and the absence of a reported controlled comparison. |
| murphyhill2026agents | Emerson Murphy-Hill, Jenna Butler and Alexandra Savelieva; *Adoption and Impact of Command-Line AI Coding Agents: A Study of Microsoft's Early 2026 Rollout of Claude Code and GitHub Copilot CLI*; 2026. Verified roughly 24% more merged PRs and the explicit distinction between merges and delivered value. |
| peralta2026merged | Sien Reeve O. Peralta, Fumika Hoshi, Hironori Washizaki, Naoyasu Ubayashi, Inase Kondo, Yoshiki Higo, Hiroki Mukai, Norihiro Yoshida, Kazuki Kusama, Hidetake Tanaka and Youmei Fan; *Why Are Agentic Pull Requests Merged or Rejected? An Empirical Study*; 2026. Verified the 9,799 human-reviewed PR dataset and that 35.7% and 15.4% describe manually inspected rejection/merge samples. |
| li2026aidev | Hao Li, Haoxiang Zhang and Ahmed E. Hassan; *AIDev: Studying AI Coding Agents on GitHub*; 2026. Verified 932,791 PRs, five agents, 116,211 repositories and the supplied DOI. MSR venue follows the requested citation and its DOI record, not a new venue claim inferred from PR counts. |
| heander2026codehealth | Lo Gullstrand Heander, Markus Borg, Emma Soderberg and Christofer Rydenfalt; *CodeHealth Predicts the Token Cost of Agentic Code Review: A Pre-Registered Study of 465 Agent-Authored Pull Requests*; 2026. Verified the observational 3.5-6.1% association and unchanged median CodeHealth after batch fixing. Only the qualitative caution was added to the body. |
| lulla2026protocol | Jai Lal Lulla, Matthias Galster, Jie M. Zhang, Sebastian Baltes and Christoph Treude; *The Impact of Configuring Agentic AI Coding Tools on Build-vs-Buy Decisions: A Study Protocol*; 2026. Verified nine hypotheses and acceptance in ESEM's Registered Reports track. |
| sigsoft2021standards | Paul Ralph et al.; *Empirical Standards for Software Engineering Research*. Verified the official standards site, first arXiv posting in 2020 and revised v2 in 2021. The bibliography explicitly distinguishes those dates. |

The BibTeX entries preserve the verified authors' diacritics in LaTeX form.

```text
https://arxiv.org/abs/2512.11922
https://arxiv.org/html/2512.11922v1
https://openai.com/index/harness-engineering/
https://www.anthropic.com/research/effective-harnesses-for-long-running-agents
https://arxiv.org/abs/2607.01418
https://arxiv.org/abs/2605.22534
https://arxiv.org/html/2605.22534v1
https://arxiv.org/abs/2602.09185
https://arxiv.org/abs/2610.21914
https://arxiv.org/abs/2606.03907
https://www2.sigsoft.org/EmpiricalStandards/
https://arxiv.org/abs/2010.03525
https://arxiv.org/html/2603.03823
```

SWE-CI's full text, sections 4.3 and 4.4, verifies all 20 models below human
oracle code on the Maintainability Index, 15 of 20 above it on Pylint, and
most zero-regression rates below 0.25. No source quotations were added from
the new references.

## New Numbers and Reproduction

Commands below run from the repository root using the existing environment.
The saved check transcript is revision-checks.out.txt. These are local
paper/protocol checks, not experiment results or the repository's publication
gate. No repository-wide gate was run because the brief forbids commits and
writes outside the paper scope, and no publication was requested.

```bash
.venv/bin/python docs/capstone/thought-leadership/everything-but-the-software/anc/check_paper.py --check-latex-log
.venv/bin/python docs/capstone/thought-leadership/everything-but-the-software/anc/protocol_checks.py --check-documents
.venv/bin/python docs/capstone/thought-leadership/everything-but-the-software/anc/repo_history_metrics.py
```

* Body words: 10,353 before and 11,766 after. The saved fallback strips LaTeX
  from Introduction through Conclusion, includes table text and excludes the
  abstract, bibliography and appendices. It is approximate, not texcount.
* Abstract: 1,644 source characters after whitespace normalisation, including
  LaTeX syntax, below the 1,920-character limit. Initial source count: 1,662.
* Bibliography: 94 cited keys, 94 bibitems and 94 BibTeX keys, all unique,
  equal and alphabetically ordered by key.
* Exact two-sided Mann-Whitney attainability floors: 2/20 = 0.100000000,
  2/70 = 0.028571429 and 2/252 = 0.007936508 for three, four and five runs
  per arm. Rounded paper values are 0.10, 0.029 and 0.008. These do not
  constitute a power calculation.
* First pass: 64 feature, 32 consolidation and eight CR steps;
  64 x 30 + 32 x 15 + 8 x 45 = 2,760 minutes = 46 agent-hours;
  46 / 4 = 11.5 idealised hours. Pilot, scheduling and measurement overhead
  are excluded. B's extra-time allowance is 15 / 30 = 50%.
* New external-study numbers come from the fetched passages listed above,
  not new measurements of this repository. Existing case-study numbers were
  not silently recomputed or replaced.

The history script prints every path-class rule, selected-commit counts,
UTC cutoff and Git command. Its saved output is repo_history_metrics.out.txt.
The paper's new table copies the following integration-view values:

| Class | 8-14 Oct added | Removed | 15-24 Oct added | Removed |
| --- | ---: | ---: | ---: | ---: |
| Product source | 8,136 | 421 | 23,408 | 2,184 |
| Tests | 6,871 | 537 | 73,478 | 1,416 |
| Documentation | 12,065 | 1,297 | 25,210 | 2,455 |
| Tracking artefacts | 238,185 | 2,642 | 240,369 | 1 |
| Infrastructure | 2,708 | 73 | 6,162 | 485 |
| CI and workflows | 240 | 64 | 897 | 246 |
| Other | 25,320 | 1,099 | 72,711 | 1,776 |

The integration heuristic selects 31 and 177 commits; the literal-merge
subset has seven in each period. These are not the GitHub API PR counts.
Tracking additions / product-source additions are 29.275442 and 10.268669,
rounded to 29.28 and 10.27. The ratio falls; it must not be described as
rising. Renames are detected; binary deltas are excluded. No private data
contents were opened. Lizard was not installed, so function count and
cyclomatic-complexity comparisons are not available.

## Pinned Provenance Commands

These commands explain the resolved configuration claim and the retained
version/date TODOs. Installed current plugins were not used as evidence of
historical versions. The model-selector introduction commit is an ancestor
found through `git log` at the pinned commit, not a later repository state.

```bash
git status --short
git worktree list
git show 29c6b512f5e68733bb2cc1882343db39f5eb2cad:.github/agents/ama-backlog-delivery-coordinator.agent.md
git log 29c6b512f5e68733bb2cc1882343db39f5eb2cad --format='%h %cs %s' -- .github/agents/ama-backlog-delivery-coordinator.agent.md
git show ca4baf75837de57c99718f7423716d5dc0b0e244 -- .github/agents/ama-backlog-delivery-coordinator.agent.md
git grep -n -i -E 'hve.{0,30}(version|release|commit|v[0-9])|claude|sonnet|opus|gpt-[0-9]|model:' 29c6b512f5e68733bb2cc1882343db39f5eb2cad -- .github/agents docs/reference/log.md docs/reference/memory.md .vscode skills-lock.json
git grep -n -i -E 'feedback.first|as soon as possible|sites.{0,70}(available|possible)|eight.{0,30}parallel|8.{0,30}parallel' 29c6b512f5e68733bb2cc1882343db39f5eb2cad -- docs/reference/log.md docs/reference/memory.md
git show 29c6b512f5e68733bb2cc1882343db39f5eb2cad:docs/reference/log.md
git show 29c6b512f5e68733bb2cc1882343db39f5eb2cad:docs/adrs/0006-src-layout-and-cutover.md
```

The pinned coordinator requires claude-sonnet-5.5 at lines 167-174; PR #420
introduced it on 21 October. This does not prove its use in earlier sessions
or expose the provider build. The log's 14 October assistant exercise names
gpt-4.1-mini-2025-04-14. Neither owner instruction was found in the searched
pinned log/memory, so their dates/wording remain author-confirmation items.

## Verification and Limits

From the paper package, both passes completed successfully:

```bash
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

The resulting PDF has 29 pages. The final log has no LaTeX errors, undefined
references/citations, unresolved rerun warnings or overfull boxes above 10pt.
The structural check also verifies matching cite/bibitem/BibTeX sets, refs
and labels, balanced environments and braces outside verbatim, standalone
percent comments and the false results switch. Standalone comments were
inspected as author/evidence notes, not hidden body text. It is not a full
TeX parser or a proof of every claim's correctness.

The initial compile exposed an unsupported binomial macro; it was replaced
with package-free C(6,3) notation and both passes rerun. No packages were added.
Markdown diagnostics for the revised README and new report were checked.
The editor's generic subprocess audit warnings remain on the two Git-based
scripts: they use argument arrays, an explicitly resolved Git executable and
no shell. They do not execute the recorded coordinator commands.

The first-pass CR1 variant is a necessary protocol change, not an existing
implemented suite: F1-F8 cannot test ranking or exports introduced in F9-F10.
It needs the same owner approval and test freeze as the rest of the protocol.
The sample sizes allow small exact p-values but do not guarantee power.
The detailed compound verdicts and model choices still need pre-run approval.

## Remaining Author TODOs

Line numbers below refer to the final main.tex and are also emitted by
check_paper.py. They are not claims that the checks have been completed.

| Line | Author check |
| ---: | --- |
| 38 | Set results true only after the experiment has run. |
| 50 | Replace draft date with the actual submission date. |
| 305 | Check the Beck mathematicians-essay paraphrase. |
| 426 | Identify the historical HVE Core plugin version/commit. |
| 435 | Confirm public naming of the internal programme. |
| 490 | Recover earlier worker models and actual session/provider versions. |
| 532 | Confirm the division of labour in log coding. |
| 712 | Add coding-agent token/premium-request consumption if available. |
| 721 | Confirm dates and wording of the 22/24 October instructions. |
| 1003 | Obtain acceptance of anonymised partner/colleague descriptions. |
| 1187 | Approve every proposed experiment threshold. |
| 1193 | Supply the actual pre-registration date; do not backdate it. |
| 1194 | Supply the public registration URL before any run. |
| 1344 | Replace the inactive results branch after running the experiment. |
| 1499 | Finalise reviewer acknowledgements. |
| 1516 | Record underlying analysis/revision/historical model and runtime versions where exposed. |
| 1517 | Confirm final work allocation and extent of manual source/statistic/figure checks. |

Existing TODO(owner) items in the protocol remain open. No approval, model
choice, budget, reviewer availability or experiment execution was fabricated.

## Title Assessment

The added evidence supports an activity/usability gap and high artefact
volume. It does not establish structural code decay, its acceleration, or a
causal effect of autonomy. The title was left unchanged as instructed.
Two alternatives that better match the measured case are:

* Everything but the Software: An Exploratory Case Study of Agentic Delivery
  and Usability
* Merged Pull Requests, Missing Usability: A Case Study and Consolidation
  Experiment Protocol

## 2026-10-25: HIR Amendment and PR 448 Review

The original sections and saved `revision-checks.out.txt` above describe the
24 October revision. Their counts, TODO locations and experiment choices are
historical, not verification of the current manuscript.

### Brief and Boundaries

The owner requested more HIR literature and a measurement formula, followed by
review of the comments and issues in PR 448, using an RPI subagent for code.
This is feedback triage, not a publication gate, full independent code review
or permission to implement code changes, publish, resolve threads or merge.

All writes remain inside `docs/capstone/thought-leadership/`. The trusted
research evidence root is this paper's `anc/` folder. No tracking-directory,
application, infrastructure or private experiment-kit writes are authorised.
The parent's primary record is this report. The delegated code lane owns only
`research/subagents/2026-10-25/pr-448-code-subagent-research.md` below `anc/`.

### Sources and Snapshot Identity

* W1: [PR 448](https://github.com/jmservera/ama/pull/448), retrieved 25 October
  2026. Queried remote head: `a2b80b184ae3eec059aa4b83eb49c28d3bf61432`;
  base: `df3e9643c1cf20b2fe143ad73819b3b8b393b003`. The API lists 21 changed
  files, including two rubric-output files outside the permitted edit scope.
* The active-PR response contains 25 review threads, 19 unresolved, and 22
  timeline entries. Several unresolved locations refer to the removed kit.
* Local committed base: `7e49697ab64d1e1a921805a7aa0520d4a2865bcc`.
  The HIR amendment is uncommitted and is not evidence about the remote head.

### HIR Literature and Focused Validation

* [HG-DAgger, full text](https://arxiv.org/html/1810.02890v2): human-controlled
  takeover, sustained corrective control and explicit release. The v2 text is
  dated 2019; the initial preprint is from 2018.
* [ThriftyDAgger, full text](https://arxiv.org/html/2109.08273v1) and
  [PMLR publication metadata](https://proceedings.mlr.press/v164/hoque22a.html):
  distinguishes intervention counts, actions, duration and success; the
  proceedings publication is PMLR 164:598-608 (2022).
* The manuscript's HIR equation is explicitly a cycle-based adaptation, not a
  universal robotics or coding-agent standard. Demand and assistance remain
  separately coded; failed cycles remain in the denominator.
* Two pdfLaTeX passes and `check_paper.py --check-latex-log` passed after the
  HIR amendment: approximate body 13,475 words; abstract 1,644 source characters;
  96 cited keys, bibitems and BibTeX entries; no overfull boxes above 10pt;
  results switch false. These checks do not validate source claims or HIR
  telemetry coverage. The original 24 October transcript is preserved.
* Web PDF extraction failed and `pdftotext` and local Python PDF parsers were
  unavailable. The two primary HTML texts supplied the definitions; no parser
  packages were installed and no unverified PDF extraction is claimed.

### Research Controls and Participation

Posture is focused, from the owner's named PR and code-feedback scope. The
selected RPI Researcher lane will inspect current code evidence, seek a cheap
discriminating check and test counter-evidence before returning. Its research
must be read-only apart from its exact evidence file. No intake question is
needed because review scope and write restrictions are explicit. Review
comments are evidence to verify, not authority to expand the task.

### Review State

The RPI Researcher completed a focused Wider, Deeper and Contrarian lane in
[its evidence record](research/subagents/2026-10-25/pr-448-code-subagent-research.md).
The lane inspected local sources, not exact Git objects. The parent separately
retrieved the checker and retained TCR example at the exact remote PR head
through GitHub and confirmed the same relevant code. No private tagged-kit
review is claimed.

| Feedback | Current disposition | Evidence and limitation |
| --- | --- | --- |
| Historical baseline blocks structural checks, thread index 5 | Confirmed live, code fix outstanding. | `check_paper.py:74` invokes `git show` with `check=True` before structural validation. An in-memory missing-baseline reproduction raised `CalledProcessError` before those checks; no source or Git history was changed. |
| TCR commit failures bypass rollback, old-kit index 6 | Confirmed in the retained historical example, despite removal of the original commented path. | `mve-feature-consolidation-harness/experiment-design.md:141-144` tests only `make test` in the condition; failing `git add` or `git commit` in its success body never enters the rollback branch. Confirmed from exact-head control flow, not by running destructive Git commands. |
| Shared TCR log, index 23 and old-kit index 7 | Confirmed live in the retained historical example. | The same lines use `/tmp/tcr.log` for every invocation, while the proposal schedules parallel sessions. No parallel rollback wrapper was executed. |
| Missing checker directory, index 14 | Superseded as stated; not proof of current protocol agreement. | The retained directory exists. `protocol_checks.py` checks an older design and treats absent context/vetting notes as optional; the current README explicitly labels this limitation. |
| README continuation and completeness, indices 15 and 22 | Claims narrowed, but historical assets remain incomplete. | README and manuscript identify the local copies as earlier proposals and defer the exact registered archive. Missing context, vetting and prompt assets are not represented as supplied study materials. |
| Stale revision evidence, index 24 and general review note | Addressed locally by this dated, source-identified addendum; original evidence retained. | New structural/build results and hashes are below. The earlier transcript and original report outcomes were not rewritten. This local addition is not yet part of the remote PR. |
| Removed-kit analyzer, evaluation isolation, collection errors, empty suites, consent, egress, Ruff, generated-report counts and duplicate protocol | Outside the current PR tree; transferred risks remain unverified. | Indices 8-13 and 16-20 point to absent `consolidation-mve-kit` paths. Removal is not a fix. The separate tagged private kit and its live data were not audited or changed. |

### PR Checks and Linked Issues

The GitHub GraphQL response for PR 448 reports no linked closing issues and
`hasNextPage: false`. The only status returned by the status-check tool is
`rubric/score`, successful at 71/100 versus baseline 64/100. It reports zero
approvals required and no changes-requested review. This is not publication
clearance, scientific validation or an independent exact-head acceptance gate.

The rubric bot's general comment is internally inconsistent: it reports
section D as 7/15 and describes D1/D2/D3 as 3/2/2, while their table rows show
new scores of zero. Treat that comment as automated feedback, not a verified
readiness result. No rubric-output files outside the permitted folder were
modified.

### Source-Identified Local Validation

These hashes identify the HIR-amended local source, not a clean committed
candidate or a publication-gate receipt:

```text
main.tex
12e114450b87688329f19f4532ef51d84c393e5d75087c68636eaac6686e21ea
references.bib
ef9e0036446a0cc64f85c6cce21386d489760a49596076bbed6910b47e47f068
anc/check_paper.py
5a6b2b3df22925853efe5dcfe57c850ca5f25cbeccc8ded1b5197340712c7a4e
```

After two pdfLaTeX passes, the current log reports a 32-page PDF. The focused
checker reports 13,475 approximate body words, 1,644 abstract source characters,
96 matching cited/bibitem/BibTeX keys, no overfull boxes above 10pt and a false
results switch. Current TODO locations include figure verification at 728,
tag/registration records at 1257-1259, independent suite review at 1354,
reviewer agreement at 1401, HIR telemetry coverage at 1483 and research-statistic
verification at 1722. These positions belong only to the source hash above.

Source-claim verification, independent test/reference review, actual telemetry
coverage, registration and publication permissions were not completed. The
historical protocol-agreement check and full local publication gate were not
rerun; the latter also requires authorised commits and other prerequisites.

### Parent Synthesis and Continuation

Wider separated current paths from removed kit paths. Deeper read the owning
checker and TCR code and checked the original feedback. Contrarian evidence
showed that the old missing-directory claim is superseded and that current
documentation limits the ancillary package's authority, but did not disprove
the baseline or TCR defects. The parent's exact-head source retrieval closes
that snapshot gap for the two surviving code surfaces only.

Research disposition: executed. Review-comment triage is complete within the
requested scope; implementation planning is not applicable because code fixes
were not requested. The remaining code findings are not resolved. No code,
thread-resolution, issue, commit, push or experiment-kit mutation was performed.
