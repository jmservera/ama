<!-- markdownlint-disable-file -->
# Contained behavior run (2026-11-05, pass 5)

* Profile mechanism: child `copilot --agent hve-core-all:hve-artifact-tester --model auto --available-tools view grep glob --no-ask-user --disable-builtin-mcps --max-ai-credits 60 -s -p ...` with `--share` transcripts. Share transcripts record "Auto selected GPT-6 Luna" for executors and grader. Tier unresolved (autoTier unset); the Auto router may pick other models on other runs.
* Containment: read-only tools; shell, merge, push and cleanup were text decisions only; synthetic fixtures; no live data.
* Roles: scenarios and rubric authored by the lead before execution; executor and grader were separate child runs; the lead did not grade.
* Results: real instruction T1-T6 all Pass per the independent grader; negative control (candidate-counting sentence removed, scratch copy in /tmp) answered "Yes" for T3 and was graded Fail as expected.
* Limits: one run per case, so no variance estimate; the executor sees only text and cannot exercise tools; earlier proxy runs are historical and not re-graded here; Auto profile is faithful to the coordinator launch profile only as far as the router choice is observable per run.
* Traces: executor-real-trace.txt, executor-negctl-trace.txt, executor-*-share.md, profile-probe-share.md, grader-output.txt, grader-share.md.

Note: raw transcripts had trailing whitespace stripped only (git diff --check); content otherwise verbatim.
