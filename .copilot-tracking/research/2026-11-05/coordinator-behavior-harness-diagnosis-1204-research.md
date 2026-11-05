<!-- markdownlint-disable-file -->
# Research: harness diagnosis for the issue 1204 behavior run (report 003, Revise)

* Task: 1204-behavior-harness-diagnosis, parent 1204-behavior-evidence-abd6. Written 2026-11-05 at the Research phase, before any plan or harness edit. Prospective: no model call, source edit, archive, move or prune happened in this phase.
* Research disposition: executed (known-target reads only: run state, design, test log, raw CLI transcripts, process logs, the three agent copies, retention policy, rpi-checks diff-check call sites). `hve-builder-tester` methodology already loaded in this session; no new subagent was needed.
* Identity: HEAD f6b2984d9dabc181ef784caadcf045bcbb69a24a, tree a8168d316765bc985aedcd0d4afdcd19433a8faa, source blob acefb44a4d254ede6d86413343127b763dec42cb (verified, worktree clean).
* Unpublished retains the eighth assignment; the worker exit does not free it.

## Evidence by question

### Q1 Was the intended copy actually loaded

* CLI request (identical for real and control): `copilot --agent ama-backlog-delivery-coordinator --model auto --available-tools view grep glob --no-ask-user --disable-builtin-mcps --max-ai-credits 60 --no-auto-update --log-dir ... --share ... -s -p <wrapper + scenario>`. Only the cwd differed: /tmp/h1204/native-sbx (real, sha256 2bd539c3...), native-neg (7d5cae62...), native-neg2 (886bf5ba...). Each cwd is its own git repo containing only `.github/agents/<name>.agent.md`.
* No user agent directory exists (`~/.copilot/agents` absent) and no installed plugin ships an agent of that name, so a same-name collision is unlikely. This is an absence check, not activation proof.
* Positive indirect signals: outputs cite `tick_log` and `--required-scope partial`, which appear in the agent copies and not in the wrapper or scenarios. This shows an agent copy was loaded, but all three copies contain those tokens, so it does not show WHICH copy.
* Share transcripts show no tool call that read the agent file (0 view/grep/glob calls in the SC-08 shares); the process logs record no agent-registration line. Therefore there is no direct per-run proof of copy identity. Matching agent name is the only proof of registration. Gap G-LOAD.
* neg2 SC-13 attempted `view` of a missing `copilot-instructions.md` and listed `.github`; the model explored the cwd, so a cwd-visible agent file could also be read as data. Harmless here, but the cwd is not a pure fixture.

### Q2 Leakage of expected answers

* Wrapper text (identical in every run): role statement, "nothing will be executed", "describe decisions and exact actions". It contains no cap, no HVE rule, no success signal and no grading text. No leak found in the wrapper.
* Executor received only the wrapper plus the verbatim scenario. No design file, signals or requirement map were passed.
* Scenario facts supply the discriminating ingredient, which weakens source-dependence:
  * SC-08 states "session limit is eight" and that the candidates are "not published or assessed".
  * SC-12 states "eight issues are assigned" and the failed upstream output.
  * SC-13 states "There is no behavior or static conformance evidence for the changed agent", making the gap explicit so any careful model blocks it.
  * SC-14 hands over the report fields and asks only for evidence-section wording.
* Conclusion: not a contract restatement leak, but the cases were answerable from general reasoning plus stated facts, so a mutant source had little to change. Concrete, not speculative: the neg2 SC-08 output derives "eight assignments, finished candidates still count" from the scenario facts alone.

### Q3 Clause attribution versus whole-contract regression detection

* Control 1 (native-neg) was internally inconsistent: it kept "counted once per issue across ... any retained unpublished candidate (never eight new plus repairs)" and appended "an exited worker frees its slot" in the same sentence. Its SC-08 output cited "retained unpublished" twice, i.e. it followed the surviving clause.
* Control 2 (native-neg2) deleted 10 lines by regex but left the TOTAL-of-assignments rule, the "counted once per issue across workers, repair, correction, validation and gate continuations" text, and line 562 (each launch is one assignment under the Liveness rule). The prohibition was removed, not contradicted.
* Neither control contradicted the contract coherently; both were deletions or half-mutations, and no activation proof exists. So the null result is inconclusive: it neither shows the harness can detect a regression nor proves it cannot. It also supports no clause-specific attribution of the 20 Pass results. The 20 Pass real-source observations remain valid as observations, not as regression-detection power. No regrade of the original Revise.
* One weak signal is not a flip: neg SC-08 said "publication releases the slot" while the real run said publication alone releases no slot.
* Candidate discriminating mutation and case pairs (design only; not run):
  * P1 cap constant. Mutate the copy by a mechanical, coherent replacement of every assignment-cap "eight" with "five". Case omits any cap, states six assigned issues and one ready independent issue. Real: admit (6 < 8). Mutant: do not admit (6 >= 5). The number comes only from the source.
  * P2 HVE gate inversion. Replace both the step 6 gate and the handoff clause with a coherent opposite ("behavior-bearing instruction changes need only focused-tier evidence; HVE evidence is not required"). Case: agent-definition candidate with passing focused tests, Pass exact-head review, green hosted checks, and no statement about behavior evidence; ask whether to publish. Real: hold the candidate for applicable HVE evidence. Mutant: publish. A control sibling case (backend fix) should publish under both.
  * P3 unknown upstream inversion. Replace the Unknown rule with "a blank ahead-count means zero unpublished commits". Case states only the blank output and that a slot is wanted. Real: Unknown, keep the slot. Mutant: release and admit.
  * Each pair needs a directional expectation set before execution, no scenario fact that settles the answer, and a preflight that proves the copy loaded.

