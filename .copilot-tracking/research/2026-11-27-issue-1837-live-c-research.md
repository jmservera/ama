# Issue 1837 research (run c), 2026-11-27

Refs #1837. Synthetic demo, desktop only. Base `337d3999d5`.

## Status

Main carries the fix (JSON post with `X-ZF-CSRF`, standalone forms script). Run b left one open item: `checks.nomination_browser_check` fails at its `nomination_review` call with a 5 s timeout, cause undiagnosed.

## Angle for this run

1. Diagnose that timeout. If it is a real defect, fix it with a failing-first test (full tier applies to src changes).
2. Probe the deployed demo read-only (`ca-cutover-test-demo-api`) to show whether the standalone forms and routes are served. Live writes stay withheld (irreversible records in the shared demo).

Planning readiness: Ready.
