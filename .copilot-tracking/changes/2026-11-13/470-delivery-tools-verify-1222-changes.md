# Changes: tools/ verification (Refs #470, #1204, #1297)

Base 74a93a137a983e0a87418e3321a6847ba9bcd278. No edits to tools/, src/ or docs/. Only .copilot-tracking artifacts added.
Environment: scratch venv /tmp/venv-470tools (system site packages, editable core/agents/api from this worktree, python-pptx and pillow added for rename tests), PYTHONDONTWRITEBYTECODE=1, empty PYTHONPATH. Logs in /tmp/tools-verify-1222. Exit codes are the direct producer `$?`.

| Module | Tests | Skips | Seconds | Exit | Log sha256 |
| --- | --- | --- | --- | --- | --- |
| test_ama_worker_watch.py | 6 | 0 | 0.38 | 0 | d1a4286a886325e07204a81cb055adee99e65bcc60e031b12853c5970c698c70 |
| test_backlog_sync.py | 17 | 0 | 0.15 | 0 | c9fb899dcc140ec0bcdfe85c6ae36eafda8d002ba14d187976c641ebb3d61abd |
| test_check_demo_feedback.py | 88 | 0 | 2.87 | 0 | 7c1190592aecf92cb9b4db78ee40af73113478d20becc2aa1645e1779a784fab |
| test_check_design_trace.py | 11 | 0 | 0.19 | 0 | afe849eab04f1aa142b9abdb1bf4b62ec86e6e40da35af13141300cb010263c1 |
| test_ci_affected.py | 19 | 0 | 0.56 | 0 | d78969b1f8b8e2f04c358aefcb44860eedfa866ff6aa45ba4f7265f7b2c781d5 |
| test_climate_paired_blocker.py | 3 | 0 | 0.13 | 0 | d454b1f55ac3c5a6a321eebe1a1c1b3b155c2826d0a914ac9bc23d10e9cc7ef0 |
| test_climate_paired_bounds.py | 31 | 0 | 1.47 | 0 | 8015701b6dfdd576b207a979966639a17de972d724a2751b69c32520fe516c24 |
| test_climate_station_bounds.py | 8 | 0 | 0.25 | 0 | a27e783334753319469d6ad2c4e3e0189952f603628e2d3530bae23e6788fb54 |
| test_install_actionlint.py | 12 | 0 | 0.26 | 0 | b0301a12b2ffa4185176e5c7f00afdc46fdd350a0cb05a4d22ded90b4b4560a0 |
| test_rpi_checks.py | 103 | 0 | 58.93 | 0 | bc1a1a323f404ebf08999770a37a16b015ff0789e6100f887b069903e7fd384b |
| test_rpi_phase_witness.py | 33 | 0 | 7.93 | 0 | 563044206e9190138387ee14c25541339aec510d75f692ebbd56ff8e2812dfde |
| test_tracking_retention.py (pytest, no cache) | 37 | 0 | 5.06 | 0 | f791c89277aef9e687387c7148ebc5c7451a669ab0cd239ab143d356c19ad2ea |
| rename-zava-tests.py | 25 | 0 | 1.79 | 0 | 7a407c5dc4673a4f091a6fe44ca78010dfe2e7b7731ffac96d2d4a8dbc76d493 |

Total 393 tests, 0 skips, all exit 0 in the final run.

## Divergence recorded

* First rename-zava-tests.py run exited 1 (errors=7, log sha256 914b67e2383a221efa36090d18063fe0bfe1ecaf56e55d6f3dedeb4607701b74): ModuleNotFoundError for pptx (4) and PIL (3). This was an environment gap in the scratch venv, not a repository defect. After pip installing python-pptx and pillow into the scratch venv only, the rerun passed 25/25.
* test_rpi_checks.py prints nested "FAILED required group" lines; these are expected negative-path fixture output inside passing tests (Ran 103, OK).
* test_tracking_retention.py is pytest style; unittest would discover zero tests, so pytest was used (critique requirement).

## Side effects

* git status --short --ignored identical before and after (baseline compared); no bytecode, caches or state files in the worktree.
* /tmp/ama-rpi-heavy.lock mtime unchanged (1794432439) before and after; lock tests are redirected to temp paths.
* No network use beyond the pip install of python-pptx and pillow into the scratch venv; no Docker, browsers, cloud or GitHub writes.
