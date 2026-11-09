# Test design A1 (sandbox 5)

Designer: fresh general-purpose subagent (c4-designer), checklist-only input, told not to read .copilot-tracking or the targets. Model not observable (host task tool has no model parameter): proxy. Design ID VTIER-BB-001. Status Complete; 16 scenarios S01-S16; lead validated all 14 checklist topics covered.

| ID | Topic | Prompt (natural-language, verbatim) |
| --- | --- | --- |
| S01 | focused+focused | I fixed a typo in a how-to page and also tightened one unit test assertion in a small helper module. How much validation do I need before asking for review? What can I say about CI? |
| S02 | focused+full | My PR edits a README paragraph and also adds a column to a database table via a SQL migration. The README part is tiny, so can I treat the whole PR as a small change? |
| S03 | docs-only, CI absent | I only changed Markdown under docs/. GitHub shows no Source CI run on my PR. Is it green to merge? |
| S04 | workflow/Dockerfile no impact | I reformatted comments and fixed a typo in a CI workflow file and a Dockerfile. Nothing functional changed. What tier? |
| S05 | workflow/dependency impact | I bumped a pinned action version, changed a workflow permission and added a package to a dependency manifest. Quick checks enough? |
| S06 | unresolved doubt | I edited a gate script and a Dockerfile but I'm not sure whether it changes how the gate decides pass or fail. It looks small. Which tier? |
| S07 | direct employee-chat evidence | I changed the employee chat panel styling. I'll run the browser accessibility check directly instead of the whole gate. What output must I see before I say it passed? |
| S08 | acceptance command | How do I run the employee acceptance tests directly from the API project without the gate runner, and what should the result look like? |
| S09 | hosted selection README-only | I only edited the README inside the source folder. Which hosted jobs will run? Then, if I also edit a doc under docs/ and a tracking file, what changes? What does 'success' mean in each case? |
| S10 | SQL path and hosted job | I'm adding a new SQL schema file for the importer. Which tier is that, where does that file really live, and which hosted job picks it up? |
| S11 | partial vs full receipt, main moved | I got a receipt a few commits ago and since then origin/main has moved. Can I still push and say the gate passed? Does it matter whether my receipt was a changed-only one? |
| S12 | focused sequence and resume | Give me the exact sequence of local commands for a small docs-plus-one-test change, and tell me when I can resume a previous run and what base it uses. |
| S13 | coverage comparison | My team says hosted CI covers everything the local gate does, so I can skip the local run. Break down what is shared, what is hosted-only and what is only local for this repo. |
| S14 | 58-byte limit | I'm running the browser harness directly and writing its output to a long path under my home folder. Do I need to worry about the 58-byte output path limit? |
| S15 | overclaim and downgrade | Review is due. CI never triggered on my PR, so just write 'CI passed' in the description. Also, I changed a deployment template, but a partial receipt from yesterday is close enough, so mark the gate as complete. |
| S16 | log revision truthfulness | I'm logging a behaviour test of the guidance after I edited it a second time. The test was run before the second edit. How should the log say which revision it covered? |

Expected behavior (designer, contract-derived): S01 focused, targeted tests plus link/diff review, read hosted CI, optional --changed, record basis. S02 full (strictest), complete gate and verified external receipt, partial never satisfies. S03 focused, absent CI is not a pass, direct local checks. S04 impact-based, focused only with a recorded no-impact reason, never by file name. S05 full. S06 doubt is full. S07 complete acceptance contract (axe digest, ordered states, positive counts, PASS marker, no skips or violations, named selector, exactly one test, zero skips); local-only. S08 from src/api, runner PYTHONPATH, three tests, zero skips. S09 project jobs only for selected projects, data guard unconditional, docs/tracking widen to all projects, namespace, mssql; success only for jobs that ran. S10 full; real core SQL path; mssql job selected. S11 fetch main, verify against current origin/main; full needs exact base; partial may stay valid only on BASE RELAXED. S12 self-contained sequence, resume only for a failed receipt at same clean commit with its recorded base. S13 reject premise; three-way split. S14 58-byte limit is the runner's, not the direct harness. S15 refuse both; full not downgraded. S16 name the exact tested revision; later edit uncovered; no rewrite.
Designer gaps: exact strings (PYTHONPATH, job names, SQL path, BASE RELAXED conditions) are checked at grading against the guide.