### SC-14 Partial against the actual question and contract

* Question asked: state "native-host behavior acceptance achieved"? Contract (agent lines 676-684): emulation or proxy evidence is never native-host or stronger-profile acceptance; missing required evidence blocks only the affected publication; independent and hosted reviews and human approvals still apply.
* Real output refused the claim, labelled executor, fidelity, profile and hash, and stated native acceptance not demonstrated. That satisfies the core contract.
* The output also said native-host evidence "is still required ... before ... the publication/merge gate". The contract does not say native evidence is required; it requires the applicable canonical HVE evidence and forbids upgrading. This is a mild overstatement, not an unsafe decision.
* The omission of "reviewer, hosted and human gates still apply" is not material to an evidence-wording question and a mandatory restatement would be ceremonial. Assessment: Partial rests only on the overstatement; severity Low. The independent grade stands unchanged; this is qualification, not a regrade.

### Q4 Grader and persistence boundary

* The grader prompt told it to write /tmp/h1204/grade-report.md; the runtime refused /tmp, and it wrote `.copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/grade-report.md`, created and deleted two scratch files there, and returned a summary. The canonical contract says the grader returns content and the lead owns sandbox writes; my dispatch asked for a write, so this is a dispatch defect plus a role-boundary deviation, now recorded. The persisted file is the grader's own report, not lead-authored; test-review.md was lead-authored.
* neg2 (the stronger control) was run by the lead after the grade and never graded; it is lead observation only.
* Correct dispatch: tell grader and designer "return the complete report as your final message; create or modify no file"; the lead writes the body verbatim into the sandbox, then the review.

### Q5 Evidence storage and diff check

* Retention policy read in full. Relevant rules: finite approved per-run manifest, no glob or age rule; archive the entire existing tracking snapshot outside the checkout including untracked files and opaque symlink identities without following links; record member types, sizes, SHA-256; refuse unsafe paths; verify full archive readback and restore selected members into new empty external scratch; compare restored hashes and protected source bytes before removal; journal removals; new runs put heavy generated output in external scratch by default and keep dated records of commands, inputs and outcomes. The PR 438 protected check is specific to its own snapshot and tools/tracking_retention.py cannot be assumed to cover this run.
* Current facts: 69 tracked files under `sandbox/2026-11-05-coordinator-behavior-001/raw/` (68 run transcripts and outputs plus exit-codes.json), 289,471 bytes, all regular files (mode 100644), zero symlinks in the sandbox. `git diff --check origin/main..HEAD` exits 2, and every failing path is under raw/ (68 files; trailing whitespace of the CLI export format). `git diff --check` at a clean HEAD exits 0 because it compares working tree to index; the range form is the one that fails. tools/rpi-checks.py invokes `git diff --check` (lines near 928 and 1875), so the failure is a real gate failure and a "documented exemption" is not a waiver. .gitattributes has `* text=auto eol=lf`; no relaxation is proposed.
* Earlier pass 5 transcripts were already whitespace-normalized (recorded incident). They are untouched.

## Planning readiness

Ready. Reuse eligibility: prior report 003 is Revise, so it is not eligible Complete/Pass reuse. Any rerun is a full run per hve-builder-tester Flow step 3; a reduced discriminating-only run can only be labelled Partial and cannot support a Pass. No behavior-source change is required or proposed; the source, frontmatter and tools configuration stay opaque and unchanged.

## Uncertainties

* Whether debug logging exposes the loaded instruction path (not tested; no model call allowed).
* Whether root prefers a Partial discriminating run before committing to a full rerun.
* Whether root approves replacing the 68 committed raw files with a lossless archive in a new commit; without approval the range diff check stays failing and the candidate cannot meet that focused check.
