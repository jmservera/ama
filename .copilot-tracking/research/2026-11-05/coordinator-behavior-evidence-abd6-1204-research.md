<!-- markdownlint-disable-file -->
# Research: full behavior evidence continuation at abd6b3f5f (issue 1204, pass 7)

Written 2026-11-05 in original session 6e276cf2 before any new evidence file other than this research. Disposition: executed (bounded, inline). Not a source correction.

## Frozen identity

* HEAD abd6b3f5fea1c3618f79feb813555b866bccd60d, tree 93c4137d24e3b3602365f4f294f72702c295b778, source blob acefb44a4d254ede6d86413343127b763dec42cb (must stay byte-unchanged), main bb3a3b03cb unchanged, worktree clean.
* Coordinator-supplied targeted static closure (session file hve-static-1204-abd6-targeted-closure.md): S01 and S02 Closed, targeted static Pass; initial Revise report preserved. Not repeated here.

## Reuse eligibility (hve-builder-tester step 3)

Prior behavior evidence (pass 5, six text scenarios plus negative control at 11cfb) is Pass but the requirement mapping and scenario set change (S01 and S02 add contract and cases), and it was lead-designed. Equivalence fails, so this is a FULL run. Prior evidence is historical and unreused.

## Mechanism findings (read-only probes)

* The registered agent `ama-backlog-delivery-coordinator` activates natively under the CLI: `copilot --agent ama-backlog-delivery-coordinator --model auto --available-tools view grep glob --no-ask-user --disable-builtin-mcps --max-ai-credits 30 -s -p ...` run from an isolated throwaway git repo containing a byte-identical copy of the source (sha256 2bd539c3...fa05f equals `git show HEAD:` of the target). Probe exit 0; the agent named its role and listed only view, rg, glob and a parallel wrapper; share transcript records "Auto selected GPT-6 Luna since the task has low complexity." Probe files: /tmp/h1204/native-probe-share.md, native-probe-out.txt.
* Containment: enforced by --available-tools (no shell, no edit, no network tools), --disable-builtin-mcps, --no-ask-user, a credit cap, and an isolated cwd outside the worktree; no global settings are changed (autoTier and model config remain unset). Native activation does not execute shell, merge, cleanup or Graph actions; those stay text decisions. The target's own tools frontmatter is opaque and was not inspected or graded.
* Intended profile: Automatic (`--model auto`). autoTier is unset, so the tier is unknown; the Auto router selects a model per run and its choice is recorded from the share transcript. Canonical High/Medium/Low labels are not imposed. Not a proxy for Automatic; it is native fidelity with read-only enforced containment, but text-only (the agent cannot exercise its write tools).
* Generic design and grading stages use harness defaults (task subagent with no model override; the lead and subagent default is Sonnet 5.5); no model is pinned or invented.
* Current live schedules (coordinator-supplied, not read by this worker): delivery 15 (10 min) and cleanup 8 (hourly); stale ids are not authority. Not retested as runtime.

## Coverage required

Existing: full classification and no idle on unknown or unreviewed closure, blocked lane plus independent work, approval routing, one question at a time, actual session provenance, stacks and worker publication ban, gates, retention-safe cleanup, 20-PR drain thresholds, no double count of continuations, full versus focused tier and single heavy-lock holder, ignored-evidence provenance. New: exited worker with unpublished candidate still counts (eight assignments, not tmux); proved published-only dependency-gated pause releases the slot while PR and parent stay monitored; unknown upstream cannot release; missing applicable HVE evidence blocks instruction publication though focused tests pass; no proxy or simulation upgrade to native or stronger-profile acceptance; HVE not applicable for unrelated non-behavior changes. Plus a negative control on an intentionally broken isolated copy.

## Limits carried

Text-only native runs, single run per scenario, router model may vary, tier unknown, scenarios synthetic. Normalized pass 5 transcripts are not byte-exact raw copies. No whole HVE or issue Pass from this pass alone.

## Planning Readiness

Ready.
