# Everything but the Software — arXiv source package (draft v2, 24 Oct 2026)

Working title: *Everything but the Software: How Coding Agents Accelerate Feature-Driven Decay. An Experience Report and an Experiment Protocol.*

## Files

| File | Purpose |
| --- | --- |
| `main.tex` | Paper source. The bibliography is embedded, so it compiles on arXiv without BibTeX. |
| `fig-log-growth.png` | Figure 1: words and hedging phrases appended to the project log per day (400 dpi). |
| `fig-causal-loop.png` | Figure 2: the reinforcing loop and the feedback-first intervention (400 dpi). |
| `references.bib` | The same 85 references as BibTeX, for reuse or a later switch to `\bibliography{}`. |
| `anc/log_metrics.py` | Recomputes the log measures in Appendix A from `docs/reference/log.md` at commit `29c6b51`; `--json` writes the per-day data. |
| `anc/log_daily.json` | Per-day entries, words and hedging phrases (output of `log_metrics.py --json`). |
| `anc/make_figures.py` | Redraws both figures from `anc/log_daily.json`. |
| `anc/mve-feature-consolidation-harness/` | The experiment protocol in HVE Core's Experiment Designer (MVE) format: context and evidence register, hypotheses, vetting, design, plan, and the three step prompts. |

arXiv publishes everything under `anc/` as ancillary files.

## Figures

The figures are plain PNG files, generated from public data in the repository, so they carry no document protection. pdfLaTeX reads PNG directly. SVG is not an option for arXiv, because the `svg` package needs Inkscape and shell escape, which arXiv does not run.

Before you upload, check that the PNG copies synced to your OneDrive open without a protection prompt. If any copy has picked up protection, redraw the figures on a machine outside the corporate tenant:

```
pip install matplotlib pillow
python3 anc/make_figures.py          # writes both PNGs next to main.tex
```

To rebuild the data from the public repository first:

```
git clone https://github.com/jmservera/ama && git -C ama checkout 29c6b512f5e68733bb2cc1882343db39f5eb2cad
python3 anc/log_metrics.py ama/docs/reference/log.md --json anc/log_daily.json
```

## Compile

- Overleaf: upload the zip as a new project. The compiler is pdfLaTeX. The zip has `main.tex` and `anc/` at its root, the layout arXiv expects.
- Locally: run `pdflatex main.tex` twice.
- Packages, all in TeX Live: lmodern, geometry, microtype, graphicx, booktabs, tabularx, array, enumitem, xcolor, natbib, xurl, caption, hyperref.
- The switch `\resultsfalse` near the top keeps Section 8.4 as a status note. Set `\resultstrue` and replace the placeholder once the experiment has run.

## What changed in draft v2

- New thesis. Feature accumulation degrades software, and agents speed this up through compounding errors and output that exceeds review capacity.
- New background. It covers software evolution (Lehman, Parnas, Eick, Cunningham, Fowler, Tornhill and Borg, Besker) and recent studies of agent-driven decay. Counter-evidence is included (Echoes of AI, SWE-Maintain, and the Herraiz caveat on Lehman's laws).
- New Table 4, which maps the base rate and the two accelerants to the five mechanisms.
- New Section 7.1, *A consolidation harness*: after every feature the loop stops, then reviews and refactors through test && commit || revert before the next feature starts.
- New Section 8, *Testing the harness*. It covers hypotheses H1–H7, three arms (no consolidation, consolidation, placebo review-only), suites, measures, analysis and bias controls.
- New Appendix B with the consolidation prompt.
- New sources, including Lanzetta (two articles) and Lamanna (*Changing how we build*).

## Before you submit

1. Resolve every `TODO(author)` comment in `main.tex` (search for `TODO`):
   - check the paraphrase of Beck's "Mathematicians…" essay against the full text;
   - state the HVE Core version and the model versions used;
   - confirm how the internal programme may be named;
   - confirm that the partners and the colleague concerned accept their anonymised descriptions;
   - add coding-agent consumption for 15–24 Oct if you have it;
   - confirm the dates and wording of your "feedback-first" and "sites ASAP" instructions;
   - confirm every experiment threshold before the pilot, then do not change it;
   - after the runs, set `\resultstrue` and write the results;
   - update the date, the acknowledgements and the generative-AI statement.
2. Resolve every `TODO(owner)` in `anc/mve-feature-consolidation-harness/`. The open choices are thresholds, model and runtime, budgets, first pass only or main runs, and suite S2 (library suite or SlopCodeBench).
3. Rewrite in your own voice where needed. The rubric allows AI drafting, but the insight, evidence and recommendation must be yours.
4. Get the internal approvals Microsoft requires for external publication.
5. Compile, then read the PDF end to end. Check tables and figures for overflow.
6. arXiv publishes the source files, comments included. Before you upload, strip the comments (for example with `arxiv_latex_cleaner`) and leave out `README.md`.

## Running the experiment with HVE Core

To continue in VS Code with the Experiment Designer agent, copy `anc/mve-feature-consolidation-harness/` into the experiment repository as `.copilot-tracking/mve/2026-10-24/feature-consolidation-harness/`. Keep the published copy under `anc/` as the record of the precommitted protocol.

## arXiv notes (checked 24 Oct 2026)

- Primary category: cs.SE. Optional cross-lists: cs.HC, cs.AI.
- Since 31 Oct 2025, arXiv CS accepts review articles and position papers only after peer-review acceptance. Research papers are not affected, so keep the paper framed as a data-backed case study with a method, data and threats to validity, not as an opinion piece.
- Since 21 Jan 2026, a first-time submitter in cs.SE needs either prior authorship in the domain or a personal endorsement from an established arXiv cs.SE author.
- arXiv asks authors to report significant use of generative AI. AI tools cannot be authors, and authors are responsible for all content.
- The abstract field limit is 1,920 characters. The abstract is about 1,660.
