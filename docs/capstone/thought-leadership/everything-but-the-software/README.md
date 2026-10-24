---
title: Everything but the Software - arXiv source package (draft v3)
description: Exploratory case study, unexecuted experiment protocol and reproduction scripts
ms.date: 2026-10-24
---

Working title: *Everything but the Software: How Coding Agents Accelerate Feature-Driven Decay. An Exploratory Case Study and an Experiment Protocol.*

## Files

| File | Purpose |
| --- | --- |
| `main.tex` | Paper source. The bibliography is embedded, so it compiles on arXiv without BibTeX. |
| `fig-log-growth.png` | Figure 1: words and hedging phrases appended to the project log per day (400 dpi). |
| `fig-causal-loop.png` | Figure 2: the reinforcing loop and the feedback-first intervention (400 dpi). |
| `references.bib` | The same 94 references as BibTeX, for reuse or a later switch to `\bibliography{}`; both bibliographies are ordered by key. |
| `anc/log_metrics.py` | Recomputes the log measures in Appendix A from `docs/reference/log.md` at commit `29c6b51`; `--json` writes the per-day data. |
| `anc/log_daily.json` | Per-day entries, words and hedging phrases (output of `log_metrics.py --json`). |
| `anc/make_figures.py` | Redraws both figures from `anc/log_daily.json`. |
| `anc/check_paper.py` | Reproduces the approximate body count against the starting draft and checks citations, labels, environments, braces, inline comments and abstract length. |
| `anc/protocol_checks.py` | Reproduces exact rank-test floors and first-pass step/time arithmetic; `--check-documents` checks protocol agreement. |
| `anc/repo_history_metrics.py` | Measures path-class line churn at the pinned commit, separating literal merges from PR-numbered first-parent integrations. |
| `anc/repo_history_metrics.out.txt` | Saved history measurement, including definitions, commands and limitations. |
| `anc/mve-feature-consolidation-harness/` | The experiment protocol in HVE Core's Experiment Designer (MVE) format: context and evidence register, hypotheses, vetting, design, plan, and the three step prompts. |

arXiv publishes everything under `anc/` as ancillary files.

## Figures

The figures are plain PNG files, generated from public data in the repository, so they carry no document protection. pdfLaTeX reads PNG directly. SVG is not an option for arXiv, because the `svg` package needs Inkscape and shell escape, which arXiv does not run.

Before you upload, check that the PNG copies synced to your OneDrive open without a protection prompt. If any copy has picked up protection, redraw the figures on a machine outside the corporate tenant:

```bash
pip install matplotlib pillow
python3 anc/make_figures.py          # writes both PNGs next to main.tex
```

To rebuild the data from the public repository first:

```bash
git clone https://github.com/jmservera/ama && git -C ama checkout 29c6b512f5e68733bb2cc1882343db39f5eb2cad
python3 anc/log_metrics.py ama/docs/reference/log.md --json anc/log_daily.json
```

## Compile

* Overleaf: upload the zip as a new project. The compiler is pdfLaTeX. The zip has `main.tex` and `anc/` at its root, the layout arXiv expects.
* Locally: run `pdflatex main.tex` twice.
* Packages, all in TeX Live: lmodern, geometry, microtype, graphicx, booktabs, tabularx, array, enumitem, xcolor, natbib, xurl, caption, hyperref.
* The switch `\resultsfalse` near the top keeps Section 8.4 as a status note. Set `\resultstrue` and replace the placeholder once the experiment has run.

## What changed in draft v2

