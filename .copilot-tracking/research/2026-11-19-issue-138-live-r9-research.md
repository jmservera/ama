# Issue 138 live r9 research (2026-11-19)

Refs #138. Read-only recheck against [r8](../../docs/reference/research/issue-138-live-r8-2026-11-19.md).
Observed 2026-11-19: repository variables only GH_AW_DEFAULT_MAX_DAILY_AI_CREDITS (no AZURE_*);
environments copilot, dev-plan, pilot-plan, test-plan each with 0 protection rules; 0 self-hosted runners;
0 src-deploy.yml runs. Every remaining criterion needs owner settings (Entra federation, environment
reviewers, runner) or a pushed workflow run, which this worker may not perform. Disposition: stop, no source change.
