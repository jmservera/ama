---
title: Everything but the Software - arXiv source package (draft v3)
description: Exploratory case study, author clarifications and registration-pending experiment protocol
ms.date: 2026-10-25
---

Working title: *Everything but the Software: How Coding Agents Accelerate Feature-Driven Decay. An Exploratory Case Study and an Experiment Protocol.*

## Current status

The 25 October author clarification supersedes the earlier method and study
descriptions below. Execution is paused. The author reports tagging the protocol;
the exact snapshot and completed registration remain to be supplied. Earlier
runs retain their original labels and timestamps and will not enter the fresh
registered confirmatory analysis. No study results are reported.

The separate private experiment kit is the intended study record. The ancillary
MVE notes here are earlier proposals, not the frozen or registered protocol.
Do not overwrite the tagged kit with these copies. Registration preparation is
deferred; public release and external deposits remain subject to permission.

## Related Work Review of 25 October

Reviewed Pavlenko et al.,
[Towards an AI Software Factory for Data Systems, v1](https://arxiv.org/html/2609.36323v1),
submitted 28 September 2026 and retrieved 25 October 2026. The
[arXiv metadata](https://arxiv.org/abs/2609.36323v1) supplies the 26-author
bibliographic record. The manuscript and reusable bibliography now include it
as `pavlenko2026factory`.

* The paper is directly relevant to feedback starvation and reflective
   delegation. Hotspan selects evidence-backed optimisation targets; Darwin's
   agents use test and runtime feedback to generate, refine and select
   hypotheses. This is bounded steering against measurable objectives in
   existing systems, not evidence of autonomous product selection.
* Its World Model separates raw evidence from rebuildable views and compact,
   provenance-linked retrieval. Updates are reviewed. This provides an
   alternative to expecting every session to read an accumulating log, not a
   tested remedy for this case's learning evaporation. The fine-tuning evidence
   is an early circle-packing demonstration, not general proof of durable
   engineering judgement.
* The reported threefold productivity estimate concerns application-work PRs
   per engineer-hour, excluding 57% of team time spent on infrastructure and
   repository onboarding. Output enters engineering review queues. The 13.8%
   mean performance gain applies to the best-performing 20 of 45 OSS systems.
   Neither number is a controlled estimate of maintainability or end-to-end
   delivery effectiveness.
* The token-efficiency comparator is inconsistent within v1: the introduction
   and Section 2.3 associate 22x with OpenEvolve, whereas Section 4 reports 22x
   against MAP-Elites and 17x against OpenEvolve. The manuscript does not import
   that multiplier or attempt to resolve the discrepancy.
* The novelty wording now concerns the effect of scheduled consolidation
   between feature additions, not the invention of automated improvement or
   agent reflection. The reviewed paper does not isolate that intervention or
   evaluate an unforeseen change request. This focused review does not establish
   an exhaustive literature search.

The experiment's hypotheses, thresholds, budgets and tagged materials are
unchanged. Reported findings are attributed to the source authors; source
checking is not independent replication or the manuscript author's pending
verification of research statistics.

## Files

| File | Purpose |
| --- | --- |
| `main.tex` | Paper source. The bibliography is embedded, so it compiles on arXiv without BibTeX. |
| `fig-log-growth.png` | Figure 1: words and hedging phrases appended to the project log per day (400 dpi). |
| `fig-causal-loop.png` | Figure 2: the reinforcing loop and the feedback-first intervention (400 dpi). |
| `references.bib` | The same 97 references as BibTeX, for reuse or a later switch to `\bibliography{}`; both bibliographies are ordered by key. |
| `anc/log_metrics.py` | Recomputes the log measures in Appendix A from `docs/reference/log.md` at commit `29c6b51`; `--json` writes the per-day data. |
| `anc/log_daily.json` | Per-day entries, words and hedging phrases (output of `log_metrics.py --json`). |
| `anc/make_figures.py` | Redraws both figures from `anc/log_daily.json`. |
| `anc/check_paper.py` | Reports the current approximate body count and checks citations, labels, environments, braces, inline comments and abstract length. Historical comparison is optional. |
| `anc/test_paper_tooling.py` | Isolated stdlib regressions for the paper checker and exported TCR helper. |
| `anc/protocol_checks.py` | Historical check of rank-test floors and the earlier eight-feature A/B proposal; it does not check the current ten-feature A/B/C design. |
| `anc/repo_history_metrics.py` | Measures path-class line churn at the pinned commit, separating literal merges from PR-numbered first-parent integrations. |
| `anc/repo_history_metrics.out.txt` | Saved history measurement, including definitions, commands and limitations. |
| `anc/mve-feature-consolidation-harness/` | Earlier MVE proposal notes: divergence log, experiment design, hypotheses and plan. Not the separate tagged study kit. |

arXiv publishes everything under `anc/` as ancillary files.

### Tooling export provenance

The minimal [TCR helper](anc/mve-feature-consolidation-harness/tcr) is adapted
from private `jmservera/ama-thought-mve`, `skeleton/tcr`, commit
`20e7f97c5c162cffd0f771ce501e146081912edc`, Git blob
`aa35d75d77ec13aab2384481917e66c243e8ba64`, using the source supplied by the
parent. The adaptation replaces the shared log with a cleaned-up per-invocation
log and includes test, staging and commit failures in the rollback path, with
stage-specific diagnostics and nonzero status. It retains `make -s test`, the
`tcr:` commit prefix and the untracked `reports/` exclusion. This is not the
full registered study kit, and no fix to the private source is claimed.

The helper is destructive: use it only in an explicitly disposable worktree,
never in AMA or the private study repository. See its
[usage and rollback limits](anc/mve-feature-consolidation-harness/experiment-design.md#5-the-harness-consolidation-step-arm-b).
The checker runs without Git or repository metadata, including source archives;
when the old object is missing it reports `HISTORICAL_COMPARISON UNAVAILABLE`
and still validates the current paper. Existing historical-comparison output
is retained when that source is available.

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
* The switch `\resultsfalse` near the top keeps the study status note visible. Set `\resultstrue` only after the registered runs and checked analysis are complete.

## What changed in draft v2

* New thesis. Feature accumulation degrades software, and agents speed this up through compounding errors and output that exceeds review capacity.
* New background. It covers software evolution (Lehman, Parnas, Eick, Cunningham, Fowler, Tornhill and Borg, Besker) and recent studies of agent-driven decay. Counter-evidence is included (Echoes of AI, SWE-Maintain, and the Herraiz caveat on Lehman's laws).
* New Table 4, which maps the base rate and the two accelerants to the five mechanisms.
* New Section 7.1, *A consolidation harness*: after every feature the loop stops, then reviews and refactors through test && commit || revert before the next feature starts.
* New Section 8, *Testing the harness*. It covers hypotheses H1–H7, three arms (no consolidation, consolidation, placebo review-only), suites, measures, analysis and bias controls.
* New Appendix B with the consolidation prompt.
* New sources, including Lanzetta (two articles) and Lamanna (*Changing how we build*).

## Original draft v3 changes

These notes record the earlier revision, before the author clarification below.
Its method attribution and experimental choices are superseded where stated.

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

## Author clarification of 25 October

* Corrected the method: the author supplied observations, explanations and the
   consolidation remedy; GitHub Copilot organised and named patterns. This was
   not systematic entry-by-entry qualitative coding. Microsoft 365 Copilot
   summarised and found sources; Copilot Cowork generated slides.
* Recorded the author-confirmed HVE snapshot, programme name, historical model
   roles and selective specification review. Replaced daily MVP use with
   intermittent use and distinguished product-use feedback from approvals and
   technical oversight.
* Qualified learning loss and noted documentation growth before the backlog
   loop. Generalised partner descriptions; permission for the peer observation
   and external publication remains pending.
* Added the account-wide rolling 28-day dashboard totals with their limits:
   USD 1,809 price-list consumption value, not an invoice or AMA-only cost.
* Recorded the selected S1 design: A/B/C, ten features plus CR1, four independent
   runs per arm; Sonnet 5.5, medium effort and CLI 1.0.103. Local execution has
   residual access risk, not container isolation. S2 library lending is deferred.
* Checked the accepted arithmetic: 212 first-pass sessions and 89 agent-hours;
   262 sessions and 109 agent-hours including the pilot. The combined ceiling
   is 2,500 AI credits. Its relation to the separate $500 budget is unverified.
* Kept HIR extraction prospective: Cowork extraction followed by author checks
   and adjudication. Telemetry coverage is unverified; missing events do not
   establish zero interventions. Independent suite review, research-statistic
   checks, figure verification and reviewer participation remain TODOs.
* Added HG-DAgger and ThriftyDAgger as intervention-measurement precedents,
   with explicit HIR and demand-rate formulas. The cycle denominator is a
   study-specific adaptation, not a universal standard; incidence, event
   frequency and human effort remain distinct.
* Reframed the abstract, research questions and discussion around whether an
   additional agent can perform reflection and course correction. The current
   consolidation experiment is a bounded first test, not a test of unrestricted
   steering or proof that reflective work is exclusively human. Tagged study
   materials, hypotheses and thresholds are unchanged.
* Preserved earlier protocol proposals and kept `\resultsfalse`. A Git tag is
   not registration, and earlier started runs cannot be retrospectively
   described as preregistered.

Run the saved checks from the repository root, using its existing environment:

```bash
.venv/bin/python docs/capstone/thought-leadership/everything-but-the-software/anc/check_paper.py
.venv/bin/python -B -m unittest discover -s docs/capstone/thought-leadership/everything-but-the-software/anc -p test_paper_tooling.py -v
.venv/bin/python docs/capstone/thought-leadership/everything-but-the-software/anc/repo_history_metrics.py
```

The historical `protocol_checks.py --check-documents` mode expects the earlier
proposal wording across the manuscript and local protocol copies. It is not a
current-revision agreement check. Its legacy arithmetic remains historical;
the accepted A/B/C design has 120 feature, 80 post-feature and 12 CR sessions:
`(120 * 30 + 80 * 15 + 12 * 45) / 60 = 89` agent-hours, excluding the pilot.

## Before you submit

1. Resolve every `TODO(author)` comment in `main.tex` (search for `TODO`):
    * verify research statistics against original papers and the log-growth figure against daily data;
    * retain source metadata, dashboard evidence and original instruction messages where available;
    * recover historical runtime/build identifiers without inventing unexposed versions;
    * obtain permissions and confirm partner anonymisation without naming either partner or its staff;
    * verify the exact tagged protocol, suite, analysis and prior-run chronology before registration;
    * complete registration before fresh confirmatory runs and retain the real date and URL;
    * complete independent suite review, reviewer recruitment and HIR coverage checks;
    * reconcile credit and monetary limits, calibration choices and analysis rules;
    * write results and update acknowledgements only after the corresponding work occurs.
2. Treat the local MVE copies as historical proposals. Archive the exact authorised registered study materials separately, preserving originals and excluding credentials, DLP sidecars and unapproved internal content.
3. Rewrite in your own voice where needed. The rubric allows AI drafting, but the insight, evidence and recommendation must be yours.
4. Get the internal approvals Microsoft requires for external publication.
5. Compile, then read the PDF end to end. Check tables and figures for overflow.
6. arXiv publishes the source files, comments included. Before you upload, strip the comments (for example with `arxiv_latex_cleaner`) and leave out `README.md`.

## Running the experiment with HVE Core

Continue from the separately tagged private study kit, not from the earlier
ancillary proposal copies. Verify that the tagged record matches the accepted
design and analysis before registration. Preserve every earlier run and its
original labels and timestamps; start fresh confirmatory runs only after
registration. Do not change frozen materials in place or silently replace the
original design after seeing results.

## arXiv notes (checked 24 Oct 2026)

* Primary category: cs.SE. Optional cross-lists: cs.HC, cs.AI.
* Since 31 Oct 2025, arXiv CS accepts review articles and position papers only after peer-review acceptance. Research papers are not affected, so keep the paper framed as a data-backed case study with a method, data and threats to validity, not as an opinion piece.
* Since 21 Jan 2026, a first-time submitter in cs.SE needs either prior authorship in the domain or a personal endorsement from an established arXiv cs.SE author.
* arXiv asks authors to report significant use of generative AI. AI tools cannot be authors, and authors are responsible for all content.
* The abstract field limit is 1,920 characters. The conservative source count
   after the framing revision is 1,619, including LaTeX syntax and normalised whitespace.
