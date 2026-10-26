# Correction 6: hosted review findings on c662fae2 (#462)

Date: 2026-10-26. Branch feat/resident-azure-showcase-462. Gate on c662fae2 passed (receipt aca26b26...) before this change; this commit invalidates it, so the coordinator must rerun.

## Research and plan (read before editing)
* Read PR 463 review threads 4381849672 (public class=0 grant), 4382387930 (concurrent revoke), 4382387982 (README redirect 0644) and the demo.js focus finding (no thread id was returned by the comments API).
* Plan: lock revoke, extend the public-grant query, document umask 077 subshell, focus first revealed h2 with a live-region announcement.

## Critique and review (disclosed)
* No independent subagent critique or review was run for this small correction; the checks below are self-recorded. Independent review is left to the coordinator and hosted review.

## Changes
* resident_showcase.py: threading.Lock around SessionCodec.revoke; two-thread regression test.
* resident_showcase_sql.py: public grants at class 0 other than CONNECT are refused; test added.
* README and verifier docstring: `(umask 077; ... > owner-only-file)`. The helper writes only to stdout, so the shell creates the file; the documented command now guarantees 0600.
* demo.js: after sign-in, focus the first content heading (tabindex -1) and announce "You are signed in. Your progress is shown below."; static contract test added. Not browser-tested here.

## Results
* core: mypy strict, ruff check and format clean; resident tests 70 OK (13 skipped). api resident 50 OK. infra 445 OK. node --check demo.js OK.
* Live SQL semantics of the extended query remain unproven (fake cursor only).