* New thesis. Feature accumulation degrades software, and agents speed this up through compounding errors and output that exceeds review capacity.
* New background. It covers software evolution (Lehman, Parnas, Eick, Cunningham, Fowler, Tornhill and Borg, Besker) and recent studies of agent-driven decay. Counter-evidence is included (Echoes of AI, SWE-Maintain, and the Herraiz caveat on Lehman's laws).
* New Table 4, which maps the base rate and the two accelerants to the five mechanisms.
* New Section 7.1, *A consolidation harness*: after every feature the loop stops, then reviews and refactors through test && commit || revert before the next feature starts.
* New Section 8, *Testing the harness*. It covers hypotheses H1–H7, three arms (no consolidation, consolidation, placebo review-only), suites, measures, analysis and bias controls.
* New Appendix B with the consolidation prompt.
* New sources, including Lanzetta (two articles) and Lamanna (*Changing how we build*).

## What changed in draft v3

* Reframed the paper as an exploratory single-case study with a
   participant-observer, a defined unit of analysis and a bounded MVP-week contrast.
   Added the ACM SIGSOFT reporting standard and disclosed AI-assisted log coding.
* Added nine references on flow and debt, deployed harness practices, PR-based
   evaluation, CodeHealth and registered-report protocols. The novelty is a
   controlled test of a practised intervention, not the invention of clean-up.
   Waseem et al.'s full text contains descriptive scan counts, contrary to the
   review brief's blanket description of no quantitative results.
* Softened causal claims and added six rival explanations, including migration,
   my gate rules, budget constraints and identity setup.
* Changed the exploratory first pass to four runs per arm and eight features;
   retained five runs per arm per suite for the main study. Verified rank-test
   floors and the 64 feature, 32 consolidation and eight change-request steps:
   46 agent-hours, or 11.5 idealised hours across four parallel sessions.
* Scoped first-pass CR1 to available F1-F8 behaviour. Full ranking/export checks
   still require F9-F10 in the main study. Both variants must be frozen before
   the pilot; they cannot be selected after seeing results.
* Made suite a fixed effect and run a random intercept. Clarified interval-based
   verdicts, the post-consolidation end state, missing features, change-request
   regression protection and B's extra time. Registration remains pending; no
   date or URL has been invented. The pre-run changes are in the divergence log.
* Reported the Sonnet 5.5 worker selector introduced on 21 October in PR #420,
   Automatic coordinator selection and the separate deployed assistant model.
   Historical HVE and underlying service versions remain author checks.
* Added human intervention rate (HIR) and intervention-demand rate as secondary
   measures, with whole-feature-cycle denominators, event reasons and human
   minutes. Primary runs remain unassisted; actual rescue is a recorded deviation,
   not a replacement run. No hypothesis threshold or adoption gate was changed.
* Added pinned line-churn evidence with literal-merge and squash-integration
   views. Artefact/source additions are 29.28 before the loop and 10.27 during it.
   These counts do not establish structural decay. Complexity was not measured
   because lizard was not installed; no dependencies were installed.
* Retained the main title, Monday checklist, PNG figures and `\resultsfalse`.
   The optional 15% body cut was not attempted; the required additions increase
   the body. The experiment has not been run.

Run the saved checks from the repository root, using its existing environment:

```bash
.venv/bin/python docs/capstone/thought-leadership/everything-but-the-software/anc/check_paper.py
.venv/bin/python docs/capstone/thought-leadership/everything-but-the-software/anc/protocol_checks.py --check-documents
.venv/bin/python docs/capstone/thought-leadership/everything-but-the-software/anc/repo_history_metrics.py
```

## Before you submit

1. Resolve every `TODO(author)` comment in `main.tex` (search for `TODO`):
   * check the paraphrase of Beck's "Mathematicians…" essay against the full text;
   * state the HVE Core version and the model versions used;
   * confirm how the internal programme may be named;
   * confirm that the partners and the colleague concerned accept their anonymised descriptions;
   * add coding-agent consumption for 15–24 Oct if you have it;
   * confirm the dates and wording of your "feedback-first" and "sites ASAP" instructions;
   * record owner approval and the dated frozen protocol version, including hypotheses and thresholds, before the pilot; record scope, sample sizes and optional arm C before any non-pilot run;
   * after the runs, set `\resultstrue` and write the results;
   * update the date, the acknowledgements and the generative-AI statement.
2. Resolve every `TODO(owner)` in `anc/mve-feature-consolidation-harness/`. The open choices are thresholds, model and runtime, budgets, first pass only or main runs, and suite S2 (library suite or SlopCodeBench).
3. Rewrite in your own voice where needed. The rubric allows AI drafting, but the insight, evidence and recommendation must be yours.
4. Get the internal approvals Microsoft requires for external publication.
5. Compile, then read the PDF end to end. Check tables and figures for overflow.
6. arXiv publishes the source files, comments included. Before you upload, strip the comments (for example with `arxiv_latex_cleaner`) and leave out `README.md`.

## Running the experiment with HVE Core

To continue in VS Code with the Experiment Designer agent, copy `anc/mve-feature-consolidation-harness/` into the experiment repository as `.copilot-tracking/mve/2026-10-24/feature-consolidation-harness/`. The current protocol is provisional, not yet approved or frozen. Once owner approval and freezing are recorded, keep that published version under `anc/` as the precommitted record and log subsequent deviations separately.

## arXiv notes (checked 24 Oct 2026)

* Primary category: cs.SE. Optional cross-lists: cs.HC, cs.AI.
* Since 31 Oct 2025, arXiv CS accepts review articles and position papers only after peer-review acceptance. Research papers are not affected, so keep the paper framed as a data-backed case study with a method, data and threats to validity, not as an opinion piece.
* Since 21 Jan 2026, a first-time submitter in cs.SE needs either prior authorship in the domain or a personal endorsement from an established arXiv cs.SE author.
* arXiv asks authors to report significant use of generative AI. AI tools cannot be authors, and authors are responsible for all content.
* The abstract field limit is 1,920 characters. The conservative source count
   for this revision is 1,644, including LaTeX syntax and normalised whitespace.
