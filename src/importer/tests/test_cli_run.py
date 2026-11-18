from __future__ import annotations

import contextlib
import io
import json
import unittest

from zava_forward.importer.__main__ import main as importer_main
from zava_forward.importer.version import __version__


class ImporterBoundedRunTests(unittest.TestCase):
    def _base_env(self) -> dict[str, str]:
        return {
            "IMPORT_QUEUE": "import-jobs",
            "QUEUE_ENDPOINT": "https://stforwarddev.queue.core.windows.net",
            "BLOB_ENDPOINT": "https://stforwarddev.blob.core.windows.net",
            "ZF_STORE": "mssql",
            "SQL_SERVER": "sql-forward-dev.database.windows.net",
            "SQL_DATABASE": "sqldb-forward-dev",
        }

    def test_no_args_prints_version_for_container_smoke_probe(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            rc = importer_main([], env={})
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.getvalue().strip(), f"zava-forward-import {__version__}")

    def test_run_emits_sorted_standby_json_for_valid_mssql_and_local_store(self) -> None:
        for env in (
            self._base_env(),
            {
                "IMPORT_QUEUE": "import-jobs",
                "QUEUE_ENDPOINT": "https://stforwarddev.queue.core.windows.net",
                "ZF_STORE": "json",
            },
        ):
            with self.subTest(store=env["ZF_STORE"]):
                stdout = io.StringIO()
                stderr = io.StringIO()
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    rc = importer_main(["run"], env=env)
                self.assertEqual(rc, 0, stderr.getvalue())
                self.assertEqual(
                    json.loads(stdout.getvalue()),
                    {
                        "importQueue": "import-jobs",
                        "job": "importer",
                        "mode": "standby",
                        "status": "ok",
                        "version": __version__,
                    },
                )

    def test_run_fails_closed_on_missing_or_invalid_job_configuration(self) -> None:
        invalid_cases = {
            "missing_queue": {**self._base_env(), "IMPORT_QUEUE": "  "},
            "http_queue_endpoint": {
                **self._base_env(),
                "QUEUE_ENDPOINT": "http://stforwarddev.queue.core.windows.net",
            },
            "http_blob_endpoint": {
                **self._base_env(),
                "BLOB_ENDPOINT": "http://stforwarddev.blob.core.windows.net",
            },
            "mssql_missing_sql_server": {**self._base_env(), "SQL_SERVER": ""},
            "unset_store_missing_sql_database": {
                **self._base_env(),
                "ZF_STORE": "",
                "SQL_DATABASE": "",
            },
            "ungated_dispatch": {**self._base_env(), "ZF_IMPORT_DISPATCH": "autonomous"},
        }
        for label, env in invalid_cases.items():
            with self.subTest(case=label):
                stdout = io.StringIO()
                stderr = io.StringIO()
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    rc = importer_main(["run"], env=env)
                self.assertEqual(rc, 2)
                self.assertEqual(stdout.getvalue(), "")
                self.assertIn("zava-forward-import run:", stderr.getvalue())

    def test_run_refuses_to_start_when_enforced_container_hardening_is_violated(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        env = {**self._base_env(), "ZF_CONTAINER_HARDENING": "enforced"}
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            rc = importer_main(["run"], env=env)
        self.assertEqual(rc, 2)
        self.assertIn("Refusing to start", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
