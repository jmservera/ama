---
title: Everything but the Software - Draft v3 Revision Report
description: Phase outcomes, verified sources, reproducible numbers and remaining author checks
ms.date: 2026-10-24
---

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
