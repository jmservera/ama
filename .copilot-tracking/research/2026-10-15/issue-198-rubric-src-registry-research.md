# Research: issue 198 rubric registry for src counting

* Disposition: executed. Planning readiness: Ready.
* Evidence: issue #198 and its comment, ADR 0006 (Rubric counting), `.github/rubric/artifacts.json`, `scripts/prepare.py` glob rules, `test_prepare.py`.
* Finding: `src/**/*` is already in `solution-code`; `mvp/data/**` and `mvp/web/vendor/**` are excluded but no `src/` excludes exist.
* Finding: `prepare.glob_match` treats `**/` as zero or more directories, so `src/**/data/**` matches `src/core/data/x`.
* Baseline: 47/100 at commit fa730d6 (latest.json); solution-code criteria A1=4, A3=5, A4=5, A5=3, A6=3, A7=4, B6=4.
* Baseline test state: 19 pre-existing failures (gate, scorecard adapter, 8 prototype-path cases, 1 drop case); identical with and without this change.
* Owner decisions: build in src/, temporary dip accepted, no rubric_version bump, mvp globs stay until #201/#202.
