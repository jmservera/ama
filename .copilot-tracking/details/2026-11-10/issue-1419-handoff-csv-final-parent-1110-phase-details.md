<!-- markdownlint-disable-file -->
# Phase details: final-parent revalidation (#1419)

* P1 commands: `git diff 37828a41 HEAD --stat -- src`; `git ls-tree HEAD <server.py app.js ops.js>`; `sha256sum` of those; `python -c "import zava_forward.api.server ..."` to print file origins.
* P2 commands run from src/api with /home/azureuser/.venvs/issue1419/bin/python.
* P3 command per module: `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p "<module>.py"`. Record test count, skips, exit code. A skipped browser case is never reported as a pass.
* P4: `ZF_BROWSER_TESTS=1` with the same discover command for test_unaccepted_handoff_download_ui and test_handoff_read_guidance; the modules take `/tmp/ama-rpi-heavy.lock` non-blocking and SkipTest if busy.
* P5: review of the actual changed files is the merge's test stub plus unchanged owned hunks; guidelines source is refetched before review.
* Stop conditions: unexpected failure => record exactly, amend plan only for a tightly coupled defect, else route to Root.
